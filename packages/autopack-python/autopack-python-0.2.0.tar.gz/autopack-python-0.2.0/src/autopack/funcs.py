import os
import zipfile
import shutil  
import time
from tqdm import tqdm
import sys

def get_cpath():
    return os.path.dirname(__file__).replace("\\","/")

def only_left(list1,list2):
    return [i for i in list1 if i not in list2]

def find_all_file(path,ignore):

    allFileList = []
    for r,n,f in os.walk(path):
        rootPath = r.replace("\\","/")
        dirList = [f"{rootPath}/{i}" for i in n ]
        fileList = [f"{rootPath}/{i}" for i in f ]
        break
    
    dirList =only_left(dirList,ignore)
    fileList = only_left(fileList,ignore)

    allFileList = allFileList + fileList

    
    if len(dirList) == 0:return allFileList
    for dirPath in dirList:
        allFileList = allFileList + find_all_file(dirPath,ignore)

    return allFileList

def find_all_py_file(path,ignore):
    allFiles = find_files(path)
    ignoreFiles = [find_files(i) for i in ignore]
    ignoreFiles = list(set(sum(ignoreFiles, [])))  

    needFind = only_left(allFiles,ignoreFiles)
    needFind = [i for i in needFind if pyFile_is(i)]
    return needFind 


def find_files(path):  
    """  
    找到给定目录下的所有文件  
    """  
    if os.path.isfile(path):
        return [path]

    file_paths = []  
    for dirpath, dirnames, filenames in os.walk(path):  
        for filename in filenames:  
            file_paths.append(os.path.join(dirpath, filename).replace("\\", "/") )
    return file_paths


def hook_allPackage(path,hookIgnore):
    needHookFileList = find_all_py_file(path,hookIgnore)
    localPy = set()
    globalPy = set()
    cantHook = set()

    sys.path.append(path)

    for file in needHookFileList:
        code = open(file,"r",encoding="utf-8").read().split("\n")

        for line in code:
            lineSplit = line.split()
            if "import" not in lineSplit: continue
            
            if "from" in lineSplit:
                lineSplit = lineSplit[:2]
                lineSplit[0] = "import"

            packName = lineSplit[-1]
            importLine = " ".join(lineSplit)
            try:exec(importLine)
            except Exception as e:print(e)
            try:
                packPath = eval(f"{packName}.__file__")
                packPath = packPath.replace("\\","/")

                if parentDir(path,packPath):
                    localPy.add(packPath)
                else:
                    globalPy.add(packName)

            except:
                cantHook.add(packName)
    
    
    return localPy,globalPy,cantHook



def parentDir(parent,child):
    parentLen = len(parent)
    if child[:parentLen] == parent:return True
    return False



def pyFile_is(path):
    if path[-3:] == ".py":return True
    else:return False



def write_file(path,content):
    open(path,"w",encoding="utf-8").write(content)


def add_import_py(pyfile,importList):
    importList = list(importList)
    importList = [i.replace("/",",") for i in importList]
    importStr = "\n".join([f"import {i}" for i in importList])

    code = open(pyfile,"r",encoding="utf-8").read()
    code = f"{importStr}\n{code}"
    write_file(pyfile,code)

def plist(l1):
    l1 = repr(l1)
    l1 = l1.split(",")
    for dex,i in enumerate(l1):
        if dex == len(l1) -1:
            print(i)
        else:
            print(f"{i},")

def move_packFile(originPath,output,mainpy,localpy):

    

    allPy = [mainpy[:-3]] + localpy
    s = [f"{originPath}/{i}.py" for i in allPy]
    d = [f"{output}/{i}.py" for i in allPy]
    

    for sp,dp in zip(s,d):
        check_create_path(dp)
        shutil.copyfile(sp,dp)

def move_file(originPath,output,file):
    s = [f"{originPath}/{i}" for i in file]
    d = [f"{output}/{i}" for i in file]
    
    for sp,dp in zip(s,d):
        check_create_path(dp)
        if os.path.isfile(sp):
            shutil.copy2(sp,dp)
        if os.path.isdir(sp):
            copy_folder(sp,dp)

def check_create_path(path):  
    path = get_file_path(path)
    if not os.path.exists(path):  
        os.makedirs(path)

def get_file_path(path):  
    path = path.replace("\\","/")
    path = path.split("/")
    if "." in path[-1]:
        path.pop(-1)
    return "/".join(path)
    
def delete_and_create_folder(folder_name):  
    # 检查文件夹是否存在,如果存在则删除它  
    if os.path.exists(folder_name):  
        shutil.rmtree(folder_name)  
      
    # 创建新的文件夹  
    os.makedirs(folder_name)


