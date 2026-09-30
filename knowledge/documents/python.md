# Python 故障知识库

## ModuleNotFoundError 模块缺失

### 关键词
ModuleNotFoundError No module named 找不到模块 没有这个模块 import 模块 安装

### 症状
- No module named 'xxx'
- 程序报错找不到某个模块

### 常见原因
- 当前环境没有安装该模块
- pip 与 python 指向不同环境
- 虚拟环境未激活，或 IDE 使用了错误解释器

### 检查命令
- python --version
- where python
- python -m pip show <模块名>

### 解决思路
- 使用 python -m pip install <模块名> 安装
- 确认在正确的虚拟环境内安装
- 在 IDE 中选择正确的 Python 解释器

## ImportError 导入失败

### 关键词
ImportError cannot import name 导入失败 循环导入 相对导入

### 症状
- ImportError: cannot import name 'X'
- from xxx import yyy 报错

### 常见原因
- 模块未安装
- 循环导入（A 导入 B，B 又导入 A）
- 相对导入写错或运行入口不对

### 检查命令
- python -m pip show <模块名>
- python -c "import <模块名>"

### 解决思路
- 检查是否存在循环导入，调整依赖方向
- 修正相对导入（from . import x）
- 确保包有 __init__.py 并从项目根目录运行

## SyntaxError 语法错误

### 关键词
SyntaxError invalid syntax 语法错误 括号 冒号 expected

### 症状
- SyntaxError: invalid syntax
- SyntaxError: unexpected EOF while parsing

### 常见原因
- 括号、引号未闭合
- 冒号缺失或关键字拼写错误
- 混用中英文标点

### 检查命令
- python -m py_compile <文件.py>

### 解决思路
- 定位报错行，逐行检查括号闭合
- 检查是否缺少冒号、拼写错误
- 确保使用英文标点

## IndentationError 缩进错误

### 关键词
IndentationError unexpected indent 缩进错误 Tab 空格 expected an indented block

### 症状
- IndentationError: unexpected indent
- IndentationError: expected an indented block

### 常见原因
- 混用 Tab 与空格
- 缩进层级不一致
- 代码块内缺少缩进

### 检查命令
- 编辑器开启显示空白字符

### 解决思路
- 统一使用 4 个空格缩进
- 将 Tab 批量替换为空格
- 检查 if/for/def 后是否缩进

## TypeError 类型错误

### 关键词
TypeError 类型错误 NoneType not callable 参数 argument unsupported operand

### 症状
- TypeError: 'NoneType' object is not callable
- TypeError: unsupported operand type(s)

### 常见原因
- 对 None 调用了方法
- 函数参数类型或数量不匹配
- 对不支持的类型执行运算

### 检查命令
- print(type(x))

### 解决思路
- 调用前判断 if x is not None
- 检查函数签名与调用参数
- 用 type() 确认实际类型

## ValueError 值错误

### 关键词
ValueError 值错误 invalid literal int float 格式转换 shape

### 症状
- ValueError: invalid literal for int()
- ValueError: 数值转换失败

### 常见原因
- 字符串无法转换为数字
- 数组维度不匹配
- 传入值超出合法范围

### 检查命令
- print(repr(value))

### 解决思路
- 转换前先校验（str.isdigit() 等）
- 检查数组 shape
- 用 try/except 捕获并打印异常值

## FileNotFoundError 文件未找到

### 关键词
FileNotFoundError No such file or directory 找不到文件 路径 path 不存在

### 症状
- FileNotFoundError: No such file or directory
- 打开文件时提示文件不存在

### 常见原因
- 路径写错（相对/绝对路径混淆）
- 当前工作目录与预期不符
- 文件名或扩展名错误

### 检查命令
- os.getcwd()
- os.path.exists(path)

### 解决思路
- 使用绝对路径或 os.path.join 拼接
- 确认当前工作目录
- 检查文件名拼写与扩展名

## NameError 名称未定义

### 关键词
NameError is not defined 未定义 变量 拼写 作用域

### 症状
- NameError: name 'xxx' is not defined

### 常见原因
- 变量使用前未赋值
- 变量名拼写错误
- import 缺失或作用域问题

### 检查命令
- 检查变量赋值位置

### 解决思路
- 检查拼写是否一致
- 使用前先定义变量
- 在文件顶部补充 import

## PermissionError 权限错误

### 关键词
PermissionError Errno 13 权限 denied 拒绝 文件占用 只读

### 症状
- PermissionError: [Errno 13] Permission denied

### 常见原因
- 文件被其他程序占用
- 没有读写权限
- 路径指向目录而非文件

### 检查命令
- 关闭占用文件的程序

### 解决思路
- 关闭占用进程后重试
- 以管理员身份运行
- 确认路径指向文件而非目录

## 虚拟环境 venv

### 关键词
venv virtualenv 虚拟环境 activate 激活 隔离 环境 解释器

### 症状
- 不同项目依赖互相干扰
- 需要隔离依赖环境

### 常见原因
- 未创建或未激活虚拟环境
- 在错误环境下安装了依赖

### 检查命令
- python -m venv venv
- venv\Scripts\activate（Windows）

### 解决思路
- 创建：python -m venv venv
- 激活：venv\Scripts\activate
- 激活后再安装依赖
