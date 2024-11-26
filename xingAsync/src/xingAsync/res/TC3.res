BEGIN_FUNCTION_MAP
.Feed, 해외선물체결, TC3, block, key=7, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
    end
    OutBlock,출력,output;
    begin
		라인일련번호,  	lineseq,    lineseq,	long,   10;
		KEY,		    key,		key,		char,	11;
		조작자ID,		user,	    user,	   	char,	 8;

        서비스ID,           svc_id,                  svc_id,                char,    4;
        주문일자,           ordr_dt,                 ordr_dt,               char,    8;
        지점번호,           brn_cd,                  brn_cd,                char,    3;
        주문번호,           ordr_no,                 ordr_no,               long,    10;
        원주문번호,         orgn_ordr_no,            orgn_ordr_no,          long,    10;
        모주문번호,         mthr_ordr_no,            mthr_ordr_no,          long,    10;
        계좌번호,           ac_no,                   ac_no,                 char,    11;
        종목코드,           is_cd,                   is_cd,                 char,    30;
        매도매수유형,       s_b_ccd,                 s_b_ccd,               char,    1;
        정정취소유형,       ordr_ccd,                ordr_ccd,              char,    1;
        체결수량,           ccls_q,                  ccls_q,                long,    15;
        체결가격,           ccls_prc,                ccls_prc,              double,  18.11;
        체결번호,           ccls_no,                 ccls_no,               char,    10;
        체결시간,           ccls_tm,                 ccls_tm,               char,    9;
        매입평균단가,       avg_byng_uprc,           avg_byng_uprc,         double,  18.11;
        매입금액,           byug_amt,                byug_amt,              double,  25.8;
        청산손익,           clr_pl_amt,              clr_pl_amt,            double,  19.2;
        위탁수수료,         ent_fee,                 ent_fee,               double,  19.2;
        매입잔고수량,       fcm_fee,                 fcm_fee,               long,    19;
        사용자ID,           userid,                  userid,                char,    8;
        현재가격,           now_prc,                 now_prc,               double,  18.11;
        통화코드,           crncy_cd,                crncy_cd,              char,    3;
        만기일자,           mtrt_dt,                 mtrt_dt,               char,    8;
        주문상품구분코드,   ord_prdt_tp_code,        ord_prdt_tp_code,      char,    1;
        주문상품구분코드,   exec_prdt_tp_code,       exec_prdt_tp_code,     char,    1;
        스프레드종목여부,   sprd_base_isu_yn,        sprd_base_isu_yn,      char,    1;
        체결일자,           ccls_dt,                 ccls_dt,               char,    8;
        FILLER2,            filler2,                 filler2,               char,    30;
        스프레드종목코드,   sprd_is_cd,              sprd_is_cd,            char,    30;
        LME상품유형,        lme_prdt_ccd,            lme_prdt_ccd,          char,    1;
        LME스프레드가격,    lme_sprd_prc,            lme_sprd_prc,          double,  18.11;
        최종현재가격,       last_now_prc,            last_now_prc,          double,  18.11;
        이전만기일자,       bf_mtrt_dt,              bf_mtrt_dt,            char,    8
        청산수량,           clr_q,                   clr_q,                 long,    15;
        기준환율,           base_xchrat,             base_xchrat,           double,  10.4;
        환전단위금액,       mxchg_unit_amt,          mxchg_unit_amt,        long,    15;
        원화환산평가손익,   krw_conv_eval_pnl_amt,   krw_conv_eval_pnl_amt, double,  19.2;
        평가손익,       	eval_pnl_amt,            eval_pnl_amt,          long,    19;
    end
    END_DATA_MAP
END_FUNCTION_MAP
