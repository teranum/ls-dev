BEGIN_FUNCTION_MAP
.Func,시간별예상체결가(t1486),t1486,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1486InBlock,기본입력,input;
	begin
		단축코드,shcode,shcode,char,6;
		시간CTS,cts_time,cts_time,char,10;
		조회건수,cnt,cnt,long,4;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1486OutBlock,출력,output;
	begin
		시간CTS,cts_time,cts_time,char,10;
		거래소별단축코드,ex_shcode,ex_shcode,char,10;
	end
	t1486OutBlock1,출력1,output,occurs;
	begin
		시간,chetime,chetime,char,8;
		예상체결가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,double,6.2;
		예상체결량,cvolume,cvolume,long,12;
		매도호가,offerho1,offerho1,long,8;
		매수호가,bidho1,bidho1,long,8;
		매도잔량,offerrem1,offerrem1,long,12;
		매수잔량,bidrem1,bidrem1,long,12;
		거래소명,exchname,exchname,char,3;
	end
	END_DATA_MAP
END_FUNCTION_MAP
