#!/usr/bin/python
# -*- coding: UTF-8 -*-
#ape2flac.py version 0.3 by luping@shtel.com.cn
#2018.10.15

import os,sys,getopt,subprocess
from collections import namedtuple
import re


help_txt = '''
ape2flac.py -d <directory> -h -e -n -o
translate music file('.ape','.flac','.wav','.wv') into flac formate and split  multi track if have .cue file.
note:script must run in python3
-d --directory work directory
-h --help this help
-e --earse original compress and music file
-n --notrans do not translate music file,uncompress and convert utf8 only
-o --overwrite will overwrite existing files, otherwise it will skip existing files
this script search gived dfirectory and do this job:
1,uncompress .rar file with diregtory
2,translate .txt and .cue file into encode UTF-8,older file weill backup like xxx.cue.bak0
3,translate '.ape','.flac','.wav','.wv' file into .flac file(split one track file to multi track if have .cue file in same directory as same filename) and write id[3]v2 to flac file
script need som installed pacakage,for example in archlinux:pacman -S ffmpg flac shntool unzip unrar enca sed cuetools metaflac
and in debain whill using apg-get instal command.
metaflac reference:https://xiph.org/flac/documentation_tools_metaflac.html
Vorbis comment specification：https://xiph.org/vorbis/doc/v-comment.html
cueprint script reference：https://www.xuebuyuan.com/105556.html?mobile=1
'''

Music = namedtuple('Music',['artist','album','tranknum','title']) #具名元组定义音乐
del_flag = False
notrans_flag = False
overwrite_flag = False

def Validate_char(chname): #非法字符转换为_,文件名不允许出现
    #rstr1 = r"[\/\\\:\*\?\"\<\>\|\(\)\']"  # '/ \ : * ? " < > |'
    rstr = r"[\/\\\:\*\?\<\>\|\"]"  #非法字符< > / | : " * ? 
    new_chname = re.sub(rstr, "_", chname)  # 替换为下划线
    return new_chname

def Validate_filename(chname):  #命令行或者文件名中转义
    for achar in ("'",'"','*','?','~','`','!','#','$','&','|','{','}',';','<','>','^',' ','(',')','[',']'): 
        chname = chname.replace(achar,'\\' + achar)
    return chname

def Exec(cmd): #执行shell命令
    print(cmd)
    try:
        (status,output) = subprocess.getstatusoutput(cmd)
    except UnicodeDecodeError:
        print("UnicodeDecodeError......") #有时候会返回错误的unicode
        status = 100
    if status !=0:
        print("error code:"+str(status))
    else:
        print("...ok")
    return status

def Uncompress(file): #解压rar，del_flag = True 解压后删除原文件
    global del_flag
    global notrans_flag
    global overwrite_flag  
    file_ext = os.path.splitext(file)[1].lower() #文件后缀
    fname = os.path.splitext(file)[0] #无后缀文件名
    '''
    unzip会产生乱码，暂时不用
    if file_ext == '.zip':
        if Exec('unzip -o "'+ file+'" -d "'+os.path.dirname(file)+'"') ==0:
            if del_flag == True:
                os.remove(file)
    '''
    if file_ext == '.rar':
        Exec('mkdir -p '+Validate_filename(fname))
        if Exec('unrar x -y '+ Validate_filename(file)+' '+Validate_filename(fname)) ==0:
            if del_flag == True:
                os.remove(file)

def Convert_utf8(file): #转换编码为utf8
    Exec('enca -L zh_CN -x UTF-8 '+ Validate_filename(file))

def Backup_file(file):#复制文件生成.cue.bak1-99
    for i in range(100):
        if os.path.exists(file+'.bak'+str(i)):
            continue
        else:
            Exec("cp "+Validate_filename(file)+" "+Validate_filename(file)+'.bak'+str(i))
            Exec("chmod +w "+Validate_filename(file)) 
            break
          
def Convert_filename(cuefile,file): #cuefile中的file字段替换成file 
        #sed -i '0,/^FILE \".*\"/s//FILE \"xxx.ape\"/g' xxx.cue 替换第一次出现的匹配的FILE "samplefile.ape"
        file = Validate_filename(file)
        file = file.replace('\\\'','\'\\\'\'') #正则表达式遇到'，需要分段才能正确识别(如：'\'')
        Exec("sed -i '0,/^FILE \\\".*\\\"/s//FILE \\\""+file+"\\\"/g' "+Validate_filename(cuefile))
        

