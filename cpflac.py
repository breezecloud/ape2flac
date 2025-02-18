#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#ape2flacbat.py version 0.1 by luping.sh@chinatelecom.cn
#2024.4.5
#对应ape2flacbat脚本，可以将转换好的flac复制到原目录，并且删除原理的ape文件
 
import os,sys,subprocess,logging
def Exec(cmd): #执行shell命令
    print(cmd)
    try:
        (status,output) = subprocess.getstatusoutput(cmd)
    except UnicodeDecodeError:
        print("UnicodeDecodeError......") #有时候会返回错误的unicode
        status = 100
    if status !=0:
        logging.error("error code:"+str(status))
    else:
        print("...ok")
    return status

def main(argv):
    print("cpflac.py program start...")
    logging.basicConfig(level=logging.DEBUG, filename='cpflac.log', filemode='a')
    target="/s_music"
    source="/d_music"
    for path,dirs,files in os.walk(source,topdown=False):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀
            if file_ext in('.flac'):
                fname = os.path.splitext(file)[0] #无后缀文件名
                source_file = os.path.join(path,file)
                target_dir = os.path.join(path.replace(source,target,1))
                target_ape = os.path.join(target_dir,fname+".ape")
                # print("source_file:",source_file,"\n")
                # print("target_dir:",target_dir,"\n")
                # print("target_ape",target_ape,"\n")
                if not os.path.exists(os.path.join(target_dir,fname+".flac")):
                    if Exec('cp -f  "'+source_file + '" "' + target_dir+'"') != 0:
                        logging.error("errr in copy for:"+source_file)
                        sys.exit(1)
                    else:
                        logging.info("copy for:"+source_file)
                        if os.path.exists(target_ape):
                            if Exec('rm -f "'+target_ape+'"') !=0:
                                logging.warn("rm file is error:"+target_ape)
                else:
                    logging.warn("file exists:"+os.path.join(target_dir,fname+".flac")," skip")

if __name__ == "__main__":
    if sys.version_info.major == 3:
        main(sys.argv[1:])
    else:
        print("script must run in python3!")