BEGIN_FUNCTION_MAP
    .Feed, KRX+NXT���� VI �ߵ�/����, UVI, attr, key=10, group=1;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
        �ŷ��Һ������ڵ�                                    ,   ex_shcode,       ex_shcode,         char,   10;
    end
    OutBlock,���,output;
    begin
        KRXVI����(0:���� 1:�����ߵ� 2:�����ߵ� 3:����&����) ,   krx_vi_gubun,     krx_vi_gubun,       char,   1;
        KRX����VI�ߵ����ذ���                               ,   krx_svi_recprice, krx_svi_recprice,   long,   8;
        KRX����VI�ߵ����ذ���                               ,   krx_dvi_recprice, krx_dvi_recprice,   long,   8;
        KRXVI�ߵ�����                                       ,   krx_vi_trgprice,  krx_vi_trgprice,    long,   8;
        KRX�ð�                                             ,   krx_time,         krx_time,           char,   6;
        NXTVI����(0:���� 1:�����ߵ� 2:�����ߵ� 3:����&����) ,   nxt_vi_gubun,     nxt_vi_gubun,       char,   1;
        NXT����VI�ߵ����ذ���                               ,   nxt_svi_recprice, nxt_svi_recprice,   long,   8;
        NXT����VI�ߵ����ذ���                               ,   nxt_dvi_recprice, nxt_dvi_recprice,   long,   8;
        NXTVI�ߵ�����                                       ,   nxt_vi_trgprice,  nxt_vi_trgprice,    long,   8;
        NXT�ð�                                             ,   nxt_time,         nxt_time,           char,   6;
        �����ڵ�                                            ,   shcode,           shcode,             char,   9;
        �����ڵ�(�̻��)                                    ,   ref_shcode,       ref_shcode,         char,   6;
        �ŷ��Ҹ�                                            ,   exchname,         exchname,           char,   3;   // KRX NXT
        �ŷ��Һ������ڵ�                                    ,   ex_shcode,        ex_shcode,          char,   10;
    end 
    END_DATA_MAP
END_FUNCTION_MAP
