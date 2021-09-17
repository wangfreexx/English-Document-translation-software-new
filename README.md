英文即时划词翻译软件
=======
本项目fork了但又没有整体fork，所以未能直接分支，另外开了一个

原始地址
<[git@github.com:zhangcf0110/English-Document-translation-software.git](https://github.com/zhangcf0110/English-Document-translation-software)>

修正了以下问题：

* 谷歌翻译器年久失修
* pdfjs年久失修导致复制出现问题
* 历史记录用config.txt容易误解
* 重新打包了软件

优化或者添加了以下东西：

* 添加了百度翻译和腾讯翻译
* 打包了exe放在dist下，由于单个文件太大，因此将其分卷压缩了，解压到dist目录即可使用



集成阅读器和翻译器于一体，边看边翻译。采用谷歌引擎，准确高效。UI界面干净纯粹，拒绝花里胡哨。
------
<div align=center><img src="https://github.com/zhangcf0110/English-Document-translation-software/blob/master/illustration_image/%E6%B5%81%E7%A8%8B%E5%9B%BE.png" width = "700" height = "400" alt="" ></div>


<div align=center>软件使用说明可看:(https://www.bilibili.com/video/BV1Jt4y1y7eU/) </div>


----------------------------------------------------------------------
<div align=center><font  face="黑体" size=10>如果觉得还行可以点加星呀！哈哈哈</font></div>


## 1.开发背景

>（1）随着全球化的不断深入，如何快速、准确地实现中、英文这两种使用人数最多、范围最广的文字互译变得尤为重要。

>（2）当前普通社会公民、公司研发人员、科研研究者、高校学生等英语水平参差不齐，英文阅读成为很多人获取信息、学习知识、科学研究道路上的拦路虎，严重影响工作、学习效率。

>（3）调研目前能够实现英汉互译的软件及平台多为在线翻译，需要`从文档阅读器中手动的将需要翻译的内容复制到在线翻译网址`，阅读者`需要同时开启文档阅读器及网络浏览器两个应用进程`，不仅占用计算机内存资源，而且需来回切换、多步操作，以致容易出错，效率低下。

>（4）利用在线翻译时，如`若复制的内容格式有误，需要自己手动调整，进行回车或者删格等操作，费事耗力`。

## 2.软件特点
>（1）**无需安装，随开随用**。
 
>（2）**将能够阅读常规的文本如PDF、word类型的阅读器和英汉划词互译功能集成到一个软件中**。避免使用者为了实现翻译功能，既要打开文件阅读器，又要打开在线翻译网址的麻烦，同时能够节省计算机内存等资源的使用，提高使用者工作、学习效率。
 
>（3）**增加文字预处理模块，最大程度降低由于原文本格式问题导致翻译不准确**。无需阅读者手动调整，就能获得高质量的翻译结果。

>（4）通过**监听鼠标的实时状态自动的实现复制和翻译的功能，实现真正意义上的划词中英文互译**，省去外文文献、资料阅读者将需要翻译的内容右击复制到在线翻译网址中去这无意义的繁琐操作。

## 3.设计结构

<div align=center><img src="https://github.com/zhangcf0110/English-Document-translation-software/blob/master/illustration_image/%E7%BB%98%E5%9B%BE1.jpg" width = "350" height = "350" alt="设计结构" ></div>

## 4.需要改进

> (1)一键隐藏功能还有bug。

> (2) 可以添加将PDF转WORD功能。

