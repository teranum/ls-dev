BEGIN_FUNCTION_MAP
	.Func,�ؿ��ֽ�API���ֿ�����ȸ(g3103),g3103,attr,block,svr=GTS,headtype=A;
	BEGIN_DATA_MAP
	g3103InBlock,�⺻�Է�,input;
	begin
		��������,delaygb,delaygb,char,1;
		KEY�����ڵ�,keysymbol,keysymbol,char,18;
		�ŷ����ڵ�,exchcd,exchcd,char,2;
		�����ڵ�,symbol,symbol,char,16;
		�ֱⱸ��,gubun,gubun,char,1;
		��ȸ����,date,date,char,8;
	end
	g3103OutBlock,���,output;
	begin
		��������,delaygb,delaygb,char,1;
		KEY�����ڵ�,keysymbol,keysymbol,char,18;
		�ŷ����ڵ�,exchcd,exchcd,char,2;
		�����ڵ�,symbol,symbol,char,16;
		�ֱⱸ��,gubun,gubun,char,1;
		��ȸ����,date,date,char,8;
	end
	g3103OutBlock1,���1,output,occurs;
	begin
		��������,chedate,chedate,char,8;
		���簡,price,price,double,15.6;
		���ϴ�񱸺�,sign,sign,char,1;
		���ϴ��,diff,diff,double,15.6;
		�����,rate,rate,float,6.2;
		�����ŷ���,volume,volume,long,16;
		�ð�,open,open,double,15.6;
		����,high,high,double,15.6;
		����,low,low,double,15.6;
		�Ҽ����ڸ���,floatpoint,floatpoint,char,1;
	end
	END_DATA_MAP
END_FUNCTION_MAP
