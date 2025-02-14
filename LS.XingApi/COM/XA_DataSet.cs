// This file was auto generated by ComType Tool at 2025-02-04 오후 1:47:50
// File : C:\LS_SEC\xingAPI\XA_DataSet.dll
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

namespace LS.XingApi.COM;

[ComImport]
[Guid("AAF89E20-1F84-4B1F-B6EE-617B6F2C9CD4")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
internal interface _IXAQueryEvents
{
    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(1)]
    void _event_ReceiveData([MarshalAs(UnmanagedType.BStr)] string szTrCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(2)]
    void _event_ReceiveMessage(bool bIsSystemError, [MarshalAs(UnmanagedType.BStr)] string nMessageCode, [MarshalAs(UnmanagedType.BStr)] string szMessage);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(3)]
    void _event_ReceiveChartRealData([MarshalAs(UnmanagedType.BStr)] string szTrCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(4)]
    void _event_ReceiveSearchRealData([MarshalAs(UnmanagedType.BStr)] string szTrCode);

}

[ComImport]
[Guid("255B43AE-B290-4435-9BA7-37FCAAD04D77")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
internal interface IXAQuery
{
    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(2)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetFieldData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName, int nRecordIndex);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(3)]
    int Request(bool bNext);

    [DispId(5)]
    string ResFileName
    {
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(5)]
        [return: MarshalAs(UnmanagedType.BStr)]
        get;
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(5)]
        [param: In]
        [param: MarshalAs(UnmanagedType.BStr)]
        set;
    }

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(6)]
    bool LoadFromResFile([MarshalAs(UnmanagedType.BStr)] string szFileName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(7)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetTrCode();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(8)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetTrDesc();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(14)]
    void GetBlockInfo([MarshalAs(UnmanagedType.BStr)] string szFieldName, IntPtr szNameK, IntPtr szNameE, IntPtr nRecordType);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(15)]
    void SetFieldData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName, int nOccursIndex, [MarshalAs(UnmanagedType.BStr)] string szData);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(17)]
    void GetFieldInfo([MarshalAs(UnmanagedType.BStr)] string szFieldName, [MarshalAs(UnmanagedType.BStr)] string szItemName, IntPtr nItemType, IntPtr nDataSize, IntPtr nDotPoint, IntPtr nOffSet);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(18)]
    int GetBlockType([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(19)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetResData();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(23)]
    int GetBlockSize([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(24)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetFieldDescList([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [DispId(29)]
    bool IsNext
    {
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(29)]
        get;
    }

    [DispId(30)]
    string ContinueKey
    {
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(30)]
        [return: MarshalAs(UnmanagedType.BStr)]
        get;
    }

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(31)]
    int GetBlockCount([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(32)]
    void SetBlockCount([MarshalAs(UnmanagedType.BStr)] string szBlockName, int nCount);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(33)]
    void ClearBlockdata([MarshalAs(UnmanagedType.BStr)] string szFieldName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(34)]
    int GetLastError();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(35)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetErrorMessage(int nErrorCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(36)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetAccountList(int nIndex);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(37)]
    int GetAccountListCount();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(38)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetBlockData([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(39)]
    int RequestService([MarshalAs(UnmanagedType.BStr)] string szCode, [MarshalAs(UnmanagedType.BStr)] string szData);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(40)]
    int RemoveService([MarshalAs(UnmanagedType.BStr)] string szCode, [MarshalAs(UnmanagedType.BStr)] string szData);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(41)]
    bool RequestLinkToHTS([MarshalAs(UnmanagedType.BStr)] string szLinkName, [MarshalAs(UnmanagedType.BStr)] string szData, [MarshalAs(UnmanagedType.BStr)] string szFiller);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(42)]
    int Decompress([MarshalAs(UnmanagedType.BStr)] string szBlockName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(43)]
    int GetTRCountPerSec([MarshalAs(UnmanagedType.BStr)] string szCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(44)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetAccountName([MarshalAs(UnmanagedType.BStr)] string szAcc);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(45)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetAcctDetailName([MarshalAs(UnmanagedType.BStr)] string szAcc);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(46)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetAcctNickname([MarshalAs(UnmanagedType.BStr)] string szAcc);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(47)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetFieldChartRealData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(48)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetAttribute([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName, [MarshalAs(UnmanagedType.BStr)] string szAttribute, int nRecordIndex);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(49)]
    int GetTRCountBaseSec([MarshalAs(UnmanagedType.BStr)] string szCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(50)]
    int GetTRCountRequest([MarshalAs(UnmanagedType.BStr)] string szCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(51)]
    int GetTRCountLimit([MarshalAs(UnmanagedType.BStr)] string szCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(52)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetFieldSearchRealData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(53)]
    void SetProgramOrder(bool bProgramOrder);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(54)]
    bool GetProgramOrder();

}

