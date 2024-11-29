using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using LS.XingApi;
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
                AppentResult(e.Message);
            };

            _api.OnRealtimeEvent += (s, e) =>
            {
                string text = $"[{e.TrCode}] {e.Key} {e.RealtimeBody}";
                AppentResult(text);
            };
        }

        public string UserId { get; set; } = string.Empty;
        public string UserPwd { get; set; } = string.Empty;
        public string CertPwd { get; set; } = string.Empty;
        public bool IsRemember { get; set; }
        public IList<string> Samples { get; } = ["로그인", "로그아웃", "Sample3"];
        public string SelectedSample { get; set; } = "로그인";
        [ObservableProperty]
        public string _ResultText;

        void AppentResult(string text)
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

                        AppentResult("로그인 요청중...");
                        await _api.ConnectAsync(UserId, UserPwd, CertPwd);
                        AppentResult(_api.LastMessage);
                    }
                    break;
                case "로그아웃":
                    {
                        AppentResult("로그아웃");
                        _api.Close();
                    }
                    break;
                case "Sample3":
                    break;
            }
        }

    }
}