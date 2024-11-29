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
        XingApi _api = new();
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
        public IList<string> Samples { get; } = ["로그인", "로그아웃", "업종-전체조회"];
        public string SelectedSample { get; set; } = "로그인";
        [ObservableProperty]
        public string _ResultText;

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
            switch (SelectedSample)
            {
                case "로그인":
                    {

                        AppendResult("로그인 요청중...");
                        await _api.ConnectAsync(UserId, UserPwd, CertPwd);
                        AppendResult(_api.LastMessage);
                    }
                    break;
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
            }
        }

        void AppendResult(ResponseTrData response)
        {
            StringBuilder sb = new();
            if (response is not null)
            {
                foreach (var (key, value) in response.body)
                {
                    if (value is IList list)
                    {
                        sb.AppendLine($"{key}: [{list.Count}]");
                        foreach (var line in list)
                        {
                            if (line is IDictionary dict)
                            {
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
                                sb.AppendLine("}");
                            }
                            else
                                sb.AppendLine(line.ToString());
                        }
                    }
                    else if (value is IDictionary dict)
                    {
                        sb.AppendLine($"{key}: [{dict.Count}]");
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
                        sb.AppendLine("}");
                    }
                    else 
                        sb.AppendLine(value.ToString());
                }
            }
            AppendResult(sb.ToString());
        }
    }
}