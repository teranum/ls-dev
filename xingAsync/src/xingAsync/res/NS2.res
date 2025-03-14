BEGIN_FUNCTION_MAP
.Feed, NXT KOSPI + KOSDAQ 우선호가(NS2), NS2, attr, key=10, group=4;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
		거래소별단축코드,               ex_shcode,     ex_shcode,     char,   10;
    end
    OutBlock,출력,output;
    begin
		매도호가,						offerho,		offerho,		long,	8;
		매수호가,						bidho,			bidho,			long,	8;
		단축코드,						shcode,			shcode,			char,	9;
		거래소별단축코드,               ex_shcode,      ex_shcode,      char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
