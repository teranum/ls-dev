BEGIN_FUNCTION_MAP
	.Func,해외주식차트NTICK,g3202,attr,block,svr=GTS,headtype=A;
	BEGIN_DATA_MAP
	g3202InBlock,기본입력,input;
	begin
		지연구분,delaygb,delaygb,char,1;
		KEY종목코드,keysymbol,keysymbol,char,18;
		거래소코드,exchcd,exchcd,char,2;
		종목코드,symbol,symbol,char,16;
		단위(n틱),ncnt,ncnt,long,4;
		요청건수(최대-압축:2000비압축:500),qrycnt,qrycnt,long,4;
		압축여부(Y:압축N:비압축),comp_yn,comp_yn,char,1;
		시작일자,sdate,sdate,char,8;
		종료일자,edate,edate,char,8;
		연속시퀀스,cts_seq,cts_seq,long,17;
	end
	g3202OutBlock,출력,output;
	begin
		지연구분,delaygb,delaygb,char,1;
		KEY종목코드,keysymbol,keysymbol,char,18;
		거래소코드,exchcd,exchcd,char,2;
		종목코드,symbol,symbol,char,16;
		연속시퀀스,cts_seq,cts_seq,long,17;
		레코드카운트,rec_count,rec_count,long,7;
		전일시가,preopen,preopen,double,15.8;
		전일고가,prehigh,prehigh,double,15.8;
		전일저가,prelow,prelow,double,15.8;
		전일종가,preclose,preclose,double,15.8;
		전일거래량,prevolume,prevolume,long,16;
		당일시가,open,open,double,15.8;
		당일고가,high,high,double,15.8;
		당일저가,low,low,double,15.8;
		당일종가,close,close,double,15.8;
		장시작시간(HHMMSS),s_time,s_time,char,6;
		장종료시간(HHMMSS),e_time,e_time,char,6;
		마지막Tick건수,last_count,last_count,char,4;
		시차,timediff,timediff,char,4;
	end
	g3202OutBlock1,출력1,output,occurs;
	begin
		날짜,date,date,char,8;
		현지시간,loctime,loctime,char,6;
		시가,open,open,double,15.8;
		고가,high,high,double,15.8;
		저가,low,low,double,15.8;
		종가,close,close,double,15.8;
		체결량,exevol,exevol,long,16;
		수정구분,jongchk,jongchk,long,13;
		수정비율,prtt_rate,prtt_rate,double,6.2;
		수정주가반영항목,pricechk,pricechk,long,13;
		종가등락구분(1:상한2:상승3:보합4:하한5:하락주식일만사용),sign,sign,char,1;
	end
	END_DATA_MAP
END_FUNCTION_MAP

