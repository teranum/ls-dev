BEGIN_FUNCTION_MAP
.Feed, �ؿܼ���ü��, TC3, block, key=7, group=1;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
    end
    OutBlock,���,output;
    begin
		�����Ϸù�ȣ,  	lineseq,    lineseq,	long,   10;
		KEY,		    key,		key,		char,	11;
		������ID,		user,	    user,	   	char,	 8;

        ����ID,           svc_id,                  svc_id,                char,    4;
        �ֹ�����,           ordr_dt,                 ordr_dt,               char,    8;
        ������ȣ,           brn_cd,                  brn_cd,                char,    3;
        �ֹ���ȣ,           ordr_no,                 ordr_no,               long,    10;
        ���ֹ���ȣ,         orgn_ordr_no,            orgn_ordr_no,          long,    10;
        ���ֹ���ȣ,         mthr_ordr_no,            mthr_ordr_no,          long,    10;
        ���¹�ȣ,           ac_no,                   ac_no,                 char,    11;
        �����ڵ�,           is_cd,                   is_cd,                 char,    30;
        �ŵ��ż�����,       s_b_ccd,                 s_b_ccd,               char,    1;
        �����������,       ordr_ccd,                ordr_ccd,              char,    1;
        ü�����,           ccls_q,                  ccls_q,                long,    15;
        ü�ᰡ��,           ccls_prc,                ccls_prc,              double,  18.11;
        ü���ȣ,           ccls_no,                 ccls_no,               char,    10;
        ü��ð�,           ccls_tm,                 ccls_tm,               char,    9;
        ������մܰ�,       avg_byng_uprc,           avg_byng_uprc,         double,  18.11;
        ���Աݾ�,           byug_amt,                byug_amt,              double,  25.8;
        û�����,           clr_pl_amt,              clr_pl_amt,            double,  19.2;
        ��Ź������,         ent_fee,                 ent_fee,               double,  19.2;
        �����ܰ����,       fcm_fee,                 fcm_fee,               long,    19;
        �����ID,           userid,                  userid,                char,    8;
        ���簡��,           now_prc,                 now_prc,               double,  18.11;
        ��ȭ�ڵ�,           crncy_cd,                crncy_cd,              char,    3;
        ��������,           mtrt_dt,                 mtrt_dt,               char,    8;
        �ֹ���ǰ�����ڵ�,   ord_prdt_tp_code,        ord_prdt_tp_code,      char,    1;
        �ֹ���ǰ�����ڵ�,   exec_prdt_tp_code,       exec_prdt_tp_code,     char,    1;
        �����������񿩺�,   sprd_base_isu_yn,        sprd_base_isu_yn,      char,    1;
        ü������,           ccls_dt,                 ccls_dt,               char,    8;
        FILLER2,            filler2,                 filler2,               char,    30;
        �������������ڵ�,   sprd_is_cd,              sprd_is_cd,            char,    30;
        LME��ǰ����,        lme_prdt_ccd,            lme_prdt_ccd,          char,    1;
        LME�������尡��,    lme_sprd_prc,            lme_sprd_prc,          double,  18.11;
        �������簡��,       last_now_prc,            last_now_prc,          double,  18.11;
        ������������,       bf_mtrt_dt,              bf_mtrt_dt,            char,    8
        û�����,           clr_q,                   clr_q,                 long,    15;
        ����ȯ��,           base_xchrat,             base_xchrat,           double,  10.4;
        ȯ�������ݾ�,       mxchg_unit_amt,          mxchg_unit_amt,        long,    15;
        ��ȭȯ���򰡼���,   krw_conv_eval_pnl_amt,   krw_conv_eval_pnl_amt, double,  19.2;
        �򰡼���,       	eval_pnl_amt,            eval_pnl_amt,          long,    19;
    end
    END_DATA_MAP
END_FUNCTION_MAP
