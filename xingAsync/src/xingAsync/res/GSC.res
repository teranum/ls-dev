BEGIN_FUNCTION_MAP
.Feed, �ؿ��ֽ� ü��(GSC), GSC, attr, svr=OVS, key=18, group=1;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
        �����ڵ�,       keysymbol,   keysymbol,    char,   	18;
    end
    OutBlock,���,output;
    begin
        �����ڵ�   ,       symbol,      symbol    , char   ,  16;
		ü������(����)   , ovsdate    , ovsdate   , char   ,   8;
		ü������(�ѱ�)   , kordate    , kordate   , char   ,   8;
		ü��ð�(����)   , trdtm      , trdtm     , char   ,   6;
		ü��ð�(�ѱ�)   , kortm      , kortm     , char   ,   6;
		���ϴ�񱸺�     , sign		  , sign	  , char   ,   1;
		ü�ᰡ��         , price      , price     , double ,   15.6;
		���ϴ��         , diff       , diff      , double ,   15.6;
		�����			 , rate       ,	rate      ,	float  ,	6.2;
		�ð�			 , open		  , open	  , double ,   15.6;
		��			 , high		  , high	  , double ,   15.6;
		����			 , low 		  , low 	  , double ,   15.6;
		�Ǻ�ü�����     , trdq       , trdq      , long   ,  10;
		����ü�����     , totq       , totq      , char   ,  15;
		ü�ᱸ��		 , cgubun     , cgubun    , char   ,   1;
		�ʴ������	     , lSeq	      , lSeq	  , char   ,   3;
		�����ŷ����     , amount     , amount    , char   ,  16;
		52�ְ�		 , high52p	  , high52p	  , double ,   15.6;
		52������		 , low52p 	  , low52p 	  , double ,   15.6;
    end
    END_DATA_MAP
END_FUNCTION_MAP
