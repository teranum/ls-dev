BEGIN_FUNCTION_MAP
	.Func,외인기관종목별동향(t1702),t1702,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1702InBlock,기본입력,input;
	begin
		종목코드,shcode,shcode,char,6;
		종료일자,todt,todt,char,8;
		금액수량구분(0:금액1:수량2:단가),volvalgb,volvalgb,char,1;
		매수매도구분(0:순매수1:매수2:매도),msmdgb,msmdgb,char,1;
		누적구분(0:일간1:누적),cumulgb,cumulgb,char,1;
		CTSDATE,cts_date,cts_date,char,8;
		CTSIDX,cts_idx,cts_idx,long,4;
	end
	t1702OutBlock,기본출력,output;
	begin
		CTSIDX,cts_idx,cts_idx,long,4;
		CTSDATE,cts_date,cts_date,char,8;
	end
	t1702OutBlock1,출력,output,occurs;
	begin
		일자,date,date,char,8;
		종가,close,close,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		누적거래량,volume,volume,long,12;
		사모펀드,amt0000,amt0000,long,12;
		증권,amt0001,amt0001,long,12;
		보험,amt0002,amt0002,long,12;
		투신,amt0003,amt0003,long,12;
		은행,amt0004,amt0004,long,12;
		종금,amt0005,amt0005,long,12;
		기금,amt0006,amt0006,long,12;
		기타법인,amt0007,amt0007,long,12;
		개인,amt0008,amt0008,long,12;
		등록외국인,amt0009,amt0009,long,12;
		미등록외국인,amt0010,amt0010,long,12;
		국가외,amt0011,amt0011,long,12;
		기관,amt0018,amt0018,long,12;
		외인계(등록+미등록),amt0088,amt0088,long,12;
		기타계(기타+국가),amt0099,amt0099,long,12;
	end
	END_DATA_MAP
END_FUNCTION_MAP

t1702