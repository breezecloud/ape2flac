ape2flac脚本作用<br>
The ape2flac script acts on<br>
======

  批量将ape，wav，wx音频文件转换成flac文件，如果有cue分轨文件，将这些文件分割成单独的flac文件，同时将cue文件里的专辑、歌手、音轨、标题信息写入flac文件。脚本下载：https://github.com/breezecloud/ape2flac<br>
  Batch the ape, wav, Wx audio files into FLAC files, if there is a cue file, these files are divided into separate FLAC files, while the cue file album, singer, tracknum, title information written in the FLAC file. Script Download: https://github.com/breezecloud/ape2flac<br>

修改日志<br>
Change log<br>
======

[2025.2] 
1. 废弃了使用enca命令进行字符编码码转换，改为iconv命令转换，并增加了字符编码自动识别功能。2. 增加了日志功能，在运行目录下生成ape2flac.log日志文件以记录运行过程。3. 修正了一些bug
1. Abandoned the use of the Enca command for character encoding code conversion and replaced it with the Iconv command conversion, and added automatic character encoding recognition function. 2. Added logging function, generating ape2flac.log log files in the running directory to record the running process. 3. Fixed some bugs

为何要使用flac格式<br>
Why use FLAC format <br>
======

　　很多人有收藏的爱好，有钱的收藏古董、字画，没钱的收藏玩具、石头。我也喜欢收藏，我喜欢收藏音乐(文件)，一来不用花钱(基本网上下载)，二来也不占地方。而且还有使用价值，兴致来了拿出来欣赏欣赏。收集的多了，麻烦也随之而来。音乐文件有各种格式，mp3、wav、ape、flac、wx、m4a等等。如何管理和播放这些文件是个问题，需要播放器支持不同的音频格式，还需要支持cue分轨文件，还需要管理曲库，实在在不到很好的方案，好在原来的文件都在dvd上，也难得拿出来欣赏，到也问题不大。  
　　最近diy了一个nas，想有了这个家伙我可以把大部分的音乐文件放上去，这样随时随地就可以欣赏高品质的音乐，岂不美哉。自然而然就是想如何管理这些文件？人往往得寸进尺，当得到一点东西，马上希望能得到更多。有了nas，就想能否建立自己的音乐库，能否长期地保存这些音乐而不会因为格式太老被淘汰。  
　　以前在网上看到别人文章，说建议把收藏的音乐文件全部转换成wave，从此天下太平。因为wave是原始音频格式，肯定不会被抛弃，而且可以方便的转换成其他格式。不过wave文件实在太大，一张CD需要650M的容量，对存储容量和性能都是一个挑战。后来我觉得转换成flac也许是个更好主意。flac格式本身是开源的，不会涉及商业问题（ape格式不是开源，本人是开源铁粉），而且flac是无损格式，保证了音乐的品质。就这样，我计划写一个python脚本，可以将我硬盘里的wav、ape、wx文件转换成flac格式（不转换mp3和m4a等压缩文件是因为转换之后文件太大），并且如果有cue分轨文件，把单个文件分割成多个文件，这样对播放器的要求就很低（只需要支持flac格式）。<br>

Many people have collections of hobbies, richer collections of antiques, calligraphy and paintings, no money to collect toys and stones. I also like to collect, I like to collect music (files), one does not need to spend money (basic online download), two do not occupy space. And there is also the use value, the interest comes out to appreciate appreciation. With so much collection, trouble will follow. Music files have various formats, such as MP3, WAV, ape, FLAC, Wx, m4a and so on. How to manage and play these files is a problem, need the player to support different audio formats, also need to support the cue split file, also need to manage the music library, is not a very good solution, fortunately, the original files are on the dvd, it is rare to come out to appreciate, to the problem is not too big.

Recently DIY had a nas, and it was nice to have this guy that I could put most of the music files up so that I could enjoy high quality music anytime, anywhere. Naturally, how do you want to manage these documents? People tend to be insatiable. When they get something, they hope to get more. With nas, you wonder if you can build your own music library, and if you can keep the music for a long time without being obsolete because the format is too old.

In the past, I saw other people's articles on the internet, saying that I suggested converting all the music files into waves, and the world was peaceful from then on. Because the wave is the original audio format, it certainly won't be abandoned, and can be easily converted to other formats. But the wave file is so big that a CD needs 650M capacity, which is a challenge to storage capacity and performance. Later I thought it might be a better idea to switch to FLAC. Flac format itself is open source, will not involve commercial issues (ape format is not open source, I am open source iron powder), and FLAC is a lossless format, to ensure the quality of music. So, I plan to write a python script that converts my hard drive's wav, ape, Wx files to FLAC format (not converting MP3 and m4a compressed files because they're too large after conversion), and if there's a cue split file, splitting a single file into multiple files makes the player less demanding (only FLAC format is required. <br>

第三方软件<br>
Third party software <br>
---

