BEGIN_FUNCTION_MAP
.Feed, NXT KOSPI + KOSDAQ �켱ȣ��(NS2), NS2, attr, key=10, group=4;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
		�ŷ��Һ������ڵ�,               ex_shcode,     ex_shcode,     char,   10;
    end
    OutBlock,���,output;
    begin
		�ŵ�ȣ��,						offerho,		offerho,		long,	8;
		�ż�ȣ��,						bidho,			bidho,			long,	8;
		�����ڵ�,						shcode,			shcode,			char,	9;
		�ŷ��Һ������ڵ�,               ex_shcode,      ex_shcode,      char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