[ComImport]
[Guid("ED0FC93A-7879-4C0D-BA8F-71A7E2B5A737")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
internal interface IXAReal
{
    [DispId(1)]
    string ResFileName
    {
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(1)]
        [return: MarshalAs(UnmanagedType.BStr)]
        get;
        [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
        [DispId(1)]
        [param: In]
        [param: MarshalAs(UnmanagedType.BStr)]
        set;
    }

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(6)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetTrCode();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(7)]
    bool LoadFromResFile([MarshalAs(UnmanagedType.BStr)] string szFileName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(8)]
    void SetFieldData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName, [MarshalAs(UnmanagedType.BStr)] string szData);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(11)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetFieldData([MarshalAs(UnmanagedType.BStr)] string szBlockName, [MarshalAs(UnmanagedType.BStr)] string szFieldName);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(12)]
    void AdviseRealData();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(13)]
    void UnadviseRealData();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(14)]
    void UnadviseRealDataWithKey([MarshalAs(UnmanagedType.BStr)] string szCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(15)]
    void AdviseLinkFromHTS();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(16)]
    void UnAdviseLinkFromHTS();

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(17)]
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetBlockData([MarshalAs(UnmanagedType.BStr)] string szBlockName);

}

[ComImport]
[Guid("16602768-2C96-4D93-984B-E36E7E35BFBE")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
internal interface _IXARealEvents
{
    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(1)]
    void _event_ReceiveRealData([MarshalAs(UnmanagedType.BStr)] string szTrCode);

    [MethodImpl(MethodImplOptions.InternalCall | MethodImplOptions.PreserveSig, MethodCodeType = MethodCodeType.Runtime)]
    [DispId(2)]
    void _event_RecieveLinkData([MarshalAs(UnmanagedType.BStr)] string szLinkName, [MarshalAs(UnmanagedType.BStr)] string szData, [MarshalAs(UnmanagedType.BStr)] string szFiller);

}

/// <summary>ReceiveData 이벤트</summary>
public class _IXAQueryEvents_ReceiveDataEventArgs(string szTrCode) : EventArgs
{
    /// <summary>szTrCode</summary>
    public string szTrCode = szTrCode;
}

/// <summary>ReceiveMessage 이벤트</summary>
public class _IXAQueryEvents_ReceiveMessageEventArgs(bool bIsSystemError, string nMessageCode, string szMessage) : EventArgs
{
    /// <summary>bIsSystemError</summary>
    public bool bIsSystemError = bIsSystemError;
    /// <summary>nMessageCode</summary>
    public string nMessageCode = nMessageCode;
    /// <summary>szMessage</summary>
    public string szMessage = szMessage;
}

/// <summary>ReceiveChartRealData 이벤트</summary>
public class _IXAQueryEvents_ReceiveChartRealDataEventArgs(string szTrCode) : EventArgs
{
    /// <summary>szTrCode</summary>
    public string szTrCode = szTrCode;
}

/// <summary>ReceiveSearchRealData 이벤트</summary>
public class _IXAQueryEvents_ReceiveSearchRealDataEventArgs(string szTrCode) : EventArgs
{
    /// <summary>szTrCode</summary>
    public string szTrCode = szTrCode;
}

/// <summary>XAQueryClass</summary>
[Guid("781520A9-4C8C-433B-AA6E-EE9E94108639")]
public class XAQueryClass : _IXAQueryEvents
{
    // public const string PROGID = "XA_DataSet.XAQuery.1";

    private readonly IXAQuery com = null!;
    void _IXAQueryEvents._event_ReceiveData(string szTrCode) => OnReceiveData?.Invoke(this, new(szTrCode));
    void _IXAQueryEvents._event_ReceiveMessage(bool bIsSystemError, string nMessageCode, string szMessage) => OnReceiveMessage?.Invoke(this, new(bIsSystemError, nMessageCode, szMessage));
    void _IXAQueryEvents._event_ReceiveChartRealData(string szTrCode) => OnReceiveChartRealData?.Invoke(this, new(szTrCode));
    void _IXAQueryEvents._event_ReceiveSearchRealData(string szTrCode) => OnReceiveSearchRealData?.Invoke(this, new(szTrCode));

