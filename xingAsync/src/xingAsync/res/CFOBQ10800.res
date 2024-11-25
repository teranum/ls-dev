BEGIN_FUNCTION_MAP
    .Func,선물옵션 옵션매도시 주문증거금조회,CFOBQ10800,SERVICE=CFOBQ10800,headtype=B,CREATOR=원종혁,CREDATE=2023-05-16 08:36:13;
    BEGIN_DATA_MAP    
    	CFOBQ10800InBlock1,In(*EMPTY*),input;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		종목중분류코드, IsuMdclssCode, IsuMdclssCode, char, 2;
		종목소분류코드, IsuSmclssCode, IsuSmclssCode, char, 3;
		만기년월, DueYymm, DueYymm, char, 6;
		결제주간수, SettWklyCnt, SettWklyCnt, char, 2;
		특별일자유형코드, SpclDtPtnCode, SpclDtPtnCode, char, 3;
	end
    	CFOBQ10800OutBlock1,In(*EMPTY*),output;
	begin
		레코드갯수, RecCnt, RecCnt, long, 5
		종목중분류코드, IsuMdclssCode, IsuMdclssCode, char, 2;
		종목소분류코드, IsuSmclssCode, IsuSmclssCode, char, 3;
		만기년월, DueYymm, DueYymm, char, 6;
		결제주간수, SettWklyCnt, SettWklyCnt, char, 2;
		특별일자유형코드, SpclDtPtnCode, SpclDtPtnCode, char, 3;
	end
	CFOBQ10800OutBlock2,Out(*EMPTY*),output,occurs;
	begin
		행사가, ElwXrcPrc, ElwXrcPrc, double, 13.2;
		선물옵션종목번호, FnoIsuNo, FnoIsuNo, char, 12;
		한글종목명1, HanglIsuNm1, HanglIsuNm1, char, 40;
		구분명1, TpNm1, TpNm1, char, 40;
		상승옵션조정이론가, UpOptRegulThrprc, UpOptRegulThrprc, double, 27.8;
		이론가1, Thrprc1, Thrprc1, double, 19.8;
		기준가1, BasePrc1, BasePrc1, double, 13.2;
		주문증거금액1, OrdMgn1, OrdMgn1, long, 16;
		선물옵션종목번호0, FnoIsuNo0, FnoIsuNo0, char, 12;
		한글종목명2, HanglIsuNm2, HanglIsuNm2, char, 40;
		구분명2, TpNm2, TpNm2, char, 40;
		하락옵션조정이론가, DownOptRegulThrprc, DownOptRegulThrprc, double, 27.8;
		이론가2, Thrprc2, Thrprc2, double, 19.8;
		기준가2, BasePrc2, BasePrc2, double, 13.2;
		주문증거금액2, OrdMgn2, OrdMgn2, long, 16;
	end
    END_DATA_MAP
END_FUNCTION_MAP
