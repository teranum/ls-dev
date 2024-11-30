using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using LS.XingApi;
using System.Collections;
using System.Text;
using System.Windows;

namespace CSharp_test
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    [ObservableObject]
    public partial class MainWindow : Window
    {
        private readonly XingApi _api = new();
        public MainWindow()
        {
            InitializeComponent();
            _ResultText = "Hello, World!\n";

            IsRemember = Properties.Settings.Default.IsRemember;
            if (IsRemember)
            {
                UserId = Properties.Settings.Default.UserId;
                UserPwd = Properties.Settings.Default.UserPwd;
                CertPwd = Properties.Settings.Default.CertPwd;
            }
            Closed += (s, e) =>
            {
                Properties.Settings.Default.IsRemember = IsRemember;
                if (IsRemember)
                {
                    Properties.Settings.Default.UserId = UserId;
                    Properties.Settings.Default.UserPwd = UserPwd;
                    Properties.Settings.Default.CertPwd = CertPwd;
                }
                else
                {
                    Properties.Settings.Default.UserId = string.Empty;
                    Properties.Settings.Default.UserPwd = string.Empty;
                    Properties.Settings.Default.CertPwd = string.Empty;
                }
                Properties.Settings.Default.Save();
            };

            DataContext = this;

            _api.OnMessageEvent += (s, e) =>
            {
                AppendResult(e.Message);
            };

            _api.OnRealtimeEvent += (s, e) =>
            {
                string text = $"[{e.TrCode}] {e.Key} {e.RealtimeBody}";
                AppendResult(text);
            };
        }

        public string UserId { get; set; } = string.Empty;
        public string UserPwd { get; set; } = string.Empty;
        public string CertPwd { get; set; } = string.Empty;
        public bool IsRemember { get; set; }
        public IList<string> Samples { get; } =
            [
            "로그인", "로그아웃", "업종-전체조회", "업종-차트조회",
            "주식-차트조회", "주식-현재가", "2-주식-현재가",
            ];
        public string SelectedSample { get; set; } = "로그인";
        [ObservableProperty]
        public string _ResultText;
        public bool IsCheckClear { get; set; } = true;

        void AppendResult(string text)
        {
            ResultText += text + "\n";
        }

        [RelayCommand]
        void Clear()
        {
            ResultText = string.Empty;
        }

        [RelayCommand]
        async Task RunSampleAsync()
        {
            if (IsCheckClear)
                ResultText = string.Empty;
            if (SelectedSample.Equals("로그인"))
            {
                AppendResult("로그인 요청중...");
                await _api.ConnectAsync(UserId, UserPwd, CertPwd);
                AppendResult(_api.LastMessage);
                return;
            }

            if (!_api.Logined)
            {
                AppendResult("로그인이 필요합니다.");
                return;
            }

            switch (SelectedSample)
            {

                case "로그아웃":
                    {
                        AppendResult("로그아웃");
                        _api.Close();
                    }
                    break;

                case "업종-전체조회":
                    {
                        var tr_cd = "t8424";
                        var response = await _api.RequestAsync(tr_cd, "0"); // 0: 전체, 1: 코스피업종, 2: 코스닥업종, 3: 섹터지수, 4: 특수계열지수
                        AppendResult($"{tr_cd}: {_api.LastMessage}");
                        if (response is not null)
                        {
                            AppendResult(response);
                        }
                    }
                    break;

                case "업종-차트조회":
                    {
                        var inputs = new Dictionary<string, object>
                        {
                            ["shcode"] = "001",     // 업종코드 (001: 종합...)
                            ["gubun"] = "1",        // 주기구분(0:틱1:분2:일3:주4:월)
                            ["qrycnt"] = 100,       // 조회건수 (1 이상 500 이하값만 유효)
                            ["tdgb"] = "0",         // 당일구분(0:전체1:당일만)
                        };
                        var tr_cd = "t4203"; // 업종차트(종합)
                        var response = await _api.RequestAsync(tr_cd, inputs);
                        AppendResult($"{tr_cd}: {_api.LastMessage}");
                        if (response is not null)
                        {
                            AppendResult(response);
                        }
                    }
                    break;

                case "주식-차트조회":
                    {
                        var inputs = new Dictionary<string, object>
                        {
                            ["shcode"] = "005930",  // 삼성전자
                            ["gubun"] = "2",        // 주기구분(2:일3:주4:월5:년)
                            ["qrycnt"] = 1000,      // 요청건수(최대-압축:2000비압축:500)
                            ["edate"] = "99999999", // 종료일자
                            ["comp_yn"] = "Y",      // 압축여부(Y:압축N:비압축)
                            ["sujung"] = "Y",       // 수정주가여부(Y:적용N:비적용)
                        };
                        var tr_cd = "t8410"; // 주식챠트(일주월년)(API용)
                        var response = await _api.RequestAsync(tr_cd, inputs);
                        AppendResult($"{tr_cd}: {_api.LastMessage}");
                        if (response is not null)
                        {
                            AppendResult(response);
                        }
                    }
                    break;

                case "주식-현재가":
                    {
                        var inputs = "005930";
                        var tr_cd = "t1102";
                        var response = await _api.RequestAsync(tr_cd, inputs);
                        AppendResult($"{tr_cd}: {_api.LastMessage}");
                        if (response is not null)
                        {
                            AppendResult(response);
                        }
                    }
                    break;

                case "2-주식-현재가":
                    {
                        var other_api = new XingApi();
                        var inputs = "005930";
                        var tr_cd = "t1102";
                        var response = await other_api.RequestAsync(tr_cd, inputs);
                        AppendResult($"{tr_cd}: {other_api.LastMessage}");
                        if (response is not null)
                        {
                            AppendResult(response);
                        }
                    }
                    break;
            }
        }

        void AppendResult(ResponseTrData response)
        {
            StringBuilder sb = new();
            if (response is not null)
            {
                sb.Append($"id: {response.id}, time(ms): ");
                bool first = true;
                foreach (var tick in response.ticks)
                {
                    if (!first)
                        sb.Append(", ");
                    sb.Append($", {tick / 10000.0}");
                    first = false;
                }
                sb.AppendLine();
                foreach (var (key, value) in response.body)
                {
                    if (value is IList list)
                    {
                        sb.AppendLine($"{key}: [{list.Count}]");
                        foreach (var line in list)
                        {
                            if (line is IDictionary dict)
                            {
                                sb.AppendLine(dict.ToJson());
                            }
                            else
                                sb.AppendLine(line.ToString());
                        }
                    }
                    else if (value is IDictionary dict)
                    {
                        sb.AppendLine($"{key}: ({dict.Count})");
                        sb.AppendLine(dict.ToJson());
                    }
                    else
                        sb.AppendLine(value.ToString());
                }
            }
            AppendResult(sb.ToString());
        }
    }

    static class Extensions
    {
        public static string ToJson(this IDictionary dict)
        {
            StringBuilder sb = new();
            sb.Append('{');
            bool first = true;
            foreach (DictionaryEntry item in dict)
            {
                if (!first)
                    sb.Append(", ");
                if (item.Value is string str)
                    sb.Append($"\"{item.Key}\": \"{str}\"");
                else
                    sb.Append($"\"{item.Key}\": {item.Value}");
                first = false;
            }
            sb.Append("}");
            return sb.ToString();
        }
    }
}