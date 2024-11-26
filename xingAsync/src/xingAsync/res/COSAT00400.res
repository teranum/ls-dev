BEGIN_FUNCTION_MAP
    .Func,해외주식 예약주문 등록 및 취소,COSAT00400,SERVICE=COSAT00400,SIGNATURE,headtype=B,CREATOR=이유리,CREDATE=2023-05-25 09:24:31;
    BEGIN_DATA_MAP    
    	COSAT00400InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		처리구분코드, TrxTpCode, TrxTpCode, char, 1;
		국가코드, CntryCode, CntryCode, char, 3;
		예약주문입력일자, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		예약주문번호, RsvOrdNo, RsvOrdNo, long, 10;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		외화시장코드, FcurrMktCode, FcurrMktCode, char, 2;
		종목번호, IsuNo, IsuNo, char, 12;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		호가유형코드, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		예약주문시작일자, RsvOrdSrtDt, RsvOrdSrtDt, char, 8;
		예약주문종료일자, RsvOrdEndDt, RsvOrdEndDt, char, 8;
		예약주문조건코드, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		신용거래코드, MgntrnCode, MgntrnCode, char, 3;
		대출일자, LoanDt, LoanDt, char, 8;
		대출상세분류코드, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
    	COSAT00400OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		처리구분코드, TrxTpCode, TrxTpCode, char, 1;
		국가코드, CntryCode, CntryCode, char, 3;
		예약주문입력일자, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		예약주문번호, RsvOrdNo, RsvOrdNo, long, 10;
		매매구분코드, BnsTpCode, BnsTpCode, char, 1;
		계좌번호, AcntNo, AcntNo, char, 20;
		비밀번호, Pwd, Pwd, char, 8;
		외화시장코드, FcurrMktCode, FcurrMktCode, char, 2;
		종목번호, IsuNo, IsuNo, char, 12;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		등록통신매체코드, RegCommdaCode, RegCommdaCode, char, 2;
		호가유형코드, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		예약주문시작일자, RsvOrdSrtDt, RsvOrdSrtDt, char, 8;
		예약주문종료일자, RsvOrdEndDt, RsvOrdEndDt, char, 8;
		예약주문조건코드, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		신용거래코드, MgntrnCode, MgntrnCode, char, 3;
		대출일자, LoanDt, LoanDt, char, 8;
		대출상세분류코드, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
	COSAT00400OutBlock2,Out(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		예약주문번호, RsvOrdNo, RsvOrdNo, long, 10;
	end
    END_DATA_MAP
END_FUNCTION_MAP
