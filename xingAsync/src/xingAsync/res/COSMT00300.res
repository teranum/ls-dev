BEGIN_FUNCTION_MAP
    .Func,해외증권 매도상환주문(미국),COSMT00300,SERVICE=COSMT00300,headtype=B,CREATOR=서충희,CREDATE=2023-05-12 09:15:26;
    BEGIN_DATA_MAP    
    	COSMT00300InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문유형코드, OrdPtnCode, OrdPtnCode, char, 2;
		원주문번호, OrgOrdNo, OrgOrdNo, long, 10;
		계좌번호, AcntNo, AcntNo, char, 20;
		입력비밀번호, InptPwd, InptPwd, char, 8;
		주문시장코드, OrdMktCode, OrdMktCode, char, 2;
		종목번호, IsuNo, IsuNo, char, 12;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		호가유형코드, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		중개인구분코드, BrkTpCode, BrkTpCode, char, 2;
		신용거래코드, MgntrnCode, MgntrnCode, char, 3;
		대출일자, LoanDt, LoanDt, char, 8;
		대출상세분류코드, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
    	COSMT00300OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문유형코드, OrdPtnCode, OrdPtnCode, char, 2;
		원주문번호, OrgOrdNo, OrgOrdNo, long, 10;
		계좌번호, AcntNo, AcntNo, char, 20;
		입력비밀번호, InptPwd, InptPwd, char, 8;
		주문시장코드, OrdMktCode, OrdMktCode, char, 2;
		종목번호, IsuNo, IsuNo, char, 12;
		주문수량, OrdQty, OrdQty, long, 16;
		해외주문가, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		호가유형코드, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		등록통신매체코드, RegCommdaCode, RegCommdaCode, char, 2;
		중개인구분코드, BrkTpCode, BrkTpCode, char, 2;
		신용거래코드, MgntrnCode, MgntrnCode, char, 3;
		대출일자, LoanDt, LoanDt, char, 8;
		대출상세분류코드, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
	COSMT00300OutBlock2,Out(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문번호, OrdNo, OrdNo, long, 10;
		계좌명, AcntNm, AcntNm, char, 40;
		종목명, IsuNm, IsuNm, char, 40;
	end
    END_DATA_MAP
END_FUNCTION_MAP
