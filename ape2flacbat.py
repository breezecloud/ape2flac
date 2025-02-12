#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#ape2flacbat.py version 0.1 by luping.sh@chinatelecom.cn
#2024.4.5
#脚本读入source目录的所有文件，如果是ape格式的文件，在相应的target目录转换一个对应目录的flac文件。
import os,sys,subprocess,logging
def Exec(cmd): #执行shell命令
    print(cmd)
    try:
        (status,output) = subprocess.getstatusoutput(cmd)
    except UnicodeDecodeError:
        print("UnicodeDecodeError......") #有时候会返回错误的unicode
        status = 0
    if status !=0:
        logging.error("error code:"+str(status))
    else:
        print("...ok")
    return status

def main(argv):
    print("cpfilter.py program start...")
    logging.basicConfig(level=logging.DEBUG, filename='ape2flacbat.log', filemode='a')
    source="/s_music"
    target="/d_music"
    for path,dirs,files in os.walk(source,topdown=False):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀
            if file_ext in('.ape'):
                fname = os.path.splitext(file)[0] #无后缀文件名
                source_file = os.path.join(path,file)
                target_dir = os.path.join(path.replace(source,target,1))
                target_file = os.path.join(target_dir,fname+".flac")
                #print("source:",source_file,"\n")
                #print("target:",target_file,"\n")
                #print("target_dir",target_dir,"\n")
                if Exec('mkdir -p '+'"'+target_dir+'"') != 0:
                   logging.error("errr in makdir for"+target_dir)
                   sys.exit(1)
                if os.path.exists(target_file):
                    logging.warn(target_file+" is exist,skip")
                elif Exec('ffmpeg -y -i "'+source_file + '" "' + target_file+'"') != 0:
                    logging.error("errr in ffmpeg for"+target_file)
                    sys.exit(1)
                else:
                    logging.info("success in ffmpeg for"+target_file)
                     

if __name__ == "__main__":
    if sys.version_info.major == 3:
        main(sys.argv[1:])
    else:
        print("script must run in python3!")
