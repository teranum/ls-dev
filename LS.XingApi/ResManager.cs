namespace LS.XingApi
{
    internal class FieldSpec
    {
        public enum VarType
        {
            STRING,
            INT,
            LONG,
            DOUBLE,
        }

        public string name;
        public string desc;
        public string? content;
        public VarType type;
        public int size;
        public int dot_size;
        public double dot_value;

        public FieldSpec(string name, string desc, string type, double size)
        {
            this.name = name;
            this.desc = desc;
            this.type = type switch
            {
                "INT" => VarType.INT,
                "LONG" => VarType.INT,
                "DOUBLE" => VarType.DOUBLE,
                _ => VarType.STRING,
            };

            this.size = (int)size;
            this.dot_value = 0;
            this.dot_size = (int)(size * 10 - this.size * 10);
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

    internal class BlockSpec
    {
        public string name;
        public bool is_output;
        public bool is_occurs;
        public IList<FieldSpec> fields = [];
        public int record_size;

        public BlockSpec(string name, bool isOutput, bool isOccurs)
        {
            this.name = name;
            this.is_output = isOutput;
            this.is_occurs = isOccurs;
        }
    }

    internal class ResInfo
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
        public string filepath;
        public string res_text;
        public bool is_correct;

        public string tr_cd;
        public string tr_desc;
        public bool is_func;
        public bool is_attr;
        public bool is_block;
        public bool compressable;

        public string headtype;

        public IList<BlockSpec> in_blocks = [];
        public IList<BlockSpec> out_blocks = [];

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
            compressable = false;
            headtype = string.Empty;

            if (!string.IsNullOrEmpty(filePath))
            {
                try
                {
                    FromText(File.ReadAllText(filePath));
                }
                catch
                {
                }
            }
        }

        public void FromText(string text)
        {
            res_text = text;
            is_correct = false;
            is_func = is_attr = is_block = compressable = false;
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
                    if (line.StartsWith("BEGIN FUNCTION MAP"))
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
                    if (line.Equals("BEGIN DATA MAP"))
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
                        var field_name = spec_fields[0];
                        var field_desc = spec_fields[2];
                        var field_type = spec_fields[3];
                        var field_size = double.Parse(spec_fields[4]);
                        blockSpec!.fields.Add(new FieldSpec(field_name, field_desc, field_type, field_size));
                    }
                }
                else if (readState == RESFILE_READ_STATE.FOUNDED_BLOCK_END)
                {
                    if (line.Equals("END DATA MAP"))
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
                    if (line.StartsWith("END FUNCTION MAP"))
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
                            compressable = true;
                            break;
                        }
                    }
                }
            }
        }
    }

    internal class ResManager
    {
        private string _user_folder;
        private string _xing_folder;
        private IDictionary<string, ResInfo> _resources = new Dictionary<string, ResInfo>();

        public ResManager(string userFolder, string xingFolder)
        {
            _user_folder = userFolder;
            _xing_folder = xingFolder;
        }

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

        public void LoadFromFolder(string folderPath)
        {
            foreach (string filePath in Directory.GetFiles(folderPath, "*.res"))
            {
                SetFromFilePath(filePath);
            }
        }

        public ResInfo? GetResInfo(string tr_cd)
        {
            if (_resources.TryGetValue(tr_cd, out var info))
            {
                return info;
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
    }
}
