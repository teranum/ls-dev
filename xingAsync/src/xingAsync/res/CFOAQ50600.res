BEGIN_FUNCTION_MAP
	.Func,�����ɼ� �����ܰ� �� ����Ȳ3,CFOAQ50600,SERVICE=CFOAQ50600,ENCRYPT,headtype=B,CREATOR=������,CREDATE=2022/02/16 14:37:34;
	BEGIN_DATA_MAP
	CFOAQ50600InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		�Էº�й�ȣ, InptPwd, InptPwd, char, 8;
		�ֹ���, OrdDt, OrdDt, char, 8;
		�ܰ��򰡱���, BalEvalTp, BalEvalTp, char, 1;
		���������򰡱���, FutsPrcEvalTp, FutsPrcEvalTp, char, 1;
		û�������ȸ����, LqdtQtyQryTp, LqdtQtyQryTp, char, 1;
	end
	CFOAQ50600OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		�Էº�й�ȣ, InptPwd, InptPwd, char, 8;
		�ֹ���, OrdDt, OrdDt, char, 8;
		�ܰ��򰡱���, BalEvalTp, BalEvalTp, char, 1;
		���������򰡱���, FutsPrcEvalTp, FutsPrcEvalTp, char, 1;
		û�������ȸ����, LqdtQtyQryTp, LqdtQtyQryTp, char, 1;
	end
	CFOAQ50600OutBlock2,Out(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¸�, AcntNm, AcntNm, char, 40;
		�򰡿�Ź���Ѿ�, EvalDpsamtTotamt, EvalDpsamtTotamt, long, 15;
		�����򰡿�Ź�ݾ�, MnyEvalDpstgAmt, MnyEvalDpstgAmt, long, 15;
		��Ź���Ѿ�, DpsamtTotamt, DpsamtTotamt, long, 16;
		��Ź����, DpstgMny, DpstgMny, long, 16;
		��Ź���, DpstgSubst, DpstgSubst, long, 16;
		��ȭ���ݾ�, FcurrSubstAmt, FcurrSubstAmt, long, 16;
		���Ⱑ���ѱݾ�, PsnOutAbleTotAmt, PsnOutAbleTotAmt, long, 15;
		���Ⱑ�����ݾ�, PsnOutAbleCurAmt, PsnOutAbleCurAmt, long, 16;
		���Ⱑ�ɴ��ݾ�, PsnOutAbleSubstAmt, PsnOutAbleSubstAmt, long, 16;
		�ֹ������ѱݾ�, OrdAbleTotAmt, OrdAbleTotAmt, long, 15;
		�����ֹ����ɱݾ�, MnyOrdAbleAmt, MnyOrdAbleAmt, long, 16;
		��Ź���ű��Ѿ�, CsgnMgnTotamt, CsgnMgnTotamt, long, 16;
		������Ź���űݾ�, MnyCsgnMgn, MnyCsgnMgn, long, 16;
		�������ű��Ѿ�, MtmgnTotamt, MtmgnTotamt, long, 15;
		�����������űݾ�, MnyMaintMgn, MnyMaintMgn, long, 16;
		�߰����ű��Ѿ�, AddMgnTotamt, AddMgnTotamt, long, 15;
		�����߰����űݾ�, MnyAddMgn, MnyAddMgn, long, 16;
		������, CmsnAmt, CmsnAmt, long, 16;
		�̼��ݾ�, RcvblAmt, RcvblAmt, long, 16;
		�̼���ü��, RcvblOdpnt, RcvblOdpnt, long, 16;
		�����򰡼��ͱݾ�, FutsEvalPnlAmt, FutsEvalPnlAmt, long, 16;
		�ɼ��򰡼��ͱݾ�, OptEvalPnlAmt, OptEvalPnlAmt, long, 16;
		�ɼ��򰡱ݾ�, OptEvalAmt, OptEvalAmt, long, 16;
		�ɼǸŸż��ͱݾ�, OptBnsplAmt, OptBnsplAmt, long, 16;
		������������, FutsAdjstDfamt, FutsAdjstDfamt, long, 16;
		�ɼǸŸűݾ�, OptBnsAmt, OptBnsAmt, long, 16;
		�Ѽ��ͱݾ�, TotPnlAmt, TotPnlAmt, long, 16;
		�����ͱݾ�, NetPnlAmt, NetPnlAmt, long, 16;
		�����򰡱ݾ�, BaseEvalAmt, BaseEvalAmt, long, 16;
		�����򰡺���, AcntEvalRat, AcntEvalRat, double, 7.2;
		�򰡺���, EvalRat, EvalRat, double, 7.2;
	end
	CFOAQ50600OutBlock3,Out2(*EMPTY*),output,occurs;
	begin
		�����ɼ������ȣ, FnoIsuNo, FnoIsuNo, char, 12;
		�����, IsuNm, IsuNm, char, 40;
		�Ÿű���, BnsTpCode, BnsTpCode, char, 1;
		�Ÿű���, BnsTpNm, BnsTpNm, char, 10;
		�̰�������, UnsttQty, UnsttQty, long, 16;
		��հ�, FnoAvrPrc, FnoAvrPrc, double, 19.8;
		�����ɼ����簡, FnoNowPrc, FnoNowPrc, double, 27.8;
		�����ɼǴ��, FnoCmpPrc, FnoCmpPrc, double, 27.8;
		�򰡼���, EvalPnl, EvalPnl, long, 16;
		������, PnlRat, PnlRat, double, 18.6;
		�򰡱ݾ�, EvalAmt, EvalAmt, long, 16;
		�򰡺���, EvalRat, EvalRat, double, 7.2;
		û�갡�ɼ���, LqdtAbleQty, LqdtAbleQty, long, 16;
		�Ÿż��ͱݾ�, BnsplAmt, BnsplAmt, long, 16;
	end
	END_DATA_MAP
END_FUNCTION_MAP
