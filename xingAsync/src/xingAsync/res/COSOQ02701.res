BEGIN_FUNCTION_MAP
    .Func,해외주식 예수금 조회 API,COSOQ02701,SERVICE=COSOQ02701,headtype=B,CREATOR=이유리,CREDATE=2024-06-04 09:46:07;
    BEGIN_DATA_MAP    
    	COSOQ02701InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		통화코드, CrcyCode, CrcyCode, char, 3;
	end
    	COSOQ02701OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		통화코드, CrcyCode, CrcyCode, char, 3;
	end
	COSOQ02701OutBlock2,Out1(*EMPTY*),output,occurs;
	begin
		통화코드, CrcyCode, CrcyCode, char, 3;
		외화매수정산금1, FcurrBuyAdjstAmt1, FcurrBuyAdjstAmt1, double, 17.4;
		외화매수정산금2, FcurrBuyAdjstAmt2, FcurrBuyAdjstAmt2, double, 17.4;
		외화매수정산금3, FcurrBuyAdjstAmt3, FcurrBuyAdjstAmt3, double, 17.4;
		외화매수정산금4, FcurrBuyAdjstAmt4, FcurrBuyAdjstAmt4, double, 17.4;
		외화매도정산금1, FcurrSellAdjstAmt1, FcurrSellAdjstAmt1, double, 17.4;
		외화매도정산금2, FcurrSellAdjstAmt2, FcurrSellAdjstAmt2, double, 17.4;
		외화매도정산금3, FcurrSellAdjstAmt3, FcurrSellAdjstAmt3, double, 17.4;
		외화매도정산금4, FcurrSellAdjstAmt4, FcurrSellAdjstAmt4, double, 17.4;
		추정외화예수금1, PrsmptFcurrDps1, PrsmptFcurrDps1, double, 17.4;
		추정외화예수금2, PrsmptFcurrDps2, PrsmptFcurrDps2, double, 17.4;
		추정외화예수금3, PrsmptFcurrDps3, PrsmptFcurrDps3, double, 17.4;
		추정외화예수금4, PrsmptFcurrDps4, PrsmptFcurrDps4, double, 17.4;
		추정환전가능금1, PrsmptMxchgAbleAmt1, PrsmptMxchgAbleAmt1, double, 17.4;
		추정환전가능금2, PrsmptMxchgAbleAmt2, PrsmptMxchgAbleAmt2, double, 17.4;
		추정환전가능금3, PrsmptMxchgAbleAmt3, PrsmptMxchgAbleAmt3, double, 17.4;
		추정환전가능금4, PrsmptMxchgAbleAmt4, PrsmptMxchgAbleAmt4, double, 17.4;
	end
	COSOQ02701OutBlock3,Out2(*EMPTY*),output,occurs;
	begin
		국가명, CntryNm, CntryNm, char, 40;
		통화코드, CrcyCode, CrcyCode, char, 3;
		T4외화예수금, T4FcurrDps, T4FcurrDps, double, 21.4;
		외화예수금, FcurrDps, FcurrDps, double, 17.4;
		외화주문가능금액, FcurrOrdAbleAmt, FcurrOrdAbleAmt, double, 17.4;
		가환전주문가능금액, PrexchOrdAbleAmt, PrexchOrdAbleAmt, double, 21.4;
		외화주문금액, FcurrOrdAmt, FcurrOrdAmt, double, 24.4;
		외화담보금액, FcurrPldgAmt, FcurrPldgAmt, double, 17.4;
		체결재사용외화금액, ExecRuseFcurrAmt, ExecRuseFcurrAmt, double, 17.4;
		외화환전가능금, FcurrMxchgAbleAmt, FcurrMxchgAbleAmt, double, 17.4;
		기준환율, BaseXchrat, BaseXchrat, double, 15.4;
	end
	COSOQ02701OutBlock4,Out3(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		원화예수금잔고금액, WonDpsBalAmt, WonDpsBalAmt, long, 16;
		출금가능금액, MnyoutAbleAmt, MnyoutAbleAmt, long, 16;
		원화가환전가능금액, WonPrexchAbleAmt, WonPrexchAbleAmt, long, 16;
		해외증거금, OvrsMgn, OvrsMgn, long, 17;
	end
	COSOQ02701OutBlock5,Out4(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		내외국인코드, NrfCode, NrfCode, char, 2;
	end
    END_DATA_MAP
END_FUNCTION_MAP
