import torch
import torch.nn as nn
import torchvision
import torch.functional as F
import torch.optim.lr_scheduler
import numpy
import random
#import pickle
#import os
import re
import policy_lazy
import position
import board
import inout
import logging
import result
import file
import rank
import bitop
import stone
import makemove
import feature
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt

class train_policy:
    def __init__(self):
        self.train_batchsize = 32
        self.test_batchsize = 32
        self.epoch = 1
        self.iteration = 0
        self.log_file_name = 'train_policy_lazy.txt'
        self.model_file_name = 'model_lazy.pth'
        self.optimizer_file_name = 'optimizer_lazy.pth'
        self.scheduler_file_name = 'scheduler_lazy.pth'
        self.is_load_model = 0
        self.is_load_optimizer = 0
        self.is_load_scheduler = 0
        self.lr = 0.0001875#0.0001
        self.mt = 0.9
        self.wd = 0.0001
        self.shuffle_threshold = 3000
        self.is_use_sgd = 0
        self.lr_decay_threshold = 320
        self.console_out_threshold = 25
        self.record_start_number = 0
        self.record_end_number = 1000

    def train_policy(self):
        
        #�O���t�`��p��List�錾
        train_loss_log = []
        train_acc_log = []

        #���f����optimizer��p�ӂ���
        device = torch.device("cuda:0")
        model = policy_lazy.policy()
        model = model.to(device)
        optimizer = torch.optim.SGD(model.parameters(), lr = self.lr, momentum = self.mt, weight_decay = self.wd, nesterov = True)
        #optimizer = torch.optim.Adam(model.parameters())
        #optimizer = torch.optim.Adagrad(model.parameters(), weight_decay = self.wd)
        #optimizer = torch.optim.RMSprop(model.parameters());
        #optimizer = torch.optim.Adamax(model.parameters())
        #optimizer = torch.optim.Adadelta(model.parameters())
        #scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor = 0.99, patience = 50)
        #scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size = 1, gamma = 0.99996)
        #scheduler = torch.optim.lr_scheduler.CyclicLR(optimizer, base_lr = self.lr, max_lr = (self.lr * 10))

        #�e�N���X�̃C���X�^���X���쐬����
        bo = board.board()
        f = file.file()
        r = rank.rank()
        bi = bitop.bitop(bo)
        st = stone.stone()
        ma = makemove.makemove()
        ft = feature.feature(bo)

        #���f�������[�h����
        if self.is_load_model != 0:
            model.load_state_dict(torch.load(self.model_file_name))
        
        #optimizer�����[�h����
        if self.is_load_optimizer != 0:
            optimizer.load_state_dict(torch.load(self.optimizer_file_name))

        #scheduler�����[�h����
        #if self.is_load_scheduler != 0:
            #scheduler.load_state_dict(torch.load(self.scheduler_file_name))

        #������ǂݍ���
        clsio = inout.inout()
        clsre = result.result()
        clsio.read_records(clsre)
        #clsio.read_test_records(clsre)

        #�ǖʂɔԍ���t����
        pos = position.position()
        positions = pos.number_position(clsio.rec)

        #�w�K�ǖʐ��ƃe�X�g�ǖʐ����Z�b�g����
        pos_count = len(positions)
        train_count = pos_count
        #test_count = pos_count - train_count

        #�w�K�ǖʂƃe�X�g�ǖʂ𕪊�����
        train_pos = []
        for i in range(train_count):
            train_pos.append(positions[i])
        #test_pos = []
        #for i in range(train_count, pos_count):
            #test_pos.append(positions[i])

        iteration_max = train_count // self.train_batchsize
        #iteration_max = int(iteration_max)

        #epoch���̊w�K�̃��[�v
        for epoch in range(self.epoch):

            #epoch�J�n���Ԃ��o�͂���
            tdatetime = dt.now()
            tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
            tstr = "epoch start! " + tstr
            print(tstr)

            #�w�K�ǖʂ��V���b�t������
            random.shuffle(train_pos)

            iteration = 0
            shuffle_counter = 0
            lr_decay_counter = 0
            console_out_counter = 0

            while iteration < iteration_max:

                #臒l�ɂȂ����烋�[�v�𔲂���
                #if self.iteration + 1 == iteration:
                    #break

                #臒l�ɒB������w�K�ǖʂ��V���b�t������
                #if shuffle_counter == self.shuffle_threshold:
                    #shuffle_counter = 0
                    #msg = "data shuffle!"
                    #print(msg)
                    #random.shuffle(train_pos)

                #SGD�̏ꍇ�A臒l�ɒB������w�K������������
                #if self.is_use_sgd == 1 and lr_decay_counter == self.lr_decay_threshold:
                    #lr_decay_counter = 0
                    #self.lr -= 0.000015
                    #optimizer = torch.optim.SGD(model.parameters(), lr = self.lr, momentum = self.mt, weight_decay = self.wd, nesterov = True)
                    #msg = "lr decay!"
                    #print(msg)

                loop_start = iteration * self.train_batchsize
                loop_end = iteration * self.train_batchsize + self.train_batchsize

	            #�w�K�p�̃~�j�o�b�`�𐶐�����
                train_batch = []
                train_label = []

                for i in range(loop_start, loop_end):
                    #�����ԍ����擾����
                    record_no = train_pos[i].record_no

                    #�萔���擾����
                    current_ply = train_pos[i].ply

                    #����擾����
                    current_move = clsio.rec[record_no].moves[current_ply]

                    #���x���̃��X�g�ɕۑ�����
                    lbl = ft.make_output_labels(bo, current_move)
                    train_label.append(lbl)

                    #�擾�����萔�܂Ŋ������Đ�����
                    bo = board.board()
                    color = 0
                    for ply in range(current_ply):
                        move = clsio.rec[record_no].moves[ply]
                        ma.makemove(bo, move, color, ply, f, r, bi, st)
                        color = color ^ 1

                    #���݂̋ǖʂ���������擾����
                    fe = ft.make_input_features(bo, clsio.rec[record_no], current_ply - 1, color)
                    train_batch.append(fe)
            
                train_loss = 0
                train_acc = 0
                tcnt = 0

                #�w�K���J�n����
                model.train()

                #�o�b�`��GPU�ɓ]������
                train_batch = numpy.array(train_batch)
                train_label = numpy.array(train_label)
                x = torch.tensor(train_batch, dtype = torch.float)
                x = x.to(device)
                t = torch.tensor(train_label, dtype = torch.long)
                t = t.to(device)

                #���`�d�����s����
                model.batch_size = self.train_batchsize
                y = model.forward(x)

                #���z������������
                model.zero_grad()
                optimizer.zero_grad()

                #�����֐����v�Z����
                criterion = nn.CrossEntropyLoss()
                t = t.reshape(self.train_batchsize, 361)
                loss = criterion(y, t)

                #���O�p�̃p�����[�^���X�V����
                train_loss += loss.item()
                pre = y.max(1)[1]
                train_acc += (pre == t).sum().item()
                tcnt += t.size(0)
                avg_train_loss = train_loss / self.train_batchsize
                avg_train_acc = train_acc / tcnt

                #�t�`�d�����s����
                loss.backward()

                #�p�����[�^���X�V����
                optimizer.step()

                #�X�P�W���[�����X�V����
                #scheduler.step(loss)
                #scheduler.step()

                #�J�E���^���X�V����
                iteration += 1
                shuffle_counter += 1
                lr_decay_counter += 1
                console_out_counter += 1

                #�O���t�`��p�̃p�����[�^��List�ɕۑ�����
                train_loss_log.append(avg_train_loss)
                train_acc_log.append(avg_train_acc)
                #test_loss_log.append(avg_test_loss)
                #test_acc_log.append(avg_test_acc)

                #�R���\�[���ɓr���o�߂��o�͂���
                if console_out_counter == self.console_out_threshold:
                    console_out_counter = 0
                    print('epoch = [{}/{}], ith = [{}/{}], train_loss: {a:.10f}'.format(epoch + 1, self.epoch, iteration, iteration_max, a=avg_train_loss))

            #epoch�I�����Ԃ��o�͂���
            tdatetime = dt.now()
            tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
            tstr = "epoch end! " + tstr
            print(tstr)

            #if avg_test_acc >= 0.95:
                #break
                
        #���f����ۑ�����
        torch.save(model.state_dict(), self.model_file_name)
        #optimizer��ۑ�
        torch.save(optimizer.state_dict(), self.optimizer_file_name)
        #scheduler��ۑ�����
        #torch.save(scheduler.state_dict(), self.scheduler_file_name)

        #�O���t��`�悷��
        #if epoch > 5:
            #self.draw_graph(train_loss_log, train_acc_log, test_loss_log, test_acc_log)

    def draw_graph(self, train_loss_log, train_acc_log, test_loss_log, test_acc_log):
        plt.figure()
        plt.plot(range(self.epoch), train_loss_log, color="blue", linestyle="-", label="train_loss")
        plt.plot(range(self.epoch), test_loss_log, color="green", linestyle="--", label="test_loss")
        plt.legend()
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.title("Training and Testing loss")
        plt.grid()

        plt.figure()
        plt.plot(range(self.epoch), train_acc_log, color="blue", linestyle="-", label="train_accuracy")
        plt.plot(range(self.epoch), test_acc_log, color="green", linestyle="--", label="test_accuracy")
        plt.legend()
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        plt.title("Training and Testing accuracy")
        plt.grid()

        plt.show()