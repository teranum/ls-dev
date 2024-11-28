#pragma once
#include <iostream>
#include <sstream>

#include "IXingApi.h"
#include "AsyncMsgManager.h"
namespace xing
{
	struct AccountInfo
	{
		std::string number, name, detail_name, nick_name;
	};

	struct ResponseData
	{
		std::string tr_cd;
		std::string indatas;

		bool success = false;
		std::string rsp_cd;
		std::string rsp_msg;
		bool cont_yn = false;
		std::string cont_key;

		struct name_data
		{
			std::string name, data;
		};
		std::vector<name_data> outdatas;
	};

	class XingApi : private IXingApi
	{
		typedef BOOL(__stdcall* FP_XING64_Init) (LPCTSTR);
	private:
		HWND m_hWnd;
		AsyncMsgManager m_asyncManager;
	public:
		bool is_logined;
		std::string last_message;
		std::vector<AccountInfo> account_list;

		XingApi()
		{
			m_hWnd = nullptr;
			is_logined = false;
		}

	public:
		BOOL IsInit() const { return IXingApi::IsInit(); }
		BOOL Init(HWND hWnd, LPCTSTR szXingFolder)
		{
			m_hWnd = hWnd;

#ifdef _WIN64
			bool is_loaded = IXingApi::Init("xingAPI64.dll");
			if (!is_loaded)
			{
				last_message = "Already logined!";
				return false;
			}
			FP_XING64_Init XING64_Init = (FP_XING64_Init)GetProcAddress(m_hModule, "XING64_Init");
			if (!XING64_Init(szXingFolder))
			{
				last_message = "Failed to init xing64.!";
				FreeLibrary(m_hModule);
				m_hModule = NULL;
				return false;
			}
#else
			std::string szPath = szXingFolder;
			szPath += "\\xingAPI.dll";
			return IXingApi::Init(szPath.c_str());
#endif
			return true;
		}
		const auto& get_account_list() const { return account_list; };

		std::string get_error_message(int err_code) {
			char msg[0x100];
			ETK_GetErrorMessage(err_code, msg, sizeof(msg));
			return msg;
		}

		bool login(LPCSTR user_id, LPCSTR user_pwd, LPCSTR crt_pwd, int server_type, BOOL show_crt_pwd) {
			if (is_logined) {
				last_message = "Already logined!";
				return false;
			}

			if (!m_hModule) {
				last_message = "Failed to load xingAPI.dll!";
				return false;
			}

			bool is_simulation = crt_pwd == nullptr || strlen(crt_pwd) == 0;
			auto ret = ETK_Connect(m_hWnd, is_simulation ? simul_domain : real_domain, serveer_port, WM_USER, -1, -1);
			if (!ret) {
				last_message = "Failed to connect!";
				return false;
			}

			ret = ETK_Login(m_hWnd, user_id, user_pwd, crt_pwd, server_type, show_crt_pwd);
			if (!ret) {
				last_message = "Failed to login!";
				ETK_Disconnect();
				return false;
			}

			auto node = m_asyncManager.CreateNode(0);

			std::string code, msg;
			auto lambda = [&code, &msg](WPARAM wParam, LPARAM lParam) {
				code = (LPCSTR)wParam;
				msg = (LPCSTR)lParam;
				};
			node->callback_proc = std::move(lambda);
			if (!node->wait()) {
				last_message = "Failed to login!";
				ETK_Disconnect();
				return false;
			}

			last_message = msg;
			if (code != "0000") {
				ETK_Disconnect();
				return false;
			}

			is_logined = true;

			// get account list
			account_list.clear();
			int count = ETK_GetAccountListCount();
			if (count > 0) {
				account_list.resize(count);
				for (int i = 0; i < count; i++) {
					char number[0x40], name[0x40], detail_name[0x40], nick_name[0x40];
					ETK_GetAccountList(i, number, sizeof(number));
					ETK_GetAccountName(number, name, sizeof(name));
					ETK_GetAcctDetailName(number, detail_name, sizeof(detail_name));
					ETK_GetAcctNickname(number, nick_name, sizeof(nick_name));
					account_list[i] = { number, name, detail_name, nick_name };
				}
			}

			return true;
		}

		ResponseData request(LPCSTR tr_cd, const std::string& indatas, BOOL bNext = false, LPCSTR next_key = "", int nTimeOut = 0) {
			ResponseData response;
			response.tr_cd = tr_cd;
			response.indatas = indatas;
			if (!is_logined) {
				response.rsp_cd = "-1";
				response.rsp_msg = "Not logined!";
				return response;
			}
			auto ret = ETK_Request(m_hWnd, tr_cd, indatas.c_str(), (int)indatas.size(), bNext, next_key, nTimeOut);
			if (ret < 0) {
				response.rsp_cd = std::to_string(ret);
				response.rsp_msg = get_error_message(ret);
				return response;
			}


			auto node = m_asyncManager.CreateNode(ret);

			auto lambda = [&response](WPARAM wParam, LPARAM lParam) {
				std::stringstream ss;
				if (wParam == REQUEST_DATA) {
					auto recv_packet = (LPRECV_PACKET)lParam;
					response.cont_yn = recv_packet->cCont[0] == '1';
					response.cont_key = recv_packet->szContKey;
					std::string data;
					// recv_packet->lpData, recv_packet->nDataLength 파싱 (res파일 참조)
					response.outdatas.push_back({ recv_packet->szBlockName, data });
				}
				else if (wParam == MESSAGE_DATA || wParam == SYSTEM_ERROR_DATA) {
					LPMSG_PACKET msg_packet = (LPMSG_PACKET)lParam;
					response.rsp_cd = msg_packet->szMsgCode;
					response.rsp_msg = std::string((LPCSTR)msg_packet->lpszMessageData, msg_packet->nMsgLength);
				};
			};
			node->callback_proc = std::move(lambda);
			if (!node->wait(10000)) {
				response.rsp_cd = "-2";
				response.rsp_msg = "async time out!";
				return response;
			}

			response.success = true;
			return response;
		}


		LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
			auto xm = message - WM_USER;
			std::cout << "XM=" << xm << ", wParam=" << wParam << ", lParam=" << lParam << std::endl;
			switch (xm) {
			case XM_LOGIN:
			{
				AsyncNode* node = m_asyncManager.GetNode(0);
				if (node) {
					if (node->callback_proc)
						node->callback_proc(wParam, lParam);
					node->set();
				}
			}
				break;
			case XM_RECEIVE_DATA:
			{
				switch (wParam)
				{
				case REQUEST_DATA:
				case MESSAGE_DATA:
				case SYSTEM_ERROR_DATA:
				{
					int nRqID = *((int*)lParam);
					AsyncNode* node = m_asyncManager.GetNode(nRqID);
					if (node) {
						if (node->callback_proc)
							node->callback_proc(wParam, lParam);
					}
				}
					break;
				case RELEASE_DATA:
				{
					int nRqID = (int)lParam;
					AsyncNode* node = m_asyncManager.GetNode(nRqID);
					if (node) {
						node->set();
					}
					ETK_ReleaseRequestData(nRqID);
				}
					break;
				default:
					break;
				}
			}
				break;
			default:
				break;
			}
			return 0;
		}
	};
}
