BEGIN_FUNCTION_MAP
    .Func,�ؿ����� �ŵ���ȯ�ֹ�(�̱�),COSMT00300,SERVICE=COSMT00300,headtype=B,CREATOR=������,CREDATE=2023-05-12 09:15:26;
    BEGIN_DATA_MAP    
    	COSMT00300InBlock1,In(*EMPTY*),input;
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
		�ſ�ŷ��ڵ�, MgntrnCode, MgntrnCode, char, 3;
		��������, LoanDt, LoanDt, char, 8;
		����󼼺з��ڵ�, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
    	COSMT00300OutBlock1,In(*EMPTY*),output;
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
		�ſ�ŷ��ڵ�, MgntrnCode, MgntrnCode, char, 3;
		��������, LoanDt, LoanDt, char, 8;
		����󼼺з��ڵ�, LoanDtlClssCode, LoanDtlClssCode, char, 2;
	end
	COSMT00300OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		�ֹ���ȣ, OrdNo, OrdNo, long, 10;
		���¸�, AcntNm, AcntNm, char, 40;
		�����, IsuNm, IsuNm, char, 40;
	end
    END_DATA_MAP
END_FUNCTION_MAP
