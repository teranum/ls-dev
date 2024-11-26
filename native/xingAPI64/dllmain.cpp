// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

#include "xingAPI64.h"

CXingApi64 g_xingApi64;

#define ETK_BASE_BODY(func_name) \
{ \
	if (g_xingApi64.is_loaded) \
	{ \
		CVariantArray params, rets; \
		params.push_back(XID(#func_name));

#define ETK_FUNC_IMPLE_0(ret_type, func_name) \
ret_type APIENTRY func_name() ETK_BASE_BODY(func_name)

#define ETK_FUNC_IMPLE_1(ret_type, func_name, t1) \
ret_type APIENTRY func_name(t1 p1)  ETK_BASE_BODY(func_name) \
		params.push_back(p1);

#define ETK_FUNC_IMPLE_2(ret_type, func_name, t1, t2) \
ret_type APIENTRY func_name(t1 p1, t2 p2)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2);

#define ETK_FUNC_IMPLE_3(ret_type, func_name, t1, t2, t3) \
ret_type APIENTRY func_name(t1 p1, t2 p2, t3 p3)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2); \
		params.push_back(p3);

#define ETK_FUNC_HWND_IMPLE_0(ret_type, func_name) \
ret_type APIENTRY func_name(HWND hWnd)  ETK_BASE_BODY(func_name)

#define ETK_FUNC_HWND_IMPLE_1(ret_type, func_name, t1) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1)  ETK_BASE_BODY(func_name) \
		params.push_back(p1);

#define ETK_FUNC_HWND_IMPLE_2(ret_type, func_name, t1, t2) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1, t2 p2)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2);

#define ETK_FUNC_HWND_IMPLE_3(ret_type, func_name, t1, t2, t3) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1, t2 p2, t3 p3)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2); \
		params.push_back(p3);

#define ETK_FUNC_HWND_IMPLE_4(ret_type, func_name, t1, t2, t3, t4) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1, t2 p2, t3 p3, t4 p4)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2); \
		params.push_back(p3); \
		params.push_back(p4);

#define ETK_FUNC_HWND_IMPLE_5(ret_type, func_name, t1, t2, t3, t4, t5) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1, t2 p2, t3 p3, t4 p4, t5 p5)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2); \
		params.push_back(p3); \
		params.push_back(p4); \
		params.push_back(p5);

#define ETK_FUNC_HWND_IMPLE_6(ret_type, func_name, t1, t2, t3, t4, t5, t6) \
ret_type APIENTRY func_name(HWND hWnd, t1 p1, t2 p2, t3 p3, t4 p4, t5 p5, t6 p6)  ETK_BASE_BODY(func_name) \
		params.push_back(p1); \
		params.push_back(p2); \
		params.push_back(p3); \
		params.push_back(p4); \
		params.push_back(p5); \
		params.push_back(p6);

#define ETK_END_VOID \
		if (g_xingApi64.SendData(params, rets)) \
		{ \
		} \
	} \
}

#define ETK_END_FUNC \
		if (g_xingApi64.SendData(params, rets)) \
		{ \
			if (rets.size()) \
			{ \
				return rets[0]; \
			} \
		} \
	} \
	return 0; \
}

#define ETK_FUNC_0(ret_type, func_name) \
	ETK_FUNC_IMPLE_0(ret_type, func_name) ETK_END_FUNC

#define ETK_FUNC_1(ret_type, func_name, t1) \
	ETK_FUNC_IMPLE_1(ret_type, func_name, t1) ETK_END_FUNC

#define ETK_FUNC_2(ret_type, func_name, t1, t2) \
	ETK_FUNC_IMPLE_2(ret_type, func_name, t1, t2) ETK_END_FUNC

#define ETK_FUNC_3(ret_type, func_name, t1, t2, t3) \
	ETK_FUNC_IMPLE_3(ret_type, func_name, t1, t2, t3) ETK_END_FUNC

#define ETK_FUNC_HWND_0(ret_type, func_name) \
	ETK_FUNC_IMPLE_0(ret_type, func_name) ETK_END_FUNC

#define ETK_FUNC_HWND_1(ret_type, func_name, t1) \
	ETK_FUNC_HWND_IMPLE_1(ret_type, func_name, t1) ETK_END_FUNC

#define ETK_FUNC_HWND_2(ret_type, func_name, t1, t2) \
	ETK_FUNC_HWND_IMPLE_2(ret_type, func_name, t1, t2) ETK_END_FUNC

#define ETK_FUNC_HWND_3(ret_type, func_name, t1, t2, t3) \
	ETK_FUNC_HWND_IMPLE_3(ret_type, func_name, t1, t2, t3) ETK_END_FUNC

#define ETK_FUNC_HWND_4(ret_type, func_name, t1, t2, t3, t4) \
	ETK_FUNC_HWND_IMPLE_4(ret_type, func_name, t1, t2, t3, t4) ETK_END_FUNC

#define ETK_FUNC_HWND_5(ret_type, func_name, t1, t2, t3, t4, t5) \
	ETK_FUNC_HWND_IMPLE_5(ret_type, func_name, t1, t2, t3, t4, t5) ETK_END_FUNC

#define ETK_FUNC_HWND_6(ret_type, func_name, t1, t2, t3, t4, t5, t6) \
	ETK_FUNC_HWND_IMPLE_6(ret_type, func_name, t1, t2, t3, t4, t5, t6) ETK_END_FUNC

#define ETK_VOID_1(func_name, t1) \
	ETK_FUNC_IMPLE_1(void, func_name, t1) ETK_END_VOID

#define ETK_VOID_2(func_name, t1, t2) \
	ETK_FUNC_IMPLE_2(void, func_name, t1, t2) ETK_END_VOID

#define ETK_VOID_3(func_name, t1, t2, t3) \
	ETK_FUNC_IMPLE_3(void, func_name, t1, t2, t3) ETK_END_VOID

#define ETK_BOOL_CENTER_LPSTR(func_name, t1) \
BOOL APIENTRY func_name(t1 p1, LPSTR pszData, int nDataSize) \
{ \
	if (g_xingObject.is_loaded)\
	{\
		BlockingMemory::CVariantArray params, rets;\
		params.push_back(XID(#func_name));\
		params.push_back(p1);\
		if (g_xingObject.m_DataManager.SendData(params, rets))\
		{\
			if (rets.size())\
			{\
				auto& var = rets[0];\
				if (var.vt == XING_VT_STR)\
				{\
					auto length = (int)var.m_string.length();\
					if (length > nDataSize)\
					{\
						return FALSE;\
					}\
					memcpy(pszData, var.m_string.c_str(), length);\
					pszData[length] = 0;\
					return TRUE;\
				}\
			}\
		}\
	}\
    return FALSE;\
}

#define ETK_VOID_LPSTR(func_name) \
void APIENTRY func_name(LPSTR pszMsg) \
{ \
	if (g_xingObject.is_loaded) \
	{ \
		BlockingMemory::CVariantArray params, rets; \
		params.push_back(XID(#func_name)); \
		if (g_xingObject.m_DataManager.SendData(params, rets)) \
		{ \
			if (rets.size()) \
			{ \
				auto& var = rets[0]; \
				if (var.vt == XING_VT_STR) \
				{ \
					auto length = (int)var.m_string.length(); \
					if (length > 0x100) \
					{ \
						return; \
					} \
					memcpy(pszMsg, var.m_string.c_str(), length); \
					pszMsg[length] = 0; \
				} \
			} \
		} \
	} \
}