    /// <summary>ReceiveData event</summary>
    public event EventHandler<_IXAQueryEvents_ReceiveDataEventArgs>? OnReceiveData;
    /// <summary>ReceiveMessage event</summary>
    public event EventHandler<_IXAQueryEvents_ReceiveMessageEventArgs>? OnReceiveMessage;
    /// <summary>ReceiveChartRealData event</summary>
    public event EventHandler<_IXAQueryEvents_ReceiveChartRealDataEventArgs>? OnReceiveChartRealData;
    /// <summary>ReceiveSearchRealData event</summary>
    public event EventHandler<_IXAQueryEvents_ReceiveSearchRealDataEventArgs>? OnReceiveSearchRealData;

    /// <inheritdoc cref="IXAQuery.GetFieldData"/>
    public string GetFieldData(string szBlockName, string szFieldName, int nRecordIndex) => com.GetFieldData(szBlockName, szFieldName, nRecordIndex);
    /// <inheritdoc cref="IXAQuery.Request"/>
    public int Request(bool bNext) => com.Request(bNext);
    /// <inheritdoc cref="IXAQuery.ResFileName"/>
    public string ResFileName { get => com.ResFileName; set => com.ResFileName = value; }
    /// <inheritdoc cref="IXAQuery.LoadFromResFile"/>
    public bool LoadFromResFile(string szFileName) => com.LoadFromResFile(szFileName);
    /// <inheritdoc cref="IXAQuery.GetTrCode"/>
    public string GetTrCode() => com.GetTrCode();
    /// <inheritdoc cref="IXAQuery.GetTrDesc"/>
    public string GetTrDesc() => com.GetTrDesc();
    /// <inheritdoc cref="IXAQuery.GetBlockInfo"/>
    public void GetBlockInfo(string szFieldName, IntPtr szNameK, IntPtr szNameE, IntPtr nRecordType) => com.GetBlockInfo(szFieldName, szNameK, szNameE, nRecordType);
    /// <inheritdoc cref="IXAQuery.SetFieldData"/>
    public void SetFieldData(string szBlockName, string szFieldName, int nOccursIndex, string szData) => com.SetFieldData(szBlockName, szFieldName, nOccursIndex, szData);
    /// <inheritdoc cref="IXAQuery.GetFieldInfo"/>
    public void GetFieldInfo(string szFieldName, string szItemName, IntPtr nItemType, IntPtr nDataSize, IntPtr nDotPoint, IntPtr nOffSet) => com.GetFieldInfo(szFieldName, szItemName, nItemType, nDataSize, nDotPoint, nOffSet);
    /// <inheritdoc cref="IXAQuery.GetBlockType"/>
    public int GetBlockType(string szBlockName) => com.GetBlockType(szBlockName);
    /// <inheritdoc cref="IXAQuery.GetResData"/>
    public string GetResData() => com.GetResData();
    /// <inheritdoc cref="IXAQuery.GetBlockSize"/>
    public int GetBlockSize(string szBlockName) => com.GetBlockSize(szBlockName);
    /// <inheritdoc cref="IXAQuery.GetFieldDescList"/>
    public string GetFieldDescList(string szBlockName) => com.GetFieldDescList(szBlockName);
    /// <inheritdoc cref="IXAQuery.IsNext"/>
    public bool IsNext => com.IsNext;
    /// <inheritdoc cref="IXAQuery.ContinueKey"/>
    public string ContinueKey => com.ContinueKey;
    /// <inheritdoc cref="IXAQuery.GetBlockCount"/>
    public int GetBlockCount(string szBlockName) => com.GetBlockCount(szBlockName);
    /// <inheritdoc cref="IXAQuery.SetBlockCount"/>
    public void SetBlockCount(string szBlockName, int nCount) => com.SetBlockCount(szBlockName, nCount);
    /// <inheritdoc cref="IXAQuery.ClearBlockdata"/>
    public void ClearBlockdata(string szFieldName) => com.ClearBlockdata(szFieldName);
    /// <inheritdoc cref="IXAQuery.GetLastError"/>
    public int GetLastError() => com.GetLastError();
    /// <inheritdoc cref="IXAQuery.GetErrorMessage"/>
    public string GetErrorMessage(int nErrorCode) => com.GetErrorMessage(nErrorCode);
    /// <inheritdoc cref="IXAQuery.GetAccountList"/>
    public string GetAccountList(int nIndex) => com.GetAccountList(nIndex);
    /// <inheritdoc cref="IXAQuery.GetAccountListCount"/>
    public int GetAccountListCount() => com.GetAccountListCount();
    /// <inheritdoc cref="IXAQuery.GetBlockData"/>
    public string GetBlockData(string szBlockName) => com.GetBlockData(szBlockName);
    /// <inheritdoc cref="IXAQuery.RequestService"/>
    public int RequestService(string szCode, string szData) => com.RequestService(szCode, szData);
    /// <inheritdoc cref="IXAQuery.RemoveService"/>
    public int RemoveService(string szCode, string szData) => com.RemoveService(szCode, szData);
    /// <inheritdoc cref="IXAQuery.RequestLinkToHTS"/>
    public bool RequestLinkToHTS(string szLinkName, string szData, string szFiller) => com.RequestLinkToHTS(szLinkName, szData, szFiller);
    /// <inheritdoc cref="IXAQuery.Decompress"/>
    public int Decompress(string szBlockName) => com.Decompress(szBlockName);
    /// <inheritdoc cref="IXAQuery.GetTRCountPerSec"/>
    public int GetTRCountPerSec(string szCode) => com.GetTRCountPerSec(szCode);
    /// <inheritdoc cref="IXAQuery.GetAccountName"/>
    public string GetAccountName(string szAcc) => com.GetAccountName(szAcc);
    /// <inheritdoc cref="IXAQuery.GetAcctDetailName"/>
    public string GetAcctDetailName(string szAcc) => com.GetAcctDetailName(szAcc);
    /// <inheritdoc cref="IXAQuery.GetAcctNickname"/>
    public string GetAcctNickname(string szAcc) => com.GetAcctNickname(szAcc);
    /// <inheritdoc cref="IXAQuery.GetFieldChartRealData"/>
    public string GetFieldChartRealData(string szBlockName, string szFieldName) => com.GetFieldChartRealData(szBlockName, szFieldName);
    /// <inheritdoc cref="IXAQuery.GetAttribute"/>
    public string GetAttribute(string szBlockName, string szFieldName, string szAttribute, int nRecordIndex) => com.GetAttribute(szBlockName, szFieldName, szAttribute, nRecordIndex);
    /// <inheritdoc cref="IXAQuery.GetTRCountBaseSec"/>
    public int GetTRCountBaseSec(string szCode) => com.GetTRCountBaseSec(szCode);
    /// <inheritdoc cref="IXAQuery.GetTRCountRequest"/>
    public int GetTRCountRequest(string szCode) => com.GetTRCountRequest(szCode);
    /// <inheritdoc cref="IXAQuery.GetTRCountLimit"/>
    public int GetTRCountLimit(string szCode) => com.GetTRCountLimit(szCode);
    /// <inheritdoc cref="IXAQuery.GetFieldSearchRealData"/>
    public string GetFieldSearchRealData(string szBlockName, string szFieldName) => com.GetFieldSearchRealData(szBlockName, szFieldName);
    /// <inheritdoc cref="IXAQuery.SetProgramOrder"/>
    public void SetProgramOrder(bool bProgramOrder) => com.SetProgramOrder(bProgramOrder);
    /// <inheritdoc cref="IXAQuery.GetProgramOrder"/>
    public bool GetProgramOrder() => com.GetProgramOrder();

