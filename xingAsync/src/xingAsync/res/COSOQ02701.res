BEGIN_FUNCTION_MAP
    .Func,�ؿ��ֽ� ������ ��ȸ API,COSOQ02701,SERVICE=COSOQ02701,headtype=B,CREATOR=������,CREDATE=2024-06-04 09:46:07;
    BEGIN_DATA_MAP    
    	COSOQ02701InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
	end
    	COSOQ02701OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
	end
	COSOQ02701OutBlock2,Out1(*EMPTY*),output,occurs;
	begin
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		��ȭ�ż������1, FcurrBuyAdjstAmt1, FcurrBuyAdjstAmt1, double, 17.4;
		��ȭ�ż������2, FcurrBuyAdjstAmt2, FcurrBuyAdjstAmt2, double, 17.4;
		��ȭ�ż������3, FcurrBuyAdjstAmt3, FcurrBuyAdjstAmt3, double, 17.4;
		��ȭ�ż������4, FcurrBuyAdjstAmt4, FcurrBuyAdjstAmt4, double, 17.4;
		��ȭ�ŵ������1, FcurrSellAdjstAmt1, FcurrSellAdjstAmt1, double, 17.4;
		��ȭ�ŵ������2, FcurrSellAdjstAmt2, FcurrSellAdjstAmt2, double, 17.4;
		��ȭ�ŵ������3, FcurrSellAdjstAmt3, FcurrSellAdjstAmt3, double, 17.4;
		��ȭ�ŵ������4, FcurrSellAdjstAmt4, FcurrSellAdjstAmt4, double, 17.4;
		������ȭ������1, PrsmptFcurrDps1, PrsmptFcurrDps1, double, 17.4;
		������ȭ������2, PrsmptFcurrDps2, PrsmptFcurrDps2, double, 17.4;
		������ȭ������3, PrsmptFcurrDps3, PrsmptFcurrDps3, double, 17.4;
		������ȭ������4, PrsmptFcurrDps4, PrsmptFcurrDps4, double, 17.4;
		����ȯ�����ɱ�1, PrsmptMxchgAbleAmt1, PrsmptMxchgAbleAmt1, double, 17.4;
		����ȯ�����ɱ�2, PrsmptMxchgAbleAmt2, PrsmptMxchgAbleAmt2, double, 17.4;
		����ȯ�����ɱ�3, PrsmptMxchgAbleAmt3, PrsmptMxchgAbleAmt3, double, 17.4;
		����ȯ�����ɱ�4, PrsmptMxchgAbleAmt4, PrsmptMxchgAbleAmt4, double, 17.4;
	end
	COSOQ02701OutBlock3,Out2(*EMPTY*),output,occurs;
	begin
		������, CntryNm, CntryNm, char, 40;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		T4��ȭ������, T4FcurrDps, T4FcurrDps, double, 21.4;
		��ȭ������, FcurrDps, FcurrDps, double, 17.4;
		��ȭ�ֹ����ɱݾ�, FcurrOrdAbleAmt, FcurrOrdAbleAmt, double, 17.4;
		��ȯ���ֹ����ɱݾ�, PrexchOrdAbleAmt, PrexchOrdAbleAmt, double, 21.4;
		��ȭ�ֹ��ݾ�, FcurrOrdAmt, FcurrOrdAmt, double, 24.4;
		��ȭ�㺸�ݾ�, FcurrPldgAmt, FcurrPldgAmt, double, 17.4;
		ü�������ȭ�ݾ�, ExecRuseFcurrAmt, ExecRuseFcurrAmt, double, 17.4;
		��ȭȯ�����ɱ�, FcurrMxchgAbleAmt, FcurrMxchgAbleAmt, double, 17.4;
		����ȯ��, BaseXchrat, BaseXchrat, double, 15.4;
	end
	COSOQ02701OutBlock4,Out3(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		��ȭ�������ܰ�ݾ�, WonDpsBalAmt, WonDpsBalAmt, long, 16;
		��ݰ��ɱݾ�, MnyoutAbleAmt, MnyoutAbleAmt, long, 16;
		��ȭ��ȯ�����ɱݾ�, WonPrexchAbleAmt, WonPrexchAbleAmt, long, 16;
		�ؿ����ű�, OvrsMgn, OvrsMgn, long, 17;
	end
	COSOQ02701OutBlock5,Out4(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���ܱ����ڵ�, NrfCode, NrfCode, char, 2;
	end
    END_DATA_MAP
END_FUNCTION_MAP
