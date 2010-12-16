JS/CSS Compressor
==================================================
js-css-compressor is a python program to compress and combine js/css files.

How to use it:
----------
run the js-compressor.py like this
    python js-compressor.py done.js http://xxx.com/12.js;http://aa.com/13.js
OR
    python js-compressor.py done.js http://xxx.com/22.js

 - the done.js is the filename which store the data after compress and combine.
 - The first style will compress and combine the two javascript files
 - The second style just compress the single file.


使用方法：
----------
在支持pyton  的机器上以下列方式运行此程序：
    python js-compressor.py done.js http://xxx.com/12.js;http://aa.com/13.js
或者
    python js-compressor.py done.js http://xxx.com/22.js

 - 命令中的 done.js 是压缩后的文件名，可以自己命名。
 - 第一种方式，会压缩并且合并这两个文件。
 - 第二种方式，只会压缩一个文件。


说明：
----------
这个压缩工具使用的是 [closure compiler](http://closure-compiler.appspot.com/) 提供的服务。