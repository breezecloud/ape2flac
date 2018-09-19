#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands,os,sys,getopt

help_txt = '''
ape2flac.py -d <directory> -h -u -n
translate music file('.ape','.flac','.wav','.wv') into flac formate and split  multi track if have .cue file
-d --directory work directory
-h --help this help
-u --undel undelete original compress and music file
-n --notrans do not translate music file,uncompress and convert utf8 only

this script search gived directory and do this job:
1,uncompress .rar file
2,translate .txt and .cue file into encode UTF-8
3,translate '.ape','.flac','.wav','.wv' file into .flac file(split one track file to multi track if have .cue file in same directory as same filename)
script need install some pacakage,for example in archlinux:pacman -S ffmpg flac shntool unzip unrar mac enca
and in debain whill using apg-get instal command.
'''

def Exec(cmd):
#执行外部命令
    print("exec:"+cmd)
    (status,output) = commands.getstatusoutput(cmd)
    if (cmd == 'mac') and (status ==65280): #mac命令无法正常返回0
        status = 0 
    if status !=0:
        print("error in exec:"+ cmd+" return error code:"+str(status))
    return status

def Uncompress(path,file,undel_flag):
    file_ext = os.path.splitext(file)[1].lower() #文件后缀
    fname = os.path.splitext(file)[0] #无后缀文件名
    '''
    unzip会产生乱码，暂时不用
    if file_ext == '.zip':
        if Exec('unzip -o "'+ os.path.join(path,file)+'" -d "'+fname+'"') ==0:
            if undel_flag == False:
                os.remove(os.path.join(path,file))
    '''
    if file_ext == '.rar':
        if Exec('unrar x -y "'+ os.path.join(path,file)+'" "'+os.path.join(path,fname)+'"/') ==0:
            if undel_flag == False:
                os.remove(os.path.join(path,file))

def Convert_utf8(path,file):
    file_ext = os.path.splitext(file)[1].lower() #文件后缀
    fname = os.path.splitext(file)[0] #无后缀文件名
    if file_ext in ('.cue','.txt'):
        Exec('enca -L zh_CN -x UTF-8 "'+ os.path.join(path,file)+'"')

def Convert_flac(path,file,undel_flag):
    fname = os.path.splitext(file)[0] #无后缀文件名 
    #查询相应的cue文件
    if os.path.exists(os.path.join(path,file)+'.cue'):
        #shntool split -t "%n.%p.%t" -f test.cue -o flac test. -d output
        Exec('shntool split -t "%n.%p.%t" -f "' + os.path.join(path,file)+'.cue"' + ' -o flac -O always "' +os.path.join(path,file)+'" -d "'+path+'"')
    else:
        if os.path.exists(os.path.join(path,fname)+'.cue'): 
            Exec('shntool split -t "%n.%p.%t" -f "'+ os.path.join(path,fname)+'.cue"' + ' -o flac -O always "' +os.path.join(path,file)+'" -d "'+path+'"')
        elif os.path.splitext(file)[1] != '.flac' :#找不到cue文件,转换为单个文件
            # ffmpeg -i test.ape  test.flac
            Exec('ffmpeg -i "'+os.path.join(path,file) + '" "' + os.path.join(path,fname)+'.flac"')
    if undel_flag == False:
        os.remove(os.path.join(path,file))

def main(argv):
    #处理命令行参数
    undel_flag = False
    notrans_flag = False
    target_dir = ""
    try:
        opts, args = getopt.getopt(argv,"hund:",["help","undel","notrans","directory="])
    except getopt.GetoptError:
        print(help_txt)
        sys.exit(2)       
    if len(argv) < 1:
        print(help_txt)
        sys.exit(2)          
    for opt, arg in opts:
        if (opt in ("-h","--help")):
            print(help_txt)
            sys.exit()
        if opt in ("-d","--directory"):
            target_dir = arg
        if opt in ("-u","--undel"):
            undel_flag = True
        if opt in ("-n","--notrans"): 
            notrans_flag = True     
    if target_dir == "":
        print(help_txt)
        sys.exit()        

    #检查需要安装的软件包
    cmds = ('ffmpeg -version','flac -version','shntool -v','unzip -v','unrar -v','mac','enca -v')
    for cmd in cmds:
        if Exec(cmd) != 0:
            print("one of cmomand is not run correct,run ape2flac.py -h for help")
            sys.exit(1)

    #第一次遍历目录，下解压zip、rar，并移除原压缩文件;2,将cue和txt文件编码转换成UTF-8
    for path, dirs, files in os.walk(target_dir, topdown=False): 
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀
            if file_ext =='.rar':
                Uncompress(path,file,undel_flag) #解压到当前目录并删除原文件

    #第二次遍历目录，将cue和txt文件编码转换成UTF-8
    for path, dirs, files in os.walk(target_dir, topdown=False): 
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀  
            if file_ext in ('.txt','.cue'):
                Convert_utf8(path,file)

    #第三次遍历目录，正式转换
    if notrans_flag == False:
        for path, dirs, files in os.walk(target_dir, topdown=False): #
            print("enter "+path+" starting Convert...")
            for file in files:
                file_ext = os.path.splitext(file)[1].lower() #文件后缀
                #if file_ext in ('.ape','.flac','.wav','.m4a','.mp3','.wv'): #暂时不转换m4a和mp3，转换结果太大
                if file_ext in ('.ape','.flac','.wav','.wv'): #找到需要处理文件
                    Convert_flac(path,file,undel_flag)    
            print("leave "+path+",Convert done.")
        #exit
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
