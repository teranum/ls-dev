BEGIN_FUNCTION_MAP
.Feed, NXT VI �ߵ� ����(NVI), NVI, attr, key=10, group=1;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
		�ŷ��Һ������ڵ�                                ,   ex_shcode,     ex_shcode,     char,   10;
    end
    OutBlock,���,output;
    begin
		����(0:���� 1:�����ߵ� 2:�����ߵ� 3:����&����)  ,	vi_gubun,		vi_gubun,		char,	1;
		����VI�ߵ����ذ���				                ,	svi_recprice,	svi_recprice,	long,	8;
		����VI�ߵ����ذ���				                ,	dvi_recprice,	dvi_recprice,	long,	8;
		VI�ߵ�����						                ,	vi_trgprice,	vi_trgprice,	long,	8;
		�����ڵ�						                ,	shcode,			shcode,			char,	9;
		�����ڵ�(�̻��)				                ,	ref_shcode,		ref_shcode,		char,	6;
		�ð�							                ,	time,			time,			char,	6;
		�ŷ��Ҹ�                                        ,   exchname,       exchname,       char,   3;  // KRX NXT
		�ŷ��Һ������ڵ�                                ,   ex_shcode,      ex_shcode,      char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
