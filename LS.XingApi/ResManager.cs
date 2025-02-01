using System.Reflection;
using System.Runtime.InteropServices;

namespace LS.XingApi
{
    /// <summary>필드 데이터</summary>
    public class FieldSpec
    {
        /// <summary>필드타입</summary>
        public enum VarType
        {
            /// <summary>문자열</summary>
            STRING,
            /// <summary>정수(int)</summary>
            INT,
            /// <summary>정수(long)</summary>
            LONG,
            /// <summary>실수</summary>
            DOUBLE,
        }

        /// <summary>필드명</summary>
        public string name;
        /// <summary>필드설명</summary>
        public string desc;
        /// <summary>필드내용</summary>
        public string? content;
        /// <summary>필드타입</summary>
        public VarType type;
        /// <summary>필드길이</summary>
        public int size;
        /// <summary>소수점길이</summary>
        public int dot_size;
        /// <summary>소수점값</summary>
        public double dot_value;

        /// <summary>생성자</summary>
        public FieldSpec(string name, string desc, string type, int field_size, int dot_size)
        {
            this.name = name;
            this.desc = desc;
            this.type = type switch
            {
                "long" => VarType.INT,
                "int" => VarType.INT,
                "float" => VarType.DOUBLE,
                "double" => VarType.DOUBLE,
                _ => VarType.STRING,
            };

            this.size = field_size;
            this.dot_size = dot_size;
            if (this.dot_size > 0)
            {
                this.dot_value = Math.Pow(10, this.dot_size);
            }
            else
            {
                if (this.type == VarType.INT && this.size >= 10)
                {
                    this.type = VarType.LONG;
                }
            }
        }
    }

    /// <summary>블록 데이터</summary>
    public class BlockSpec
    {
        /// <summary>블록명</summary>
        public string name;
        /// <summary>출력여부</summary>
        public bool is_output;
        /// <summary>반복여부</summary>
        public bool is_occurs;
        /// <summary>필드 목록</summary>
        public IList<FieldSpec> fields = [];
        /// <summary>레코드 크기</summary>
        public int record_size;

        /// <summary>생성자</summary>
        public BlockSpec(string name, bool isOutput, bool isOccurs)
        {
            this.name = name;
            this.is_output = isOutput;
            this.is_occurs = isOccurs;
        }
    }

    /// <summary>리소스 정보</summary>
    public class ResInfo
    {
        enum RESFILE_READ_STATE
        {
            NONE,
            FOUNDED_BEGIN_FUNCTION_MAP,
            FOUNDED_TR_TITLE,
            FOUNDED_BEGIN_DATA_MAP,
            FOUNDED_BLOCK_TITLE,
            FOUNDED_BLOCK_BEGIN,
            FOUNDED_BLOCK_END,
            FOUNDED_END_DATA_MAP,
            FOUNDED_END_FUNCTION_MAP,
        }
        /// <summary>파일경로</summary>
        public string filepath;
        /// <summary>리소스 텍스트</summary>
        public string res_text;
        /// <summary>정상여부</summary>
        public bool is_correct;

        /// <summary>TR 코드</summary>
        public string tr_cd;
        /// <summary>TR 설명</summary>
        public string tr_desc;
        /// <summary>함수여부</summary>
        public bool is_func;
        /// <summary>속성여부</summary>
        public bool is_attr;
        /// <summary>블록여부</summary>
        public bool is_block;
        /// <summary>압축가능여부</summary>
        public bool is_comp_yn;
        /// <summary>헤드타입</summary>
        public string headtype;

        /// <summary>입력 블록 목록</summary>
        public IList<BlockSpec> in_blocks = [];
        /// <summary>출력 블록 목록</summary>
        public IList<BlockSpec> out_blocks = [];

        /// <summary>생성자</summary>
        public ResInfo(string filePath = "")
        {
            filepath = filePath;
            res_text = string.Empty;
            is_correct = false;

            tr_cd = string.Empty;
            tr_desc = string.Empty;
            is_func = false;
            is_attr = false;
            is_block = false;
            is_comp_yn = false;
            headtype = string.Empty;

            if (!string.IsNullOrEmpty(filePath))
            {
                try
                {
                    var all_bytes = File.ReadAllBytes(filePath);
                    var ansi_striing = Marshal.PtrToStringAnsi(Marshal.UnsafeAddrOfPinnedArrayElement(all_bytes, 0), all_bytes.Length);
                    FromText(ansi_striing);
                }
                catch
                {
                }
            }
        }

