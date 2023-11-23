from funcs import *
import configparser


def hook():
    def read(section,option):
        return eval(config[section][option])
    
    config = configparser.ConfigParser()
    config.read('auto_pack/exec_clause.ini',encoding="utf-8")

    global path
    path = read('pack','path')
    hookIgnore = read('hook','hookignore')

    localPy,globalPy,cantHook = hook_allPackage(path,hookIgnore)

    config["import"]["localpy"] = repr(localPy)
    config["import"]["globalpy"] = repr(globalPy)
    config["import"]["canthook"] = repr(cantHook)

    config.write(open('auto_pack/exec_clause.ini',"w",encoding="utf-8"))



hook()