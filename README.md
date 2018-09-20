ape2flac脚本作用<br>
======

  批量将ape，wav，wx音频文件转换成flac文件，如果有cue分轨文件，将这些文件分割成单独的flac文件。脚本下载：https://github.com/breezecloud/ape2flac<br>

为何要使用flac格式<br>
======

  很多人有收藏的爱好，有钱的收藏古董、字画，没钱的收藏玩具、石头。我也喜欢收藏，我喜欢收藏音乐(文件)，一来不用花钱(基本网上下载)，二来也不占地方。而且还有使用价值，兴致来了拿出来欣赏欣赏。收集的多了，麻烦也随之而来。音乐文件有各种格式，mp3、wav、ape、flac、wx、m4a等等。如何管理和播放这些文件是个问题，需要播放器支持不同的音频格式，还需要支持cue分轨文件，还需要管理曲库，实在在不到很好的方案，好在原来的文件都在dvd上，也难得拿出来欣赏，到也问题不大。  
  最近diy了一个nas，想有了这个家伙我可以把大部分的音乐文件放上去，这样随时随地就可以欣赏高品质的音乐，岂不美哉。自然而然就是想如何管理这些文件？人往往得寸进尺，当得到一点东西，马上希望能得到更多。有了nas，就想能否建立自己的音乐库，能否长期地保存这些音乐而不会因为格式太老被淘汰。  
  以前在网上看到别人文章，说建议把收藏的音乐文件全部转换成wave，从此天下太平。因为wave是原始音频格式，肯定不会被抛弃，而且可以方便的转换成其他格式。不过wave文件实在太大，一张CD需要650M的容量，对存储容量和性能都是一个挑战。后来我觉得转换成flac也许是个更好主意。flac格式本身是开源的，不会涉及商业问题（ape格式不是开源，本人是开源铁粉），而且flac是无损格式，保证了音乐的品质。就这样，我计划写一个python脚本，可以将我硬盘里的wav、ape、wx文件转换成flac格式（不转换mp3和m4a等压缩文件是因为转换之后文件太大），并且如果有cue分轨文件，把单个文件分割成多个文件，这样对播放器的要求就很低（只需要支持flac）。<br>

第三方软件<br>
---

顺利运行脚本需要如下第三方软件：  
1，ffmpeg，转换的核心程序，支持各种音视频格式。  
2，flac，flac编码软件  
3，shntool，cue切割软件  
4，unrar，rar解压  
5，mac，Monkey's Audio Console，支持ape文件格式  
6，enca，将文件转换成utf-8格式  
安装这些软件在aurchlinux下只要执行pacman -S ffmpeg flac shntool unrar mac enca。在debain下只要执行apt-get install是一样的，当然要观察执行结果，是不是每个软件都顺利安装在你的系统上。<br>

脚本的内部流程和使用<br>
---

命令格式：  
ape2flac.py -d <directory> -h -u -n  
-d --directory 需要执行的目录  
-h --help 帮助说明  
-u --undele 不删除转换后的文件（压缩和音频文件）  
-n --notrans 不做音频文件转换，只做解压和文本文件编码转换  
本脚本在指定的目录中完成如下操作：  
1，解压缩rar文件，之所以不支持zip文件，是zip格式解压出来中文文件名是乱码。  
2，将.txt和.cue文件的编码转换成UTF-8  
3，转换'.ape','.flac','.wav','.wv'格式的文件到.flac文件，如果同一目录下有相同文件名的cue文件，将根据cue文件生成多个文件。  
第一次执行可以用-n参数，让脚步只做前面两步，然后在根据情况调整一下目录结构，如有时候太目录太深等等，根据自己情况整理成比较合适的目录结构，然后在进行实际的转换。如果没有备份，可以先用-u参数不删除转换或者解压之前的文件。<br>  
	
#后续设想<br>
---

脚本运行顺利的话，无损文件都统一成flac格式，并且只要有分轨文件，都转换成每个曲目一个flac文件。下一步我会将nas设置成媒体服务器，用来管理这些音乐文件，方便进行查询和播放。如果有这样一套稳定的系统，我可以不断完善自己的音乐库信息，作为我个人的收藏。  
