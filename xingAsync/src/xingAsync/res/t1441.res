BEGIN_FUNCTION_MAP
.Func,등락율상위(t1441),t1441,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1441InBlock,기본입력,input;
	begin
		구분,gubun1,gubun1,char,1;
		상승하락,gubun2,gubun2,char,1;
		당일전일,gubun3,gubun3,char,1;
		대상제외,jc_num,jc_num,long,12;
		시작가격,sprice,sprice,long,8;
		종료가격,eprice,eprice,long,8;
		거래량,volume,volume,long,12;
		IDX,idx,idx,long,4;
		대상제외2,jc_num2,jc_num2,long,12;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1441OutBlock,출력,output;
	begin
		IDX,idx,idx,long,4;
	end
	t1441OutBlock1,출력1,output,occurs;
	begin
		한글명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,double,6.2;
		누적거래량,volume,volume,long,12;
		매도잔량,offerrem1,offerrem1,long,12;
		매도호가,offerho1,offerho1,long,12;
		매수호가,bidho1,bidho1,long,12;
		매수잔량,bidrem1,bidrem1,long,12;
		연속,updaycnt,updaycnt,long,4;
		전일등락율,jnildiff,jnildiff,double,6.2;
		종목코드,shcode,shcode,char,6;
		시가,open,open,long,8;
		고가,high,high,long,8;
		저가,low,low,long,8;
		거래량대비율,voldiff,voldiff,double,8.2;
		거래대금,value,value,long,15;
		시가총액,total,total,long,12;
		거래소별단축코드,ex_shcode,ex_shcode,char,10;
	end
	END_DATA_MAP
END_FUNCTION_MAP
