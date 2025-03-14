BEGIN_FUNCTION_MAP
.Func, 주식시간대별체결조회2(t8454), t8454, attr, block, headtype=A;
	BEGIN_DATA_MAP
	t8454InBlock,기본입력,input;
	begin
		단축코드            , shcode           , shcode           , char             , 6;
		특이거래량          , cvolume          , cvolume          , long             , 12;
		시작시간            , starttime        , starttime        , char             , 4;
		종료시간            , endtime          , endtime          , char             , 4;
		시간CTS             , cts_time         , cts_time         , char             , 10;
		거래소구분코드      , exchgubun        , exchgubun        , char             , 1;
	end
	t8454OutBlock,출력,output;
	begin
		시간CTS             , cts_time         , cts_time         , char             , 10;
		거래소별단축코드    , ex_shcode        , ex_shcode        , char             , 10;
	end
	t8454OutBlock1,출력1,output,occurs;
	begin
		시간                , chetime          , chetime          , char             , 10;
		현재가              , price            , price            , long             , 8;
		전일대비구분        , sign             , sign             , char             , 1;
		전일대비            , change           , change           , long             , 8;
		등락율              , diff             , diff             , double           , 6.2;
		체결수량            , cvolume          , cvolume          , long             , 12;
		체결강도            , chdegree         , chdegree         , double           , 8.2;
		거래량              , volume           , volume           , long             , 12;
		매도체결수량        , mdvolume         , mdvolume         , long             , 12;
		매도체결건수        , mdchecnt         , mdchecnt         , long             , 8;
		매수체결수량        , msvolume         , msvolume         , long             , 12;
		매수체결건수        , mschecnt         , mschecnt         , long             , 8;
		순체결량            , revolume         , revolume         , long             , 12;
		순체결건수          , rechecnt         , rechecnt         , long             , 8;
		거래소명            , exchname         , exchname         , char             , 3;
	end
	END_DATA_MAP
END_FUNCTION_MAP
