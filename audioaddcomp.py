#!/usr/bin/python3
# -*- coding:utf-8 -*-
# audioaddcomp.py
# version 0.3
"""
mutagen库:
github地址：https://github.com/quodlibet/mutagen
帮助文档地址：https://mutagen.readthedocs.io/en/latest/
pypi地址：https://pypi.org/project/mutagen/

使用参考：
https://www.jb51.net/article/265818.htm
https://github.com/backtracker/music_tag_tool/blob/master/music_tag_tool.py
https://www.cnblogs.com/yongdaimi/p/14990902.html ID3介绍
https://blog.csdn.net/thefutureit/article/details/129155713 ID3 tag version 2.3.0（非正式文档中文翻译）

脚本功能:
遍历整个当前目录，包括子目录。扫描每个目录下的flac、mp3、dsf、wave文件，获取元数据。如果同一目录下同一张专辑有多个artist和album的组合，则批量将每个文件加上COMPILATION=1标记，除非这个文件本来就有COMPILATION标记
日志：
2024-12-18 增加了display，clear的功能
发现一张专辑相同的专辑名称和歌手但还是显示两张专辑，后根据比对，单独的两首dsf歌曲文件有如下标记：TCMP(encoding=<Encoding.LATIN1: 0>, text=['1'])，手工删除之后就合并同一张专辑了。
from mutagen.dsf import DSF
audio = DSF(file)
del audio["TCMP"]
audio.save()
"""
import os,logging,sys

try:
    import mutagen
except ImportError:
    print("ERROR:mutagen not install,you can install like execut 'pip install mutagen'")
    exit(0)

from mutagen.mp3 import MP3
from mutagen.dsf import DSF
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.id3 import ID3,TXXX

metas,plan_metas,albums = [],[],[]
strHelp = "usage: audioaddcomp or audioaddcomp clear or audioaddcomp display"

logger = logging.getLogger('flac_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别
# 创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 创建一个handler，用于输出到文件
fh = logging.FileHandler('audioaddcomp.log')
fh.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(ch)
logger.addHandler(fh)

def getMeta(file):
    """
    根据file参数，当artist、album都有效的情况下，获取file,artist,album,COMPILATION,audio追加metas、plan_metas、albums列表
    """
    #print(file)
    artist,album,COMPILATION = '','',''
    try:
        audio=mutagen.File(file)
    except mutagen.mp3.HeaderNotFoundError as e:
        logger.warning(f"Can't sync to MPEG frame when open {file}")
        return
    except:
        logger.warning(f"Can't correct analysis {file}")
        return

    if type(audio) == mutagen.mp3.MP3:
        audio = ID3(file)
        artist = audio["TPE1"].text[0] if "TPE1" in audio.keys() else "" #artist
        album = audio["TALB"].text[0] if "TALB" in audio.keys() else "" #album
        COMPILATION = audio["TXXX:COMPILATION"].text[0] if "TXXX:COMPILATION" in audio.keys() else "" #COMPILATION
    elif  type(audio) == mutagen.dsf.DSF:
        audio = DSF(file)
        artist = str(audio["TPE1"]) if "TPE1" in audio.keys() else ""
        album = str(audio["TALB"]) if "TALB" in audio.keys() else ""
        COMPILATION = audio["TXXX:COMPILATION"].text[0] if "TXXX:COMPILATION" in audio.keys() else "" 
    elif type(audio) == mutagen.flac.FLAC:
        audio = FLAC(file)
        artist = audio["artist"] if "artist" in audio.keys() else [""] 
        artist = " ".join(artist) #列表转换成字符串才能使用set，下同
        album = audio["album"] if "album" in audio.keys() else [""]
        album = " ".join(album)
        COMPILATION, = audio["COMPILATION"] if "compilation" in audio.keys() else [""]
    elif type(audio) == mutagen.wave.WAVE:
        audio = WAVE(file)
        artist = str(audio["TPE1"]) if "TPE1" in audio.keys() else ""
        album = str(audio["TALB"]) if "TALB" in audio.keys() else ""
        COMPILATION = audio["TXXX:COMPILATION"].text[0] if "TXXX:COMPILATION" in audio.keys() else ""         
    else:
        return
    if (artist != "") and (album != ""):
        metas.append([file,artist,album,COMPILATION,audio])
        plan_metas.append(artist+album) 
        albums.append(album)
    else: 
        logger.warning(f"warning:wrong {file} meta info,no artist or album filed")

def DisplayMeta():
    """
    显示metas列表中文件修改前主要元数据和修改后主要元数据
    """
    global metas,plan_metas,albums 
    logger.info("before...")
    for meta in metas:
        logger.info(meta[0:4])  
    files = [] #暂存文件名列表
    for _ in metas:
        files.append(_[0])
    metas,plan_metas,albums = [],[],[] 
    for file in files:
        getMeta(file)
    logger.info("after...")
    for meta in metas:
        logger.info(meta[0:4])

def setCompilatton(path):
    """
    遍历整个当前目录，包括子目录。扫描每个目录下的flac、mp3、dsf、wave文件，获取元数据。如果同一目录下同一张专辑有多个artist和album的组合，则批量将每个文件加上COMPILATION=1标记，除非这个文件本来就有COMPILATION标记
    """
    global metas,plan_metas,albums 
    metas,plan_metas,albums = [],[],[]
    # 获取当前目录下的所有文件和目录
    filesAndDir = os.listdir(path)
    # 过滤出文件（排除目录）
    files = [f for f in filesAndDir if os.path.isfile(os.path.join(path, f))]
    # 获取文件相关meta信息保存到列表
    for file in files:
        getMeta(os.path.join(path, file))
    modifyFlag = False
    #print(albums)
    if len(set(albums)) == 1: #确认目录下歌曲都是同一张专辑
        if len(set(plan_metas)) >1 :#有不同的artist和album
            for meta in metas:
                if meta[3] == '': #没有设定过COMPILATION字段
                    audio = meta[4]
                    if (type(audio) == mutagen.id3.ID3) or \
                            (type(audio) == mutagen.dsf.DSF) or \
                            (type(audio) == mutagen.wave.WAVE) : 
                        audio["TXXX"] = TXXX(desc=u"COMPILATION", text=["1"]) #MP3,DSF,wave修改需要按照ID3规范修改，TXXX代表自定义属性
                    elif type(audio) == mutagen.flac.FLAC:
                        audio["COMPILATION"] = "1"
                    audio.save()
                    modifyFlag = True
    #显示结果
    if modifyFlag == True:
        DisplayMeta()
    
def traverse_dir(path):
    """
    遍历目录并调用setCompilatton
    """
    logger.info(f'Enter direct:[{path}]\n') 
    if os.path.isdir(path): #当前目录
        setCompilatton(path)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):#是目录
            #print("文件夹：", file_path)
            traverse_dir(file_path)

