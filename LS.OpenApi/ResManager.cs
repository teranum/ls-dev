namespace LS.OpenApi;
/// <summary>자원관리자</summary>
public class ResManager
{
    static readonly Dictionary<string, List<string>> _group = new()
    {
        ["업종"] = [
            "[업종] 시세;/indtp/market-data",
            "업종기간별추이;t1514",
            "전체업종;t8424",
            "예상지수;t1485",
            "업종현재가;t1511",
            "업종별종목시세;t1516",

            "[업종] 차트;/indtp/chart",
            "업종차트(종합);t4203",
            "업종차트(틱/n틱);t8417",
            "업종차트(N분);t8418",
            "업종차트(일주월);t8419",

            "[업종] 실시간 시세;/websocket",
            "업종별투자자별매매현황;BM_",
            ],
        ["주식"] = [
            "[주식] 시세;/stock/market-data",
            "주식현재가호가조회;t1101",
            "주식현재가(시세)조회;t1102",
            "주식현재가시세메모;t1104",
            "주식피봇/디마크조회;t1105",
            "시간외체결량;t1109",
            "주식시간대별체결조회;t1301",
            "주식분별주가조회;t1302",
            "기간별주가;t1305",
            "주식시간대별체결조회챠트;t1308",
            "주식당일전일분틱조회;t1310",
            "관리/불성실/투자유의조회;t1404",
            "투자경고/매매정지/정리매매조회;t1405",
            "초저유동성조회;t1410",
            "상/하한;t1422",
            "상/하한가직전;t1427",
            "신고/신저가;t1442",
            "가격대별매매비중조회;t1449",
            "시간대별호가잔량추이;t1471",
            "체결강도추이;t1475",
            "시간별예상체결가;t1486",
            "예상체결가등락율상위조회;t1488",
            "API용주식멀티현재가조회;t8407",
            "주식마스터조회API용;t9945",

            "[주식] 거래원;/stock/exchange",
            "종목별상위회원사;t1752",
            "회원사리스트;t1764",
            "종목별회원사추이;t1771",

            "[주식] 투자정보;/stock/investinfo",
            "뉴스본문;t3102",
            "종목별증시일정;t3202",
            "FNG_요약;t3320",
            "재무순위종합;t3341",
            "투자의견;t3401",
            "해외실시간지수;t3518",
            "해외지수조회(API용);t3521",
            "증시주변자금추이;t8428",

            "[주식] 프로그램;/stock/program",
            "프로그램매매종합조회;t1631",
            "시간대별프로그램매매추이;t1632",
            "기간별프로그램매매추이;t1633",
            "종목별프로그램매매동향;t1636",
            "종목별프로그램매매추이;t1637",
            "프로그램매매종합조회(미니);t1640",
            "시간대별프로그램매매추이(차트);t1662",

            "[주식] 투자자;/stock/investor",
            "투자자별종합;t1601",
            "시간대별투자자매매추이;t1602",
            "시간대별투자자매매추이상세;t1603",
            "투자자매매종합1;t1615",
            "투자자매매종합2;t1617",
            "업종별분별투자자매매동향(챠트용);t1621",
            "투자자매매종합(챠트);t1664",

            "[주식] 외인/기관;/stock/frgr-itt",
            "외인기관종목별동향;t1702",
            "외인기관종목별동향;t1716",
            "외인기관종목별동향;t1717",

            "[주식] ELW;/stock/elw",
            "ELW현재가(시세)조회;t1950",
            "ELW시간대별체결조회;t1951",
            "ELW일별주가;t1954",
            "ELW현재가(확정지급액)조회;t1956",
            "ELW종목비교;t1958",
            "LP대상종목정보조회;t1959",
            "ELW등락율상위;t1960",
            "ELW거래량상위;t1961",
            "ELW전광판;t1964",
            "ELW거래대금상위;t1966",
            "ELW지표검색;t1969",
            "ELW현재가호가조회;t1971",
            "ELW현재가(거래원)조회;t1972",
            "ELW시간대별예상체결조회;t1973",
            "ELW기초자산동일종목;t1974",
            "기초자산리스트조회;t1988",
            "ELW종목조회;t8431",
            "기초자산리스트조회;t9905",
            "만기월조회;t9907",
            "ELW마스터조회API용;t9942",

            "[주식] ETF;/stock/etf",
            "ETF현재가(시세)조회;t1901",
            "ETF시간별추이;t1902",
            "ETF일별추이;t1903",
            "ETF구성종목조회;t1904",
            "ETFLP호가;t1906",

            "[주식] 섹터;/stock/sector",
            "테마별종목;t1531",
            "종목별테마;t1532",
            "특이테마;t1533",
            "테마종목별시세조회;t1537",
            "전체테마;t8425",

            "[주식] 종목검색;/stock/item-search",
            "신호조회;t1809",
            "종목Q클릭검색(씽큐스마트);t1825",
            "종목Q클릭검색리스트조회(씽큐스마트);t1826",
            "서버저장조건 리스트조회;t1866",
            "서버저장조건 조건검색;t1859",
            "서버저장조건 실시간검색;t1860",

            "[주식] 상위종목;/stock/high-item",
            "등락율상위;t1441",
            "시가총액상위;t1444",
            "거래량상위;t1452",
            "거래대금상위;t1463",
            "전일동시간대비거래급증;t1466",
            "시간외등락율상위;t1481",
            "시간외거래량상위;t1482",
            "예상체결량상위조회;t1489",
            "단일가예상등락율상위;t1492",

            "[주식] 차트;/stock/chart",
            "기간별투자자매매추이(차트);t1665",
            "API전용주식차트(일주월년);t8410",
            "주식차트(틱/n틱);t8411",
            "주식차트(N분);t8412",

            "[주식] 기타;/stock/etc",
            "예탁담보융자가능종목현황조회;CLNAQ00100",
            "신규상장종목조회;t1403",
            "증거금율별종목조회;t1411",
            "종목별잔량/사전공시;t1638",
            "신용거래동향;t1921",
            "종목별신용정보;t1926",
            "공매도일별추이;t1927",
            "종목별대차거래일간추이;t1941",
            "주식종목조회;t8430",
            "주식종목조회 API용;t8436",

            "[주식] 계좌;/stock/accno",
            "계좌 거래내역;CDPCQ04700",
            "계좌별신용한도조회;CSPAQ00600",
            "현물계좌예수금 주문가능금액 총평가 조회;CSPAQ12200",
            "BEP단가조회;CSPAQ12300",
            "현물계좌 주문체결내역 조회(API);CSPAQ13700",
            "현물계좌예수금 주문가능금액 총평가2;CSPAQ22200",
            "현물계좌증거금률별주문가능수량조회;CSPBQ00200",
            "주식계좌 기간별수익률 상세;FOCCQ33600",
            "주식당일매매일지/수수료;t0150",
            "주식당일매매일지/수수료(전일);t0151",
            "주식잔고2;t0424",
            "주식체결/미체결;t0425",

            "[주식] 주문;/stock/order",
            "현물주문;CSPAT00601",
            "현물정정주문;CSPAT00701",
            "현물취소주문;CSPAT00801",

            "[주식] 실시간 시세;/websocket",
            "ETF호가잔량;B7_",
            "KOSPI시간외단일가호가잔량;DH1",
            "KOSDAQ시간외단일가호가잔량;DHA",
            "KOSDAQ시간외단일가체결;DK3",
            "KOSPI시간외단일가체결;DS3",
            "시간외단일가VI발동해제;DVI",
            "KOSPI호가잔량;H1_",
            "KOSPI장전시간외호가잔량;H2_",
            "KOSDAQ호가잔량;HA_",
            "KOSDAQ장전시간외호가잔량;HB_",
            "코스피ETF종목실시간NAV;I5_",
            "지수;IJ_",
            "KOSPI거래원;K1_",
            "KOSDAQ체결;K3_",
            "KOSDAQ프로그램매매종목별;KH_",
            "KOSDAQ프로그램매매전체집계;KM_",
            "KOSDAQ우선호가;KS_",
            "KOSDAQ거래원;OK_",
            "KOSPI프로그램매매종목별;PH_",
            "KOSPI프로그램매매전체집계;PM_",
            "KOSPI우선호가;S2_",
            "KOSPI체결;S3_",
            "KOSPI기세;S4_",
            "주식주문접수;SC0",
            "주식주문체결;SC1",
            "주식주문정정;SC2",
            "주식주문취소;SC3",
            "주식주문거부;SC4",
            "상/하한가근접진입;SHC",
            "상/하한가근접이탈;SHD",
            "상/하한가진입;SHI",
            "상/하한가이탈;SHO",
            "VI발동해제;VI_",
            "예상지수;YJ_",
            "KOSDAQ예상체결;YK3",
            "KOSPI예상체결;YS3",
            "뉴ELW투자지표민감도;ESN",
            "ELW장전시간외호가잔량;h2_",
            "ELW호가잔량;h3_",
            "ELW거래원;k1_",
            "ELW우선호가;s2_",
            "ELW체결;s3_",
            "ELW기세;s4_",
            "ELW예상체결;Ys3",
            "API사용자조건검색실시간;AFR",
            ],
        ["선물/옵션"] = [
            "[선물/옵션] 시세;/futureoption/market-data",
            "선물/옵션현재가(시세)조회;t2101",
            "선물/옵션현재가호가조회;t2105",
            "선물/옵션현재가시세메모;t2106",
            "선물옵션시간대별체결조회;t2201",
            "기간별주가;t2203",
            "선물옵션시간대별체결조회(단일출력용);t2210",
            "옵션전광판;t2301",
            "선물옵션호가잔량비율챠트;t2405",
            "미결제약정추이;t2421",
            "EUREXKOSPI200옵션선물현재가(시세)조회;t2830",
            "EUREXKOSPI200옵션선물호가조회;t2831",
            "EUREX야간옵션선물시간대별체결조회;t2832",
            "EUREX야간옵션선물기간별추이;t2833",
            "EUREX옵션선물시세전광판;t2835",
            "주식선물마스터조회(API용);t8401",
            "주식선물현재가조회(API용);t8402",
            "주식선물호가조회(API용);t8403",
            "주식선물시간대별체결조회(API용);t8404",
            "주식선물기간별주가(API용);t8405",
            "주식선물틱분별체결조회(API용);t8406",
            "상품선물마스터조회(API용);t8426",
            "과거데이터시간대별조회;t8427",
            "지수선물마스터조회API용;t8432",
            "지수옵션마스터조회API용;t8433",
            "선물/옵션멀티현재가조회;t8434",
            "파생종목마스터조회API용;t8435",
            "CME/EUREX마스터조회(API용);t8437",
            "지수선물마스터조회API용;t9943",
            "지수옵션마스터조회API용;t9944",

            "[선물/옵션] 투자자;/futureoption/investor",
            "상품선물투자자매매동향(실시간);t2541",
            "상품선물투자자매매동향(챠트용);t2545",

            "[선물/옵션] 차트;/futureoption/chart",
            "선물옵션틱분별체결조회차트;t2209",
            "선물옵션차트(틱/n틱);t8414",
            "선물/옵션차트(N분);t8415",
            "선물/옵션차트(일주월);t8416",
            "EUREX야간옵션선물틱분별체결조회차트;t8429",

            "[선물/옵션] 계좌;/futureoption/accno",
            "선물옵션 계좌 주문체결내역 조회;CFOAQ00600",
            "선물옵션 계좌잔고 및 평가현황3;CFOAQ50600",
            "선물옵션 주문가능수량조회;CFOAQ10100",
            "선물옵션 계좌예탁금증거금조회;CFOBQ10500",
            "선물옵션가정산예탁금상세;CFOEQ11100",
            "선물옵션 일별 계좌손익내역;CFOEQ82600",
            "계좌 미결제 약정현황(평균가);CFOFQ02400",
            "선물/옵션체결/미체결;t0434",
            "선물/옵션잔고평가(이동평균);t0441",
            "EUREX 주문체결내역조회;CEXAQ21100",
            "EUREX 주문가능 수량/금액 조회;CEXAQ21200",
            "EUREX 야간장잔고및 평가현황;CEXAQ31100",
            "EUREX 예탁금 및 통합잔고조회;CEXAQ31200",
            "EUREX 야간옵션 기간주문체결조회;CEXAQ44200",
            "선물옵션 기간별 계좌 수익률 현황;FOCCQ33700",

            "[선물/옵션] 주문;/futureoption/order",
            "선물옵션 정상주문;CFOAT00100",
            "선물옵션 정정주문;CFOAT00200",
            "선물옵션 취소주문;CFOAT00300",
            "선물옵션 옵션매도시 주문증거금조회(옵션매도시 1계약당 주문증거금);CFOBQ10800",
            "EUREX 매수/매도주문;CEXAT11100",
            "EUREX 정정주문;CEXAT11200",
            "EUREX 취소주문;CEXAT11300",

            "[선물/옵션] 기타;/futureoption/etc",
            "파생상품증거금율조회;MMDAQ91200",

            "[선물/옵션] 실시간 시세;/websocket",
            "선물주문체결;C01",
            "상품선물실시간상하한가;CD0",
            "EUREX연계KP200지수옵션선물체결;EC0",
            "EUREX연계KP200지수옵션선물호가;EH0",
            "EUX접수;EU0",
            "EUX체결;EU1",
            "EUX확인;EU2",
            "KOSPI200선물체결;FC0",
            "KOSPI200선물실시간상하한가;FD0",
            "KOSPI200선물호가;FH0",
            "KOSPI200선물가격제한폭확대;FX0",
            "선물주문정정취소;H01",
            "주식선물체결;JC0",
            "주식선물실시간상하한가;JD0",
            "주식선물호가;JH0",
            "주식선물가격제한폭확대;JX0",
            "선물접수;O01",
            "KOSPI200옵션체결;OC0",
            "KOSPI200옵션실시간상하한가;OD0",
            "KOSPI200옵션호가;OH0",
            "KOSPI200옵션민감도;OMG",
            "KOSPI200옵션가격제한폭확대;OX0",
            "상품선물예상체결;YC3",
            "지수선물예상체결;YFC",
            "주식선물예상체결;YJC",
            "지수옵션예상체결;YOC",
            ],
        ["해외선물"] = [
            "[해외선물] 시세;/overseas-futureoption/market-data",
            "해외선물마스터조회;o3101",
            "해외선물 일별체결 조회;o3104",
            "해외선물 현재가(종목정보) 조회;o3105",
            "해외선물 현재가호가 조회;o3106",
            "해외선물 관심종목 조회;o3107",
            "해외선물 시간대별(Tick)체결 조회;o3116",
            "해외선물옵션 마스터 조회;o3121",
            "해외선물옵션 차트 분봉 조회;o3123",
            "해외선물옵션 현재가(종목정보) 조회;o3125",
            "해외선물옵션 현재가호가 조회;o3126",
            "해외선물옵션 관심종목 조회;o3127",
            "해외선물옵션 차트 일주월 조회;o3128",
            "해외선물옵션 시간대별 Tick 체결 조회;o3136",
            "해외선물옵션 차트 NTick 체결 조회;o3137",

            "[해외선물] 계좌;/overseas-futureoption/accno",
            "해외선물 체결내역개별 조회(주문가능수량);CIDBQ01400",
            "해외선물 미결제잔고내역 조회;CIDBQ01500",
            "해외선물 주문내역 조회;CIDBQ01800",
            "해외선물 주문체결내역 상세 조회;CIDBQ02400",
            "해외선물 예수금/잔고현황;CIDBQ03000",
            "해외선물 예탁자산 조회;CIDBQ05300",
            "일자별 미결제 잔고내역;CIDEQ00800",

            "[해외선물] 주문;/overseas-futureoption/order",
            "해외선물 신규주문;CIDBT00100",
            "해외선물 정정주문;CIDBT00900",
            "해외선물 취소주문;CIDBT01000",

            "[해외선물] 차트;/overseas-futureoption/chart",
            "해외선물차트 분봉 조회;o3103",
            "해외선물차트(일주월) 조회;o3108",
            "해외선물 차트 NTick 체결 조회;o3117",
            "해외선물옵션차트용NTick(고정형)-API용;o3139",

            "[해외선물] 실시간 시세;/websocket",
            "해외선물 체결;OVC",
            "해외선물 호가;OVH",
            "해외옵션 체결;WOC",
            "해외옵션 호가;WOH",
            "해외선물 주문접수;TC1",
            "해외선물 주문응답;TC2",
            "해외선물 주문체결;TC3",
            ],
        ["기타"] = [
            "[기타] 시간조회;/etc/time-search",
            "서버시간조회;t0167",

            "[기타] 실시간 시세;/websocket",
            "장운영정보;JIF",
            "실시간뉴스제목패킷;NWS",
            ],
        ["실시간 시세 투자정보"] = [
            "[실시간 시세 투자정보] 투자정보;/websocket",
            "시간대별투자자매매추이;BMT",
            "현물정보USD실시간;CUR",
            "US지수;MK2",
            ],
    };
    static readonly Dictionary<string, ResInfo> _mapCodeToResInfo = [];

