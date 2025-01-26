//using XA_SESSIONLib;
//using LS.XA_SESSIONLib;
using LS.XACom;

namespace ConsoleApp;

class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        //MainStart();
        Application.EnableVisualStyles();
        Form form = new()
        {
            FormBorderStyle = FormBorderStyle.FixedToolWindow,
            ShowInTaskbar = false,
            StartPosition = FormStartPosition.Manual,
            Location = new Point(-2000, -2000),
            Size = new Size(1, 1),
        };
        form.Shown += (s, e) => { MainStart(); };
        Application.Run(form);
    }

    static async void MainStart()
    {

        Console.WriteLine("Hello, World!");

        var api = XAControl.Instance;
        api.OnMessageEvent += (s, e) => { Console.WriteLine(e.Message); };
        api.OnRealtimeEvent += (s, e) => { Console.WriteLine(e.TrCode); };

        var ret = await api.LoginAsync("api.ls-sec.co.kr", Secret.user_id, Secret.user_pwd, Secret.crt_pwd, 0, false);
        if (ret)
        {
            Console.WriteLine($"Login Success: {api.LastMessage}");
        }
        else
        {
            Console.WriteLine($"Login Fail: {api.LastMessage}");
        }

        // 업종코드 조회
        Dictionary<string, object> inputs = new () {
            { "t8424InBlock",
                new Dictionary<string, string> (){
                    { "gubun", "0" },
                }
            },
        };
        var query = await api.RequestAsync("t8424", inputs);
        Console.WriteLine($"Request state: {api.LastMessage}");
        if (query is not null)
        {
            int count = query.GetBlockCount("t8424OutBlock");
            for (int i = 0; i < count; i++)
            {
                Console.WriteLine($"{query.GetFieldData("t8424OutBlock", "hname", i)}: {query.GetFieldData("t8424OutBlock", "upcode", i)}");
            }
        }

        var real = api.AdviseRealData("S3_", "shcode", ["005930"]);
    }
}
