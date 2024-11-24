// console_test.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <windows.h>
#include <iostream>
#include "../native/IXingApi.h"
#include "../app_key.h"
using namespace xing;

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

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
        return 1;
    }

	//////////////////////////////////////////////
	// xingapi connect and login, check the result, message
	//////////////////////////////////////////////

	IXingApi api;
    if (!api.Init("C:\\LS_SEC\\xingAPI\\xingAPI.dll"))
	{
		std::cerr << "Failed to load xingAPI.dll!" << std::endl;
		return 1;
	}

    // connect
    auto ret = api.ETK_Connect(hWnd, real_domain, serveer_port, WM_USER, -1, -1);
	if (!ret) {
		std::cerr << "Failed to connect!" << std::endl;
		return 1;
	}

    // login
    ret = api.ETK_Login(hWnd, user_id, user_pwd, crt_pwd, 0 ,false);
	if (!ret) {
		std::cerr << "Failed to login!" << std::endl;
		return 1;
	}

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
	if (xm > 0 && xm < XM::XM_LAST)
	{
		std::cout << "XM=" << xm  << ", wParam=" << wParam << ", lParam=" << lParam<< std::endl;
        switch (xm) {
		case XM::XM_LOGIN:
			std::cout << "XM_LOGIN: " << "code=" << (LPCSTR)wParam << " msg=" << (LPCSTR)lParam << std::endl;
			break;
        default:
            break;
        }
        return 0;
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

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
