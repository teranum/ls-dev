BEGIN_FUNCTION_MAP
    .Func,�ؿ��ֽ� �����ܰ��� API,COSOQ00201,SERVICE=COSOQ00201,ENCRYPT,headtype=B,CREATOR=������,CREDATE=2024-06-26 16:43:03;
    BEGIN_DATA_MAP    
    	COSOQ00201InBlock1,In(*EMPTY*),input;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��������, BaseDt, BaseDt, char, 8;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		�ؿ������ܰ����ڵ�, AstkBalTpCode, AstkBalTpCode, char, 2;
	end
    	COSOQ00201OutBlock1,In(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		���¹�ȣ, AcntNo, AcntNo, char, 20;
		��й�ȣ, Pwd, Pwd, char, 8;
		��������, BaseDt, BaseDt, char, 8;
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		�ؿ������ܰ����ڵ�, AstkBalTpCode, AstkBalTpCode, char, 2;
	end
	COSOQ00201OutBlock2,Out1(*EMPTY*),output;
	begin
		���ڵ尹��, RecCnt, RecCnt, long, 5
		������, ErnRat, ErnRat, double, 18.6;
		������ȯ���򰡱ݾ�, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		�ֽ�ȯ���򰡱ݾ�, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		��Ź�ڻ�ȯ���򰡱ݾ�, DpsastConvEvalAmt, DpsastConvEvalAmt, long, 16;
		��ȭ���հ�ݾ�, WonEvalSumAmt, WonEvalSumAmt, long, 16;
		ȯ���򰡼��ͱݾ�, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		��ȭ�������ܰ�ݾ�, WonDpsBalAmt, WonDpsBalAmt, long, 16;
		D2����������, D2EstiDps, D2EstiDps, long, 16;
		����ݾ�, LoanAmt, LoanAmt, long, 16;
	end
	COSOQ00201OutBlock3,Out2(*EMPTY*),output,occurs;
	begin
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		��ȭ������, FcurrDps, FcurrDps, double, 21.4;
		��ȭ�򰡱ݾ�, FcurrEvalAmt, FcurrEvalAmt, double, 21.4;
		��ȭ�򰡼��ͱݾ�, FcurrEvalPnlAmt, FcurrEvalPnlAmt, double, 21.4;
		������, PnlRat, PnlRat, double, 18.6;
		����ȯ��, BaseXchrat, BaseXchrat, double, 15.4;
		������ȯ���򰡱ݾ�, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		���Աݾ�, PchsAmt, PchsAmt, long, 16;
		�ֽ�ȯ���򰡱ݾ�, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		ȯ���򰡼��ͱݾ�, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		��ȭ�ż��ݾ�, FcurrBuyAmt, FcurrBuyAmt, double, 21.4;
		��ȭ�ֹ����ɱݾ�, FcurrOrdAbleAmt, FcurrOrdAbleAmt, double, 19.2;
		����ݾ�, LoanAmt, LoanAmt, long, 16;
	end
	COSOQ00201OutBlock4,Out3(*EMPTY*),output,occurs;
	begin
		��ȭ�ڵ�, CrcyCode, CrcyCode, char, 3;
		���������ȣ, ShtnIsuNo, ShtnIsuNo, char, 9;
		�����ȣ, IsuNo, IsuNo, char, 12;
		�Ϻ������ѱ������, JpnMktHanglIsuNm, JpnMktHanglIsuNm, char, 100;
		�ؿ������ܰ����ڵ�, AstkBalTpCode, AstkBalTpCode, char, 2;
		�ؿ������ܰ����ڵ��, AstkBalTpCodeNm, AstkBalTpCodeNm, char, 40;
		�ؿ������ܰ����, AstkBalQty, AstkBalQty, double, 28.6;
		�ؿ����Ǹŵ����ɼ���, AstkSellAbleQty, AstkSellAbleQty, double, 28.6;
		��ȭ���Ǵܰ�, FcstckUprc, FcstckUprc, double, 24.4;
		��ȭ�ż��ݾ�, FcurrBuyAmt, FcurrBuyAmt, double, 21.4;
		��ȭ���ǽ��������ڵ�, FcstckMktIsuCode, FcstckMktIsuCode, char, 18;
		�ؿ����ǽü�, OvrsScrtsCurpri, OvrsScrtsCurpri, double, 28.7;
		��ȭ�򰡱ݾ�, FcurrEvalAmt, FcurrEvalAmt, double, 21.4;
		��ȭ�򰡼��ͱݾ�, FcurrEvalPnlAmt, FcurrEvalPnlAmt, double, 21.4;
		������, PnlRat, PnlRat, double, 18.6;
		����ȯ��, BaseXchrat, BaseXchrat, double, 15.4;
		���Աݾ�, PchsAmt, PchsAmt, long, 16;
		������ȯ���򰡱ݾ�, DpsConvEvalAmt, DpsConvEvalAmt, long, 16;
		�ֽ�ȯ���򰡱ݾ�, StkConvEvalAmt, StkConvEvalAmt, long, 16;
		ȯ���򰡼��ͱݾ�, ConvEvalPnlAmt, ConvEvalPnlAmt, long, 16;
		�ؿ����ǰ�������, AstkSettQty, AstkSettQty, double, 28.6;
		���屸�и�, MktTpNm, MktTpNm, char, 20;
		��ȭ�����ڵ�, FcurrMktCode, FcurrMktCode, char, 2;
		��������, LoanDt, LoanDt, char, 8;
		����󼼺з��ڵ�, LoanDtlClssCode, LoanDtlClssCode, char, 2;
		����ݾ�, LoanAmt, LoanAmt, long, 16;
		��������, DueDt, DueDt, char, 8;
		�ؿ����Ǳ��ذ���, AstkBasePrc, AstkBasePrc, double, 28.6;
	end
    END_DATA_MAP
END_FUNCTION_MAP
