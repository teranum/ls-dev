BEGIN_FUNCTION_MAP
    .Func,해외주식  API 주문체결조회,COSAQ00102,SERVICE=COSAQ00102,headtype=B,CREATOR=이유리,CREDATE=2024-06-24 15:02:15;
    BEGIN_DATA_MAP    
    	COSAQ00102InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		조회구분코드, QryTpCode, QryTpCode, char, 1;
		역순구분코드, BkseqTpCode, BkseqTpCode, char, 1;
		주문시장코드, OrdMktCode, OrdMktCode, char, 2;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		종목번호, IsuNo, IsuNo, char, 12;
		시작주문번호, SrtOrdNo, SrtOrdNo, long, 10;
		주문일자, OrdDt, OrdDt, char, 8;
		체결여부, ExecYn, ExecYn, char, 1;
		통화코드, CrcyCode, CrcyCode, char, 3;
		당일매매적용여부, ThdayBnsAppYn, ThdayBnsAppYn, char, 1;
		대출잔고보유여부, LoanBalHldYn, LoanBalHldYn, char, 1;
	end
    	COSAQ00102OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		조회구분코드, QryTpCode, QryTpCode, char, 1;
		역순구분코드, BkseqTpCode, BkseqTpCode, char, 1;
		주문시장코드, OrdMktCode, OrdMktCode, char, 2;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		종목번호, IsuNo, IsuNo, char, 12;
		시작주문번호, SrtOrdNo, SrtOrdNo, long, 10;
		주문일자, OrdDt, OrdDt, char, 8;
		체결여부, ExecYn, ExecYn, char, 1;
		통화코드, CrcyCode, CrcyCode, char, 3;
		당일매매적용여부, ThdayBnsAppYn, ThdayBnsAppYn, char, 1;
		대출잔고보유여부, LoanBalHldYn, LoanBalHldYn, char, 1;
	end
	COSAQ00102OutBlock2,Out(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌명, AcntNm, AcntNm, char, 40;
		일본시장한글종목명, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		관리지점명, MgmtBrnNm, MgmtBrnNm, char, 40;
		매도체결외화금액, SellExecFcurrAmt, SellExecFcurrAmt, double, 21.4;
		매도체결수량, SellExecQty, SellExecQty, long, 16;
		매수체결외화금액, BuyExecFcurrAmt, BuyExecFcurrAmt, double, 21.4;
		매수체결수량, BuyExecQty, BuyExecQty, long, 16;
	end
	COSAQ00102OutBlock3,ST_COSAQ00102_OUT(*EMPTY*),output,occurs;
	begin
		관리지점번호, MgmtBrnNo, MgmtBrnNo, char, 3;
		계좌번호, AcntNo, AcntNo, char, 20;
		계좌명, AcntNm, AcntNm, char, 40;
		체결시각, ExecTime, ExecTime, char, 9;
		주문시각, OrdTime, OrdTime, char, 9;
		주문번호, OrdNo, OrdNo, long, 10;
		원주문번호, OrgOrdNo, OrgOrdNo, long, 10;
		단축종목번호, ShtnIsuNo, ShtnIsuNo, char, 9;
		주문처리유형명, OrdTrxPtnNm, OrdTrxPtnNm, char, 50;
		주문처리유형코드, OrdTrxPtnCode, OrdTrxPtnCode, long, 9;
		정정취소가능수량, MrcAbleQty, MrcAbleQty, long, 16;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 22.7;
		체결수량, ExecQty, ExecQty, long, 16;
		해외체결가, OvrsExecPrc, OvrsExecPrc, double, 28.7;
		호가유형코드, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		호가유형명, OrdprcPtnNm, OrdprcPtnNm, char, 40;
		주문유형명, OrdPtnNm, OrdPtnNm, char, 40;
		주문유형코드, OrdPtnCode, OrdPtnCode, char, 2;
		정정취소구분코드, MrcTpCode, MrcTpCode, char, 1;
		정정취소구분명, MrcTpNm, MrcTpNm, char, 10;
		전체체결수량, AllExecQty, AllExecQty, long, 16;
		통신매체코드, CommdaCode, CommdaCode, char, 2;
		주문시장코드, OrdMktCode, OrdMktCode, char, 2;
		시장명, MktNm, MktNm, char, 40;
		통신매체명, CommdaNm, CommdaNm, char, 40;
		일본시장한글종목명, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		미체결수량, UnercQty, UnercQty, long, 16;
		확인수량, CnfQty, CnfQty, long, 16;
		통화코드, CrcyCode, CrcyCode, char, 3;
		등록시장코드, RegMktCode, RegMktCode, char, 2;
		종목번호, IsuNo, IsuNo, char, 12;
		중개인구분코드, BrkTpCode, BrkTpCode, char, 2;
		상대중개인명, OppBrkNm, OppBrkNm, char, 40;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		대출일자, LoanDt, LoanDt, char, 8;
		대출금액, LoanAmt, LoanAmt, long, 16;
	end
    END_DATA_MAP
END_FUNCTION_MAP
