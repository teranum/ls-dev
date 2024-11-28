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
        public string type;
        public int size;
        public int dot_size;
        public double dot_value;

        public FieldSpec(string name, string desc, string type, double size)
        {
            this.name = name;
            this.desc = desc;
            this.type = type;
            this.size = (int)size;
            this.dot_value = 0;
            this.dot_size = (int)(size * 10 - this.size * 10);
            if (this.dot_size > 0)
            {
                this.dot_value = Math.Pow(10, this.dot_size);
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
            throw new NotImplementedException();
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
            ResInfo resInfo = new ResInfo();
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
            ResInfo resInfo = new ResInfo(filePath);
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

        public ResInfo GetResInfo(string tr_cd)
        {
            if (_resources.ContainsKey(tr_cd))
            {
                return _resources[tr_cd];
            }
            ResInfo resInfo = new ResInfo();
            string filePath = Path.Combine(_user_folder, tr_cd + ".res");
            if (!File.Exists(filePath))
            {
                filePath = Path.Combine(_xing_folder, tr_cd + ".res");
            }
            if (File.Exists(filePath))
            {
                resInfo.FromText(File.ReadAllText(filePath));
                _resources[tr_cd] = resInfo;
            }
            return resInfo;
        }
    }
}
