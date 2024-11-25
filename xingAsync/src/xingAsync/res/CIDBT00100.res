BEGIN_FUNCTION_MAP
	.Func,해외선물신규주문,CIDBT00100,SERVICE=CIDBT00100,ENCRYPT,SIGNATURE,headtype=B,CREATOR=이호섭,CREDATE=2022/04/28 13:26:59;
	BEGIN_DATA_MAP
	CIDBT00100InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문일자, OrdDt, OrdDt, char, 8;
		지점코드, BrnCode, BrnCode, char, 7;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		종목코드값, IsuCodeVal, IsuCodeVal, char, 30;
		선물주문구분코드, FutsOrdTpCode, FutsOrdTpCode, char, 1;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		해외선물주문유형코드, AbrdFutsOrdPtnCode, AbrdFutsOrdPtnCode, char, 1;
		통화코드, CrcyCode, CrcyCode, char, 3;
		해외파생주문가격, OvrsDrvtOrdPrc, OvrsDrvtOrdPrc, double, 30.11;
		조건주문가격, CndiOrdPrc, CndiOrdPrc, double, 30.11;
		주문수량, OrdQty, OrdQty, long, 16;
		상품코드, PrdtCode, PrdtCode, char, 6;
		만기년월, DueYymm, DueYymm, char, 6;
		거래소코드, ExchCode, ExchCode, char, 10;
	end
	CIDBT00100OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문일자, OrdDt, OrdDt, char, 8;
		지점코드, BrnCode, BrnCode, char, 7;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		종목코드값, IsuCodeVal, IsuCodeVal, char, 30;
		선물주문구분코드, FutsOrdTpCode, FutsOrdTpCode, char, 1;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		해외선물주문유형코드, AbrdFutsOrdPtnCode, AbrdFutsOrdPtnCode, char, 1;
		통화코드, CrcyCode, CrcyCode, char, 3;
		해외파생주문가격, OvrsDrvtOrdPrc, OvrsDrvtOrdPrc, double, 30.11;
		조건주문가격, CndiOrdPrc, CndiOrdPrc, double, 30.11;
		주문수량, OrdQty, OrdQty, long, 16;
		상품코드, PrdtCode, PrdtCode, char, 6;
		만기년월, DueYymm, DueYymm, char, 6;
		거래소코드, ExchCode, ExchCode, char, 10;
	end
	CIDBT00100OutBlock2,Out(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		계좌번호, AcntNo, AcntNo, char, 20;
		해외선물주문번호, OvrsFutsOrdNo, OvrsFutsOrdNo, char, 10;
	end
	END_DATA_MAP
END_FUNCTION_MAP
