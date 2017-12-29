#!/usr/bin/python
#-*- coding: utf-8 -*-

import os

def utest_create_checklist_file(path=""):
    fn = os.path.join(path, "check_list.xls")
    print("INFO : CheckList -> {:s}".format(fn))
    with open(fn, 'w', encoding="gbk") as f:
        header = u"文件名 \t" + u"函数原型 \t" + u"状态 \t" + u"用例数 \t" \
                + u"失败数 \t" + u"语句覆盖 \t" + u"MC\DC \t" + u"说明 \t" \
                + u"验证" + "\r\n"
        f.write(header)
    return fn

def utest_check_list_deflist_writer(filename, deflist=None, debug=False):
    func_dict.setdefault(filename, list())
    for d in deflist:
        if debug and d is None: print("Definition in list is invalid.")
        func_dict[filename].append(d.prototype)

def utest_check_list_table_writer(xlsfile, filename, debug=False):
    row = ""
    rows = list()
    for v in func_dict[filename]:
        row = filename + " \t " + v + "\r\n"
        rows.append(row)
        row = ""
    xlsfile.writelines(rows)

def utest_check_list_processor(tblpath, filepath, deflist=None, debug=False):
    if deflist is None or len(deflist)==0:
        if debug: print("None valid definition list.")
        return
    
    filename = ""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        # fetch the base filename from path
        filename = os.path.basename(filepath)
        # write src file name mapping definitions list
        utest_check_list_deflist_writer(filename, deflist, debug)

        with open(tblpath, 'a', encoding="gbk") as f:
            row = ""
            rows = list()
            for v in func_dict[filename]:
                row = filename + " \t " + v + "\r\n"
                rows.append(row)
                row = ""
            f.writelines(rows)

