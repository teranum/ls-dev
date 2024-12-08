from enum import Enum
import os
import __main__

class FieldSpec:
    class VarType(Enum):
        STRING = 0
        INT = 1
        FLOAT = 2

    def __init__(self, name: str, desc: str, var_type: str, size: float):
        self.name = name
        self.desc = desc
        match var_type:
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

class BlockSpec:
    def __init__(self, name: str, is_output: bool, is_occurs: bool):
        self.name = name
        self.is_output = is_output
        self.is_occurs = is_occurs
        self.fields: list[FieldSpec] = []
        self.record_size = 0

class ResInfo:
    class RESFILE_READ_STATE(Enum):
        NONE = 0
        FOUNDED_BEGIN_FUNCTION_MAP = 1
        FOUNDED_TR_TITLE = 2
        FOUNDED_BEGIN_DATA_MAP = 3
        FOUNDED_BLOCK_TITLE = 4
        FOUNDED_BLOCK_BEGIN = 5
        FOUNDED_BLOCK_END = 6
        FOUNDED_END_DATA_MAP = 7
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
        self.compressable = False
        self.headtype = str()
        self.in_blocks: list[BlockSpec] = []
        self.out_blocks: list[BlockSpec] = []

        if filepath:
            try:
                with open(filepath, encoding="euc-kr") as f:
                    self.from_text(f.read())
            except:
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
                    # field_name = spec_fields[1] # not used
                    field_name = spec_fields[2]
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
            if len(self.in_blocks) > 0:
                comp_yn = next((x for x in self.in_blocks[0].fields if x.name == "comp_yn"), None)
                self.compressable = comp_yn is not None

class ResourceManager:
    _resources: dict[str, ResInfo] = {}
    def __init__(self, xing_folder = ""):
        self._package_folder = os.path.dirname(os.path.abspath(__file__))
        self._user_folder = os.path.dirname(os.path.abspath(__main__.__file__))
        self._xing_folder = xing_folder

        # ELW관련 중복네임 파일들은 미리 로드
        if self._resources.get("h2_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\h2_4ELW.res")
        if self._resources.get("h3_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\h3_4ELW.res")
        if self._resources.get("k1_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\k1_4ELW.res")
        if self._resources.get("s2_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\s2_4ELW.res")
        if self._resources.get("s3_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\s3_4ELW.res")
        if self._resources.get("s4_", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\s4_ELW.res")
        if self._resources.get("Ys3", None) is None:
            self.set_from_filepath(self._package_folder + "\\res\\Ys3_4ELW.res")

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
        except:
            pass

    def get(self, code: str) -> ResInfo | None:
        exist = self._resources.get(code, None)
        if exist is not None:
            if exist.is_correct:
                return exist
            return None

        # load from file at res folder
        filename = code + ".res"
        path = self._package_folder + "\\res\\" + filename # package res folder
        if not os.path.exists(path):
            path = self._user_folder + "\\" + filename # user folder
            if not os.path.exists(path):
                path = self._user_folder + "\\res\\" + filename # user res folder
                if not os.path.exists(path):
                    path = self._xing_folder + "\\res\\" + filename # xing res folder
                    if not os.path.exists(path):
                        path = ""

        res_info = ResInfo(path)
        self._resources[code] = res_info
        if res_info.is_correct:
            return res_info

        return None

if __name__ == "__main__":
    resManager = ResourceManager()
    resManager.load_from_folder(os.path.dirname(os.path.abspath(__file__)) + "\\res")

    print(f"Loaded {len(resManager._resources)} resources")

    infos = resManager._resources

    for key, value in infos.items():
        # check in_blocks count
        if len(value.in_blocks) > 1:
            print(f"{value.tr_cd}: {value.tr_desc} in_blocks count = {len(value.in_blocks)}")

        # #check headtype is not A
        # if value.headtype not in ["A", ""]:
        #     print(f"{value.tr_cd}: {value.tr_desc} headtype = {value.headtype}")

        # # find field name is 'comp_yn'
        # for block in value.in_blocks:
        #     for field in block.fields:
        #         if field.name == "comp_yn":
        #             print(f"{value.tr_cd}: {value.tr_desc} comp_yn in {block.name}")

        # find if filename != tr_cd
        path = value.filepath
        filename = os.path.basename(path)
        if filename != value.tr_cd + ".res":
            print(f"{key} != {filename}")
