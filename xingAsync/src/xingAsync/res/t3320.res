BEGIN_FUNCTION_MAP
.Func, FNG_���(t3320), t3320, attr, block, headtype=A;
	BEGIN_DATA_MAP
	t3320InBlock,�⺻�Է�,input;
	begin
		�����ڵ�                  , gicode          , gicode          , char      , 7;
	end
	t3320OutBlock,����⺻����,output;
	begin
		�������и�                , upgubunnm       , upgubunnm       , char      , 40;
		���屸��                  , sijangcd        , sijangcd        , char      , 1;
		���屸�и�                , marketnm        , marketnm        , char      , 10;
		�ѱ۱����                , company         , company         , char      , 100;
		�����ּ�                  , baddress        , baddress        , char      , 100;
		������ȭ��ȣ              , btelno          , btelno          , char      , 20;
		�ֱٰ��⵵              , gsyyyy          , gsyyyy          , char      , 4;
		����                    , gsmm            , gsmm            , char      , 2;
		�ֱٰ����              , gsym            , gsym            , char      , 6;
		�ִ�׸鰡                , lstprice        , lstprice        , long      , 12;
		�ֽļ�                    , gstock          , gstock          , long      , 12;
		Homepage                  , homeurl         , homeurl         , char      , 50;
		�׷��                    , grdnm           , grdnm           , char      , 30;
		�ܱ���                    , foreignratio    , foreignratio    , double    , 6.2;
		�ִ���ȭ                  , irtel           , irtel           , char      , 30;
		�ں���                    , capital         , capital         , double    , 12;
		�ð��Ѿ�                  , sigavalue       , sigavalue       , double    , 12;
		����                    , cashsis         , cashsis         , double    , 12;
		��������                , cashrate        , cashrate        , double    , 13.2;
		���簡                    , price           , price           , long      , 8;
		��������                  , jnilclose       , jnilclose       , long      , 8;
		�����������1_�����Ÿ�    , notice1         , notice1         , char      , 1;
		�����������2_��������    , notice2         , notice2         , char      , 1;
		�����������3_�ܱ����    , notice3         , notice3         , char      , 1;
	end
	t3320OutBlock1,����繫����,output;
	begin
		����ڵ�                  , gicode          , gicode          , char      , 7;
		�����                  , gsym            , gsym            , char      , 6;
		��걸��                  , gsgb            , gsgb            , char      , 1;
		PER                       , per             , per             , double    , 13.2;
		EPS                       , eps             , eps             , double    , 13;
		PBR                       , pbr             , pbr             , double    , 13.2;
		ROA                       , roa             , roa             , double    , 13.2;
		ROE                       , roe             , roe             , double    , 13.2;
		EBITDA                    , ebitda          , ebitda          , double    , 13.2;
		EVEBITDA                  , evebitda        , evebitda        , double    , 13.2;
		�׸鰡                    , par             , par             , double    , 13.2;
		SPS                       , sps             , sps             , double    , 13.2;
		CPS                       , cps             , cps             , double    , 13.2;
		BPS                       , bps             , bps             , double    , 13;
		T.PER                     , t_per           , t_per           , double    , 13.2;
		T.EPS                     , t_eps           , t_eps           , double    , 13;
		PEG                       , peg             , peg             , double    , 13.2;
		T.PEG                     , t_peg           , t_peg           , double    , 13.2;
		�ֱٺб�⵵              , t_gsym          , t_gsym          , char      , 6;
	end
	END_DATA_MAP
END_FUNCTION_MAP