    /// <summary>
    /// 그룹 정보 목록.
    /// </summary>
    public static readonly List<GroupInfo> GroupInfos = [];
    static ResManager()
    {
        foreach (var (key, value) in _group)
        {
            var groupInfo = new GroupInfo
            {
                Name = key,
                SubGroupInfos = [],
            };
            string url = "";
            bool isRealtime = false;
            foreach (var item in value)
            {
                if (item.StartsWith("["))
                {
                    url = item.Split(';')[1];
                    isRealtime = url.Equals("/websocket");
                    var subGroupInfo = new SubGroupInfo
                    {
                        Name = item[1..^1],
                        Url = url,
                        ResInfos = [],
                    };
                    groupInfo.SubGroupInfos.Add(subGroupInfo);
                }
                else
                {
                    var subGroupInfo = groupInfo.SubGroupInfos[^1];
                    var name_code = item.Split(';');
                    var resInfo = new ResInfo
                    {
                        Name = name_code[0],
                        Code = name_code[1],
                        Url = url,
                        IsRealtime = isRealtime,
                    };
                    subGroupInfo.ResInfos.Add(resInfo);
                    _mapCodeToResInfo[resInfo.Code] = resInfo;
                }
            }
            GroupInfos.Add(groupInfo);
        }
    }

