import configparser
import zipfile
from funcs import *




def pack():
    def read(section,option):
        return eval(config[section][option])
    
    config = configparser.ConfigParser()
    config.read('auto_pack/exec_clause.ini',encoding="utf-8")

    global path
    path = read('pack','path')
    mainpy = read("pack","mainpy")
    pack_clause = read("pack","pack_clause")
    pyd_clause = read("pack","pyd_clause")
    


    localignorepyd = read("import","localignorepyd")
    globalimportignore = read("import","globalimportignore")
    localpy = read("import","localPy")
    globalpy = read("import","globalpy")




    outputpack = read('output','outputpack')
    outputallfile = read('output','outputallfile')
    outputpyd = read("output","outputpyd")
    allfileZipName = read("output","allfileZipName")

    allpyd = read("pyd","allpyd")


    allfile = read("file","allfile")

    localImport = only_left(localpy,localignorepyd)
    globalImport = only_left(globalpy,globalimportignore)


    localImport = [i[len(path) + 1:-3] for i in localImport]

    allImport = globalImport + localImport


    delete_and_create_folder(outputpack)
    delete_and_create_folder(outputallfile)

    move_packFile(path,outputpack,mainpy,localImport)
    add_import_py(f"{outputpack}/{mainpy}",allImport)

    package(pack_clause,mainpy,outputpack,outputallfile)

    pyd(path,outputpyd,allpyd,pyd_clause)
    copy_folder(outputpyd,outputallfile)

    move_file(path,outputallfile,allfile)
    
    zip_folder_progress(outputallfile,allfileZipName)


pack()




