BEGIN_FUNCTION_MAP
	.Func,주식현재가시세메모(t1104),t1104,block,headtype=A;
	BEGIN_DATA_MAP
	t1104InBlock,기본입력,input;
	begin
		종목코드,code,code,char,6;
		건수,nrec,nrec,char,2;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1104InBlock1,기본입력1,input,occurs;
	begin
		인덱스,indx,indx,char,1;
		조건구분,gubn,gubn,char,1;
		데이타1,dat1,dat1,char,1;
		데이타2,dat2,dat2,char,8;
	end
	t1104OutBlock,출력,output;
	begin
		출력건수,nrec,nrec,char,2;
	end
	t1104OutBlock1,출력1,output,occurs;
	begin
		인덱스,indx,indx,char,1;
		조건구분,gubn,gubn,char,1;
		출력값,vals,vals,char,8;
	end
	END_DATA_MAP
END_FUNCTION_MAP

