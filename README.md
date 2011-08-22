JS/CSS Compressor
==================================================
js-css-compressor is a python program to compress and combine js/css files.

How to use js-compressor.py:
----------
run the js-compressor.py like this:
    python js-compressor.py done.js http://xxx.com/12.js;http://aa.com/13.js
OR
    python js-compressor.py done.js http://xxx.com/22.js
OR
    python js-compressor.py done.js localfile.js;localfile2.js
OR
    python js-compressor.py done.js localfile.js

 - the done.js is the filename which store the data after compress and combine.
 - The first style will compress and combine the two javascript files
 - The second style just compress the single file.

-----------

The ali-compressor.py script just for the china alibaba's guys, so just explain it with chinese.


使用方法：
----------
在支持 pyton  的机器上以下列方式运行此程序：
    python js-compressor.py done.js http://xxx.com/12.js;http://aa.com/13.js
或
    python js-compressor.py done.js http://xxx.com/22.js
或
    python js-compressor.py done.js localfile.js;localfile2.js
或
    python js-compressor.py done.js localfile.js

 - 命令中的 done.js 是压缩后的文件名，可以自己命名。
 - 第一种方式，会压缩并且合并这两个文件。
 - 第二种方式，只会压缩一个文件。

ali-compressor 使用方法：
----------
在支持 python 的机器上以下列方式运行此程序：
    python ali-compressor.py somefile.js
或
    python ali-compressor.py somefile-merge.js

脚本会根据文件内容判断此文件是 merge 文件，还是普通的 js 文件。

如果是普通文件，仅仅压缩它，并且在同目录存储为 {filename}-min.js 

如果是 merge 文件，会找出此文件中所有不以 -min.js 结尾的被 merge 文件，然后询问是否需要压缩。
对需要压缩的文件，进行压缩，并在被 merge 文件同目录存储为 {filename}-min.js，
同时修改 merge 文件中此文件的地址为 {filename}-min.js 版本 

注意：js文件需要按照规范，文本编码为GBK

说明：
----------
这个压缩工具使用的是 [closure compiler](http://closure-compiler.appspot.com/) 提供的服务。 

由于那个可恶的防火墙的原因, closure compiler REST API 并不是那么容易访问，于是在 ali-compressor.py 中，使用了我自己搭建的一个反向代理来提供此服务。
js-compress.py 没有做替换，需要的话可以自己参照 ali-cimpressor.py 做替换。
