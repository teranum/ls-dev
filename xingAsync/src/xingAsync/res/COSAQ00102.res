BEGIN_FUNCTION_MAP
    .Func,�ؿ��ֽ�  API �ֹ�ü����ȸ,COSAQ00102,SERVICE=COSAQ00102,headtype=B,CREATOR=������,CREDATE=2024-06-24 15:02:15;
    BEGIN_DATA_MAP    
    	COSAQ00102InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		��ȸ�����ڵ�, QryTpCode, QryTpCode, char, 1;
		���������ڵ�, BkseqTpCode, BkseqTpCode, char, 1;
		�ֹ������ڵ�, OrdMktCode, OrdMktCode, char, 2;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�����ֹ���ȣ, SrtOrdNo, SrtOrdNo, long, 10;
		�ֹ�����, OrdDt, OrdDt, char, 8;
		ü�Ῡ��, ExecYn, ExecYn, char, 1;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		���ϸŸ����뿩��, ThdayBnsAppYn, ThdayBnsAppYn, char, 1;
		�����ܰ�������, LoanBalHldYn, LoanBalHldYn, char, 1;
	end
    	COSAQ00102OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		��ȸ�����ڵ�, QryTpCode, QryTpCode, char, 1;
		���������ڵ�, BkseqTpCode, BkseqTpCode, char, 1;
		�ֹ������ڵ�, OrdMktCode, OrdMktCode, char, 2;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�����ֹ���ȣ, SrtOrdNo, SrtOrdNo, long, 10;
		�ֹ�����, OrdDt, OrdDt, char, 8;
		ü�Ῡ��, ExecYn, ExecYn, char, 1;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		���ϸŸ����뿩��, ThdayBnsAppYn, ThdayBnsAppYn, char, 1;
		�����ܰ�������, LoanBalHldYn, LoanBalHldYn, char, 1;
	end
	COSAQ00102OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¸�, AcntNm, AcntNm, char, 40;
		�Ϻ������ѱ������, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		����������, MgmtBrnNm, MgmtBrnNm, char, 40;
		�ŵ�ü���ȭ�ݾ�, SellExecFcurrAmt, SellExecFcurrAmt, double, 21.4;
		�ŵ�ü�����, SellExecQty, SellExecQty, long, 16;
		�ż�ü���ȭ�ݾ�, BuyExecFcurrAmt, BuyExecFcurrAmt, double, 21.4;
		�ż�ü�����, BuyExecQty, BuyExecQty, long, 16;
	end
	COSAQ00102OutBlock3,ST_COSAQ00102_OUT(*EMPTY*),output,occurs;
	begin
		����������ȣ, MgmtBrnNo, MgmtBrnNo, char, 3;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		���¸�, AcntNm, AcntNm, char, 40;
		ü��ð�, ExecTime, ExecTime, char, 9;
		�ֹ��ð�, OrdTime, OrdTime, char, 9;
		�ֹ���ȣ, OrdNo, OrdNo, long, 10;
		���ֹ���ȣ, OrgOrdNo, OrgOrdNo, long, 10;
		���������ȣ, ShtnIsuNo, ShtnIsuNo, char, 9;
		�ֹ�ó��������, OrdTrxPtnNm, OrdTrxPtnNm, char, 50;
		�ֹ�ó�������ڵ�, OrdTrxPtnCode, OrdTrxPtnCode, long, 9;
		������Ұ��ɼ���, MrcAbleQty, MrcAbleQty, long, 16;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 22.7;
		ü�����, ExecQty, ExecQty, long, 16;
		�ؿ�ü�ᰡ, OvrsExecPrc, OvrsExecPrc, double, 28.7;
		ȣ�������ڵ�, OrdprcPtnCode, OrdprcPtnCode, char, 2;
		ȣ��������, OrdprcPtnNm, OrdprcPtnNm, char, 40;
		�ֹ�������, OrdPtnNm, OrdPtnNm, char, 40;
		�ֹ������ڵ�, OrdPtnCode, OrdPtnCode, char, 2;
		������ұ����ڵ�, MrcTpCode, MrcTpCode, char, 1;
		������ұ��и�, MrcTpNm, MrcTpNm, char, 10;
		��üü�����, AllExecQty, AllExecQty, long, 16;
		��Ÿ�ü�ڵ�, CommdaCode, CommdaCode, char, 2;
		�ֹ������ڵ�, OrdMktCode, OrdMktCode, char, 2;
		�����, MktNm, MktNm, char, 40;
		��Ÿ�ü��, CommdaNm, CommdaNm, char, 40;
		�Ϻ������ѱ������, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		��ü�����, UnercQty, UnercQty, long, 16;
		Ȯ�μ���, CnfQty, CnfQty, long, 16;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		��Ͻ����ڵ�, RegMktCode, RegMktCode, char, 2;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�߰��α����ڵ�, BrkTpCode, BrkTpCode, char, 2;
		����߰��θ�, OppBrkNm, OppBrkNm, char, 40;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		��������, LoanDt, LoanDt, char, 8;
		����ݾ�, LoanAmt, LoanAmt, long, 16;
	end
    END_DATA_MAP
END_FUNCTION_MAP
