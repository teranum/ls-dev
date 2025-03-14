BEGIN_FUNCTION_MAP
.Feed, KRX+NXT통합 KOSPI + KOSDAQ 거래원(UK1), UK1, attr, key=10, group=4;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
		거래소별단축코드,               ex_shcode,      ex_shcode,      char,   10;
    end
    OutBlock,출력,output;
    begin
		매도증권사코드1 ,	            offerno1,		offerno1,		char,	3;
		매수증권사코드1 ,	            bidno1,			bidno1,			char,	3;
		매도회원사명1 ,		            offertrad1,		offertrad1,		char,	6;
		매수회원사명1 ,		            bidtrad1,		bidtrad1,		char,	6;
		매도거래량1,		            tradmdvol1,		tradmdvol1,		long,	10;
		매수거래량1,		            tradmsvol1,		tradmsvol1,		long,	10;
		매도거래량비중1,	            tradmdrate1,	tradmdrate1,	float,	6.2;
		매수거래량비중1,	            tradmsrate1,	tradmsrate1,	float,	6.2;
    	매도거래량직전대비1,	        tradmdcha1,		tradmdcha1,		long,	10;
    	매수거래량직전대비1,	        tradmscha1,		tradmscha1,		long,	10;
		매도증권사코드2 ,	            offerno2,		offerno2,		char,	3;
		매수증권사코드2 ,	            bidno2,			bidno2,			char,	3;
		매도회원사명2 ,		            offertrad2,		offertrad2,		char,	6;
		매수회원사명2 ,		            bidtrad2,		bidtrad2,		char,	6;
		매도거래량2,		            tradmdvol2,		tradmdvol2,		long,	10;
		매수거래량2,		            tradmsvol2,		tradmsvol2,		long,	10;
		매도거래량비중2,	            tradmdrate2,	tradmdrate2,	float,	6.2;
		매수거래량비중2,	            tradmsrate2,	tradmsrate2,	float,	6.2;
    	매도거래량직전대비2,	        tradmdcha2,		tradmdcha2,		long,	10;
    	매수거래량직전대비2,	        tradmscha2,		tradmscha2,		long,	10;
		매도증권사코드3 ,	            offerno3,		offerno3,		char,	3;
		매수증권사코드3 ,	            bidno3,			bidno3,			char,	3;
		매도회원사명3 ,		            offertrad3,		offertrad3,		char,	6;
		매수회원사명3 ,		            bidtrad3,		bidtrad3,		char,	6;
		매도거래량3,		            tradmdvol3,		tradmdvol3,		long,	10;
		매수거래량3,		            tradmsvol3,		tradmsvol3,		long,	10;
		매도거래량비중3,	            tradmdrate3,	tradmdrate3,	float,	6.2;
		매수거래량비중3,	            tradmsrate3,	tradmsrate3,	float,	6.2;
    	매도거래량직전대비3,	        tradmdcha3,		tradmdcha3,		long,	10;
    	매수거래량직전대비3,	        tradmscha3,		tradmscha3,		long,	10;
		매도증권사코드4 ,	            offerno4,		offerno4,		char,	3;
		매수증권사코드4 ,	            bidno4,			bidno4,			char,	3;
		매도회원사명4 ,		            offertrad4,		offertrad4,		char,	6;
		매수회원사명4 ,		            bidtrad4,		bidtrad4,		char,	6;
		매도거래량4,		            tradmdvol4,		tradmdvol4,		long,	10;
		매수거래량4,		            tradmsvol4,		tradmsvol4,		long,	10;
		매도거래량비중4,	            tradmdrate4,	tradmdrate4,	float,	6.2;
		매수거래량비중4,	            tradmsrate4,	tradmsrate4,	float,	6.2;
    	매도거래량직전대비4,	        tradmdcha4,		tradmdcha4,		long,	10;
    	매수거래량직전대비4,	        tradmscha4,		tradmscha4,		long,	10;
		매도증권사코드5 ,	            offerno5,		offerno5,		char,	3;
		매수증권사코드5 ,	            bidno5,			bidno5,			char,	3;
		매도회원사명5 ,		            offertrad5,		offertrad5,		char,	6;
		매수회원사명5 ,		            bidtrad5,		bidtrad5,		char,	6;
		매도거래량5,		            tradmdvol5,		tradmdvol5,		long,	10;
		매수거래량5,		            tradmsvol5,		tradmsvol5,		long,	10;
		매도거래량비중5,	            tradmdrate5,	tradmdrate5,	float,	6.2;
		매수거래량비중5,	            tradmsrate5,	tradmsrate5,	float,	6.2;
    	매도거래량직전대비5,	        tradmdcha5,		tradmdcha5,		long,	10;
    	매수거래량직전대비5,	        tradmscha5,		tradmscha5,		long,	10;
    	외국계증권사매도합계,	        ftradmdvol,		ftradmdvol,		char,	10;
    	외국계증권사매수합계,	        ftradmsvol,		ftradmsvol,		char,	10;
        외국계증권사매도거래량비중,	    ftradmdrate,	ftradmdrate,	float,	6.2;
        외국계증권사매수거래량비중,	    ftradmsrate,	ftradmsrate,	float,	6.2;
        외국계증권사매도거래량직전대비,	ftradmdcha, 	ftradmdcha,		char,	10;
        외국계증권사매수거래량직전대비,	ftradmscha,	    ftradmscha,		char,	10;
		단축코드,			            shcode,			shcode,			char,	9;
		매도거래대금1,                  tradmdval1,     tradmdval1,     long,   15;
		매수거래대금1,                  tradmsval1,     tradmsval1,     long,   15;
		매도평균단가1,                  tradmdavg1,     tradmdavg1,     long,   7;
		매수평균단가1,                  tradmsavg1,     tradmsavg1,     long,   7;
		매도거래대금2,                  tradmdval2,     tradmdval2,     long,   15;
		매수거래대금2,                  tradmsval2,     tradmsval2,     long,   15;
		매도평균단가2,                  tradmdavg2,     tradmdavg2,     long,   7;
		매수평균단가2,                  tradmsavg2,     tradmsavg2,     long,   7;
		매도거래대금3,                  tradmdval3,     tradmdval3,     long,   15;
		매수거래대금3,                  tradmsval3,     tradmsval3,     long,   15;
		매도평균단가3,                  tradmdavg3,     tradmdavg3,     long,   7;
		매수평균단가3,                  tradmsavg3,     tradmsavg3,     long,   7;
		매도거래대금4,                  tradmdval4,     tradmdval4,     long,   15;
		매수거래대금4,                  tradmsval4,     tradmsval4,     long,   15;
		매도평균단가4,                  tradmdavg4,     tradmdavg4,     long,   7;
		매수평균단가4,                  tradmsavg4,     tradmsavg4,     long,   7;
		매도거래대금5,                  tradmdval5,     tradmdval5,     long,   15;
		매수거래대금5,                  tradmsval5,     tradmsval5,     long,   15;
		매도평균단가5,                  tradmdavg5,     tradmdavg5,     long,   7;
		매수평균단가5,                  tradmsavg5,     tradmsavg5,     long,   7;
        외국계증권사매도거래대금,       ftradmdval,     ftradmdval,     long,   15;
        외국계증권사매수거래대금,       ftradmsval,     ftradmsval,     long,   15;
        외국계증권사매도평균단가,       ftradmdavg,     ftradmdavg,     long,   7;
        외국계증권사매수평균단가,       ftradmsavg,     ftradmsavg,     long,   7;
        수신시간,                       time,           time,           char,   6;
        거래소명,                       exchname,       exchname,       char,   3;      // KRX NXT
		거래소별단축코드,               ex_shcode,      ex_shcode,      char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
