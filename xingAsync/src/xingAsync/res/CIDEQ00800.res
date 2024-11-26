BEGIN_FUNCTION_MAP
    .Func,일자별 미결제 잔고내역,CIDEQ00800,SERVICE=CIDEQ00800,ENCRYPT,headtype=B,CREATOR=강현진,CREDATE=2024-09-30 09:43:35;
    BEGIN_DATA_MAP    
    	CIDEQ00800InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		계좌비밀번호, AcntPwd, AcntPwd, char, 8;
		거래일자, TrdDt, TrdDt, char, 8;
	end
    	CIDEQ00800OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		계좌비밀번호, AcntPwd, AcntPwd, char, 8;
		거래일자, TrdDt, TrdDt, char, 8;
	end
	CIDEQ00800OutBlock2,Out(*EMPTY*),output,occurs;
	begin
		계좌번호, AcntNo, AcntNo, char, 20;
		거래일자, TrdDt, TrdDt, char, 8;
		종목코드값, IsuCodeVal, IsuCodeVal, char, 30;
		매매구분명, BnsTpNm, BnsTpNm, char, 10;
		잔고수량, BalQty, BalQty, long, 16;
		청산가능수량, LqdtAbleQty, LqdtAbleQty, long, 16;
		매입가격, PchsPrc, PchsPrc, double, 30.11;
		해외파생현재가, OvrsDrvtNowPrc, OvrsDrvtNowPrc, double, 30.11;
		해외선물평가손익금액, AbrdFutsEvalPnlAmt, AbrdFutsEvalPnlAmt, double, 19.2;
		고객잔고금액, CustmBalAmt, CustmBalAmt, double, 19.2;
		외화평가금액, FcurrEvalAmt, FcurrEvalAmt, double, 21.4;
		종목명, IsuNm, IsuNm, char, 50;
		통화코드값, CrcyCodeVal, CrcyCodeVal, char, 3;
		해외파생상품코드, OvrsDrvtPrdtCode, OvrsDrvtPrdtCode, char, 10;
		만기일자, DueDt, DueDt, char, 8;
		계약당금액, PrcntrAmt, PrcntrAmt, double, 19.2;
		외화평가손익금액, FcurrEvalPnlAmt, FcurrEvalPnlAmt, double, 21.4;
		원화환산평가손익금액, WonConvEvalPnlAmt, WonConvEvalPnlAmt, long, 16;
	end
    END_DATA_MAP
END_FUNCTION_MAP
