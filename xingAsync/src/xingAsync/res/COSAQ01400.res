BEGIN_FUNCTION_MAP
    .Func,�����ֹ� ó����� ��ȸ,COSAQ01400,SERVICE=COSAQ01400,ENCRYPT,headtype=B,CREATOR=������,CREDATE=2023-05-24 17:15:16;
    BEGIN_DATA_MAP    
    	COSAQ01400InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		��ȸ�����ڵ�, QryTpCode, QryTpCode, char, 1;
		�����ڵ�, CntryCode, CntryCode, char, 3;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��������, SrtDt, SrtDt, char, 8;
		��������, EndDt, EndDt, char, 8;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		�����ֹ������ڵ�, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		�����ֹ������ڵ�, RsvOrdStatCode, RsvOrdStatCode, char, 1;
	end
    	COSAQ01400OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		��ȸ�����ڵ�, QryTpCode, QryTpCode, char, 1;
		�����ڵ�, CntryCode, CntryCode, char, 3;
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��������, SrtDt, SrtDt, char, 8;
		��������, EndDt, EndDt, char, 8;
		�Ÿű����ڵ�, BnsTpCode, BnsTpCode, char, 1;
		�����ֹ������ڵ�, RsvOrdCndiCode, RsvOrdCndiCode, char, 2;
		�����ֹ������ڵ�, RsvOrdStatCode, RsvOrdStatCode, char, 1;
	end
	COSAQ01400OutBlock2,Out(*EMPTY*),output,occurs;
	begin
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		���¸�, AcntNm, AcntNm, char, 40;
		�ֹ�����, OrdDt, OrdDt, char, 8;
		�ֹ���ȣ, OrdNo, OrdNo, long, 10;
		�����ֹ��Է�����, RsvOrdInptDt, RsvOrdInptDt, char, 8;
		�����ֹ���ȣ, RsvOrdNo, RsvOrdNo, long, 10;
		���������ȣ, ShtnIsuNo, ShtnIsuNo, char, 9;
		�Ϻ������ѱ������, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		�ֹ�����, OrdQty, OrdQty, long, 16;
		�ؿ��ֹ���, OvrsOrdPrc, OvrsOrdPrc, double, 28.7;
		�Ÿű��и�, BnsTpNm, BnsTpNm, char, 10;
		ü�����, ExecQty, ExecQty, long, 16;
		��ü�����, UnercQty, UnercQty, long, 16;
		��ü�����, TotExecQty, TotExecQty, long, 16;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		�����ֹ������ڵ�, RsvOrdStatCode, RsvOrdStatCode, char, 1;
		���屸�и�, MktTpNm, MktTpNm, char, 20;
		��������, ErrCnts, ErrCnts, char, 100;
		ȣ��������, OrdprcPtnNm, OrdprcPtnNm, char, 40;
		��������, LoanDt, LoanDt, char, 8;
		�ſ�ŷ��ڵ�, MgntrnCode, MgntrnCode, char, 3;
	end
    END_DATA_MAP
END_FUNCTION_MAP
