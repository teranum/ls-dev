BEGIN_FUNCTION_MAP
	.Func,�����ɼ� �ֹ����ɼ�����ȸ,CFOAQ10100,SERVICE=CFOAQ10100,headtype=B,CREATOR=������,CREDATE=2022/02/16 14:27:58;
	BEGIN_DATA_MAP
	CFOAQ10100InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȸ����, QryTp, QryTp, char, 1;
		�ֹ��ݾ�, OrdAmt, OrdAmt, long, 16;
		������, RatVal, RatVal, double, 19.8;
		�����ɼ������ȣ, FnoIsuNo, FnoIsuNo, char, 12;
		�Ÿű���, BnsTpCode, BnsTpCode, char, 1;
		�����ɼ��ֹ�����, FnoOrdPrc, FnoOrdPrc, double, 27.8;
		�����ɼ�ȣ�������ڵ�, FnoOrdprcPtnCode, FnoOrdprcPtnCode, char, 2;
	end
	CFOAQ10100OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��ȸ����, QryTp, QryTp, char, 1;
		�ֹ��ݾ�, OrdAmt, OrdAmt, long, 16;
		������, RatVal, RatVal, double, 19.8;
		�����ɼ������ȣ, FnoIsuNo, FnoIsuNo, char, 12;
		�Ÿű���, BnsTpCode, BnsTpCode, char, 1;
		�����ɼ��ֹ�����, FnoOrdPrc, FnoOrdPrc, double, 27.8;
		�����ɼ�ȣ�������ڵ�, FnoOrdprcPtnCode, FnoOrdprcPtnCode, char, 2;
	end
	CFOAQ10100OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¸�, AcntNm, AcntNm, char, 40;
		��ȸ��, QryDt, QryDt, char, 8;
		�����ɼ����簡, FnoNowPrc, FnoNowPrc, double, 27.8;
		�ֹ����ɼ���, OrdAbleQty, OrdAbleQty, long, 16;
		�ű��ֹ����ɼ���, NewOrdAbleQty, NewOrdAbleQty, long, 16;
		û���ֹ����ɼ���, LqdtOrdAbleQty, LqdtOrdAbleQty, long, 16;
		��뿹�����űݾ�, UsePreargMgn, UsePreargMgn, long, 16;
		��뿹���������űݾ�, UsePreargMnyMgn, UsePreargMnyMgn, long, 16;
		�ֹ����ɱݾ�, OrdAbleAmt, OrdAbleAmt, long, 16;
		�����ֹ����ɱݾ�, MnyOrdAbleAmt, MnyOrdAbleAmt, long, 16;
	end
	END_DATA_MAP
END_FUNCTION_MAP