def get_cue_info(cuefile):#获取cue文件的信息
    tracknames=[]
    cuefile = Validate_filename(cuefile)
    print("cueprint -d '%N' "+cuefile)
    try:
        tracks=int(os.popen("cueprint -d '%N' "+cuefile).read())
    except ValueError :
        print("cueprint error in parse file:"+cuefile)
        return tracknames
    
    for id3count in range(1,tracks+1):
        try:
            martist = os.popen("cueprint -n"+str(id3count)+" -t '%p' "+cuefile).read() 
        except UnicodeDecodeError:
            print("cueprint error in parse artist of "+cuefile)
            martist = ""
        try:
            malbum  = os.popen("cueprint -n"+str(id3count)+" -t '%T' "+cuefile).read()
        except UnicodeDecodeError:
            print("cueprint error in parse album of "+cuefile)
            malbum = "" 
        try:
            mtranknum  = os.popen("cueprint -n"+str(id3count)+" -t '%02n' "+cuefile).read()
        except UnicodeDecodeError:
            print("cueprint error in parse tranknum of "+cuefile)
            mtranknum = ""                             
        try:
            mtitle  = os.popen("cueprint -n"+str(id3count)+" -t '%t' "+cuefile).read() 
        except UnicodeDecodeError:
            print("cueprint error in parse title of "+cuefile)
            mtitle = ""         
        
        if martist == "":
            try:
                martist = os.popen("cueprint -n"+str(id3count)+" -t '%P' "+cuefile).read()  
            except UnicodeDecodeError:
                print("cueprint error in parse title of "+cuefile)
                mtitle = ""              
                 
        t_music = Music(
        artist = martist,
        album  = malbum,
        tranknum  = mtranknum,
        title  = mtitle
        )
        '''
        artist[id3count]=$(cueprint -n$id3count -t ‘%p’ “$cuefile”)
        album[$id3count]=$(cueprint -n$id3count -t ‘%T’ “$cuefile”)
        tracknum[$id3count]=$(cueprint -n$id3count -t ‘%02n’ “$cuefile”)
        title[$id3count]=$(cueprint -n$id3count -t ‘%t’ “$cuefile”)
        '''  
        tracknames.append(t_music)      
    return tracknames

def Write_id3v2(file,meta):#添加id3v2标记
    file = Validate_filename(file)
    meta = Validate_filename(meta)
    #调用matefile修改id3标记
    #Exec("metaflac --set-tag='"+meta+"' "+file)
    Exec("metaflac --set-tag="+meta+" "+file)

def Set_cue_flac(file,cuefile):#设置id3v2到flac文件
    tracknames = get_cue_info(cuefile)
    for tracknum in range(len(tracknames)):
        Write_id3v2(file+"-"+('0'+str(tracknum+1))[-2:]+'.flac','ARTIST='+tracknames[tracknum].artist)
        Write_id3v2(file+"-"+('0'+str(tracknum+1))[-2:]+'.flac','ALBUM='+tracknames[tracknum].album)
        Write_id3v2(file+"-"+('0'+str(tracknum+1))[-2:]+'.flac','TRACKNUM='+tracknames[tracknum].tranknum)
        Write_id3v2(file+"-"+('0'+str(tracknum+1))[-2:]+'.flac','TITLE='+tracknames[tracknum].title)

def Convert_flac(file): #转换音频文件为flac，del_flag = True 解压后删除原文件
    global del_flag
    global notrans_flag
    global overwrite_flag  
    success_flag = False
    fname = os.path.splitext(file)[0] #无后缀文件名
    cuefile = "" 
    tracknames = []
    #查询相应的cue文件
    if os.path.exists(file+'.cue'):
        cuefile = file+'.cue'
    else:
        if os.path.exists(fname+'.cue'):
            cuefile = fname+'.cue'
        else:
            if os.path.exists(fname+'.ape.cue'): #ape转flac之后又存在cue文件
                cuefile = fname+'.ape.cue'
    if cuefile != "":
        #生成文件名前缀
        filename = os.path.splitext(os.path.basename(file))[0]
        tracknames = get_cue_info(cuefile)
        if len(tracknames)>0:
            filename = tracknames[0].album + '-'+filename[:20] #专辑名字+文件名前20字符
        filename = Validate_char(filename[:240])
        #有些cue文件的file字段和实际文件不匹配
        Convert_filename(cuefile,os.path.basename(file))
        #是否要覆盖原文件
        overwrite = 'never'
        if overwrite_flag == True:
            overwrite = 'always'
        #shntool split -t "%n.%p.%t" -f test.cue -o flac test. -d output
        #if Exec('shntool split -t "%n.%p.%t" -f "' + os.path.join(path,file)+'.cue"' + ' -o flac -O always "' +os.path.join(path,file)+'" -d "'+path+'"') == 0:
        if Exec('shntool split -t '+Validate_filename(filename)+'-%n -f ' + Validate_filename(cuefile)+' -o flac -O '+overwrite+' '+Validate_filename(file)+' -d '+Validate_filename(os.path.dirname(file))) == 0:
            success_flag = True
        else:
            if overwrite_flag == False:
             success_flag = True # overwrite==never 也会返回错误
            #flac文件写入id[3]v2
            Set_cue_flac(os.path.split(fname)[0]+os.sep+filename,cuefile)
    elif os.path.splitext(file)[1] != '.flac' :#找不到cue文件,转换为单个文件
        if (overwrite_flag == True) or (os.path.exists(fname+'.flac') == False):
            # ffmpeg -i test.ape  test.flac
            if Exec('ffmpeg -y -i '+Validate_filename(file) + ' ' + Validate_filename(fname)+'.flac') == 0:
                success_flag = True
        else:
            success_flag = True 
                
    if (del_flag) == True and (success_flag == True):
        os.remove(file)

