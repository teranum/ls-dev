BEGIN_FUNCTION_MAP
    .Func,�̱������ֹ� API,COSAT00301,SERVICE=COSAT00301,headtype=B,CREATOR=������,CREDATE=2024-05-21 16:52:15;
    BEGIN_DATA_MAP    
    	COSAT00301InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		�ֹ������ڵ�, OrdPtnCode, OrdPtnCode, char, 2;
		���ֹ���ȣ, OrgOrdNo, OrgOrdNo, long, 10;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		�Էº�й�ȣ, InptPwd, InptPwd, char, 8;
		�ֹ������ڵ�, OrdMktCode, OrdMktCode, char, 2;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		ȣ�������ڵ�, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		�߰��α����ڵ�, BrkTpCode, BrkTpCode, char, 2;
	end
    	COSAT00301OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		�ֹ������ڵ�, OrdPtnCode, OrdPtnCode, char, 2;
		���ֹ���ȣ, OrgOrdNo, OrgOrdNo, long, 10;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		�Էº�й�ȣ, InptPwd, InptPwd, char, 8;
		�ֹ������ڵ�, OrdMktCode, OrdMktCode, char, 2;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		ȣ�������ڵ�, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		�����Ÿ�ü�ڵ�, RegCommdaCode, RegCommdaCode, char, 2;
		�߰��α����ڵ�, BrkTpCode, BrkTpCode, char, 2;
	end
	COSAT00301OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		�ֹ���ȣ, OrdNo, OrdNo, long, 10;
		���¸�, AcntNm, AcntNm, char, 40;
		�����, IsuNm, IsuNm, char, 40;
	end
    END_DATA_MAP
END_FUNCTION_MAP
