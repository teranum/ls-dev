BEGIN_FUNCTION_MAP
.Feed, NXT ������ �����ں� �Ÿ���Ȳ(�����ں� �Ÿ�����) (NBM), NBM, attr, key=4, group=4;
    BEGIN_DATA_MAP
    InBlock,�Է�,input;
    begin
        �ŷ��Һ������ڵ�,           ex_upcode,      ex_upcode,  char,   4;
    end
    OutBlock,���,output;
    begin
        �������ڵ�,                 tjjcode,        tjjcode,    char,   4;
        ���Žð�,                   tjjtime,        tjjtime,    char,   8;
        �ż� �ŷ���,                msvolume,       msvolume,   long,   8;
        �ŵ� �ŷ���,                mdvolume,       mdvolume,   long,   8;
        �ŷ��� ���ż�,              msvol,          msvol,      long,   8;
        �ŷ��� ���ż� �������,     p_msvol,        p_msvol,    long,   8;
        �ż� �ŷ����,              msvalue,        msvalue,    long,   6;
        �ŵ� �ŷ����,              mdvalue,        mdvalue,    long,   6;
        �ŷ���� ���ż�,            msval,          msval,      long,   6;
        �ŷ���� ���ż� �������,   p_msval,        p_msval,    long,   6;
        �����ڵ�,                   upcode,         upcode,     char,   3;
        �ŷ��Һ������ڵ�,           ex_upcode,      ex_upcode,  char,   4;
    end
    END_DATA_MAP
END_FUNCTION_MAP
