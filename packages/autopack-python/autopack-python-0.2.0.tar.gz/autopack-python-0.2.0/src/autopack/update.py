import configparser
from funcs import *

def update():
    def read(section,option):
        return eval(config[section][option])
    
    config = configparser.ConfigParser()
    config.read('auto_pack/exec_clause.ini',encoding="utf-8")

    global path
    path = read('pack','path')
    pyd_clause = read("pack","pyd_clause")

    updatefile = read("file","updatefile")
    updatepyd = read("pyd","updatepyd")
    outputpyd = read("output","outputpyd")

    outputupdatefile = read("output","outputupdatefile")
    updatefileZipName = read("output","updatefileZipName")

    delete_and_create_folder(outputupdatefile)
    
    pyd(path,outputpyd,updatepyd,pyd_clause)
    copy_folder(outputpyd,outputupdatefile)

    move_file(path,outputupdatefile,updatefile)

    zip_folder_progress(outputupdatefile,updatefileZipName)

update()