        /// <summary>텍스트에서 리소스 정보를 설정합니다.</summary>
        internal void FromText(string text)
        {
            res_text = text;
            is_correct = false;
            is_func = is_attr = is_block = is_comp_yn = false;
            headtype = string.Empty;
            in_blocks.Clear();
            out_blocks.Clear();

            var lines = text.Split(['\r', '\n'], StringSplitOptions.RemoveEmptyEntries);

            var readState = ResInfo.RESFILE_READ_STATE.NONE;
            BlockSpec? blockSpec = null;

            foreach (var lineText in lines)
            {
                var line = lineText.Trim();
                if (line.Length == 0)
                {
                    continue;
                }

                if (readState == RESFILE_READ_STATE.NONE)
                {
                    if (line.StartsWith("BEGIN_FUNCTION_MAP"))
                    {
                        readState = RESFILE_READ_STATE.FOUNDED_BEGIN_FUNCTION_MAP;
                    }
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BEGIN_FUNCTION_MAP)
                {
                    var spec_fields = line.Split(';')[0].Split(',').Select(x => x.Trim()).ToArray();
                    if (spec_fields.Length < 3)
                        break;
                    if (spec_fields[0].Equals(".Func"))
                        is_func = true;
                    else if (!spec_fields[0].Equals(".Feed"))
                        break;
                    tr_desc = spec_fields[1];
                    tr_cd = spec_fields[2];

                    if (spec_fields.Length > 3)
                        for (int i = 3; i < spec_fields.Length; i++)
                        {
                            var spec = spec_fields[i];
                            if (spec.StartsWith("headtype="))
                            {
                                headtype = spec.Split('=')[1];
                            }
                            else if (spec.StartsWith("attr"))
                            {
                                is_attr = true;
                            }
                            else if (spec.StartsWith("block"))
                            {
                                is_block = true;
                            }
                        }
                    readState = RESFILE_READ_STATE.FOUNDED_TR_TITLE;
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_TR_TITLE)
                {
                    if (line.Equals("BEGIN_DATA_MAP"))
                    {
                        readState = RESFILE_READ_STATE.FOUNDED_BEGIN_DATA_MAP;
                    }
                    else
                        break;
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BEGIN_DATA_MAP)
                {
                    var spec_fields = line.Split(';')[0].Split(',').Select(x => x.Trim()).ToArray();
                    var block_name = spec_fields[0];
                    var block_output = spec_fields[2].Equals("output");
                    var block_occurs = false;
                    for (int i = 3; i < spec_fields.Length; i++)
                    {
                        if (spec_fields[i].Equals("occurs"))
                        {
                            block_occurs = true;
                            break;
                        }
                    }
                    blockSpec = new BlockSpec(block_name, block_output, block_occurs);
                    readState = RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE;
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE)
                {
                    if (line.Equals("begin"))
                    {
                        readState = RESFILE_READ_STATE.FOUNDED_BLOCK_BEGIN;
                    }
                    else
                        break;
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BLOCK_BEGIN)
                {
                    if (line.Equals("end"))
                    {
                        var record_size = 0;

                        foreach (var field in blockSpec!.fields)
                        {
                            record_size += field.size;
                        }
                        if (record_size > 0 && is_attr)
                        {
                            record_size += blockSpec.fields.Count;
                        }
                        blockSpec.record_size = record_size;
                        if (blockSpec.is_output)
                            out_blocks.Add(blockSpec);
                        else
                            in_blocks.Add(blockSpec);
                        blockSpec = null;
                        readState = RESFILE_READ_STATE.FOUNDED_BLOCK_END;
                    }
                    else
                    {
                        var spec_fields = line.Split(';')[0].Split(',').Select(x => x.Trim()).ToArray();
                        if (spec_fields.Length < 5)
                            break;
                        var field_desc = spec_fields[0];
                        var field_name = spec_fields[2];
                        var field_type = spec_fields[3];
                        var fieldSize_dotSize = spec_fields[4].Split('.');
                        var field_size = 0;
                        var dot_size = 0;
                        if (fieldSize_dotSize.Length > 1)
                        {
                            field_size = int.Parse(fieldSize_dotSize[0]);
                            dot_size = int.Parse(fieldSize_dotSize[1]);
                        }
                        else
                        {
                            field_size = int.Parse(fieldSize_dotSize[0]);
                        }
                        blockSpec!.fields.Add(new FieldSpec(field_name, field_desc, field_type, field_size, dot_size));
                    }
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BLOCK_END)
                {
                    if (line.Equals("END_DATA_MAP"))
                    {
                        readState = RESFILE_READ_STATE.FOUNDED_END_DATA_MAP;
                    }
                    else
                    {
                        var spec_fields = line.Split(';')[0].Split(',').Select(x => x.Trim()).ToArray();
                        if (spec_fields.Length < 3)
                            break;
                        var block_name = spec_fields[0];
                        var block_output = spec_fields[2].Equals("output");
                        var block_occurs = false;
                        for (int i = 3; i < spec_fields.Length; i++)
                        {
                            if (spec_fields[i].Equals("occurs"))
                            {
                                block_occurs = true;
                                break;
                            }
                        }
                        blockSpec = new BlockSpec(block_name, block_output, block_occurs);
                        readState = RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE;
                    }
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_END_DATA_MAP)
                {
                    if (line.StartsWith("END_FUNCTION_MAP"))
                    {
                        readState = RESFILE_READ_STATE.FOUNDED_END_FUNCTION_MAP;
                    }
                    else
                        break;
                }
            }

            if (readState == RESFILE_READ_STATE.FOUNDED_END_FUNCTION_MAP)
            {
                is_correct = true;
                if (in_blocks.Count > 0)
                {
                    foreach (var field in in_blocks[0].fields)
                    {
                        if (field.name.Equals("comp_yn"))
                        {
                            is_comp_yn = true;
                            break;
                        }
                    }
                }
            }
        }
    }

