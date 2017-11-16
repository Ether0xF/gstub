# GStub

接收并扫描.c文件中的C代码，抽取出其中所有的函数定义并生成单元测试使用的桩函数。

## 1. 安装

### 使用exe文件安装

- 双击exe文件即可

## 使用模块包安装

- 解压zip压缩包
- 进入解压出来的文件夹
- 在命令行窗口中输入`python setup.py install`



## 2. 使用

进入需要生成桩函数的.c文件所在目录，在命令行窗口执行以下命令：

`gstub [option] <filename>` 或 `gsb [option] <filename>`

目前可用Option:

​	-h --help 打印help信息

​	-v --version 打印版本号

​	--debug	打印解析的调试信息



## 3. TODO

- 接收路径扫描当前路径下所有.c文件
- 后续debug维护