#pragma once
#include <windows.h>
// C RunTime Header Files
#include <stdlib.h>
#include <malloc.h>
#include <memory.h>
#include <tchar.h>
#include "resource.h"

#include "../app_key.h"
#include "../native/XingApi.h"

xing::XingApi api;
HWND g_hDlg;

LPCSTR samples_list[] =
{
    "계좌번호",
    "업종전체조회",
};

void OutputLog(std::string text)
{
	// assign hh:mm:ss.MMM
	SYSTEMTIME st;
	GetLocalTime(&st);
	char buf[0x100];
	sprintf_s(buf, "%02d:%02d:%02d.%03d ", st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);
	text = buf + text + "\r\n";
	auto hEdit = GetDlgItem(g_hDlg, IDC_EDIT_RESULT);
	auto len = GetWindowTextLength(hEdit);
	SendMessage(hEdit, EM_SETSEL, len, len);
	SendMessage(hEdit, EM_REPLACESEL, 0, (LPARAM)text.c_str());
}

void ClearResult()
{
	SetDlgItemText(g_hDlg, IDC_EDIT_RESULT, "");
}

void Run(LPCSTR sample)
{
	OutputLog("Run: " + std::string(sample));

	// 계좌번호 조회
	if (strcmp(sample, "계좌번호") == 0)
	{
		auto accounts = api.get_account_list();
		OutputLog("Account list: " + std::to_string(accounts.size()));
		for (auto& account : accounts)
		{
			std::string text = account.number + ", " + account.name + ", " + account.detail_name + ", " + account.nick_name;
			OutputLog(text);
		}
	}
	else if (strcmp(sample, "업종전체조회") == 0)
	{
		auto response = api.request("t8424", "0");
		if (!response.success) {
			OutputLog("t8424: Failed to request: [" + response.rsp_cd + "] " + response.rsp_msg);
			return;
		}
		OutputLog("t8424: Request success: [" + response.rsp_cd + "] " + response.rsp_msg);
		for (auto& outdata : response.outdatas)
		{
			OutputLog(outdata.name);
		}
	}
	else
	{
		OutputLog("Unknown sample: " + std::string(sample));
	}
}

// Message handler for main box.
INT_PTR CALLBACK DlgProc(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    auto xm = message - WM_USER;
    if (xm > 0 && xm < xing::XM_LAST)
    {
        api.WndProc(hDlg, message, wParam, lParam);
        return 0;
    }
    switch (message)
    {
    case WM_INITDIALOG:
    {
		g_hDlg = hDlg;
        RECT rt, rt2;
        GetWindowRect(hDlg, &rt);
        GetWindowRect(GetDesktopWindow(), &rt2);
        int x = (rt2.right - rt.right) / 2;
        int y = (rt2.bottom - rt.bottom) / 2;
        SetWindowPos(hDlg, HWND_TOPMOST, x, y, 0, 0, SWP_NOSIZE);

		auto hCombo = GetDlgItem(hDlg, IDC_COMBO_SAMPLES);
		for (auto i = 0; i < sizeof(samples_list) / sizeof(samples_list[0]); i++)
		{
			SendMessage(hCombo, CB_ADDSTRING, 0, (LPARAM)samples_list[i]);
		}
		SendMessage(hCombo, CB_SETCURSEL, 0, 0);

		auto ret = api.Init(hDlg, "C:\\LS_SEC\\xingAPI");
        if (ret) {
			OutputLog("Loaded xingAPI.dll!");
			EnableWindow(GetDlgItem(hDlg, IDC_BUTTON_LOGIN), TRUE);
        }
        else
        {
            OutputLog(api.last_message);
        }
    }
    return (INT_PTR)TRUE;

    case WM_COMMAND:
    {
		auto nID = LOWORD(wParam);
        if (nID == IDOK || nID == IDCANCEL)
        {
            EndDialog(hDlg, nID);
            return (INT_PTR)TRUE;
        }

		if (nID == IDC_BUTTON_CLEAR)
		{
            ClearResult();
		}

		if (nID == IDC_BUTTON_LOGIN)
		{
			EnableWindow(GetDlgItem(hDlg, IDC_BUTTON_LOGIN), FALSE);
            OutputLog("로그인 요청중...");
			auto ret = api.login(user_id, user_pwd, crt_pwd);
			if (!ret) {
				std::string msg = "Failed to login: " + api.last_message;
                OutputLog(msg);
				EnableWindow(GetDlgItem(hDlg, IDC_BUTTON_LOGIN), TRUE);
			}
            else
            {
                OutputLog("Login success: " + api.last_message);
            }
		}

		if (nID == IDC_BUTTON_RUN)
		{
			auto hCombo = GetDlgItem(hDlg, IDC_COMBO_SAMPLES);
			auto idx = SendMessage(hCombo, CB_GETCURSEL, 0, 0);
			if (idx >= 0)
			{
				TCHAR sample[0x100];
				SendMessage(hCombo, CB_GETLBTEXT, idx, (LPARAM)sample);
				Run(sample);
			}
		}
    }
        break;
    }
    return (INT_PTR)FALSE;
}