顺利运行脚本需要如下第三方软件：  
1，ffmpeg，转换的核心程序，支持各种音视频格式。 <br> 
2，flac，flac编码软件  <br>
3，shntool，cue切割软件  <br>
4，unrar，rar文件解压  <br>
5，mac，Monkey's Audio Console，支持ape文件格式  <br>
6，iconv，将文件转换成utf-8格式 <br>
7，sed，修改cue文件<br>
8，cuetools，支持读取cue文件<br>
9，metaflac，支持写入flac的id[3]v2标记<br>
The smooth running script needs the following third party software:
1, ffmpeg, the core program of conversion, supports all kinds of audio and video formats.<br>
2, FLAC, FLAC encoding software<br>
3, shntool, cue cutting software<br>
4, Unrar, rar file decompression<br>
5, MAC, Monkey's Audio Console, support ape file format<br>
6, iconv, convert files to UTF-8 format.<br>
7, SED, modify the cue file.<br>
8, cuetools, support reading cue files<br>
9, metaflac, supporting id[3]v2 tags written to FLAC.<br>

安装这些软件在aurchlinux下只要执行pacman -S ffmpeg flac shntool unrar mac  cuetool metaflac。在debain下只要执行apt-get install是一样的，当然要观察执行结果，是不是每个软件都顺利安装在你的系统上。在最近的debian版本上metaflac好像已经整合在flac包了，不需要单独安装metaflac，但不知道archlinux是否相同。另外iconv命令安装不同系统可能不同安装，在debian中是按照gawk包<br>

Installing these software under aurchlinux is as long as pacman-S ffmpeg FLAC shntool Unrar MAC  cuetool metaflac is executed. As long as the apt-get install is the same under debain, of course, to observe the results of the execution, is not every software installed smoothly on your system.In the recent debian version, it seems that MetaFlac has been integrated into the Flac package, and there is no need to install MetaFlac separately, but I am not sure if ArchLinux is the same.In addition, the iconv command may be installed differently for different systems. In debian, it is installed according to the gawk package<br>

脚本的内部功能和使用<br>
The internal functions of scripts and the use of <br>
---

命令格式：  
ape2flac.py -d <directory> -h -e -n -o <br>
-d --directory 需要执行的目录  <br>
-h --help 帮助说明  <br>
-e --earse 删除转换后的文件（压缩和音频文件）  <br>
-n --notrans 不做音频文件转换，只做解压和文本文件编码转换  <br>
-o --overwrite 覆盖已存在的文件<br>
本脚本在指定的目录中完成如下操作：  <br>
1，解压缩rar文件，之所以不支持zip文件，是zip格式缺少编码信息，解压出来中文文件名可能是乱码。  <br>
2，将.txt和.cue文件的编码转换成UTF-8,如果发现cue文件中的FILE字段和实际文件不符，修改FILE字段<br>
3，转换'.ape','.flac','.wav','.wv'格式的文件到.flac文件，如果同一目录下有相同文件名的cue文件，将根据cue文件生成多个文件。同时将专辑、歌手、音轨、标题信息写入flac文件。<br>
　　第一次执行可以用-n参数，让脚本只做前面两步，然后在根据情况调整一下目录结构，如有时候太目录太深等等，根据自己情况整理成比较合适的目录结构，然后在进行实际的转换。<br>  
	
Command format:<br>
Ape2flac.py -d <directory> -h -e -n -o <br>
-d --directory directory to execute<br>
-h --help help explain<br>
-e --earse delete converted files (compressed and audio files)<br>
-n --notrans does not convert audio files, only decompression and text file conversion.<br>
-o --overwrite overwrite exist file
This script completes the following operations in the specified directory:<br>
1. decompression rar file, the reason does not support zip file, ZIP format is lack of coding information, decompressed Chinese file name may be scrambled code.<br>
2. Convert the encoding of. TXT and. cue files to UTF-8. If the FILE field in the cue file does not match the actual file, modify the FILE field<br>
3. Convert'. ape','. flac','. wav','. wv'files to. FLAC files. If a cue file with the same file name is in the same directory, multiple files will be generated from the cue file. At the same time, the album, singer, sound track and heading information are written to FLAC file.<br>
The first execution uses the - n parameter, allowing the script to do only the first two steps, then adjust the directory structure according to the situation, such as sometimes too deep directory and so on, according to their own situation into a more appropriate directory structure, and then the actual conversion. <br>

#后续设想<br>
Follow up plan for <br>
---

　　脚本运行顺利的话，无损文件都统一成flac格式，并且只要有分轨文件，都转换成每个曲目一个flac文件。下一步我会将nas设置成媒体服务器，用来管理这些音乐文件，方便进行查询和播放。如果有这样一套稳定的系统，我可以不断完善自己的音乐库信息，作为我个人的收藏。 

FLAC file for each track. Next I'll set up NAS as a media server to manage these music files for easy query and playback. If there is such a stable system, I can constantly improve their music library information, as my personal collection. 
