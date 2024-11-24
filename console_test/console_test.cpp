// console_test.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <windows.h>
#include <iostream>
#include "../native/XingApi.h"
#include "../app_key.h"

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);
xing::XingApi api;

void xingapi_test(HWND hWnd)
{
	std::cout << "Test start" << std::endl;

	//////////////////////////////////////////////
	// xingapi login, show accounts
	//////////////////////////////////////////////

    if (!api.Init("C:\\LS_SEC\\xingAPI\\xingAPI.dll"))
    {
        std::cerr << "Failed to load xingAPI.dll!" << std::endl;
        return;
    }

    // login
    auto ret = api.login(hWnd, user_id, user_pwd, crt_pwd, 0, false);
    if (!ret) {
        std::cerr << "Failed to login: " << api.last_message << std::endl;
        return;
    }
    std::cout << "Login success: " << api.last_message << std::endl;

	// show account list
	auto accounts = api.get_account_list();
	std::cout << "Account list: " << accounts.size() << std::endl;
	for (auto& account : accounts)
	{
		std::cout << account.number << ", " << account.name << ", " << account.detail_name << ", " << account.nick_name << std::endl;
	}

    // 업종전체조회
	std::cout << std::endl;
	auto response = api.request("t8424", "0");
	if (!response.success) {
		std::cerr << "t8424: Failed to request: [" << response.rsp_cd << "] " << response.rsp_msg << std::endl;
		return;
	}
	std::cout << "t8424: Request success: [" << response.rsp_cd << "] " << response.rsp_msg << std::endl;
    for (auto& outdata : response.outdatas)
    {
		std::cout << outdata.name/* << ": " << outdata.data*/ << std::endl;
    }

	// 주식 현재가(시세) 조회
	// 종목코드: 005930
	std::cout << std::endl;
    response = api.request("t1102", "005930");
    if (!response.success) {
        std::cerr << "t1102: Failed to request: [" << response.rsp_cd << "] " << response.rsp_msg << std::endl;
        return;
    }
    std::cout << "t1102: Request success: [" << response.rsp_cd << "] " << response.rsp_msg << std::endl;
    for (auto& outdata : response.outdatas)
    {
        std::cout << outdata.name/* << ": " << outdata.data*/ << std::endl;
    }

	std::cout << "Test end" << std::endl;
}

int main()
{
    std::cout << "Hello World!\n";

    HINSTANCE hInstance = GetModuleHandle(NULL);
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = TEXT("ConsoleWinClass");

    if (!RegisterClass(&wc)) {
        std::cerr << "Failed to register window class!" << std::endl;
        return 1;
    }

    HWND hWnd = CreateWindow(wc.lpszClassName, TEXT("Console Window"), WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
        NULL, NULL, hInstance, NULL);

    if (!hWnd) {
        std::cerr << "Failed to create window!" << std::endl;
        return -1;
    }

	// call xingapi test
    xingapi_test(hWnd);

	// Message loop
    MSG msg = { 0 };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    std::cout << "hWnd=" << hWnd << ", Message=" << message << ", wParam=" << wParam << ", lParam=" << lParam << std::endl;

	auto xm = message - WM_USER;
	if (xm > 0 && xm < xing::XM::XM_LAST)
	{
		api.WndProc(hWnd, message, wParam, lParam);
    }
    switch (message) {
    case WM_CREATE:
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }

    return 0;
}
