#pragma once

#include "resource.h"
#include "../IXingApi.h"
#include "../shared.h"

using namespace xing;

class CXingBridge
{
private:
    IXingApi _api;
public:
	CXingBridge() {}
	~CXingBridge() {}
	LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
	{
        UINT xMsg = message - WM_USER;
		if (xMsg > 0 && xMsg < XM::XM_LAST)
		{
			return 0;
		}
        switch (message)
        {
        case WM_COMMAND:
        {
        }
        break;
        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            EndPaint(hWnd, &ps);
        }
        break;
        case WM_CLOSE:
            DestroyWindow(hWnd);
        break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
        }
        return 0;
    }
private:

};

