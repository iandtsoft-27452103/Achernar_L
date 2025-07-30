using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using static Achernar.MakeMove;

namespace Achernar
{
    internal class Test
    {
        public void TestMakeMove()
        {
            Common.Init();
            Hash.IniRand(5489U);
            Hash.IniRandomTable();
            List<Record> records = new List<Record>();
            records = IO.ReadRecordFile("test_records.txt");
            List<int> li = new List<int>();

            for (int i = 0; i < records.Count; i++)
            {
                if (i == 14 || records[i].str_moves.Length > 250)
                {
                    string s = "record_no = " + (i+1).ToString();
                    s += ", ●" + records[i].players[0];
                    s += ", ○" + records[i].players[1];
                    Console.WriteLine(s);
                    li.Add(i);
                }
            }

            Board bt = new Board();
            short color;
            for (int i = 0;i < li.Count;i++)
            {
                Record record = records[li[i]];
                bt.Init();
                color = 0;
                for (short j = 0; j < record.moves.Length; j++)
                {
                    short move = record.moves[j];

                    if (i == 12 && j == 297)
                    {
                        int a = 0;// トリによって自分の駄目を復活させる処理から再開する
                    }

                    Do(ref bt, move, color, (short)(j + 1));
                    if (i == 12 && j == 297)
                    {
                        UnDo(ref bt, move, color, (short)(j + 1));
                        OutBoard(bt);

                        /*int cnt = 0;
                        for (int k = 0; k < 256; k++)
                        {
                            if (bt.dame_sq[1, k].Contains(120))
                            {
                                cnt++;
                            }  
                        }
                        for (int k = 0; k < bt.dame_sq[1,61].Count; k++)
                        {
                            Console.Write(bt.dame_sq[1, 61][k]);
                            Console.Write(",");
                        }*/
                        //Console.WriteLine(cnt);
                        return;
                    }
                    color ^= 1;
                }
            }
        }

        private void OutBoard(Board bt)
        {
            string str_out = "";
            int cnt = 0;
            for (int i = 0; i < Common.NSquare; i++)
            {
                switch(bt.board[i])
                {
                    case 0:
                        str_out += "○ ";
                        break;
                    case 1:
                        str_out += "● ";
                        break;
                    case 2:
                        str_out += "+ ";
                        break;
                }
                cnt++;
                if (cnt == Common.NSide)
                {
                    str_out += "\n";
                    cnt = 0;
                }
            }

            str_out = str_out + "\n";
            str_out += "黒のアゲハマ" + bt.agehama[0].ToString() + "\n";
            str_out = str_out + "\n";
            str_out += "白のアゲハマ" + bt.agehama[1].ToString() + "\n";

            Console.WriteLine(str_out);
        }
    }
}