    /// <summary>리소스 매니저</summary>
    /// <remarks>생성자</remarks>
    public class ResManager(string xingFolder)
    {
        private readonly string _user_folder = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
        private readonly string _xing_folder = xingFolder;
        private readonly static Dictionary<string, ResInfo> _resources = [];

        /// <summary>텍스트에서 리소스 정보를 설정합니다.</summary>
        public ResInfo? SetFromText(string text)
        {
            ResInfo resInfo = new();
            resInfo.FromText(text);
            if (resInfo.is_correct)
            {
                _resources[resInfo.tr_cd] = resInfo;
                return resInfo;
            }
            return null;
        }

        /// <summary>파일에서 리소스 정보를 설정합니다.</summary>
        public ResInfo? SetFromFilePath(string filePath)
        {
            ResInfo resInfo = new(filePath);
            if (resInfo.is_correct)
            {
                _resources[resInfo.tr_cd] = resInfo;
                return resInfo;
            }
            return null;
        }

        /// <summary>폴더에서 리소스 정보를 설정합니다.</summary>
        public void LoadFromFolder(string folderPath)
        {
            foreach (string filePath in Directory.GetFiles(folderPath, "*.res"))
            {
                SetFromFilePath(filePath);
            }
        }

        /// <summary>TR 코드로 리소스 정보를 가져옵니다.</summary>
        public ResInfo? GetResInfo(string tr_cd)
        {
            if (_resources.TryGetValue(tr_cd, out var info))
            {
                if (info.is_correct)
                    return info;
                return null;
            }
            string filePath = Path.Combine(_user_folder, tr_cd + ".res");
            if (!File.Exists(filePath))
            {
                filePath = Path.Combine(_xing_folder, "res", tr_cd + ".res");
            }
            ResInfo resInfo = new(filePath);
            _resources[tr_cd] = resInfo;
            if (!resInfo.is_correct)
                return null;
            return resInfo;
        }

        /// <summary>TR 코드로 등록된 리소스 정보를 가져옵니다.</summary>
        public ResInfo? GetExist(string tr_cd)
        {
            if (_resources.TryGetValue(tr_cd, out var info))
            {
                return info;
            }
            return null;
        }
    }
}
