BEGIN_FUNCTION_MAP
    .Feed, KRX+NXT통합 VI 발동/해제, UVI, attr, key=10, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
        거래소별단축코드                                    ,   ex_shcode,       ex_shcode,         char,   10;
    end
    OutBlock,출력,output;
    begin
        KRXVI구분(0:해제 1:정적발동 2:동적발동 3:정적&동적) ,   krx_vi_gubun,     krx_vi_gubun,       char,   1;
        KRX정적VI발동기준가격                               ,   krx_svi_recprice, krx_svi_recprice,   long,   8;
        KRX동적VI발동기준가격                               ,   krx_dvi_recprice, krx_dvi_recprice,   long,   8;
        KRXVI발동가격                                       ,   krx_vi_trgprice,  krx_vi_trgprice,    long,   8;
        KRX시간                                             ,   krx_time,         krx_time,           char,   6;
        NXTVI구분(0:해제 1:정적발동 2:동적발동 3:정적&동적) ,   nxt_vi_gubun,     nxt_vi_gubun,       char,   1;
        NXT정적VI발동기준가격                               ,   nxt_svi_recprice, nxt_svi_recprice,   long,   8;
        NXT동적VI발동기준가격                               ,   nxt_dvi_recprice, nxt_dvi_recprice,   long,   8;
        NXTVI발동가격                                       ,   nxt_vi_trgprice,  nxt_vi_trgprice,    long,   8;
        NXT시간                                             ,   nxt_time,         nxt_time,           char,   6;
        단축코드                                            ,   shcode,           shcode,             char,   9;
        참조코드(미사용)                                    ,   ref_shcode,       ref_shcode,         char,   6;
        거래소명                                            ,   exchname,         exchname,           char,   3;   // KRX NXT
        거래소별단축코드                                    ,   ex_shcode,        ex_shcode,          char,   10;
    end 
    END_DATA_MAP
END_FUNCTION_MAP