    #region 생성자

    private readonly System.Runtime.InteropServices.ComTypes.IConnectionPoint? _pConnectionPoint;

    /// <summary>생성 여부</summary>
    public bool Created { get; private set; }

    /// <summary>생성자</summary>
    public XAQueryClass()
    {
        try
        {
            object? pUnknown = Activator.CreateInstance(Type.GetTypeFromCLSID(GetType().GUID)!);
            if (pUnknown != null)
            {
                com = (IXAQuery)pUnknown;
                if (com != null)
                {
                    Guid guidEvents = typeof(IXAQuery).GUID;
                    var pConnectionPointContainer = (System.Runtime.InteropServices.ComTypes.IConnectionPointContainer)pUnknown;
                    pConnectionPointContainer.FindConnectionPoint(ref guidEvents, out _pConnectionPoint);
                    if (_pConnectionPoint != null)
                    {
                        _pConnectionPoint.Advise(this, out int nCookie);
                        Created = true;
                    }
                }
            }
        }
        catch (Exception)
        {
        }
    }

    #endregion
}
/// <summary>ReceiveRealData 이벤트</summary>
public class _IXARealEvents_ReceiveRealDataEventArgs(string szTrCode) : EventArgs
{
    /// <summary>szTrCode</summary>
    public string szTrCode = szTrCode;
}

