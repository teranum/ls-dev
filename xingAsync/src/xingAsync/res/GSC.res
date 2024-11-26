BEGIN_FUNCTION_MAP
.Feed, 해외주식 체결(GSC), GSC, attr, svr=OVS, key=18, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
        종목코드,       keysymbol,   keysymbol,    char,   	18;
    end
    OutBlock,출력,output;
    begin
        종목코드   ,       symbol,      symbol    , char   ,  16;
		체결일자(현지)   , ovsdate    , ovsdate   , char   ,   8;
		체결일자(한국)   , kordate    , kordate   , char   ,   8;
		체결시간(현지)   , trdtm      , trdtm     , char   ,   6;
		체결시간(한국)   , kortm      , kortm     , char   ,   6;
		전일대비구분     , sign		  , sign	  , char   ,   1;
		체결가격         , price      , price     , double ,   15.6;
		전일대비         , diff       , diff      , double ,   15.6;
		등락율			 , rate       ,	rate      ,	float  ,	6.2;
		시가			 , open		  , open	  , double ,   15.6;
		고가			 , high		  , high	  , double ,   15.6;
		저가			 , low 		  , low 	  , double ,   15.6;
		건별체결수량     , trdq       , trdq      , long   ,  10;
		누적체결수량     , totq       , totq      , char   ,  15;
		체결구분		 , cgubun     , cgubun    , char   ,   1;
		초당시퀀스	     , lSeq	      , lSeq	  , char   ,   3;
		누적거래대금     , amount     , amount    , char   ,  16;
		52주고가		 , high52p	  , high52p	  , double ,   15.6;
		52주저가		 , low52p 	  , low52p 	  , double ,   15.6;
    end
    END_DATA_MAP
END_FUNCTION_MAP
