#pragma once

#include "../shared.h"
using namespace SharedMemory;
class CXingApi64
{
public:
	CXingApi64() {}
	~CXingApi64() {}

	BOOL is_loaded = FALSE;
	HWND m_hClientWnd = NULL;
	ULONG m_nUserMsg = WM_USER;

	BOOL SendData(const CVariantArray& send, CVariantArray& ret, BOOL bThreadSync = FALSE)
	{
		CVariantsStream stream((char*)send.data(), TRUE);
		stream.WriteToStream(send);
		stream.WriteToStream(ret);
		return TRUE;
	}
};
