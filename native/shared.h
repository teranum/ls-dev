#pragma once
#include <windows.h>
#include <tchar.h>
#include <vector>
#include <string>

constexpr auto HSHARE_PREID = "GG_XING_";
#define XID(x) SharedMemory::hash_value_32(x)

namespace SharedMemory
{
	inline constexpr unsigned int
		hash_value_32(const char* string)
	{
		unsigned int hash = 2166136261U;
		while (*string)
		{
			hash ^= (unsigned int)(*string++);
			hash *= 16777619U;
		}

		return hash;
	}

	enum XING_VARTYPE
	{
		XING_VT_I4,
		XING_VT_STR,
		XING_VT_ARRAY,
	};

	struct VARIANT_BYTES
	{
		LONG lSize;
		BYTE* pBytes;
	};

	class CVariant
	{
	public:
		long m_lVal;
		std::string m_string;
		XING_VARTYPE vt;
		VARIANT_BYTES m_ByteArray;
		CVariant() : vt(XING_VT_I4), m_lVal(0), m_ByteArray({ 0 }) {
		}
		CVariant(const CVariant& _Right) { *this = _Right; }
		CVariant(long lval) { *this = lval; }
		CVariant(LPCSTR string) { *this = std::string(string); }
		CVariant(VARIANT_BYTES bytes) { *this = bytes; }
		CVariant(const std::string& string) { *this = string; }
		~CVariant()
		{
		}
		_CONSTEXPR20 CVariant& operator =(long lval) {
			vt = XING_VT_I4;
			m_lVal = lval;
			return *this;
		}
		_CONSTEXPR20 CVariant& operator =(const CVariant& _Right) {
			vt = _Right.vt;
			m_lVal = _Right.m_lVal;
			m_string = _Right.m_string;
			m_ByteArray = _Right.m_ByteArray;
			return *this;
		}
		_CONSTEXPR20 CVariant& operator =(const std::string& string) {
			vt = XING_VT_STR;
			m_string = string;
			return *this;
		}
		_CONSTEXPR20 CVariant& operator =(LPCTSTR string) {
			vt = XING_VT_STR;
			m_string = string;
			return *this;
		}
		_CONSTEXPR20 CVariant& operator =(VARIANT_BYTES bytes) {
			vt = XING_VT_ARRAY;
			m_ByteArray = bytes;
			return *this;
		}

		_CONSTEXPR20 operator long() const noexcept {
			return m_lVal;
		}

		_CONSTEXPR20 operator LPCSTR() const noexcept {
			return m_string.c_str();
		}

		std::string ToString()
		{
			std::string result;
			if (vt == XING_VT_I4)
				result = std::to_string(m_lVal);
			else if (vt == XING_VT_STR)
				result = m_string;
			return result;
		}

	private:
	};

	typedef std::vector<CVariant> CVariantArray;

	class CVariantsStream
	{
	public:
		CVariantsStream(char* baseAdr, BOOL bWrite = FALSE) {
			m_bWriteMode = bWrite;
			if (bWrite)
				OpenWrite(baseAdr);
			else
				OpenRead(baseAdr);
		}
		BOOL WriteToStream(const CVariant& var)
		{
			if (m_bWriteMode == FALSE) return FALSE;
			*(XING_VARTYPE*)m_NowPos = var.vt;
			m_NowPos += sizeof(XING_VARTYPE);
			if (var.vt == XING_VT_I4)
			{
				*(int*)m_NowPos = var.m_lVal;
				m_NowPos += sizeof(int);
			}
			else if (var.vt == XING_VT_STR)
			{
				const int length = (int)var.m_string.length();
				*(int*)m_NowPos = length;
				m_NowPos += sizeof(int);
				if (length)
				{
					int bytesize = length * sizeof(CHAR);
					memcpy(m_NowPos, var.m_string.c_str(), bytesize);
					m_NowPos += bytesize;
				}
			}
			else if (var.vt == XING_VT_ARRAY)
			{
				*(int*)m_NowPos = var.m_ByteArray.lSize;
				m_NowPos += sizeof(int);
				if (var.m_ByteArray.lSize)
				{
					int bytesize = var.m_ByteArray.lSize;
					if (var.m_ByteArray.pBytes)
						memcpy(m_NowPos, var.m_ByteArray.pBytes, bytesize);
					else
						memset(m_NowPos, 0, bytesize);
					m_NowPos += bytesize;
				}
			}
			m_dwVarCount++;
			*(DWORD*)m_BaseAdr = m_dwVarCount;
			return TRUE;
		}
		void WriteToStream(const CVariantArray& vars)
		{
			for (int i = 0; i < (int)vars.size(); i++)
			{
				WriteToStream(vars[i]);
			}
		}
		BOOL ReadFromStream(CVariant& var)
		{
			if (m_bWriteMode) return FALSE;
			if (m_dwVarCount == 0) return FALSE;
			var.vt = *(XING_VARTYPE*)m_NowPos;
			m_NowPos += sizeof(XING_VARTYPE);
			m_dwVarCount--;
			if (var.vt == XING_VT_I4)
			{
				var.m_lVal = *(long*)m_NowPos;
				m_NowPos += sizeof(int);
			}
			else if (var.vt == XING_VT_STR)
			{
				const int length = *(long*)m_NowPos;
				m_NowPos += sizeof(long);
				if (length)
				{
					var.m_string.assign((CHAR*)m_NowPos, length);
					long bytesize = length * sizeof(CHAR);
					m_NowPos += bytesize;
				}
				else
				{
					var.m_string.clear();
				}
			}
			else if (var.vt == XING_VT_ARRAY)
			{
				const int length = *(long*)m_NowPos;
				m_NowPos += sizeof(long);
				if (length)
				{
					var.m_ByteArray.lSize = length;
					var.m_ByteArray.pBytes = (BYTE*)m_NowPos;
					long bytesize = length;
					m_NowPos += bytesize;
				}
			}
			return TRUE;
		}
		void ReadFromStream(CVariantArray& vars)
		{
			CVariant var;
			while (ReadFromStream(var))
			{
				vars.push_back(var);
			}
		}
	private:
		void OpenWrite(char* baseAdr)
		{
			m_BaseAdr = baseAdr;
			m_NowPos = m_BaseAdr + 4;
			*(DWORD*)m_BaseAdr = 0;
			m_dwVarCount = 0;
		}
		void OpenRead(char* baseAdr)
		{
			m_BaseAdr = baseAdr;
			m_NowPos = m_BaseAdr + 4;
			m_dwVarCount = *(DWORD*)m_BaseAdr;
		}
		BOOL m_bWriteMode;
		char* m_BaseAdr;
		char* m_NowPos;
		DWORD m_dwVarCount;
	};

	constexpr auto   WM_PRIVATE_BLOCKING_POST_MSG = (WM_APP + 101);
	constexpr auto  STATE_CLIENT_CREATED = 1;
	constexpr auto BASE_COMMON_SIZE = 0x100;

	struct BASE_COMMON_DATA
	{
		DWORD hParentWnd;
		DWORD hChildWnd;
		DWORD dwParentStack;
		DWORD dwChildStack;
		DWORD dwServerState;
		DWORD dwClientState;
		CHAR szApiFloder[0xC0];
	};

	typedef void(*BLOCKINGPROC)(LPVOID pOwner, const CVariantArray& params, CVariantArray& results);
}
