BEGIN_FUNCTION_MAP
.Feed, 해외주식주문접수(미국), AS0, key=8, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
    end
    OutBlock,출력,output;
    begin
		라인일련번호       , lineseq          , lineseq          , long  , 10;
		계좌번호           , accno            , accno            , char  , 11;
		조작자ID           , user             , user             , char  , 8; 
		헤더길이           , len              , len              , long  , 6; 
		헤더구분           , gubun            , gubun            , char  , 1; 
		압축구분           , compress         , compress         , char  , 1; 
		암호구분           , encrypt          , encrypt          , char  , 1; 
		공통시작지점       , offset           , offset           , long  , 3; 
		TRCODE             , trcode           , trcode           , char  , 8; 
		이용사번호         , comid            , comid            , char  , 3; 
		사용자ID           , userid           , userid           , char  , 16;
		접속매체           , media            , media            , char  , 2; 
		I/F일련번호        , ifid             , ifid             , char  , 3; 
		전문일련번호       , seq              , seq              , char  , 9; 
		TR추적ID           , trid             , trid             , char  , 16;
		공인IP             , pubip            , pubip            , char  , 12;
		사설IP             , prvip            , prvip            , char  , 12;
		처리지점번호       , pcbpno           , pcbpno           , char  , 3; 
		지점번호           , bpno             , bpno             , char  , 3; 
		단말번호           , termno           , termno           , char  , 8; 
		언어구분           , lang             , lang             , char  , 1; 
		AP처리시간         , proctm           , proctm           , long  , 9; 
		메세지코드         , msgcode          , msgcode          , char  , 4; 
		메세지출력구분     , outgu            , outgu            , char  , 1; 
		압축요청구분       , compreq          , compreq          , char  , 1; 
		기능키             , funckey          , funckey          , char  , 4; 
		요청레코드개수     , reqcnt           , reqcnt           , long  , 4; 
		예비영역           , filler           , filler           , char  , 6; 
		연속구분           , cont             , cont             , char  , 1; 
		연속키값           , contkey          , contkey          , char  , 18;
		가변시스템길이     , varlen           , varlen           , long  , 2; 
		가변해더길이       , varhdlen         , varhdlen         , long  , 2; 
		가변메시지길이     , varmsglen        , varmsglen        , long  , 2; 
		조회발원지         , trsrc            , trsrc            , char  , 1; 
		I/F이벤트ID        , eventid          , eventid          , char  , 4; 
		I/F정보            , ifinfo           , ifinfo           , char  , 4; 
		예비영역           , filler1          , filler1          , char  , 41;
		주문체결유형코드   , sOrdxctPtnCode   ,	sOrdxctPtnCode   , char  , 2; 
		주문시장코드       , sOrdMktCode      ,	sOrdMktCode      , char  , 2; 
		주문유형코드       , sOrdPtnCode      ,	sOrdPtnCode      , char  , 2; 
		원주문번호         , sOrgOrdNo        ,	sOrgOrdNo        , long  , 10;
		계좌번호           , sAcntNo          ,	sAcntNo          , char  , 20;
		비밀번호           , sPwd             ,	sPwd             , char  , 8; 
		종목번호           , sIsuNo           ,	sIsuNo           , char  , 12;
		단축종목번호       , sShtnIsuNo       ,	sShtnIsuNo       , char  , 9;	
		종목명             , sIsuNm           ,	sIsuNm           , char  , 40;
		주문수량           , sOrdQty          ,	sOrdQty          , double, 16;
		주문가             , sOrdPrc          ,	sOrdPrc          , double, 13;
		주문조건           , sOrdCndi         ,	sOrdCndi         , char	 , 1;	
		호가유형코드       , sOrdprcPtnCode   ,	sOrdprcPtnCode   , char	 , 2;	
		전략코드           , sStrtgCode       ,	sStrtgCode       , long	 , 6;	
		그룹ID             , sGrpId           ,	sGrpId           , char	 , 20;
		주문회차           , sOrdSeqno        ,	sOrdSeqno        , char	 , 10;
		통신매체코드       , sCommdaCode      ,	sCommdaCode      , char	 , 2;	
		주문번호           , sOrdNo           ,	sOrdNo           , char	 , 10;
		주문시각           , sOrdTime         ,	sOrdTime         , char	 , 9;	
		모주문번호         , sPrntOrdNo       ,	sPrntOrdNo       , char	 , 10;
		원주문미체결수량   , sOrgOrdUnercQty  ,	sOrgOrdUnercQty  , char	 , 16;
		원주문정정수량     , sOrgOrdMdfyQty   ,	sOrgOrdMdfyQty   , double, 16;
		원주문취소수량     , sOrgOrdCancQty   ,	sOrgOrdCancQty   , double, 16;
		비회원사송신번호   , sNmcpySndNo      ,	sNmcpySndNo      , double, 10;
		주문금액           , sOrdAmt          ,	sOrdAmt          , double, 16;
		매매구분           , sBnsTp           ,	sBnsTp           , long	 , 1;	
		복수주문일련번호   , sMtiordSeqno     ,	sMtiordSeqno     , long	 , 10;
		주문사원번호       , sOrdUserId       ,	sOrdUserId       , double, 16;
		실물주문수량       , sSpotOrdQty      ,	sSpotOrdQty      , double, 16;
		재사용주문수량     , sRuseOrdQty      ,	sRuseOrdQty      , double, 16;
		주문현금           , sOrdMny          ,	sOrdMny          , double, 16;
		주문대용금액       , sOrdSubstAmt     ,	sOrdSubstAmt     , double, 16;
		주문재사용금액     , sOrdRuseAmt      ,	sOrdRuseAmt      , double, 16;
		사용수수료         , sUseCmsnAmt      ,	sUseCmsnAmt      , double, 16;
		잔고수량           , sSecBalQty       ,	sSecBalQty       , double, 16;
		실물주문가능수량   , sSpotOrdAbleQty  ,	sSpotOrdAbleQty  , double, 16;
		주문가능재사용수량 , sOrdAbleRuseQty  ,	sOrdAbleRuseQty  , double, 16;
		변동수량           , sFlctQty         ,	sFlctQty         , double, 16;
		잔고수량(D2)       , sSecBalQtyD2     ,	sSecBalQtyD2     , double, 16;
		매도주문가능수량   , sSellAbleQty     ,	sSellAbleQty     , double, 16;
		미체결매도주문수량 , sUnercSellOrdQty ,	sUnercSellOrdQty , double, 16;
		평균매입가         , sAvrPchsPrc      ,	sAvrPchsPrc      , double, 13;
		매입금액           , sPchsAmt         ,	sPchsAmt         , double, 16;
		예수금             , sDeposit         ,	sDeposit         , double, 16;
		대용금             , sSubstAmt        ,	sSubstAmt        , double, 16;
		위탁현금증거금액   , sCsgnMnyMgn      ,	sCsgnMnyMgn      , double, 16;
		위탁대용증거금액   , sCsgnSubstMgn    ,	sCsgnSubstMgn    , double, 16;
		주문가능현금       , sOrdAbleMny      ,	sOrdAbleMny      , double, 16;
		주문가능대용금액   , sOrdAbleSubstAmt ,	sOrdAbleSubstAmt , double, 16;
		재사용가능금액     , sRuseAbleAmt     ,	sRuseAbleAmt     , double, 16;
		신용거래코드       , sMgntrnCode      ,	sMgntrnCode      , char  , 3;
    end
    END_DATA_MAP
END_FUNCTION_MAP