def Convert_ape2flac(file):#直接ape转flac，del_flag = True 解压后删除原文件
    global del_flag
    global notrans_flag
    global overwrite_flag  
    file_ext = os.path.splitext(file)[1].lower()
    success_flag = False
    fname = os.path.splitext(file)[0] #无后缀文件名 
    if file_ext == '.ape':
        if (overwrite_flag == True) or  (os.path.exists(fname+'.flac') == False):
            if Exec('ffmpeg -y -i '+Validate_filename(file) + ' ' + Validate_filename(fname+'.flac')) == 0:
                success_flag = True
        else:
            success_flag = True
    if (del_flag) == True and (success_flag == True):
        os.remove(file)        

def main(argv):
    global del_flag
    global notrans_flag
    global overwrite_flag  
    #处理命令行参数
    target_dir = ""
    try:
        opts, args = getopt.getopt(argv,"henod:",["help","earse","notrans","overwrite","directory="])
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
        if opt in ("-e","--earse"):
            del_flag = True
        if opt in ("-n","--notrans"): 
            notrans_flag = True
        if opt in ("-o","--overwrite"):
            overwrite_flag = True    
    if target_dir == "":
        print(help_txt)
        sys.exit()        

    #检查需要安装的软件包
    cmds = ('ffmpeg -version','flac -version','shntool -v','unrar -v','enca -v','sed --version','metaflac --version','cueprint --version')
    for cmd in cmds:
        if Exec(cmd) != 0:
            print("one of cmomand is not run correct,run ape2flac.py -h for help")
            sys.exit(1)

    #第一次遍历目录，解压zip、rar，并移除原压缩文件;2,将cue和txt文件编码转换成UTF-8,将'.cue'文件备份为‘.cue.bak0-99’
    for path, dirs, files in os.walk(target_dir, topdown=False): 
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀
            if file_ext =='.rar':                
                Uncompress(os.path.join(path,file)) #解压到当前目录并删除原文件
            if file_ext in ('.cue','.txt'): #.cue文件复制.cue.bak0-99；.txt文件复制为.txt.bak0-99
                Backup_file(os.path.join(path,file))

    #第二次遍历目录，将cue和txt文件编码转换成UTF-8
    for path, dirs, files in os.walk(target_dir, topdown=False): 
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() #文件后缀  
            if file_ext in ('.txt','.cue'):
                Convert_utf8(os.path.join(path,file))
            if file_ext == '.ape': #基于mac和shntool的ape转换flac发现有些ape文件无法转换(可能和ape压缩版本有关)，所以提前转换成flac
                Convert_ape2flac(os.path.join(path,file))

    #第三次遍历目录，正式转换
    if notrans_flag == False:
        for path, dirs, files in os.walk(target_dir, topdown=False): 
            print("enter "+path+" starting Convert...")
            for file in files:
                file_ext = os.path.splitext(file)[1].lower() #文件后缀
                #if file_ext in ('.ape','.flac','.wav','.m4a','.mp3','.wv'): #暂时不转换m4a和mp3，转换结果太大
                if file_ext in ('.flac','.wav','.wv'): #找到需要处理文件
                    Convert_flac(os.path.join(path,file))    
            print("leave "+path+" Convert done.")
        #exit
        sys.exit(0)

if __name__ == "__main__":
    if sys.version_info.major == 3:
        main(sys.argv[1:])
    else:
        print("script must run in python3!")