/// <summary>RecieveLinkData 이벤트</summary>
public class _IXARealEvents_RecieveLinkDataEventArgs(string szLinkName, string szData, string szFiller) : EventArgs
{
    /// <summary>szLinkName</summary>
    public string szLinkName = szLinkName;
    /// <summary>szData</summary>
    public string szData = szData;
    /// <summary>szFiller</summary>
    public string szFiller = szFiller;
}

/// <summary>XARealClass</summary>
[Guid("4D654021-F9D9-49F7-B2F9-6529A19746F7")]
public class XARealClass : _IXARealEvents
{
    // public const string PROGID = "XA_DataSet.XAReal.1";

    private readonly IXAReal com = null!;
    void _IXARealEvents._event_ReceiveRealData(string szTrCode) => OnReceiveRealData?.Invoke(this, new(szTrCode));
    void _IXARealEvents._event_RecieveLinkData(string szLinkName, string szData, string szFiller) => OnRecieveLinkData?.Invoke(this, new(szLinkName, szData, szFiller));

    /// <summary>ReceiveRealData event</summary>
    public event EventHandler<_IXARealEvents_ReceiveRealDataEventArgs>? OnReceiveRealData;
    /// <summary>RecieveLinkData event</summary>
    public event EventHandler<_IXARealEvents_RecieveLinkDataEventArgs>? OnRecieveLinkData;

    /// <inheritdoc cref="IXAReal.ResFileName"/>
    public string ResFileName { get => com.ResFileName; set => com.ResFileName = value; }
    /// <inheritdoc cref="IXAReal.GetTrCode"/>
    public string GetTrCode() => com.GetTrCode();
    /// <inheritdoc cref="IXAReal.LoadFromResFile"/>
    public bool LoadFromResFile(string szFileName) => com.LoadFromResFile(szFileName);
    /// <inheritdoc cref="IXAReal.SetFieldData"/>
    public void SetFieldData(string szBlockName, string szFieldName, string szData) => com.SetFieldData(szBlockName, szFieldName, szData);
    /// <inheritdoc cref="IXAReal.GetFieldData"/>
    public string GetFieldData(string szBlockName, string szFieldName) => com.GetFieldData(szBlockName, szFieldName);
    /// <inheritdoc cref="IXAReal.AdviseRealData"/>
    public void AdviseRealData() => com.AdviseRealData();
    /// <inheritdoc cref="IXAReal.UnadviseRealData"/>
    public void UnadviseRealData() => com.UnadviseRealData();
    /// <inheritdoc cref="IXAReal.UnadviseRealDataWithKey"/>
    public void UnadviseRealDataWithKey(string szCode) => com.UnadviseRealDataWithKey(szCode);
    /// <inheritdoc cref="IXAReal.AdviseLinkFromHTS"/>
    public void AdviseLinkFromHTS() => com.AdviseLinkFromHTS();
    /// <inheritdoc cref="IXAReal.UnAdviseLinkFromHTS"/>
    public void UnAdviseLinkFromHTS() => com.UnAdviseLinkFromHTS();
    /// <inheritdoc cref="IXAReal.GetBlockData"/>
    public string GetBlockData(string szBlockName) => com.GetBlockData(szBlockName);

    #region 생성자

    private readonly System.Runtime.InteropServices.ComTypes.IConnectionPoint? _pConnectionPoint;

    /// <summary>생성 여부</summary>
    public bool Created { get; private set; }

    /// <summary>생성자</summary>
    public XARealClass()
    {
        try
        {
            object? pUnknown = Activator.CreateInstance(Type.GetTypeFromCLSID(GetType().GUID)!);
            if (pUnknown != null)
            {
                com = (IXAReal)pUnknown;
                if (com != null)
                {
                    Guid guidEvents = typeof(IXAReal).GUID;
                    var pConnectionPointContainer = (System.Runtime.InteropServices.ComTypes.IConnectionPointContainer)pUnknown;
                    pConnectionPointContainer.FindConnectionPoint(ref guidEvents, out _pConnectionPoint);
                    if (_pConnectionPoint != null)
                    {
                        _pConnectionPoint.Advise(this, out int nCookie);
                        Created = true;
                    }
                }
            }
        }
        catch (Exception)
        {
        }
    }

    #endregion
}

