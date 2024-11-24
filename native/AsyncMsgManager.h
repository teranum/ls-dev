#pragma once

#include <vector>
#include <functional>
#include <utility>

namespace xing
{
	class AsyncNode
	{
	public:
		AsyncNode(int ident)
			: m_ident(ident)
		{
		}

		int m_ident;
		bool m_bDone = false;
		std::function<void(WPARAM, LPARAM)> callback_proc;

		auto set()
		{
			m_bDone = true;
		}

		bool wait(int rel_time = 0) const
		{
			// message loop
			auto start_time = GetTickCount64();
			MSG msg;

			// Main message loop:
			while (GetMessage(&msg, nullptr, 0, 0))
			{
				//if (!TranslateAccelerator(msg.hwnd, nullptr, &msg))
				{
					TranslateMessage(&msg);
					DispatchMessage(&msg);

					if (m_bDone)
					{
						break;
					}
				}
				if (rel_time > 0)
				{
					auto current_time = GetTickCount64();
					if (current_time - start_time > rel_time)
					{
						return false;
					}
				}
			}

			return true;
		}
	};

	class AsyncMsgManager
	{
		std::vector<AsyncNode*> m_pnodes;
	public:
		~AsyncMsgManager()
		{
			for (auto it = m_pnodes.begin(); it != m_pnodes.end(); ++it)
			{
				delete* it;
			}
			m_pnodes.clear();
		}

		AsyncNode* GetNode(int ident) const
		{
			for (auto it = m_pnodes.begin(); it != m_pnodes.end(); ++it)
			{
				if ((*it)->m_ident == ident)
				{
					return *it;
				}
			}
			return nullptr;
		}

		AsyncNode* CreateNode(int ident)
		{
			auto node = new AsyncNode(ident);
			m_pnodes.push_back(node);
			return node;
		}

		void RemoveNode(AsyncNode* node)
		{
			for (auto it = m_pnodes.begin(); it != m_pnodes.end(); ++it)
			{
				if (*it == node)
				{
					m_pnodes.erase(it);
					delete node;
					break;
				}
			}
		}

		static void Sleep(int delay_ms)
		{
			int64_t start_time = GetTickCount64();
			MSG msg;
			// Main message loop:
			while (GetMessage(&msg, nullptr, 0, 0))
			{
				//if (!TranslateAccelerator(msg.hwnd, nullptr, &msg))
				{
					TranslateMessage(&msg);
					DispatchMessage(&msg);
				}
				if (delay_ms > 0)
				{
					auto current_time = GetTickCount64();
					if (current_time - start_time > delay_ms)
					{
						break;
					}
				}
			}
		}
	};
}