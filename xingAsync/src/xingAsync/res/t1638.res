BEGIN_FUNCTION_MAP
	.Func,종목별잔량/사전공시(t1638),t1638,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1638InBlock,기본입력,input;
	begin
		구분,gubun1,gubun1,char,1;
		종목코드,shcode,shcode,char,6;
		정렬,gubun2,gubun2,char,1;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1638OutBlock,출력,output,occurs;
	begin
		순위,rank,rank,long,4;
		한글명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		시총비중,sigatotrt,sigatotrt,float,6.2;
		순매수잔량,obuyvol,obuyvol,long,12;
		매수잔량,buyrem,buyrem,long,12;
		매수공시수량,psgvolume,psgvolume,long,12;
		매도잔량,sellrem,sellrem,long,12;
		매도공시수량,pdgvolume,pdgvolume,long,12;
		시가총액,sigatot,sigatot,long,20;
		종목코드,shcode,shcode,char,6;
	end
	END_DATA_MAP
END_FUNCTION_MAP

