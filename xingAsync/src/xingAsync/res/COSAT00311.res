BEGIN_FUNCTION_MAP
    .Func,미국시장 정정주문 API,COSAT00311,SERVICE=COSAT00311,headtype=B,CREATOR=이유리,CREDATE=2024-05-21 16:53:56;
    BEGIN_DATA_MAP    
    	COSAT00311InBlock1,In(*EMPTY*),input;
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
	end
    	COSAT00311OutBlock1,In(*EMPTY*),output;
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
	end
	COSAT00311OutBlock2,Out(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		주문번호, OrdNo, OrdNo, long, 10;
		계좌명, AcntNm, AcntNm, char, 40;
		종목명, IsuNm, IsuNm, char, 40;
	end
    END_DATA_MAP
END_FUNCTION_MAP