def Clear(path): 
    """
    清除path目录下音频文件的OMPILATION标志
    """
    global metas,plan_metas,albums 
    filesAndDir = os.listdir(path)
    # 过滤出文件（排除目录）
    files = [f for f in filesAndDir if os.path.isfile(os.path.join(path, f))]
    # 获取文件相关meta信息保存到列表
    for file in files:
        getMeta(os.path.join(path, file))
    modifyFlag = False
    for meta in metas:
        if meta[3] != '': #没有设定过COMPILATION字段
            audio = meta[4]
            if (type(audio) == mutagen.id3.ID3) or \
                    (type(audio) == mutagen.dsf.DSF) or \
                    (type(audio) == mutagen.wave.WAVE) : 
                    del audio["TXXX:COMPILATION"]
            elif type(audio) == mutagen.flac.FLAC:
                del audio["COMPILATION"]
            audio.save()
            modifyFlag = True
    #显示结果
    if modifyFlag == True:
        DisplayMeta()

def Display(path): 
    """
    显示当前目录下所有meta
    """
    global metas,plan_metas,albums 
    filesAndDir = os.listdir(path)
    # 过滤出文件（排除目录）
    files = [f for f in filesAndDir if os.path.isfile(os.path.join(path, f))]
    # 获取文件相关meta信息保存到列表
    for file in files:
        getMeta(os.path.join(path, file))
    for meta in metas:
        print(meta[0])
        for key,value in (meta[4].items()):
             print(key, value)

if __name__ == '__main__':  
    logger.info("---START---")
    # 获取当前目录
    current_directory = os.getcwd()
    cmds =sys.argv
    if len(cmds) == 1:
        traverse_dir(current_directory)
    elif len(cmds) == 2:
        if cmds[1] == "clear":
            Clear(current_directory)
        elif cmds[1] == "display":
            Display(current_directory)
        else:
            print(strHelp)
    else:
        print(strHelp)
