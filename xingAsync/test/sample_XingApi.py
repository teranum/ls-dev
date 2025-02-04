################################################
# DLL모드(XingApi)를 이용한 국내주식/국내선물/해외선물/해외주식 샘플코드
# pip install xingAsync
# pip install PyQt5
# pip install qasync
# pip install prettytable
################################################

import asyncio
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic
from qasync import QEventLoop, asyncSlot
from xingAsync import XingApi
from xingAsync.models import ResponseData
from prettytable import PrettyTable
# app_key.py 파일에 사용자 ID, 비번, 공증 비번, 계좌비번을 저장해두고 import
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number

os.chdir(os.path.dirname(__file__))
form_class = uic.loadUiType('mainform.ui')[0]

class MainWindow(QMainWindow, form_class):
    samples = [
        "계좌조회",
        "업종-마스터조회", "업종-기간별추이",
        "투자정보-투자의견", "투자정보-종목별 증시일정", "투자정보-FNG_요약", "투자정보-재무순위종합",
        "국내주식-마스터-코스피", "국내주식-마스터-코스닥", "국내주식-현재가", "국내주식-현재가 시세메모",
        "국내주식-멀티종목 현재가", "국내주식-차트-분", "국내주식-차트-일주월년", "국내주식-차트-연속조회",
        "국내주식-수급", "국내주식-조건리스트", "국내주식-e종목검색",
        "국내주식-예수금조회", "국내주식-잔고조회", "국내주식-미체결조회",
        "국내선물-마스터조회", "국내선물-옵션전광판", "국내선물-차트-분",
        "국내선물-예수금조회", "국내선물-잔고조회", "국내선물-미체결조회",
        "해외선물-마스터조회", "해외선물-관심종목조회", "해외선물-차트-분",
        "해외선물-예수금조회", "해외선물-잔고조회", "해외선물-미체결조회",
        "해외주식-마스터조회", "해외주식-종목정보", "해외주식-현재가",
        "해외주식-차트-분", "해외주식-차트-일주월년",
        "해외주식-예수금조회", "해외주식-잔고조회", "해외주식-미체결조회",
        "실시간구독", "실시간해지",
    ]
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        widget_all = QWidget()
        widget_all.setContentsMargins(10, 10, 10, 10)
        widget_all.setLayout(self.verticalLayout)

        self.setCentralWidget(widget_all)
        self.combo_samples.addItems(self.samples)

        self.text_user_id.setText(user_id)
        self.text_user_pwd.setText(user_pwd)
        self.text_cert_pwd.setText(cert_pwd)

        self.btn_login.clicked.connect(self.on_login)
        self.btn_run.clicked.connect(self.on_run)
        self.btn_clear.clicked.connect(self.text_result.clear)

        self.setWindowTitle("XingAPI Test")
        self.api = XingApi()
        self.api.on_message.connect(lambda msg: self.print(f"on_message: {msg}"))
        self.api.on_realtime.connect(lambda tr_cd, key, data: self.print(f"on_realtime: {tr_cd}, {key}, {data}"))

    def print(self, data:str|ResponseData|list):
        if isinstance(data, ResponseData):
            text = f"{data.tr_cd}: [{data.rsp_cd}] {data.rsp_msg}\n"
            text += f"cont_yn: {data.cont_yn}\n"
            text += f"cont_key: {data.cont_key}\n"
            if data.res:
                for block in data.res.out_blocks:
                    block_data = data.body.get(block.name)
                    if block_data:
                        table = PrettyTable()
                        table.field_names = [x.name for x in block.fields]
                        if isinstance(block_data, list):
                            text += f"{block.name}, fields={len(block.fields)}, count={len(block_data)}\n"
                            for row in block_data:
                                table.add_row(row.values())
                        elif isinstance(block_data, dict):
                            text += f"{block.name},fields={len(block.fields)}\n"
                            table.add_row(block_data.values())
                        text += table.get_string() + "\n"
            text += f"elapsed_ms: {data.elapsed_ms}\n"
            self.text_result.appendPlainText(text)
        elif isinstance(data, list):
            row_count = len(data)
            text = f"RowCount={row_count}\n"
            if row_count > 0:
                table = PrettyTable()
                if isinstance(data[0], dict):
                    table.field_names = data[0].keys()
                for row in data:
                    table.add_row(row.values())
                text += table.get_string() + "\n"
            self.text_result.appendPlainText(text)
        else:
            self.text_result.appendPlainText(str(data))

    @asyncSlot()
    async def on_login(self):
        ret = await self.api.login(self.text_user_id.text(), self.text_user_pwd.text(), self.text_cert_pwd.text())
        self.print(self.api.last_message)
        if ret:
            self.btn_login.setEnabled(False)

    @asyncSlot()
    async def on_run(self):
        if self.check_clear.isChecked():
            self.text_result.clear()
        if not self.api.logined:
            self.print("로그인이 필요합니다.")
            return
        api = self.api
        sample = self.combo_samples.currentText()
        response = None
        match sample:
            case "계좌조회":
                response = str()
                for acc in api.accounts:
                    response += str(acc) + "\n"

            case "업종-마스터조회":
                response = await api.request("t8424", {"gubun1": "0"})

            case "업종-기간별추이":
                inputs = {
                    "upcode": "001",    # 업종코드 (001: 종합...)
                    "gubun2": "1",      # "1: 일별, 2: 주별, 3: 월별
                    "cnt": 100,         # 조회건수
                    "rate_gbn": "2",    # 비중구분 (1: 거래량, 2: 거래대금)
                }
                response = await api.request("t1514", inputs)

            case "업종-차트":
                inputs = {
                    "shcode": "001",    # 업종코드 (001: 종합...)
                    "gubun": "1",       # 주기구분 (0:틱1:분2:일3:주4:월)
                    "ncnt": 100,        # 틱개수
                    "qrycnt": 100,      # 조회건수 (1 이상 500 이하값만 유효)
                    "tdgb": "0",        # 당일구분 (0:전체1:당일만)
                    "sdate": "",        # 시작일자
                    "edate": "",        # 종료일자
                    "cts_date": "",     # 연속일자
                    "cts_time": "",     # 연속시간
                    "cts_daygb": "",    # 연속당일구분(0:연속전체1:연속당일만2:연속전일만)
                }
                response = await api.request("t4203", inputs)

            case "투자정보-투자의견":
                response = await api.request("t3401", "005930")

            case "투자정보-종목별 증시일정":
                response = await api.request("t3202", "005930")

            case "투자정보-FNG_요약":
                response = await api.request("t3320", "005930")

            case "투자정보-재무순위종합":
                inputs = {
                    "gubun": "0",   # 시장구분(0:전체1:코스피2:코스닥))
                    "gubun1": "2",  # 순위구분(1:매출액증가율2:영업이익증가율3:세전계속이익증가율4:부채비율5:유보율6:EPS7:BPS8:ROE9:PERa:PBRb:PEG)
                    "gubun2": "1",  # 1 고정
                    "idx": 0,       # 첫조회시 space, 연속조회시 Outblock의 idx 값 세팅
                }
                response = await api.request("t3341", inputs)

            case "국내주식-마스터-코스피":
                response = await api.request("t9945", "1")

            case "국내주식-마스터-코스닥":
                response = await api.request("t9945", "2")

            case "국내주식-현재가":
                # 005930: 삼성전자
                response = await api.request("t1102", "005930")

            case "국내주식-현재가 시세메모":
                inputs = {
                    "t1104InBlock": {
                        "code": "005930",    # 종목코드
                        "nrec": "4",         # 건수
                    },
                    "t1104InBlock1": [
                        {"indx": "0", "gubn": "1", "dat1": "2", "dat2": "1"}, 
                        {"indx": "1", "gubn": "1", "dat1": "3", "dat2": "1"}, 
                        {"indx": "2", "gubn": "4", "dat1": "1", "dat2": "5"}, 
                        {"indx": "3", "gubn": "4", "dat1": "1", "dat2": "20"}, 
                    ],
                }
                response = await api.request("t1104", inputs)

            case "국내주식-멀티종목 현재가":
                inputs = {
                    "nrec": 3, # 건수: 최대 50개까지
                    "shcode": "078020000660005930", # 종목코드: 구분자 없이 종목코드를 붙여서 입력, 078020, 000660, 005930 을 전송시|@078020000660005930 을 입력
                }
                response = await api.request("t8407", inputs)

            case "국내주식-차트-분":
                inputs = {
                    "shcode": "005930",     # 삼성전자
                    "ncnt": "10",           # 단위(n분)(0: 30초, 1: 1분, 2: 2분, ...n: n분)
                    "qrycnt": 100,          # 요청건수(최대-압축:2000비압축:500)
                    "nday": "0",            # 조회영업일수(0:미사용1>=사용)
                    "sdate": "",            # 시작일자
                    "stime": "",            # 시작시간(현재미사용)
                    "edate": "99999999",    # 종료일자
                    "etime": "",            # 종료시간(현재미사용)
                    "cts_date": "",         # 연속일자
                    "cts_time": "",         # 연속시간
                    "comp_yn": "N",         # 압축여부(Y:압축N:비압축)
                }
                response = await api.request("t8412", inputs)

            case "국내주식-차트-일주월년":
                inputs = {
                    "shcode": "005930",     # 삼성전자
                    "gubun": "2",           # 주기구분(2:일3:주4:월5:년)
                    "qrycnt": 2000,         # 요청건수(최대-압축:2000비압축:500)
                    "sdate": "",            # 시작일자
                    "edate": "99999999",    # 종료일자
                    "cts_date": "",         # 연속일자
                    "comp_yn": "Y",         # 압축여부(Y:압축N:비압축)
                    "sujung": "Y",          # 수정주가여부(Y:적용N:비적용)
                }
                response = await api.request("t8410", inputs)

            case "국내주식-차트-연속조회":
                inputs = {
                    "shcode": "005930",     # 삼성전자
                    "gubun": "2",           # 주기구분(2:일3:주4:월5:년)
                    "qrycnt": 2000,         # 요청건수(최대-압축:2000비압축:500)
                    "sdate": "",            # 시작일자
                    "edate": "99999999",    # 종료일자
                    "cts_date": "",         # 연속일자
                    "comp_yn": "Y",         # 압축여부(Y:압축N:비압축)
                    "sujung": "Y",          # 수정주가여부(Y:적용N:비적용)
                }
                response = await api.request("t8410", inputs)
                if not response: return self.print(f"요청실패: {api.last_message}")
                all_data = response["t8410OutBlock1"]
                 # 연속조회
                if response.cont_yn: # 연속조회가능
                    inputs["cts_date"] = response["t8410OutBlock"]["cts_date"]
                    response = await api.request("t8410", inputs, True)
                    if not response: return self.print(f"연속요청 실패: {api.last_message}")
                    all_data = response["t8410OutBlock1"] + all_data
                response = all_data

            case "국내주식-수급":
                inputs = {
                    "shcode": "005930", # 단축코드
                    "dwmcode": 1,       # 일주월구분 (일@1, 주@2, 월@3, 분)
                    "date": "",         # 날짜 (처음 조회시는 Space, 연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정)
                    "idx": 0,           # IDX (사용안함)
                    "cnt": 10,          # 건수 (1이상)
                }
                response = await api.request("t1305", inputs)

            case "국내주식-조건리스트":
                # 조건리스트보관용 변수 cond_list 체크, 변수 없는 경우 조건리스트트 요청/보관
                if not hasattr(api, "cond_list"):
                    response = await api.request("t1866", {"user_id": user_id, "gb":"0"}) # t1826: 종목Q클릭검색리스트
                    if not response: return self.print(f"서버리스트 요청실패: {api.last_message}")
                    if response["t1866OutBlock"]["result_count"] == 0: return self.print("조건식이 없습니다.")
                    api.cond_list = response["t1866OutBlock1"]
                response = api.cond_list

            case "국내주식-e종목검색":
                if not hasattr(api, "cond_list"):
                    self.print("조건리스트 요청후 다시 시도해 주세요")
                    return
                # 첫번째 조건식 요청한다
                if hasattr(api, "cond_list"):
                    self.print(f"조건식: {api.cond_list[0]['query_name']}")
                    response = await api.request("t1857", ["0", "S", api.cond_list[0]["query_index"]])

            case "국내주식-예수금조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # CSPAQ22200: 현물계좌예수금 주문가능금액 총평가2
                inputs = {"RecCnt":1, "AcntNo": acc.number, "Pwd": pass_number, "BalCreTp": "0"}
                response = await api.request("CSPAQ22200", inputs)

            case "국내주식-잔고조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                inputs = {
                    "accno": acc.number,    # 계좌번호
                    "passwd": pass_number,  # 계좌비밀번호
                    "prcgb": "1",           # 단가구분 : 1:평균단가, 2:BEP단가
                    "chegb": "2",           # 체결구분 : 0: 결제기준잔고, 2: 체결기준잔고(잔고가 없는 종목은 제외)
                    "dangb": "0",           # 단일가구분 : 0:정규장, 1:시간외 단일가
                    "charge": "1",          # 제비용포함여부 : 0:미포함, 1:포함
                    "cts_expcode": "",      # CTS종목번호 : 연속 조회시에 이전 조회한 OutBlock의 cts_expcode 값으로 설정
                }
                response = await api.request("t0424", inputs)

            case "국내주식-미체결조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                inputs = {
                    "accno": acc.number,    # 계좌번호
                    "passwd": pass_number,  # 계좌비밀번호
                    "expcode": "",          # 종목코드
                    "chegb": "2",           # 체결구분 : 0:전체, 1:체결, 2:미체결
                    "medosu": "0",          # 매도수구분 : 0:전체, 1:매도, 2:매수
                    "sortgb": "1",          # 정렬기준 : 1:주문번호 역순, 2:주문번호 순
                    "cts_ordno": "",        # 연속조회키 : 연속조회시 사용
                }
                response = await api.request("t0425", inputs)

            case "국내선물-마스터조회":
                inputs = {
                    "gubun": "0", # V:변동성지수선물, S:섹터지수선물, 그 이외의 값은 코스피200지수선물
                    }
                response = await api.request("t8432", inputs)

            case "국내선물-옵션전광판":
                inputs = {
                    "yyyymm": "W1MON", # 미니,정규: "200604",  위클리: "W1MON",  "W1THU"...
                    "gubun": "W", # M:미니, G:정규, W:위클리
                }
                # ["W1MON", "W"] 위클리 1주차 월요일 만기
                # ["W4THU", "W"] 위클리 4주차 목요일 만기
                # ["202502", "M"] 미니 
                response = await api.request("t2301", inputs)

            case "국내선물-차트-분":
                inputs = {
                    "shcode": "90199999",   # 단축코드 (코스피200 연결선물 : 90199999, 코스닥150 연결선물 : 90699999)
                    "ncnt": 1,              # 단위(n분)
                    "qrycnt": 100,          # 요청건수(최대-압축:2000비압축:500)
                    "nday": "",             # 조회영업일수(0:미사용1>=사용)
                    "sdate": "",            # 시작일자
                    "stime": "",            # 시작시간(현재미사용)
                    "edate": "99999999",    # 종료일자
                    "etime": "",            # 종료시간(현재미사용)
                    "cts_date": "",         # 연속일자
                    "cts_time": "",         # 연속시간
                    "comp_yn": "N",         # 압축여부(Y:압축N:비압축)
                    }
                response = await api.request("t8415", inputs)

            case "국내선물-예수금조회":
                # 계좌번호 가져오기
                acc_name = "선물옵션"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # CFOBQ10500: 선물옵션 계좌예탁금증거금조회
                inputs = {"RecCnt": 1, "AcntNo": acc.number, "Pwd": pass_number}
                response = await api.request("CFOBQ10500", inputs)

            case "국내선물-잔고조회":
                # 계좌번호 가져오기
                acc_name = "선물옵션"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # t0441: 선물/옵션잔고평가(이동평균)
                inputs = {
                    "accno": acc.number,    # 계좌번호
                    "passwd": pass_number,  # 비밀번호
                    "cts_expcode": "",      # CTS_종목번호
                    "cts_medocd": "",       # CTS_매매구분
                }
                response = await api.request("t0441", inputs)

            case "국내선물-미체결조회":
                # 계좌번호 가져오기
                acc_name = "선물옵션"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # t0434: 선물/옵션체결/미체결
                inputs = {
                    "accno": acc.number,    # 계좌번호
                    "passwd": pass_number,  # 비밀번호
                    "expcode": "",          # 종목번호
                    "chegb": "2",           # 체결구분: 0:전체, 1:체결, 2:미체결
                    "sortgb": "1",          # 정렬순서: 1:주문번호 역순, 2:주문번호 순
                    "cts_ordno": "",        # CTS_주문번호
                }
                response = await api.request("t0434", inputs)

            case "해외선물-마스터조회":
                inputs = {
                    "MktGb": "F",   # 시장구분 (F:해외선물, O:해외옵션)
                    "BscGdsCd": "", # 옵션기초상품코드
                    }
                response = await api.request("o3121", inputs)

            case "해외선물-관심종목조회":
                # 해외선물시장 최근월물 조회
                response = await api.request("o3101", "")
                if not response: return self.print(f"o3101 요청실패: {api.last_message}")

                comp_BscGdsCd = ""
                recent_code_lists = []
                market_items = response["o3101OutBlock"]
                for item in market_items:
                    BscGdsCd = item["BscGdsCd"]
                    if BscGdsCd != comp_BscGdsCd:
                        comp_BscGdsCd = BscGdsCd
                        recent_code_lists.append(item["Symbol"])
                self.print(f"해외선물시장 {len(market_items)}종목중 최근월물 {len(recent_code_lists)}종목 조회")

                # 조회개수, F, 종목코드1, F, 종목코드2, ... 형식으로 전달
                indatas = str(len(recent_code_lists)) + "," + ",".join(["F,"+code for code in recent_code_lists])
                response = await api.request("o3127", indatas)

            case "해외선물-차트-분":
                # 해외선물시장 최근월물 조회
                response = await api.request("o3101", "")
                if not response: return self.print(f"o3101 요청실패: {api.last_message}")
                # 항셍 최근월물 찾기
                code = next((item["Symbol"] for item in response["o3101OutBlock"] if item["SymbolNm"].startswith("Hang Seng(")), None)
                if not code: return self.print("항셍 최근월물을 찾을 수 없습니다.")
                inputs = {
                    "mktgb": "F",       # 시장구분 (F:해외선물, O:해외옵션)
                    "shcode": code,     # 단축코드
                    "ncnt": 1,          # N분주기
                    "readcnt": 100,     # 조회건수
                    "cts_date": "",     # 연속일자
                    "cts_time": "",     # 연속시간
                    }
                response = await api.request("o3123", inputs)

            case "해외선물-예수금조회":
                # 계좌번호 가져오기
                acc_name = ["해외선물", "해외선옵"]
                acc = next((item for item in api.accounts if item.detail_name in acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # CIDBQ05300: 해외선물 계좌예탁자산 조회
                inputs = {"RecCnt": 1, "OvrsAcntTpCode": "1", "AcntNo": acc.number, "AcntPwd": pass_number, "CrcyCode": "ALL"}
                response = await api.request("CIDBQ05300", inputs)

            case "해외선물-잔고조회":
                # 계좌번호 가져오기
                acc_name = ["해외선물", "해외선옵"]
                acc = next((item for item in api.accounts if item.detail_name in acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # CIDBQ01500: 해외선물 미결제 잔고내역 조회
                inputs = {"RecCnt": 1, "AcntTpCode": "1", "AcntNo": acc.number, "Pwd": pass_number, "BalTpCode": "1"}
                response = await api.request("CIDBQ01500", inputs)

            case "해외선물-미체결조회":
                # 계좌번호 가져오기
                acc_name = ["해외선물", "해외선옵"]
                acc = next((item for item in api.accounts if item.detail_name in acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # CIDBQ01800: 해외선물 주문체결내역 조회
                inputs = {
                    "RecCnt": 1,                # 레코드갯수
                    "AcntNo": acc.number,       # 계좌번호
                    "Pwd": pass_number,         # 비밀번호
                    "IsuCodeVal": "",           # 종목코드값
                    "OrdDt": "99999999",        # 주문일자
                    "ThdayTpCode": "",          # 당일구분코드
                    "OrdStatCode": "2",         # 주문상태코드 (0:전체, 1:체결, 2:미체결)
                    "BnsTpCode": "0",           # 매매구분코드 (0:전체, 1:매도, 2:매수)
                    "QryTpCode": "1",           # 조회구분코드 (1:역순 2:정순)
                    "OrdPtnCode": "00",         # 주문유형코드 (00:전체 01:일반 02:Average 03:Spread)
                    "OvrsDrvtFnoTpCode": "A",   # 해외파생선물옵션구분코드 (A:전체 F:선물 O:옵션)
                    }
                response = await api.request("CIDBQ01800", inputs)

            case "해외주식-마스터조회":
                inputs = {
                    "delaygb": "R",     # 지연구분
                    "natcode": "US",    # 국가구분
                    "exgubun": "2",     # 거래소구분 (1:뉴욕, 2:나스닥, 3:아멕스, 4:미국전체)
                    "readcnt": 0,       # 조회갯수
                    "cts_value": "",    # 연속구분
                    }
                response = await api.request("g3190", inputs)

            case "해외주식-종목정보":
                keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
                response = await api.request("g3104", ["R", keysymbol, keysymbol[:2], keysymbol[2:]])

            case "해외주식-현재가":
                keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
                response = await api.request("g3101", ["R", keysymbol, keysymbol[:2], keysymbol[2:]])

            case "해외주식-차트-분":
                keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
                inputs = {
                    "delaygb": "R",             # 지연구분 "R":실시간
                    "keysymbol": keysymbol,     # KEY종목코드
                    "exchcd": keysymbol[:2],    # 거래소코드(81: 뉴욕/아멕스, 82: 나스닥)
                    "symbol": keysymbol[2:],    # 종목코드
                    "ncnt": 10,                 # 단위(n분)
                    "qrycnt": 100,              # 요청건수(최대-압축:2000비압축:500)
                    "comp_yn": "N",             # 압축여부(Y:압축N:비압축)
                    "sdate": "",                # 시작일자
                    "edate": "",                # 종료일자
                    "cts_date": "",             # 연속일자 (연속조회시 필요)
                    "cts_time": "",             # 연속시간 (연속조회시 필요)
                    }
                response = await api.request("g3203", inputs)

            case "해외주식-차트-일주월년":
                keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
                inputs = {
                    "delaygb": "R",             # 지연구분 "R":실시간
                    "keysymbol": keysymbol,     # KEY종목코드
                    "exchcd": keysymbol[:2],    # 거래소코드(81: 뉴욕/아멕스, 82: 나스닥)
                    "symbol": keysymbol[2:],    # 종목코드
                    "gubun": "2",               # 2:일, 3:주, 4:월, 5:년
                    "qrycnt": 2000,             # 요청건수(최대-압축:2000비압축:500)
                    "comp_yn": "Y",             # 압축여부(Y:압축N:비압축)
                    "sdate": "",                # 시작일자
                    "edate": "",                # 종료일자
                    "cts_date": "",             # 연속일자 (연속조회시 필요)
                    "cts_info": "",             # 연속정보 (연속조회시 필요)
                    "sujung": "Y",              # 수정주가여부(Y:적용N:비적용)
                    }
                response = await api.request("g3204", inputs)

            case "해외주식-예수금조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                # COSOQ02701: 해외주식 예수금 조회 API
                inputs = {"RecCnt": 1, "AcntNo": acc.number, "Pwd": pass_number, "CrcyCode": "ALL"}
                response = await api.request("COSOQ02701", inputs)

            case "해외주식-잔고조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                inputs = {
                    "RecCnt": 1,            # 레코드갯수
                    "AcntNo": acc.number,   # 계좌번호
                    "Pwd": pass_number,     # 비밀번호
                    "BaseDt": "",           # 기준일자
                    "CrcyCode": "USD",      # 통화코드 (ALL:전체, USD:달러)
                    "AstkBalTpCode": "00",  # 해외증권잔고구분코드 (00:전체, 10:일반, 20:소수점))
                    }
                response = await api.request("COSOQ00201", inputs)

            case "해외주식-미체결조회":
                # 계좌번호 가져오기
                acc_name = "종합매매"
                acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
                if not acc: return self.print(f"{acc_name} 계좌가 없습니다.")
                pass_number = "0000" if api.is_simulation else acc_pwd_number

                inputs = {
                    "RecCnt": 1,            # 레코드갯수
                    "QryTpCode": "1",       # 조회구분코드 (1@계좌별)
                    "BkseqTpCode": "2",     # 역순구분코드 (1@역순, 2@정순)
                    "OrdMktCode": "82",     # 주문시장코드 (81@유욕거래소, 82@나스닥)
                    "AcntNo": acc.number,   # 계좌번호
                    "Pwd": pass_number,     # 비밀번호
                    "BnsTpCode": "0",       # 매매구분코드 (0@전체, 1@매도, 2@매수)
                    "IsuNo": "",            # 종목번호
                    "SrtOrdNo": 0,          # 시작주문번호 (역순인경우 9999999999, 정순인경우 0)
                    "OrdDt": "",            # 주문일자
                    "ExecYn": "2",          # 체결여부 (0@전체, 1@체결, 2@미체결)
                    "CrcyCode": "USD",      # 통화코드 (000:전체, USD:달러)
                    "ThdayBnsAppYn": "0",   # 당일매매적용여부 (0@전체, 1@당일적용)
                    "LoanBalHldYn": "0",    # 대출잔고보유여부 (0@전체, 1@대출잔고보유)
                    }
                response = await api.request("COSAQ00102", inputs)

            case "실시간구독":
                # 삼성전자 현재가 실시간 구독
                api.realtime("S3_", "005930", True)

                # 항셍 최근월물 실시간 구독
                # 해외선물시장 최근월물 조회/항셍 최근월물 찾기/실시간구독
                response = await api.request("o3101", "")
                if not response: return self.print(f"o3101 요청실패: {api.last_message}")
                code = next((item["Symbol"] for item in response["o3101OutBlock"] if item["SymbolNm"].startswith("Hang Seng(")), None)
                if code:
                    api.realtime("OVC",code, True)
                else:
                    self.print("항셍 최근월물을 찾을 수 없습니다.")

                # 해외주식 테슬라 현재가 실시간 구독
                api.realtime("GSC", "82TSLA", True)
                response = "실시간구독 시작"

            case "실시간해지":
                # # 삼성전자 현재가 실시간 구독해지
                # api.realtime("S3_", "005930", False)

                # # 해외주식 테슬라 현재가 실시간 구독해지
                # api.realtime("GSC", "82TSLA", False)

                # 전체실시간 구독 해지
                api.realtime("", "", False)
                response = "전체 실시간구독 해제"

        if response:
            self.print(response)
        else:
            self.print(f"{sample} request failed: {api.last_message}")

if __name__ == '__main__':
    '''메인함수'''
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    
    with loop:
        loop.run_forever()
