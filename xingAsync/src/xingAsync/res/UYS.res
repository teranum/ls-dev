BEGIN_FUNCTION_MAP
	.Feed, KOSPI + KOSDAQ ����ü��(UYS), UYS, attr, key=10, group=4;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
		�ŷ��Һ������ڵ�,		ex_shcode,		ex_shcode,		char,   10;
    end
    OutBlock,���,output;
    begin
		ȣ���ð�,				hotime,			hotime,			char,	6;
		����ü�ᰡ��,			yeprice,		yeprice,		long,	8;
		����ü�����,			yevolume,		yevolume,		long,	12;
����ü�ᰡ����������񱸺�,		jnilysign,      jnilysign,		char,	1;
����ü�ᰡ�����������,			jnilchange,		preychange,		long,	8;
����ü�ᰡ�������������,		jnilydrate,     jnilydrate,		float,	6.2;
		����ŵ�ȣ��,			yofferho0,		yofferho0,		long,	8;
		����ż�ȣ��,			ybidho0,		ybidho0,		long,	8;
		����ŵ�ȣ������,		yofferrem0,		yofferrem0,		long,	12;
		����ż�ȣ������,		ybidrem0,		ybidrem0,		long,	12;
		�����ڵ�,				shcode,			shcode,			char,	9;
		�ŷ��Ҹ�,     			exchname,       exchname,       char,   3;	// KRX NXT
		�ŷ��Һ������ڵ�,   	ex_shcode,		ex_shcode,		char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
