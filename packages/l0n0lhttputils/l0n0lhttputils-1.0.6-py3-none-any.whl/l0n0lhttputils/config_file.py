import yaml
import xlrd
from l0n0lhttputils.util import md5


class yaml_file:
    def __init__(self, filename):
        self.filename = filename
        self.config_data = {}

    def load_config(self):
        with open(self.filename, encoding='utf8') as fp:
            self.config_data = yaml.safe_load(fp.read())

    def get(self, name):
        value = self.config_data.get(name)
        if value is not None:
            return value
        return ""


class xl_file:
    def __init__(self, fname):
        self.fname = fname
        self.data = {}
        self.load()

    def load(self):
        self.data = {}
        work_book: xlrd.Book = xlrd.open_workbook(self.fname)
        sheet: xlrd.sheet.Sheet = work_book.sheets()[0]

        for i in range(3, sheet.nrows):
            data = {}
            for j in range(0, sheet.ncols):
                if sheet.cell(2, j).value == "string":
                    data[sheet.cell(0, j).value] = str(sheet.cell(i, j).value)
                if sheet.cell(2, j).value == "int":
                    data[sheet.cell(0, j).value] = int(sheet.cell(i, j).value)
                if sheet.cell(2, j).value == "float":
                    data[sheet.cell(0, j).value] = float(
                        sheet.cell(i, j).value)

            self.data[data['id']] = data

    def get(self, id):
        return self.data.get(id)


class xl_kv_file:
    def __init__(self, fname):
        self.fname = fname
        self.data = {}
        self.load()

    def load(self):
        self.data = {}
        work_book: xlrd.Book = xlrd.open_workbook(self.fname)
        sheet: xlrd.sheet.Sheet = work_book.sheets()[0]
        for i in range(2, sheet.nrows):
            self.data[sheet.cell(i, 0).value] = sheet.cell(i, 1).value
    
    def get(self, id):
        return self.data.get(id)


class changed_file_mgr:
    def __init__(self, check_epalse: int):
        """
        @check_epalse:int：文件检测时常
        """
        self.files_md5 = {}
        self.timer = 0
        self.check_epalse = check_epalse

    def add_file(self, filename):
        with open(filename, 'rb') as fp:
            self.files_md5[filename] = md5(fp.read())

    def update(self, elapse):
        self.timer += elapse
        if self.timer < self.check_epalse:
            return
        f = getattr(self, "on_file_change")
        for fname, md5value in self.files_md5.items():
            with open(fname, 'rb') as fp:
                newmd5 = md5(fp.read())
                if md5value != newmd5:
                    self.files_md5[fname] = newmd5
                    f(fname)
