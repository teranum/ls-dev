BEGIN_FUNCTION_MAP
.Func, �ֽĽð��뺰ü����ȸ2(t8454), t8454, attr, block, headtype=A;
	BEGIN_DATA_MAP
	t8454InBlock,�⺻�Է�,input;
	begin
		�����ڵ�            , shcode           , shcode           , char             , 6;
		Ư�̰ŷ���          , cvolume          , cvolume          , long             , 12;
		���۽ð�            , starttime        , starttime        , char             , 4;
		����ð�            , endtime          , endtime          , char             , 4;
		�ð�CTS             , cts_time         , cts_time         , char             , 10;
		�ŷ��ұ����ڵ�      , exchgubun        , exchgubun        , char             , 1;
	end
	t8454OutBlock,���,output;
	begin
		�ð�CTS             , cts_time         , cts_time         , char             , 10;
		�ŷ��Һ������ڵ�    , ex_shcode        , ex_shcode        , char             , 10;
	end
	t8454OutBlock1,���1,output,occurs;
	begin
		�ð�                , chetime          , chetime          , char             , 10;
		���簡              , price            , price            , long             , 8;
		���ϴ�񱸺�        , sign             , sign             , char             , 1;
		���ϴ��            , change           , change           , long             , 8;
		�����              , diff             , diff             , double           , 6.2;
		ü�����            , cvolume          , cvolume          , long             , 12;
		ü�ᰭ��            , chdegree         , chdegree         , double           , 8.2;
		�ŷ���              , volume           , volume           , long             , 12;
		�ŵ�ü�����        , mdvolume         , mdvolume         , long             , 12;
		�ŵ�ü��Ǽ�        , mdchecnt         , mdchecnt         , long             , 8;
		�ż�ü�����        , msvolume         , msvolume         , long             , 12;
		�ż�ü��Ǽ�        , mschecnt         , mschecnt         , long             , 8;
		��ü�ᷮ            , revolume         , revolume         , long             , 12;
		��ü��Ǽ�          , rechecnt         , rechecnt         , long             , 8;
		�ŷ��Ҹ�            , exchname         , exchname         , char             , 3;
	end
	END_DATA_MAP
END_FUNCTION_MAP
