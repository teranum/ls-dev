BEGIN_FUNCTION_MAP
	.Func,시간외거래량상위(t1482),t1482,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1482InBlock,기본입력,input;
	begin
		구분,gubun,gubun,char,1;
		거래량,jongchk,jongchk,char,1;
		IDX,idx,idx,long,4;
	end
	t1482OutBlock,출력,output;
	begin
		IDX,idx,idx,long,4;
	end
	t1482OutBlock1,출력1,output,occurs;
	begin
		종목명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		누적거래량,volume,volume,long,12;
		회전율,vol,vol,float,6.2;
		종목코드,shcode,shcode,char,6;
		누적거래대금,value,value,long,12;
	end
	END_DATA_MAP
END_FUNCTION_MAP

