BEGIN_FUNCTION_MAP
.Feed, 해외주식 호가(GSH), GSH, attr, svr=OVS, key=18, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
        종목코드,       keysymbol,    keysymbol,    char,   18;
    end
    OutBlock,출력,output;
    begin
		종목코드         ,   symbol      ,   symbol      , char    ,   16 ;
		현지호가시간	 ,	 loctime	 ,	 loctime	 , char	   ,   6 ;
		한국호가시간	 ,	 kortime	 ,	 kortime	 , char	   ,   6 ;

		매도호가 1       ,   offerho1    ,   offerho1    , double  ,   15.6;
		매수호가 1       ,   bidho1      ,   bidho1      , double  ,   15.6;
		매도호가 잔량 1  ,   offerrem1   ,   offerrem1   , long    ,   10;
		매수호가 잔량 1  ,   bidrem1     ,   bidrem1     , long    ,   10;
		매도호가 건수 1  ,   offerno1    ,   offerno1    , long    ,   10;
		매수호가 건수 1  ,   bidno1      ,   bidno1      , long    ,   10;
        
        매도호가 2       ,   offerho2    ,   offerho2    , double  ,   15.6;
        매수호가 2       ,   bidho2      ,   bidho2      , double  ,   15.6;
        매도호가 잔량 2  ,   offerrem2   ,   offerrem2   , long    ,   10;
        매수호가 잔량 2  ,   bidrem2     ,   bidrem2     , long    ,   10;
        매도호가 건수 2  ,   offerno2    ,   offerno2    , long    ,   10;
        매수호가 건수 2  ,   bidno2      ,   bidno2      , long    ,   10;

		매도호가 3       ,   offerho3    ,   offerho3    , double  ,   15.6;
		매수호가 3       ,   bidho3      ,   bidho3      , double  ,   15.6;
		매도호가 잔량 3  ,   offerrem3   ,   offerrem3   , long    ,   10;
		매수호가 잔량 3  ,   bidrem3     ,   bidrem3     , long    ,   10;
		매도호가 건수 3  ,   offerno3    ,   offerno3    , long    ,   10;
		매수호가 건수 3  ,   bidno3      ,   bidno3      , long    ,   10;

		매도호가 4       ,   offerho4    ,   offerho4    , double  ,   15.6;
		매수호가 4       ,   bidho4      ,   bidho4      , double  ,   15.6;
		매도호가 잔량 4  ,   offerrem4   ,   offerrem4   , long    ,   10;
		매수호가 잔량 4  ,   bidrem4     ,   bidrem4     , long    ,   10;
		매도호가 건수 4  ,   offerno4    ,   offerno4    , long    ,   10;
		매수호가 건수 4  ,   bidno4      ,   bidno4      , long    ,   10;

		매도호가 5       ,   offerho5    ,   offerho5    , double  ,   15.6;
		매수호가 5       ,   bidho5      ,   bidho5      , double  ,   15.6;
		매도호가 잔량 5  ,   offerrem5   ,   offerrem5   , long    ,   10;
		매수호가 잔량 5  ,   bidrem5     ,   bidrem5     , long    ,   10;
		매도호가 건수 5  ,   offerno5    ,   offerno5    , long    ,   10;
		매수호가 건수 5  ,   bidno5      ,   bidno5      , long    ,   10;

		매도호가 6       ,   offerho6    ,   offerho6    , double  ,   15.6;
		매수호가 6       ,   bidho6      ,   bidho6      , double  ,   15.6;
		매도호가 잔량 6  ,   offerrem6   ,   offerrem6   , long    ,   10;
		매수호가 잔량 6  ,   bidrem6     ,   bidrem6     , long    ,   10;
		매도호가 건수 6  ,   offerno6    ,   offerno6    , long    ,   10;
		매수호가 건수 6  ,   bidno6      ,   bidno6      , long    ,   10;

		매도호가 7       ,   offerho7    ,   offerho7    , double  ,   15.6;
		매수호가 7       ,   bidho7      ,   bidho7      , double  ,   15.6;
		매도호가 잔량 7  ,   offerrem7   ,   offerrem7   , long    ,   10;
		매수호가 잔량 7  ,   bidrem7     ,   bidrem7     , long    ,   10;
		매도호가 건수 7  ,   offerno7    ,   offerno7    , long    ,   10;
		매수호가 건수 7  ,   bidno7      ,   bidno7      , long    ,   10;

		매도호가 8       ,   offerho8    ,   offerho8    , double  ,   15.6;
		매수호가 8       ,   bidho8      ,   bidho8      , double  ,   15.6;
		매도호가 잔량 8  ,   offerrem8   ,   offerrem8   , long    ,   10;
		매수호가 잔량 8  ,   bidrem8     ,   bidrem8     , long    ,   10;
		매도호가 건수 8  ,   offerno8    ,   offerno8    , long    ,   10;
		매수호가 건수 8  ,   bidno8      ,   bidno8      , long    ,   10;

		매도호가 9       ,   offerho9    ,   offerho9    , double  ,   15.6;
		매수호가 9       ,   bidho9      ,   bidho9      , double  ,   15.6;
		매도호가 잔량 9  ,   offerrem9   ,   offerrem9   , long    ,   10;
		매수호가 잔량 9  ,   bidrem9     ,   bidrem9     , long    ,   10;
		매도호가 건수 9  ,   offerno9    ,   offerno9    , long    ,   10;
		매수호가 건수 9  ,   bidno9      ,   bidno9      , long    ,   10;

		매도호가 10       ,   offerho10    ,   offerho10    , double  ,   15.6;
		매수호가 10       ,   bidho10      ,   bidho10      , double  ,   15.6;
		매도호가 잔량 10  ,   offerrem10   ,   offerrem10   , long    ,   10;
		매수호가 잔량 10  ,   bidrem10     ,   bidrem10     , long    ,   10;
		매도호가 건수 10  ,   offerno10    ,   offerno10    , long    ,   10;
		매수호가 건수 10  ,   bidno10      ,   bidno10      , long    ,   10;

        매도호가총건수   ,   totoffercnt ,   totoffercnt , long    ,   10;
        매수호가총건수   ,   totbidcnt   ,   totbidcnt   , long    ,   10;
        매도호가총수량   ,   totofferrem ,   totofferrem , long    ,   10;
        매수호가총수량   ,   totbidrem   ,   totbidrem   , long    ,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
