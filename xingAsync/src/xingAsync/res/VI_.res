BEGIN_FUNCTION_MAP
.Feed, VI발동해제(VI_), VI_, attr, key=6, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
		단축코드(KEY),          shcode,     shcode,         char,   6;
    end
    OutBlock,출력,output;
    begin
		구분(0:해제 1:정적발동 2:동적발동 3:정적&동적)	,	vi_gubun	,	vi_gubun	,	char,	1;
		정적VI발동기준가격								,	svi_recprice,	svi_recprice,	long,	8;
		동적VI발동기준가격								,	dvi_recprice,	dvi_recprice,	long,	8;
		VI발동가격										,	vi_trgprice	,	vi_trgprice	,	long,	8;
		단축코드(KEY)									,	shcode		,	shcode		,	char,	6;
		참조코드(미사용)								,	ref_shcode,		ref_shcode,		char,	6;
		시간											,	time,			time,			char,	6;
		거래소명                                        ,   exchname,       exchname,       char,   3;
    end
    END_DATA_MAP
END_FUNCTION_MAP
