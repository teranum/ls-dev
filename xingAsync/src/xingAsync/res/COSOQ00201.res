BEGIN_FUNCTION_MAP
    .Func,해외주식 종합잔고평가 API,COSOQ00201,SERVICE=COSOQ00201,ENCRYPT,headtype=B,CREATOR=이유리,CREDATE=2024-06-26 16:43:03;
    BEGIN_DATA_MAP    
    	COSOQ00201InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		기준일자, BaseDt, BaseDt, char, 8;
		통화코드, CrcyCode, CrcyCode, char, 3;
		해외증권잔고구분코드, AstkBalTpCode, AstkBalTpCode, char, 2;
	end
    	COSOQ00201OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		기준일자, BaseDt, BaseDt, char, 8;
		통화코드, CrcyCode, CrcyCode, char, 3;
		해외증권잔고구분코드, AstkBalTpCode, AstkBalTpCode, char, 2;
	end
	COSOQ00201OutBlock2,Out1(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		수익율, ErnRat, ErnRat, double, 18.6;
		예수금환산평가금액, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		주식환산평가금액, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		예탁자산환산평가금액, DpsastConvEvalAmt, DpsastConvEvalAmt, long, 16;
		원화평가합계금액, WonEvalSumAmt, WonEvalSumAmt, long, 16;
		환산평가손익금액, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		원화예수금잔고금액, WonDpsBalAmt, WonDpsBalAmt, long, 16;
		D2추정예수금, D2EstiDps, D2EstiDps, long, 16;
		대출금액, LoanAmt, LoanAmt, long, 16;
	end
	COSOQ00201OutBlock3,Out2(*EMPTY*),output,occurs;
	begin
		통화코드, CrcyCode, CrcyCode, char, 3;
		외화예수금, FcurrDps, FcurrDps, double, 21.4;
		외화평가금액, FcurrEvalAmt, FcurrEvalAmt, double, 21.4;
		외화평가손익금액, FcurrEvalPnlAmt, FcurrEvalPnlAmt, double, 21.4;
		손익율, PnlRat, PnlRat, double, 18.6;
		기준환율, BaseXchrat, BaseXchrat, double, 15.4;
		예수금환산평가금액, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		매입금액, PchsAmt, PchsAmt, long, 16;
		주식환산평가금액, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		환산평가손익금액, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		외화매수금액, FcurrBuyAmt, FcurrBuyAmt, double, 21.4;
		외화주문가능금액, FcurrOrdAbleAmt, FcurrOrdAbleAmt, double, 19.2;
		대출금액, LoanAmt, LoanAmt, long, 16;
	end
	COSOQ00201OutBlock4,Out3(*EMPTY*),output,occurs;
	begin
		통화코드, CrcyCode, CrcyCode, char, 3;
		단축종목번호, ShtnIsuNo, ShtnIsuNo, char, 9;
		종목번호, IsuNo, IsuNo, char, 12;
		일본시장한글종목명, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		해외증권잔고구분코드, AstkBalTpCode, AstkBalTpCode, char, 2;
		해외증권잔고구분코드명, AstkBalTpCodeNm, AstkBalTpCodeNm, char, 40;
		해외증권잔고수량, AstkBalQty, AstkBalQty, double, 28.6;
		해외증권매도가능수량, AstkSellAbleQty, AstkSellAbleQty, double, 28.6;
		외화증권단가, FcstckUprc, FcstckUprc, double, 24.4;
		외화매수금액, FcurrBuyAmt, FcurrBuyAmt, double, 21.4;
		외화증권시장종목코드, FcstckMktIsuCode, FcstckMktIsuCode, char, 18;
		해외증권시세, OvrsScrtsCurpri, OvrsScrtsCurpri, double, 28.7;
		외화평가금액, FcurrEvalAmt, FcurrEvalAmt, double, 21.4;
		외화평가손익금액, FcurrEvalPnlAmt, FcurrEvalPnlAmt, double, 21.4;
		손익율, PnlRat, PnlRat, double, 18.6;
		기준환율, BaseXchrat, BaseXchrat, double, 15.4;
		매입금액, PchsAmt, PchsAmt, long, 16;
		예수금환산평가금액, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		주식환산평가금액, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		환산평가손익금액, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		해외증권결제수량, AstkSettQty, AstkSettQty, double, 28.6;
		시장구분명, MktTpNm, MktTpNm, char, 20;
		외화시장코드, FcurrMktCode, FcurrMktCode, char, 2;
		대출일자, LoanDt, LoanDt, char, 8;
		대출상세분류코드, LoanDtlClssCode, LoanDtlClssCode, char, 2;
		대출금액, LoanAmt, LoanAmt, long, 16;
		만기일자, DueDt, DueDt, char, 8;
		해외증권기준가격, AstkBasePrc, AstkBasePrc, double, 28.6;
	end
    END_DATA_MAP
END_FUNCTION_MAP