    /// <summary>계좌관련 실시간 시세 목록.</summary>
    public static readonly List<string> AccountRealTimes = [
        "SC0", // 주식주문접수
        "SC1", // 주식주문체결
        "SC2", // 주식주문정정
        "SC3", // 주식주문취소
        "SC4", // 주식주문거부

        "O01", // 선물접수
        "C01", // 선물주문체결
        "H01", // 선물주문정정취소

        "EU0", // EUX접수
        "EU1", // EUX체결
        "EU2", // EUX확인

        "TC1", // 해외선물 주문접수
        "TC2", // 해외선물 주문응답
        "TC3", // 해외선물 주문체결
        ];

    /// <summary>RES 정보를 가져옵니다.</summary>
    public static ResInfo? GetResInfo(string code)
    {
        if (_mapCodeToResInfo.TryGetValue(code, out var resInfo))
            return resInfo;
        return null;
    }

    /// <summary>RES 정보를 추가합니다.</summary>
    public static void AddResInfo(string name, string code, string url)
    {
        var resInfo = new ResInfo
        {
            Name = name,
            Code = code,
            Url = url,
            IsRealtime = url.Equals("/websocket"),
        };
        _mapCodeToResInfo[code] = resInfo;
    }
}

/// <summary>그룹 정보</summary>
public class GroupInfo
{
    /// <summary>그룹명</summary>
    public required string Name;
    /// <summary>서브 그룹 정보</summary>
    public required List<SubGroupInfo> SubGroupInfos;
}

/// <summary>서브 그룹 정보</summary>
public class SubGroupInfo
{
    /// <summary>서브 그룹명</summary>
    public required string Name;
    /// <summary>URL</summary>
    public required string Url;
    /// <summary>자원 정보</summary>
    public required List<ResInfo> ResInfos;
}

/// <summary>자원 정보</summary>
public class ResInfo
{
    /// <summary>TR명</summary>
    public required string Name;
    /// <summary>TR코드</summary>
    public required string Code;
    /// <summary>URL</summary>
    public required string Url;
    /// <summary>실시간 여부</summary>
    public required bool IsRealtime;
}

/*
 */