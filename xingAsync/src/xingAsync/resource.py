import os
import __main__
from enum import Enum

class FieldSpec:
    class VarType(Enum):
        STRING = 0,
        INT = 1,
        FLOAT = 2,

    def __init__(self, name: str, desc: str, type: str, size: float):
        self.name = name
        self.desc = desc
        match type:
            case "long" | "int":
                varType = FieldSpec.VarType.INT
            case "float" | "double":
                varType = FieldSpec.VarType.FLOAT
            # case "char" | "date":
            #     varType = FieldSpec.VarType.STRING
            case _:
                varType = FieldSpec.VarType.STRING
        
        self.var_type = varType

        self.size = int(size)
        self.dot_size = 0
        self.dot_value = 0
        self.dot_size = int(size * 10 - self.size * 10)
        if self.dot_size > 0:
            self.dot_value = pow(10, self.dot_size)

    @staticmethod
    def get_default_value(var_type: VarType):
        match var_type:
            case FieldSpec.VarType.INT:
                return 0
            case FieldSpec.VarType.FLOAT:
                return 0.0
            case FieldSpec.VarType.STRING:
                return ""

class BlockSpec:
    def __init__(self, name: str, is_output: bool, is_occurs: bool):
        self.name = name
        self.is_output = is_output
        self.is_occurs = is_occurs
        self.fields: list[FieldSpec] = []
        self.record_size = 0
        #
        self.nTotalBuffer = 0

class ResInfo:
    class RESFILE_READ_STATE(Enum):
        NONE = 0,
        FOUNDED_BEGIN_FUNCTION_MAP = 1,
        FOUNDED_TR_TITLE = 2,
        FOUNDED_BEGIN_DATA_MAP = 3,
        FOUNDED_BLOCK_TITLE = 4,
        FOUNDED_BLOCK_BEGIN = 5,
        FOUNDED_BLOCK_END = 6,
        FOUNDED_END_DATA_MAP = 7,
        FOUNDED_END_FUNCTION_MAP = 8

    def __init__(self, filepath = ""):
        self.filepath = filepath
        self.res_text = str()
        self.is_correct = False

        self.tr_cd = str()
        self.tr_desc = str()
        self.is_func = False
        self.is_attr = False
        self.is_block = False
        self.headtype = str()
        self.in_blocks: list[BlockSpec] = []
        self.out_blocks: list[BlockSpec] = []

        if len(filepath):
            try:
                with open(filepath, encoding="euc-kr") as f:
                    self.from_text(f.read())
            except :
                pass

    def from_text(self, text: str):
            self.res_text = text
            lines = [x.strip() for x in self.res_text.splitlines()]

            readState = ResInfo.RESFILE_READ_STATE.NONE

            blockSpec: BlockSpec = None
            for line in lines:
                if len(line) == 0:
                    continue

                if readState == ResInfo.RESFILE_READ_STATE.NONE:
                    if line == "BEGIN_FUNCTION_MAP":
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BEGIN_FUNCTION_MAP
                    else:
                        break

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_BEGIN_FUNCTION_MAP:
                    spec_fields = [x.strip() for x in line.split(';')[0].split(',')]
                    if spec_fields[0] == ".Func":
                        self.is_func = True
                    elif spec_fields[0] != ".Feed":
                        break
                    self.tr_desc = spec_fields[1]
                    self.tr_cd = spec_fields[2]

                    if len(spec_fields) > 3:
                        for spec in spec_fields[3:]:
                            if spec.startswith("headtype="):
                                self.headtype = spec.split("=")[1]
                            elif spec == "attr":
                                self.is_attr = True
                            elif spec == "block":
                                self.is_block = True
                    readState = ResInfo.RESFILE_READ_STATE.FOUNDED_TR_TITLE

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_TR_TITLE:
                    if line == "BEGIN_DATA_MAP":
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BEGIN_DATA_MAP
                    else:
                        break

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_BEGIN_DATA_MAP:
                    spec_fields = [x.strip() for x in line.split(';')[0].split(',')]
                    block_name = spec_fields[0]
                    block_output = spec_fields[2] == "output"
                    block_occurs = len(spec_fields) > 3 and "occurs" in spec_fields[3:]

                    blockSpec = BlockSpec(block_name, block_output, block_occurs)
                    readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE:
                    if line == "begin":
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_BEGIN
                    else:
                        break

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_BEGIN:
                    if line == "end":
                        record_size = 0
                        for field in blockSpec.fields:
                            record_size += field.size
                        if record_size > 0 and self.is_attr:
                            record_size += len(blockSpec.fields)
                        blockSpec.record_size = record_size
                        if blockSpec.is_output:
                            self.out_blocks.append(blockSpec)
                        else:
                            self.in_blocks.append(blockSpec)
                        blockSpec = None
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_END
                    else:
                        spec_fields = [x.strip() for x in line.split(';')[0].split(',')]
                        field_desc = spec_fields[0]
                        field_name = spec_fields[1]
                        field_type = spec_fields[3]
                        field_size = float(spec_fields[4])
                        blockSpec.fields.append(FieldSpec(field_name, field_desc, field_type, field_size))

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_END:
                    if line == "END_DATA_MAP":
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_END_DATA_MAP
                    else:
                        spec_fields = [x.strip() for x in line.split(';')[0].split(',')]
                        block_name = spec_fields[0]
                        block_output = spec_fields[2] == "output"
                        block_occurs = len(spec_fields) > 3 and "occurs" in spec_fields[3:]

                        blockSpec = BlockSpec(block_name, block_output, block_occurs)
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_BLOCK_TITLE

                elif readState == ResInfo.RESFILE_READ_STATE.FOUNDED_END_DATA_MAP:
                    if line == "END_FUNCTION_MAP":
                        readState = ResInfo.RESFILE_READ_STATE.FOUNDED_END_FUNCTION_MAP
                    else:
                        break

            if readState == ResInfo.RESFILE_READ_STATE.FOUNDED_END_FUNCTION_MAP:
                self.is_correct = True