def copy_folder(source_folder,target_folder):

    # 遍历源文件夹中的所有文件和文件夹  

    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename).replace("\\","/")  
        target_file = os.path.join(target_folder, filename).replace("\\","/")  
    
        # 如果目标文件夹中存在同名文件或文件夹,就进行覆盖操作  
        if os.path.exists(target_file):  
            if os.path.isfile(target_file):  
                os.remove(target_file)  # 如果是文件就删除并且复制
                shutil.copy2(source_file, target_file)

            if os.path.isdir(target_file):  
                copy_folder(source_file,target_file)
    
        # 将源文件或文件夹复制到目标文件夹中  
        else:
            if os.path.isfile(source_file):  
                shutil.copy2(source_file, target_file)  # 如果是文件就复制  
            
            if os.path.isdir(source_file):
                shutil.copytree(source_file, target_file)


def package(pack_clause,mainpy,outputpack,outputallfile):
    print(f" 执行打包语句 {pack_clause}")
    os.system(pack_clause)

    mainName = mainpy[:-3]

    if os.path.exists(outputallfile):  
        shutil.rmtree(outputallfile) 

    shutil.copytree(f"{outputpack}/dist/{mainName}",outputallfile)
    shutil.rmtree(f"{outputpack}/dist")
    shutil.rmtree(f"{outputpack}/build")


def pyd(path,outputpyd,pydList,pyd_clause):
    
    delete_and_create_folder(outputpyd)

    toPydList = []
    for i in pydList:
        if os.path.isfile(i):
            ii = i.split("/")[-1]
            ii = f"{outputpyd}/{ii}"
            toPydList.append([i,ii])
        
        if os.path.isdir(i):
            i = find_all_file(i,[])
            i = [[ii,"{}/{}".format(outputpyd,ii.split("/")[-1])] for ii in i if ii[-3:] == ".py" ]
            toPydList = toPydList + i
    
    for s_,d_ in toPydList:
        pyd_(s_,d_,outputpyd,pyd_clause)
        s_ = s_.replace(path,outputpyd)

        s_ = s_.replace(".py",".pyd")
        d_ = d_.replace(".py",".pyd")

        check_create_path(s_)
        
        try:shutil.move(d_,s_)
        except:pass
    
    shutil.rmtree(f"{outputpyd}/build")
    os.remove(f"{outputpyd}/setup.py")


def pyd_(s_,d_,pydPath,pyd_clause):

    name = d_.split("/")[-1]
    fp = open(f"{pydPath}/setup.py","w",encoding="utf-8")
    fp.write("from distutils.core import setup\n")
    fp.write("from Cython.Build import cythonize\n")
    fp.write(f"setup(name='setup',ext_modules=cythonize('{name}'))\n")
    fp.close()

    shutil.copy2(s_,d_)
    os.system(pyd_clause)

    os.remove(d_)
    time.sleep(0.1)
    os.remove(d_.replace(".py",".c"))

    pydList = os.listdir(pydPath)
    for i in pydList:
        if i[-4:] != ".pyd":continue
        i1 = i.split(".")[0]
        if i1 == name[:-3]:
            shutil.move(f"{pydPath}/{i}",f"{pydPath}/{i1}.pyd")
                 
    return d_.replace(".py",".pyd")


def calculate_folder_size(folder_path):  
    total_size = 0  
    for root, dirs, files in os.walk(folder_path):  
        for file in files:  
            file_path = os.path.join(root, file)  
            total_size += os.path.getsize(file_path)  
    return total_size  


def zip_folder_progress(folder_path, zip_path):  

    folder_name = get_last_directory_name(folder_path)

    total_size = calculate_folder_size(folder_path)  
    with tqdm(total=total_size, desc="Zip progress", ncols=100, ascii=True, bar_format="{l_bar}{bar}{r_bar}") as progress_bar:  
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:  
            for root, dirs, files in os.walk(folder_path):  
                for file in files:  
                    file_path = os.path.join(root, file)  
                    file_path = os.path.abspath(file_path)

                    relative_path = os.path.relpath(file_path, folder_path)  
                    relative_path = os.path.join(folder_name,relative_path)
                    
                    zipf.write(file_path, arcname=relative_path) # 将文件添加到zip文件中，不保留上级目录  
                    progress_bar.update(os.path.getsize(file_path)) # 更新进度条  

        zipf.close() # 关闭zip文件  

  
def get_last_directory_name(path):  
    # 如果路径以文件名结尾，则获取其所在的文件夹路径  
    if os.path.isfile(path):  
        path = os.path.dirname(path)  
      
    # 分割路径，取出最后一部分  
    parts = os.path.split(path)  
      
    # 返回最后一个文件夹的名称  
    return parts[-1] if parts else None