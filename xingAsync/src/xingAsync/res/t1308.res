BEGIN_FUNCTION_MAP
.Func,주식시간대별체결조회챠트(t1308),t1308,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1308InBlock,기본입력,input;
	begin
		단축코드,shcode,shcode,char,6;
		시작시간,starttime,starttime,char,4;
		종료시간,endtime,endtime,char,4;
		분간격,bun_term,bun_term,char,2;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1308OutBlock,출력,output;
	begin
		거래소별단축코드,ex_shcode,ex_shcode,char,10;
	end
	t1308OutBlock1,출력1,output,occurs;
	begin
		시간,chetime,chetime,char,8;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,double,6.2;
		체결수량,cvolume,cvolume,long,8;
		체결강도(거래량),chdegvol,chdegvol,double,8.2;
		체결강도(건수),chdegcnt,chdegcnt,double,8.2;
		거래량,volume,volume,long,12;
		매도체결수량,mdvolume,mdvolume,long,12;
		매도체결건수,mdchecnt,mdchecnt,long,8;
		매수체결수량,msvolume,msvolume,long,12;
		매수체결건수,mschecnt,mschecnt,long,8;
		시가,open,open,long,8;
		고가,high,high,long,8;
		저가,low,low,long,8;
	end
	END_DATA_MAP
END_FUNCTION_MAP
