BEGIN_FUNCTION_MAP
	.Func,주식체결/미체결(t0425),t0425,attr,headtype=D;
	BEGIN_DATA_MAP
	t0425InBlock,기본입력,Input;
	begin
		계좌번호,	accno,	accno,	char,	11;
		비밀번호,	passwd,	passwd,	char,	8;
		종목번호,	expcode,	expcode,	char,	12;
		체결구분,	chegb,	chegb,	char,	1;
		매매구분,	medosu,	medosu,	char,	1;
		정렬순서,	sortgb,	sortgb,	char,	1;
		주문번호,	cts_ordno,	cts_ordno,	char,	10;
	end
	t0425OutBlock,출력,Output;
	begin
		총주문수량,	tqty,	tqty,	long,	18;
		총체결수량,	tcheqty,	tcheqty,	long,	18;
		총미체결수량,	tordrem,	tordrem,	long,	18;
		추정수수료,	cmss,	cmss,	long,	18;
		총주문금액,	tamt,	tamt,	long,	18;
		총매도체결금액,	tmdamt,	tmdamt,	long,	18;
		총매수체결금액,	tmsamt,	tmsamt,	long,	18;
		추정제세금,	tax,	tax,	long,	18;
		주문번호,	cts_ordno,	cts_ordno,	char,	10;
	end
	t0425OutBlock1,출력1,Output,occurs;
	begin
		주문번호,	ordno,	ordno,	long,	10;
		종목번호,	expcode,	expcode,	char,	12;
		구분,	medosu,	medosu,	char,	10;
		주문수량,	qty,	qty,	long,	9;
		주문가격,	price,	price,	long,	9;
		체결수량,	cheqty,	cheqty,	long,	9;
		체결가격,	cheprice,	cheprice,	long,	9;
		미체결잔량,	ordrem,	ordrem,	long,	9;
		확인수량,	cfmqty,	cfmqty,	long,	9;
		상태,	status,	status,	char,	20;
		원주문번호,	orgordno,	orgordno,	long,	10;
		유형,	ordgb,	ordgb,	char,	20;
		주문시간,	ordtime,	ordtime,	char,	8;
		주문매체,	ordermtd,	ordermtd,	char,	10;
		처리순번,	sysprocseq,	sysprocseq,	long,	10;
		호가유형,	hogagb,	hogagb,	char,	2;
		현재가,	price1,	price1,	long,	8;
		주문구분,	orggb,	orggb,	char,	2;
		신용구분,	singb,	singb,	char,	2;
		대출일자,	loandt,	loandt,	char,	8;
		거래소명,	exchname,	exchname,	char,	3;
	end
	END_DATA_MAP
END_FUNCTION_MAP
