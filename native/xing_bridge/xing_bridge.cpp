// xing_bridge.cpp : Defines the entry point for the application.
//

#include "framework.h"
#include "xing_bridge.h"

// Global Variables:
HINSTANCE hInst;                                // current instance
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);

CXingBridge g_xingBridge;

int APIENTRY WinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    if (_tcsncmp(lpCmdLine, HSHARE_PREID, _tcslen(HSHARE_PREID)) != 0)
    {
        return 0;
    }

	TCHAR szWindowClass[0x100] = { 0, };
	auto tick_count = (DWORD)GetTickCount64();
	_stprintf_s(szWindowClass, _T("XingBridge_%X"), tick_count);

    WNDCLASSEX wcex = { 0, };
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_XINGBRIDGE));
    wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = wcex.hIcon;

    RegisterClassEx(&wcex);

    // Perform application initialization:
    HWND hWnd = CreateWindow(szWindowClass, "xing_bridge", WS_OVERLAPPEDWINDOW,
        100, 100, 300, 200, nullptr, nullptr, hInstance, nullptr);

    if (!hWnd)
    {
        return FALSE;
    }

#ifdef _DEBUG
	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);
#endif

    MSG msg;

    // Main message loop:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int) msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	return g_xingBridge.WndProc(hWnd, message, wParam, lParam);
}
