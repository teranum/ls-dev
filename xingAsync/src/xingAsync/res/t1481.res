BEGIN_FUNCTION_MAP
	.Func,시간외등락율상위(t1481),t1481,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1481InBlock,기본입력,input;
	begin
		구분,gubun1,gubun1,char,1;
		상승하락,gubun2,gubun2,char,1;
		종목체크,jongchk,jongchk,char,1;
		거래량,volume,volume,char,1;
		IDX,idx,idx,long,4;
	end
	t1481OutBlock,출력,output;
	begin
		IDX,idx,idx,long,4;
	end
	t1481OutBlock1,출력1,output,occurs;
	begin
		한글명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		누적거래량,volume,volume,long,12;
		매도잔량,offerrem1,offerrem1,long,12;
		매수잔량,bidrem1,bidrem1,long,12;
		매도호가,offerho1,offerho1,long,12;
		매수호가,bidho1,bidho1,long,12;
		종목코드,shcode,shcode,char,6;
		누적거래대금,value,value,long,12;
	end
	END_DATA_MAP
END_FUNCTION_MAP

