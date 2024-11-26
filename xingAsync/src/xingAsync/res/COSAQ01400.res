BEGIN_FUNCTION_MAP
    .Func,예약주문 처리결과 조회,COSAQ01400,SERVICE=COSAQ01400,ENCRYPT,headtype=B,CREATOR=이유리,CREDATE=2023-05-24 17:15:16;
    BEGIN_DATA_MAP    
    	COSAQ01400InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		조회구분코드, QryTpCode, QryTpCode, char, 1;
		국가코드, CntryCode, CntryCode, char, 3;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		시작일자, SrtDt, SrtDt, char, 8;
		종료일자, EndDt, EndDt, char, 8;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		예약주문조건코드, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		예약주문상태코드, RsvOrdStatCode, RsvOrdStatCode, char, 1;
	end
    	COSAQ01400OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		조회구분코드, QryTpCode, QryTpCode, char, 1;
		국가코드, CntryCode, CntryCode, char, 3;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		시작일자, SrtDt, SrtDt, char, 8;
		종료일자, EndDt, EndDt, char, 8;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		예약주문조건코드, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		예약주문상태코드, RsvOrdStatCode, RsvOrdStatCode, char, 1;
	end
	COSAQ01400OutBlock2,Out(*EMPTY*),output,occurs;
	begin
		계좌번호, AcntNo, AcntNo, char, 20;
		계좌명, AcntNm, AcntNm, char, 40;
		주문일자, OrdDt, OrdDt, char, 8;
		주문번호, OrdNo, OrdNo, long, 10;
		예약주문입력일자, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		예약주문번호, RsvOrdNo, RsvOrdNo, long, 10;
		단축종목번호, ShtnIsuNo, ShtnIsuNo, char, 9;
		일본시장한글종목명, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		매매구분명, BnsTpNm, BnsTpNm, char, 10;
		체결수량, ExecQty, ExecQty, long, 16;
		미체결수량, UnercQty, UnercQty, long, 16;
		총체결수량, TotExecQty, TotExecQty, long, 16;
		통화코드, CrcyCode, CrcyCode, char, 3;
		예약주문상태코드, RsvOrdStatCode, RsvOrdStatCode, char, 1;
		시장구분명, MktTpNm, MktTpNm, char, 20;
		오류내용, ErrCnts, ErrCnts, char, 100;
		호가유형명, OrdprcPtnNm, OrdprcPtnNm, char, 40;
		대출일자, LoanDt, LoanDt, char, 8;
		신용거래코드, MgntrnCode, MgntrnCode, char, 3;
	end
    END_DATA_MAP
END_FUNCTION_MAP
