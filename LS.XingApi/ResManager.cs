namespace LS.XingApi
{
    class FieldSpec
    {
        public string name;
        public string desc;
        public string type;
        public int length;
        public int size;
        public int dot_size;
        public int dot_value;
    }
    class BlockSpec
    {
        public string name;
        public bool is_output;
        public bool is_occurs;
        public IList<FieldSpec> fields = [];
        public int record_size;
    }

    internal class ResManager
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
        internal static object GetResInfo(string szTrCode)
        {
            throw new NotImplementedException();
        }
    }
}
