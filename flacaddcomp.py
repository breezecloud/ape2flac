#!/usr/bin/python3
# -*- coding:utf-8 -*-
# flacaddcomp.py
"""
遍历整个当前目录，包括子目录。扫描每个目录下的flac文件，获取元数据。如果同一目录下同一张专辑有多个artist和album的组合，则批量将每个文件加上COMPILATION=1标记，除非这个文件本来就有COMPILATION标记
"""
import os,subprocess,logging

metas,plan_metas,albums = [],[],[]

logger = logging.getLogger('flac_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别
# 创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 创建一个handler，用于输出到文件
fh = logging.FileHandler('flacaddcomp.log')
fh.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(ch)
logger.addHandler(fh)

def getMeta(file):
    #print(file)
    i = 0
    while True:
        result_cmd = subprocess.run(['metaflac', '--list',f'--block-number={i}',file], capture_output=True, text=True) #执行命令
        i = i + 1
        #print(i)
        lines = result_cmd.stdout.splitlines() #分割每一行
        if len(lines) > 0:
            if lines[1].strip() == 'type: 4 (VORBIS_COMMENT)':
                artist,album,COMPILATION = '','',''
                for line in lines:
                    result=line.partition(":")[2].partition("=")
                    if (result[0].strip().lower() == 'artist') and result[1] == '=':
                        artist = result[2].strip()
                    if (result[0].strip().lower() == 'album') and result[1] == '=':
                        album = result[2].strip() 
                    if (result[0].strip() == 'COMPILATION') and result[1] == '=':
                        COMPILATION = result[2].strip()
                if (artist != '') and (album != ''):
                    metas.append([file,artist,album,COMPILATION])
                    plan_metas.append(artist+album) 
                    albums.append(album)
                else: 
                    logger.warning(f"warning:wrong {file} meta info,no artist or album filed")
                break #get already
            else: #not VORBIS_COMMENT block
                continue
        else:#end meta block
            break

def setCompilatton(path):
    global metas,plan_metas,albums 
    metas,plan_metas,albums = [],[],[]
    # 获取当前目录下的所有文件和目录
    filesAndDir = os.listdir(path)
    # 过滤出文件（排除目录）
    files = [f for f in filesAndDir if os.path.isfile(os.path.join(path, f))]
    # 获取文件相关meta信息保存到列表
    for file in files:
        if file.split(".")[-1] == 'flac': #flac文件
            getMeta(os.path.join(path, file))
    modifyFlag = False
    if len(set(albums)) == 1: #确认目录下歌曲都是同一张专辑
        if len(set(plan_metas)) >1 :#有不同的artist和album
            for meta in metas:
                if meta[3] == '': #没有设定过COMPILATION字段
                    result = os.system(f'metaflac --set-tag="COMPILATION=1" "{os.path.join(current_directory,meta[0])}"')
                    if result != 0:
                        logger.error("error:exec "+f'metaflac --set-tag="COMPILATION=1" "{os.path.join(current_directory,meta[0])}"')
                    else:
                        modifyFlag = True
    #显示结果
    if modifyFlag == True:
        logger.info("before...")
        for meta in metas:
            logger.info(meta)   
        metas,plan_metas,albums = [],[],[] 
        for file in files:
            if file.split(".")[-1] == 'flac': #flac文件
                getMeta(os.path.join(path, file))
        logger.info("after...")
        for meta in metas:
            logger.info(meta)


def traverse_dir(path):
    #显示目录数据
    logger.info(f'Enter direct:[{path}]\n')    
    if os.path.isdir(path): #当前目录
        setCompilatton(path)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            #print("文件夹：", file_path)
            setCompilatton(file_path)
            traverse_dir(file_path)

if __name__ == '__main__':  
    logger.info("---START---")
    # 获取当前目录
    current_directory = os.getcwd()
    traverse_dir(current_directory)