class ResourceManager:
    def __init__(self):
        self._res_folder = os.path.dirname(os.path.abspath(__file__)) + "\\res"
        self._user_folder = os.path.dirname(os.path.abspath(__main__.__file__))
        self._resources: dict[str, ResInfo] = dict()

        res_c0003 = ('''\
            BEGIN_FUNCTION_MAP
	            .Func,리소스,c0003,block,headtype=A;
	            BEGIN_DATA_MAP
	            c0003InBlock,input,input;
	            begin
		            경로,path,path,char,0;
	            end
	            c0003OutBlock,output,output;
	            begin
		            데이터,data,data,char,0;
	            end
	            END_DATA_MAP
            END_FUNCTION_MAP
            \
        ''')
        self.set_from_text(res_c0003)
        res_UFR = ('''\
            BEGIN_FUNCTION_MAP
	            .Feed, 조건검색실시간(t1857OutBlock1), UFR, attr, key=6, group=1;
	            BEGIN_DATA_MAP
	            UFRInBlock,input,input;
	            begin
	            end
	            UFROutBlock,output,output;
	            begin
		            종목코드, shcode, shcode, char, 7;
		            종목명, hname, hname, char, 40;
		            현재가, price, price, long, 9;
		            전일대비구분, sign, sign, char, 1;
		            전일대비, change, change, long, 9;
		            등락율, diff, diff, float, 6;
		            거래량, volume, volume, long, 12;
		            종목상태(N:진입 R:재진입 O:이탈), JobFlag, JobFlag, char, 1;
	            end
	            END_DATA_MAP
            END_FUNCTION_MAP
            \
        ''')
        self.set_from_text(res_UFR)

        # self.load_from_folder(os.path.dirname(os.path.abspath(__file__)) + "\\res")

    def set_from_text(self, text: str) :
        res_info = ResInfo()
        res_info.from_text(text)
        if res_info.is_correct:
            self._resources[res_info.tr_cd] = res_info
            return res_info
        return None

    def set_from_filepath(self, filepath: str):
        res_info = ResInfo(filepath)
        if res_info.is_correct:
            self._resources[res_info.tr_cd] = res_info
            return res_info
        return None

    def load_from_folder(self, folderpath: str):
        try:
            files = os.listdir(folderpath)
            for file in files:
                if file.endswith(".res"):
                    res_info = ResInfo(folderpath + "\\" + file)
                    if res_info.is_correct and res_info.tr_cd not in self._resources:
                        self._resources[res_info.tr_cd] = res_info
        except :
            pass

    def get(self, code: str) -> ResInfo | None:
        exist = self._resources.get(code, None)
        if exist is not None:
            if exist.is_correct:
                return exist
            return None

        # load from file at res folder
        path = self._res_folder + "\\" + code + ".res"
        if os.path.exists(path):
            res_info = ResInfo(path)
            if code != res_info.tr_cd:
                return None
            self._resources[code] = res_info
            if res_info.is_correct:
                return res_info
        else:
            # load from file at user folder
            path = self._user_folder + "\\" + code + ".res"
            if os.path.exists(path):
                res_info = ResInfo(path)
                if code != res_info.tr_cd:
                    return None
                self._resources[res_info.tr_cd] = res_info
                if res_info.is_correct:
                    return res_info

        # res_info = ResInfo(self._user_folder + "\\" + code + ".res")
        # if code != res_info.tr_cd:
        #     return None
        # self._resources[code] = res_info
        # if res_info.is_correct:
        #     return res_info

        return None

if __name__ == "__main__":
    resManager = ResourceManager()
    resManager.load_from_folder(os.path.dirname(os.path.abspath(__file__)) + "\\res")

    print(f"Loaded {len(resManager._resources)} resources")

    infos = resManager._resources

    print("inblock 개수가 2개 이상인 것들만 출력")
    for key in infos:
        value = infos[key]
        if len(value.in_blocks) > 1:
            print(f"{value.tr_cd}: {value.tr_desc} {len(value.in_blocks)}")

    pass
