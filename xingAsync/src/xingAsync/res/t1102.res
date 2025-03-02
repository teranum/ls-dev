BEGIN_FUNCTION_MAP
.Func,주식현재가(시세)조회(t1102),t1102,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1102InBlock,기본입력,input;
	begin
		단축코드,shcode,shcode,char,6;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t1102OutBlock,출력,output;
	begin
		한글명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,double,6.2;
		누적거래량,volume,volume,long,12;
		기준가(평가가격),recprice,recprice,long,8;
		가중평균,avg,avg,long,8;
		상한가(최고호가가격),uplmtprice,uplmtprice,long,8;
		하한가(최저호가가격),dnlmtprice,dnlmtprice,long,8;
		전일거래량,jnilvolume,jnilvolume,long,12;
		거래량차,volumediff,volumediff,long,12;
		시가,open,open,long,8;
		시가시간,opentime,opentime,char,6;
		고가,high,high,long,8;
		고가시간,hightime,hightime,char,6;
		저가,low,low,long,8;
		저가시간,lowtime,lowtime,char,6;
		52최고가,high52w,high52w,long,8;
		52최고가일,high52wdate,high52wdate,char,8;
		52최저가,low52w,low52w,long,8;
		52최저가일,low52wdate,low52wdate,char,8;
		소진율,exhratio,exhratio,double,6.2;
		PER,per,per,double,6.2;
		PBRX,pbrx,pbrx,double,6.2;
		상장주식수(천),listing,listing,long,12;
		증거금율,jkrate,jkrate,long,8;
		수량단위,memedan,memedan,char,5;
		매도증권사코드1,offernocd1,offernocd1,char,3;
		매수증권사코드1,bidnocd1,bidnocd1,char,3;
		매도증권사명1,offerno1,offerno1,char,6;
		매수증권사명1,bidno1,bidno1,char,6;
		총매도수량1,dvol1,dvol1,long,8;
		총매수수량1,svol1,svol1,long,8;
		매도증감1,dcha1,dcha1,long,8;
		매수증감1,scha1,scha1,long,8;
		매도비율1,ddiff1,ddiff1,double,6.2;
		매수비율1,sdiff1,sdiff1,double,6.2;
		매도증권사코드2,offernocd2,offernocd2,char,3;
		매수증권사코드2,bidnocd2,bidnocd2,char,3;
		매도증권사명2,offerno2,offerno2,char,6;
		매수증권사명2,bidno2,bidno2,char,6;
		총매도수량2,dvol2,dvol2,long,8;
		총매수수량2,svol2,svol2,long,8;
		매도증감2,dcha2,dcha2,long,8;
		매수증감2,scha2,scha2,long,8;
		매도비율2,ddiff2,ddiff2,double,6.2;
		매수비율2,sdiff2,sdiff2,double,6.2;
		매도증권사코드3,offernocd3,offernocd3,char,3;
		매수증권사코드3,bidnocd3,bidnocd3,char,3;
		매도증권사명3,offerno3,offerno3,char,6;
		매수증권사명3,bidno3,bidno3,char,6;
		총매도수량3,dvol3,dvol3,long,8;
		총매수수량3,svol3,svol3,long,8;
		매도증감3,dcha3,dcha3,long,8;
		매수증감3,scha3,scha3,long,8;
		매도비율3,ddiff3,ddiff3,double,6.2;
		매수비율3,sdiff3,sdiff3,double,6.2;
		매도증권사코드4,offernocd4,offernocd4,char,3;
		매수증권사코드4,bidnocd4,bidnocd4,char,3;
		매도증권사명4,offerno4,offerno4,char,6;
		매수증권사명4,bidno4,bidno4,char,6;
		총매도수량4,dvol4,dvol4,long,8;
		총매수수량4,svol4,svol4,long,8;
		매도증감4,dcha4,dcha4,long,8;
		매수증감4,scha4,scha4,long,8;
		매도비율4,ddiff4,ddiff4,double,6.2;
		매수비율4,sdiff4,sdiff4,double,6.2;
		매도증권사코드5,offernocd5,offernocd5,char,3;
		매수증권사코드5,bidnocd5,bidnocd5,char,3;
		매도증권사명5,offerno5,offerno5,char,6;
		매수증권사명5,bidno5,bidno5,char,6;
		총매도수량5,dvol5,dvol5,long,8;
		총매수수량5,svol5,svol5,long,8;
		매도증감5,dcha5,dcha5,long,8;
		매수증감5,scha5,scha5,long,8;
		매도비율5,ddiff5,ddiff5,double,6.2;
		매수비율5,sdiff5,sdiff5,double,6.2;
		외국계매도합계수량,fwdvl,fwdvl,long,12;
		외국계매도직전대비,ftradmdcha,ftradmdcha,long,12;
		외국계매도비율,ftradmddiff,ftradmddiff,double,6.2;
		외국계매수합계수량,fwsvl,fwsvl,long,12;
		외국계매수직전대비,ftradmscha,ftradmscha,long,12;
		외국계매수비율,ftradmsdiff,ftradmsdiff,double,6.2;
		회전율,vol,vol,double,6.2;
		단축코드,shcode,shcode,char,6;
		누적거래대금,value,value,long,12;
		전일동시간거래량,jvolume,jvolume,long,12;
		연중최고가,highyear,highyear,long,8;
		연중최고일자,highyeardate,highyeardate,char,8;
		연중최저가,lowyear,lowyear,long,8;
		연중최저일자,lowyeardate,lowyeardate,char,8;
		목표가,target,target,long,8;
		자본금,capital,capital,long,12;
		유동주식수,abscnt,abscnt,long,12;
		액면가,parprice,parprice,long,8;
		결산월,gsmm,gsmm,char,2;
		대용가,subprice,subprice,long,8;
		시가총액,total,total,long,12;
		상장일,listdate,listdate,char,8;
		전분기명,name,name,char,10;
		전분기매출액,bfsales,bfsales,long,12;
		전분기영업이익,bfoperatingincome,bfoperatingincome,long,12;
		전분기경상이익,bfordinaryincome,bfordinaryincome,long,12;
		전분기순이익,bfnetincome,bfnetincome,long,12;
		전분기EPS,bfeps,bfeps,double,13.2;
		전전분기명,name2,name2,char,10;
		전전분기매출액,bfsales2,bfsales2,long,12;
		전전분기영업이익,bfoperatingincome2,bfoperatingincome2,long,12;
		전전분기경상이익,bfordinaryincome2,bfordinaryincome2,long,12;
		전전분기순이익,bfnetincome2,bfnetincome2,long,12;
		전전분기EPS,bfeps2,bfeps2,double,13.2;
		전년대비매출액,salert,salert,double,7.2;
		전년대비영업이익,opert,opert,double,7.2;
		전년대비경상이익,ordrt,ordrt,double,7.2;
		전년대비순이익,netrt,netrt,double,7.2;
		전년대비EPS,epsrt,epsrt,double,7.2;
		락구분,info1,info1,char,10;
		관리/급등구분,info2,info2,char,10;
		정지/연장구분,info3,info3,char,10;
		투자/불성실구분,info4,info4,char,12;
		장구분,janginfo,janginfo,char,10;
		T.PER,t_per,t_per,double,6.2;
		통화ISO코드,tonghwa,tonghwa,char,3;
		총매도대금1,dval1,dval1,long,18;
		총매수대금1,sval1,sval1,long,18;
		총매도대금2,dval2,dval2,long,18;
		총매수대금2,sval2,sval2,long,18;
		총매도대금3,dval3,dval3,long,18;
		총매수대금3,sval3,sval3,long,18;
		총매도대금4,dval4,dval4,long,18;
		총매수대금4,sval4,sval4,long,18;
		총매도대금5,dval5,dval5,long,18;
		총매수대금5,sval5,sval5,long,18;
		총매도평단가1,davg1,davg1,long,8;
		총매수평단가1,savg1,savg1,long,8;
		총매도평단가2,davg2,davg2,long,8;
		총매수평단가2,savg2,savg2,long,8;
		총매도평단가3,davg3,davg3,long,8;
		총매수평단가3,savg3,savg3,long,8;
		총매도평단가4,davg4,davg4,long,8;
		총매수평단가4,savg4,savg4,long,8;
		총매도평단가5,davg5,davg5,long,8;
		총매수평단가5,savg5,savg5,long,8;
		외국계매도대금,ftradmdval,ftradmdval,long,18;
		외국계매수대금,ftradmsval,ftradmsval,long,18;
		외국계매도평단가,ftradmdvag,ftradmdavg,long,8;
		외국계매수평단가,ftradmsvag,ftradmsavg,long,8;
		투자주의환기,info5,info5,char,8;
		기업인수목적회사여부,spac_gubun,spac_gubun,char,1;
		발행가격,issueprice,issueprice,long,8;
		배분적용구분코드(1:배분발생2:배분해제그외:미발생),alloc_gubun,alloc_gubun,char,1;
		배분적용구분,alloc_text,alloc_text,char,8;
		단기과열/VI발동,shterm_text,shterm_text,char,10;
		정적VI상한가,svi_uplmtprice,svi_uplmtprice,long,8;
		정적VI하한가,svi_dnlmtprice,svi_dnlmtprice,long,8;
		저유동성종목여부,low_lqdt_gu,low_lqdt_gu,char,1;
		이상급등종목여부,abnormal_rise_gu,abnormal_rise_gu,char,1;
		대차불가표시,lend_text,lend_text,char,8;
		ETF/ETN투자유의,ty_text,ty_text,char,8;
		NXT장구분,nxt_janginfo,nxt_janginfo,char,10;
		NXT단기과열/VI발동,nxt_shterm_text,nxt_shterm_text,char,10;
		NXT정적VI상한가,nxt_svi_uplmtprice,nxt_svi_uplmtprice,long,8;
		NXT정적VI하한가,nxt_svi_dnlmtprice,nxt_svi_dnlmtprice,long,8;
		거래소별단축코드,ex_shcode,ex_shcode,char,10;
	end
	END_DATA_MAP
END_FUNCTION_MAP
