BEGIN_FUNCTION_MAP
.Func, ����/�ɼ����簡(�ü�)��ȸ(t2101), t2101, attr, block, headtype=A;
	BEGIN_DATA_MAP
	t2101InBlock,�⺻�Է�,input;
	begin
		�����ڵ�                                                      , focode            , focode            , char      , 8;
	end
	t2101OutBlock,���,output;
	begin
		�ѱ۸�                                                        , hname             , hname             , char      , 20;
		���簡                                                        , price             , price             , double    , 6.2;
		���ϴ�񱸺�                                                  , sign              , sign              , char      , 1;
		���ϴ��                                                      , change            , change            , double    , 6.2;
		��������                                                      , jnilclose         , jnilclose         , double    , 6.2;
		�����                                                        , diff              , diff              , double    , 6.2;
		�ŷ���                                                        , volume            , volume            , long      , 12;
		�ŷ����                                                      , value             , value             , long      , 12;
		�̰�����                                                      , mgjv              , mgjv              , long      , 8;
		�̰�������                                                    , mgjvdiff          , mgjvdiff          , long      , 8;
		�ð�                                                          , open              , open              , double    , 6.2;
		��                                                          , high              , high              , double    , 6.2;
		����                                                          , low               , low               , double    , 6.2;
		���Ѱ�                                                        , uplmtprice        , uplmtprice        , double    , 6.2;
		���Ѱ�                                                        , dnlmtprice        , dnlmtprice        , double    , 6.2;
		52�ְ�                                                      , high52w           , high52w           , double    , 6.2;
		52������                                                      , low52w            , low52w            , double    , 6.2;
		���̽ý�                                                      , basis             , basis             , double    , 6.2;
		���ذ�                                                        , recprice          , recprice          , double    , 6.2;
		�̷а�                                                        , theoryprice       , theoryprice       , double    , 6.2;
		������                                                        , glyl              , glyl              , double    , 6.3;
		CB���Ѱ�                                                      , cbhprice          , cbhprice          , double    , 6.2;
		CB���Ѱ�                                                      , cblprice          , cblprice          , double    , 6.2;
		������                                                        , lastmonth         , lastmonth         , char      , 8;
		�ܿ���                                                        , jandatecnt        , jandatecnt        , long      , 8;
		��������                                                      , pricejisu         , pricejisu         , double    , 6.2;
		�����������ϴ�񱸺�                                          , jisusign          , jisusign          , char      , 1;
		�����������ϴ��                                              , jisuchange        , jisuchange        , double    , 6.2;
		�������������                                                , jisudiff          , jisudiff          , double    , 6.2;
		KOSPI200����                                                  , kospijisu         , kospijisu         , double    , 6.2;
		KOSPI200���ϴ�񱸺�                                          , kospisign         , kospisign         , char      , 1;
		KOSPI200���ϴ��                                              , kospichange       , kospichange       , double    , 6.2;
		KOSPI200�����                                                , kospidiff         , kospidiff         , double    , 6.2;
		�����ְ�                                                    , listhprice        , listhprice        , double    , 6.2;
		����������                                                    , listlprice        , listlprice        , double    , 6.2;
		��Ÿ                                                          , delt              , delt              , double    , 6.4;
		����                                                          , gama              , gama              , double    , 6.4;
		��Ÿ                                                          , ceta              , ceta              , double    , 6.4;
		����                                                          , vega              , vega              , double    , 6.4;
		�ο�                                                          , rhox              , rhox              , double    , 6.4;
		�ٿ������簡                                                  , gmprice           , gmprice           , double    , 6.2;
		�ٿ������ϴ�񱸺�                                            , gmsign            , gmsign            , char      , 1;
		�ٿ������ϴ��                                                , gmchange          , gmchange          , double    , 6.2;
		�ٿ��������                                                  , gmdiff            , gmdiff            , double    , 6.2;
		�̷а�                                                        , theorypriceg      , theorypriceg      , double    , 6.2;
		������������                                                  , histimpv          , histimpv          , double    , 6.2;
		���纯����                                                    , impv              , impv              , double    , 6.2;
		����BASIS                                                     , sbasis            , sbasis            , double    , 6.2;
		�̷�BASIS                                                     , ibasis            , ibasis            , double    , 6.2;
		�ٿ��������ڵ�                                                , gmfutcode         , gmfutcode         , char      , 8;
		��簡                                                        , actprice          , actprice          , double    , 6.2;
		�ŷ��ҹΰ������Žð�                                          , greeks_time       , greeks_time       , char      , 6;
		�ŷ��ҹΰ���Ȯ������                                          , greeks_confirm    , greeks_confirm    , char      , 8;
		���ϰ�ȣ������                                                , danhochk          , danhochk          , char      , 1;
		����ü�ᰡ                                                    , yeprice           , yeprice           , double    , 6.2;
		����ü�ᰡ����������񱸺�                                    , jnilysign         , jnilysign         , char      , 1;
		����ü�ᰡ�����������                                        , jnilychange       , jnilychange       , double    , 6.2;
		����ü�ᰡ�������������                                      , jnilydrate        , jnilydrate        , double    , 6.2;
		��б���(1:��а���2:�������0:�̹߻�)                        , alloc_gubun       , alloc_gubun       , char      , 1;
		�ܿ���(������)                                                , bjandatecnt       , bjandatecnt       , long      , 8;
		�����ڵ�                                                      , focode            , focode            , char      , 8;
		�ǽð��������ѿ���(0:���ƴ�1:������2:��������3:�Ͻ�����)    , dy_gubun          , dy_gubun          , char      , 1;
		�ǽð����Ѱ�                                                  , dy_uplmtprice     , dy_uplmtprice     , double    , 6.2;
		�ǽð����Ѱ�                                                  , dy_dnlmtprice     , dy_dnlmtprice     , double    , 6.2;
		����������Ȯ��(0:��Ȯ��1:Ȯ��2:���ƴ�)                      , updnstep_gubun    , updnstep_gubun    , char      , 1;
		��������ܰ�                                                  , upstep            , upstep            , char      , 2;
		��������ܰ�                                                  , dnstep            , dnstep            , char      , 2;
		3�ܰ���Ѱ�                                                   , uplmtprice_3rd    , uplmtprice_3rd    , double    , 6.2;
		3�ܰ����Ѱ�                                                   , dnlmtprice_3rd    , dnlmtprice_3rd    , double    , 6.2;
		����ü�����                                                  , expct_ccls_q      , expct_ccls_q      , long      , 9;
	end
	END_DATA_MAP
END_FUNCTION_MAP
