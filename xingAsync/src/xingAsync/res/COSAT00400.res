BEGIN_FUNCTION_MAP
    .Func,�ؿ��ֽ� �����ֹ� ��� �� ���,COSAT00400,SERVICE=COSAT00400,SIGNATURE,headtype=B,CREATOR=������,CREDATE=2023-05-25 09:24:31;
    BEGIN_DATA_MAP    
    	COSAT00400InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		ó�������ڵ�, TrxTpCode, TrxTpCode, char, 1;
		�����ڵ�, CntryCode, CntryCode, char, 3;
		�����ֹ��Է�����, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		�����ֹ���ȣ, RsvOrdNo, RsvOrdNo, long, 10;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȭ�����ڵ�, FcurrMktCode, FcurrMktCode, char, 2;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		ȣ�������ڵ�, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		�����ֹ���������, RsvOrdSrtDt, RsvOrdSrtDt, char, 8;
		�����ֹ���������, RsvOrdEndDt, RsvOrdEndDt, char, 8;
		�����ֹ������ڵ�, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		�ſ�ŷ��ڵ�, MgntrnCode, MgntrnCode, char, 3;
		��������, LoanDt, LoanDt, char, 8;
		����󼼺з��ڵ�, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
    	COSAT00400OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		ó�������ڵ�, TrxTpCode, TrxTpCode, char, 1;
		�����ڵ�, CntryCode, CntryCode, char, 3;
		�����ֹ��Է�����, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		�����ֹ���ȣ, RsvOrdNo, RsvOrdNo, long, 10;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȭ�����ڵ�, FcurrMktCode, FcurrMktCode, char, 2;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		�����Ÿ�ü�ڵ�, RegCommdaCode, RegCommdaCode, char, 2;
		ȣ�������ڵ�, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		�����ֹ���������, RsvOrdSrtDt, RsvOrdSrtDt, char, 8;
		�����ֹ���������, RsvOrdEndDt, RsvOrdEndDt, char, 8;
		�����ֹ������ڵ�, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		�ſ�ŷ��ڵ�, MgntrnCode, MgntrnCode, char, 3;
		��������, LoanDt, LoanDt, char, 8;
		����󼼺з��ڵ�, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
	COSAT00400OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		�����ֹ���ȣ, RsvOrdNo, RsvOrdNo, long, 10;
	end
    END_DATA_MAP
END_FUNCTION_MAP
