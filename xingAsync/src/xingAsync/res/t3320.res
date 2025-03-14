BEGIN_FUNCTION_MAP
.Func, FNG_요약(t3320), t3320, attr, block, headtype=A;
	BEGIN_DATA_MAP
	t3320InBlock,기본입력,input;
	begin
		종목코드                  , gicode          , gicode          , char      , 7;
	end
	t3320OutBlock,기업기본정보,output;
	begin
		업종구분명                , upgubunnm       , upgubunnm       , char      , 40;
		시장구분                  , sijangcd        , sijangcd        , char      , 1;
		시장구분명                , marketnm        , marketnm        , char      , 10;
		한글기업명                , company         , company         , char      , 100;
		본사주소                  , baddress        , baddress        , char      , 100;
		본사전화번호              , btelno          , btelno          , char      , 20;
		최근결산년도              , gsyyyy          , gsyyyy          , char      , 4;
		결산월                    , gsmm            , gsmm            , char      , 2;
		최근결산년월              , gsym            , gsym            , char      , 6;
		주당액면가                , lstprice        , lstprice        , long      , 12;
		주식수                    , gstock          , gstock          , long      , 12;
		Homepage                  , homeurl         , homeurl         , char      , 50;
		그룹명                    , grdnm           , grdnm           , char      , 30;
		외국인                    , foreignratio    , foreignratio    , double    , 6.2;
		주담전화                  , irtel           , irtel           , char      , 30;
		자본금                    , capital         , capital         , double    , 12;
		시가총액                  , sigavalue       , sigavalue       , double    , 12;
		배당금                    , cashsis         , cashsis         , double    , 12;
		배당수익율                , cashrate        , cashrate        , double    , 13.2;
		현재가                    , price           , price           , long      , 8;
		전일종가                  , jnilclose       , jnilclose       , long      , 8;
		위험고지구분1_정리매매    , notice1         , notice1         , char      , 1;
		위험고지구분2_투자위험    , notice2         , notice2         , char      , 1;
		위험고지구분3_단기과열    , notice3         , notice3         , char      , 1;
	end
	t3320OutBlock1,기업재무정보,output;
	begin
		기업코드                  , gicode          , gicode          , char      , 7;
		결산년월                  , gsym            , gsym            , char      , 6;
		결산구분                  , gsgb            , gsgb            , char      , 1;
		PER                       , per             , per             , double    , 13.2;
		EPS                       , eps             , eps             , double    , 13;
		PBR                       , pbr             , pbr             , double    , 13.2;
		ROA                       , roa             , roa             , double    , 13.2;
		ROE                       , roe             , roe             , double    , 13.2;
		EBITDA                    , ebitda          , ebitda          , double    , 13.2;
		EVEBITDA                  , evebitda        , evebitda        , double    , 13.2;
		액면가                    , par             , par             , double    , 13.2;
		SPS                       , sps             , sps             , double    , 13.2;
		CPS                       , cps             , cps             , double    , 13.2;
		BPS                       , bps             , bps             , double    , 13;
		T.PER                     , t_per           , t_per           , double    , 13.2;
		T.EPS                     , t_eps           , t_eps           , double    , 13;
		PEG                       , peg             , peg             , double    , 13.2;
		T.PEG                     , t_peg           , t_peg           , double    , 13.2;
		최근분기년도              , t_gsym          , t_gsym          , char      , 6;
	end
	END_DATA_MAP
END_FUNCTION_MAP
