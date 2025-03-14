BEGIN_FUNCTION_MAP
	.Func,주식챠트(틱/n틱)(t8453),t8453,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t8453InBlock,기본입력,input;
	begin
		단축코드,shcode,shcode,char,6;
		단위(n틱),ncnt,ncnt,long,4;
		요청건수(최대-압축:2000비압축:500),qrycnt,qrycnt,long,4;
		조회영업일수(0:미사용1>=사용),nday,nday,char,1;
		시작일자,sdate,sdate,char,8;
		시작시간(현재미사용),stime,stime,char,6;
		종료일자,edate,edate,char,8;
		종료시간(현재미사용),etime,etime,char,6;
		연속일자,cts_date,cts_date,char,8;
		연속시간,cts_time,cts_time,char,10;
		압축여부(Y:압축N:비압축),comp_yn,comp_yn,char,1;
		거래소구분코드,exchgubun,exchgubun,char,1;
	end
	t8453OutBlock,출력,output;
	begin
		단축코드,shcode,shcode,char,6;
		전일시가,jisiga,jisiga,long,8;
		전일고가,jihigh,jihigh,long,8;
		전일저가,jilow,jilow,long,8;
		전일종가,jiclose,jiclose,long,8;
		전일거래량,jivolume,jivolume,long,12;
		당일시가,disiga,disiga,long,8;
		당일고가,dihigh,dihigh,long,8;
		당일저가,dilow,dilow,long,8;
		당일종가,diclose,diclose,long,8;
		상한가,highend,highend,long,8;
		하한가,lowend,lowend,long,8;
		연속일자,cts_date,cts_date,char,8;
		연속시간,cts_time,cts_time,char,10;
		장시작시간(HHMMSS),s_time,s_time,char,6;
		장종료시간(HHMMSS),e_time,e_time,char,6;
		동시호가처리시간(MM:분),dshmin,dshmin,char,2;
		레코드카운트,rec_count,rec_count,long,7;
        NXT프리마켓장시작시간(HHMMSS)         , nxt_fm_s_time, nxt_fm_s_time, char      , 6;
        NXT프리마켓장종료시간(HHMMSS)         , nxt_fm_e_time, nxt_fm_e_time, char      , 6;
        NXT프리마켓동시호가처리시간(MM:분)    , nxt_fm_dshmin, nxt_fm_dshmin, char      , 2;
        NXT에프터마켓장시작시간(HHMMSS)       , nxt_am_s_time, nxt_am_s_time, char      , 6;
        NXT에프터마켓장종료시간(HHMMSS)       , nxt_am_e_time, nxt_am_e_time, char      , 6;
        NXT에프터마켓동시호가처리시간(MM:분)  , nxt_am_dshmin, nxt_am_dshmin, char      , 2;
	end
	t8453OutBlock1,출력1,output,occurs;
	begin
		날짜,date,date,char,8;
		시간,time,time,char,10;
		시가,open,open,long,8;
		고가,high,high,long,8;
		저가,low,low,long,8;
		종가,close,close,long,8;
		거래량,jdiff_vol,jdiff_vol,long,12;
		수정구분,jongchk,jongchk,long,13;
		수정비율,rate,rate,double,6.2;
		수정주가반영항목,pricechk,pricechk,long,13;
	end
	END_DATA_MAP
END_FUNCTION_MAP


