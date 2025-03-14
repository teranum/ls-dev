BEGIN_FUNCTION_MAP
.Func,외인기관종목별동향(t1716),t1716,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1716InBlock,기본입력,input;
	begin
		종목코드,shcode,shcode,char,6;
		구분(0:일간순매수1:기간누적순매수),gubun,gubun,char,1;
		시작일자,fromdt,fromdt,char,8;
		종료일자,todt,todt,char,8;
		PR감산적용율,prapp,prapp,long,3;
		PR적용구분(0:적용안함1:적용),prgubun,prgubun,char,1;
		기관적용,orggubun,orggubun,char,1;
		외인적용,frggubun,frggubun,char,1;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1716OutBlock,출력,output,occurs;
	begin
		일자,date,date,char,8;
		종가,close,close,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,double,6.2;
		누적거래량,volume,volume,long,12;
		거래소_개인,krx_0008,krx_0008,long,12;
		거래소_기관,krx_0018,krx_0018,long,12;
		거래소_외국인,krx_0009,krx_0009,long,12;
		프로그램,pgmvol,pgmvol,long,12;
		금감원_외인보유주식수,fsc_listing,fsc_listing,long,12;
		금감원_소진율,fsc_sjrate,fsc_sjrate,double,6.2;
		금감원_외국인,fsc_0009,fsc_0009,long,12;
		공매도수량,gm_volume,gm_volume,long,12;
		공매도대금,gm_value,gm_value,long,12;
	end
	END_DATA_MAP
END_FUNCTION_MAP
