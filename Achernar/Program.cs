using System.Linq.Expressions;
using System.Runtime.Intrinsics;
using System.Transactions;

namespace Achernar
{
    class Program
    {
        static void Main(string[] args)
        {
            //Test t = new Test();
            //t.TestMakeMove();
            int task_num, thinking_time;
            bool is_console_out;
            Common.Init();
            Hash.IniRand(5489U);
            Hash.IniRandomTable();

            string[] str_header = new string[9];
            str_header[0] = args[0];
            str_header[1] = args[1];
            str_header[2] = args[2];
            str_header[3] = args[3];
            str_header[4] = args[4];
            str_header[5] = args[5];
            str_header[6] = args[6];
            str_header[7] = args[7];
            str_header[8] = args[8];

            switch (str_header[0])
            {
                case "a":
                    task_num = int.Parse(args[5]);
                    thinking_time = int.Parse(args[6]);
                    Analyze.AnalyzeRecord(str_header[3], str_header[4], task_num, str_header, thinking_time);
                    break;
                case "s":
                    task_num = int.Parse(args[5]);
                    int game_num = int.Parse(args[7]);
                    thinking_time = int.Parse(args[6]);
                    is_console_out = bool.Parse(args[8]);
                    SelfPlay sp = new SelfPlay();
                    sp.SelfPlayWrapper(task_num, game_num, thinking_time, is_console_out);
                    break;
            }


            /*string[] str_header = new string[4];
            str_header[0] = "2022/04/03";
            str_header[1] = "第70回NHK杯1回戦";
            str_header[2] = "鈴木歩七段";
            str_header[3] = "沼舘沙輝哉七段";
            Analyze.AnalyzeRecord("20220403_nhk_hai.txt", "analyze_result.txt", 1, str_header, 10);*/

            /*str_header[0] = "2022/09/04";
            str_header[1] = "第70回NHK杯2回戦";
            str_header[2] = "羽根直樹九段";
            str_header[3] = "林漢傑八段";
            Analyze.AnalyzeRecord("20220904_nhk_hai.txt", "analyze_result.txt", 3, str_header, 3);*/

            /*str_header[0] = "2022/10/30";
            str_header[1] = "第70回NHK杯2回戦";
            str_header[2] = "井山裕太名人";
            str_header[3] = "張栩九段";
            Analyze.AnalyzeRecord("20221030_nhk_hai.txt", "analyze_result.txt", 3, str_header, 3);*/
        }
    }
}