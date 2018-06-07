import os.path
import fnmatch
import glob
import shutil

src_path = 'data/zip'
dst_path = 'data/raw'


def recursiveSearchFiles(dirPath, partFileInfo):
    fileList = []
    pathList = glob.glob(os.path.join(dirPath, '*'))  # windows path
    for mPath in pathList:
        if fnmatch.fnmatch(mPath, partFileInfo):
            fileList.append(mPath)  # 符合条件条件加到列表
        elif os.path.isdir(mPath):
            fileList += recursiveSearchFiles(mPath, partFileInfo)  # 将返回的符合文件列表追加到上层
        else:
            pass
    return fileList


files = recursiveSearchFiles(src_path, "*.wav")  # windows path

for file in files:
    basename = os.path.basename(file)
    if os.path.exists(os.path.join(dst_path, basename)):
        continue
    if 'MACOSX' in file:
        continue
    if os.path.getsize(file) == 0:
        print('0 size:', file)
        continue
    shutil.copy(file, os.path.join(dst_path, basename))
