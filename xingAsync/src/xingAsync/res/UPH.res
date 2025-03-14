BEGIN_FUNCTION_MAP
.Feed, KRX+NXT통합 프로그램매매 종목별(뉴스/검색 겸용)(UPH), UPH, attr, key=10, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
        거래소별단축코드,           ex_shcode,      ex_shcode,  char,   10;
    end
    OutBlock,출력,output;
    begin
        수신시간,                   time,           time,       char,   6;

        현재가,                     price,          price,      long,   8;
        전일대비구분,               sign,           sign,       long,   1;
        전일대비,                   change,         change,     long,   8;
        누적거래량,                 volume,         volume,     long,   10;
        등락율,                     drate,          drate,      float,  6.2;

        차익매도호가 잔량,          cdhrem,         cdhrem,     long,   12;
        차익매수호가 잔량,          cshrem,         cshrem,     long,   12;
        비차익매도호가 잔량,        bdhrem,         bdhrem,     long,   12;
        비차익매수호가 잔량,        bshrem,         bshrem,     long,   12;

        차익매도호가 수량,          cdhvolume,      cdhvolume,  long,   12;
        차익매수호가 수량,          cshvolume,      cshvolume,  long,   12;
        비차익매도호가 수량,        bdhvolume,      bdhvolume,  long,   12;
        비차익매수호가 수량,        bshvolume,      bshvolume,  long,   12;

        전체매도위탁체결수량,       dwcvolume,      dwcvolume,  long,   12;
        전체매수위탁체결수량,       swcvolume,      swcvolume,  long,   12;
        전체매도자기체결수량,       djcvolume,      djcvolume,  long,   12;
        전체매수자기체결수량,       sjcvolume,      sjcvolume,  long,   12;

        전체매도체결수량,           tdvolume,       tdvolume,   long,   12;
        전체매수체결수량,           tsvolume,       tsvolume,   long,   12;
        전체순매수 수량,            tvol,           tvol,       long,   12;

        전체매도위탁체결금액,       dwcvalue,       dwcvalue,   long,   15;
        전체매수위탁체결금액,       swcvalue,       swcvalue,   long,   15;
        전체매도자기체결금액,       djcvalue,       djcvalue,   long,   15;
        전체매수자기체결금액,       sjcvalue,       sjcvalue,   long,   15;

        전체매도체결금액,           tdvalue,        tdvalue,    long,   15;
        전체매수체결금액,           tsvalue,        tsvalue,    long,   15;
        전체순매수 금액,            tval,           tval,       long,   15;

        매도 사전공시수량,          pdgvolume,      pdgvolume,  long,   12;
        매수 사전공시수량,          psgvolume,      psgvolume,  long,   12;

        종목코드,                   shcode,         shcode,     char,   9;
		거래소별단축코드,           ex_shcode,      ex_shcode,  char,   10;
    end
    END_DATA_MAP
END_FUNCTION_MAP
