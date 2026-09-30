# Windows 故障知识库

## 命令未找到

### 关键词
不是内部或外部命令 not recognized command not found 命令 PATH 找不到

### 症状
- 'xxx' 不是内部或外部命令
- xxx is not recognized as an internal command

### 常见原因
- 程序未安装或未加入 PATH
- 安装后未重启终端
- 命令拼写错误

### 检查命令
- where <命令>

### 解决思路
- 将程序目录加入 PATH
- 重启终端/IDE
- 检查拼写

## PATH 环境变量配置

### 关键词
PATH 环境变量 配置 加入 变量 path 系统 设置

### 症状
- 程序无法全局使用

### 常见原因
- 程序目录未加入 PATH
- 修改后未生效

### 检查命令
- echo %PATH%

### 解决思路
- 系统属性 → 环境变量 → 编辑 Path
- 加入可执行目录
- 重启终端使变更生效

## 权限不足 / 拒绝访问

### 关键词
Access is denied 拒绝访问 权限 管理员 administrator UAC 提升

### 症状
- Access is denied / 拒绝访问
- 操作需要管理员权限

### 常见原因
- 需要管理员权限
- 文件受保护或被占用
- UAC 限制

### 检查命令
- 右键以管理员身份运行

### 解决思路
- 以管理员身份运行
- 检查文件是否只读
- 关闭安全软件拦截

## DLL 缺失

### 关键词
DLL load failed 找不到 dll 程序无法启动 vcruntime vc_redist 运行库

### 症状
- DLL load failed
- 程序无法启动，缺少 xxx.dll

### 常见原因
- 缺少 VC++ 运行库
- DLL 不在 PATH
- 32/64 位不匹配

### 检查命令
- 查看缺失 DLL 名称

### 解决思路
- 安装 VC++ Redistributable
- 将 DLL 目录加入 PATH
- 确认位数一致

## PowerShell 执行策略

### 关键词
执行策略 ExecutionPolicy 无法加载脚本 禁止 运行脚本 RemoteSigned

### 症状
- 无法加载脚本，因为禁止运行脚本

### 常见原因
- PowerShell 执行策略为 Restricted

### 检查命令
- Get-ExecutionPolicy

### 解决思路
- Set-ExecutionPolicy RemoteSigned
- 或 -Scope CurrentUser

## 端口占用

### 关键词
端口 占用 port 占用 Address already in use 8080 被占用

### 症状
- 端口被占用，服务无法启动

### 常见原因
- 其他进程占用了端口

### 检查命令
- netstat -ano | findstr <端口>

### 解决思路
- 找到占用进程 PID
- taskkill /PID <pid> /F
- 或更换端口

## 文件编码乱码

### 关键词
乱码 编码 encoding GBK UTF-8 中文 记事本

### 症状
- 中文显示乱码

### 常见原因
- 文件编码与读取编码不一致
- GBK 与 UTF-8 混淆

### 检查命令
- 用支持编码的编辑器查看

### 解决思路
- 统一使用 UTF-8
- Python 读文件指定 encoding="utf-8"

## 设置系统环境变量

### 关键词
环境变量 setx 设置 系统 永久 用户 JAVA_HOME 变量

### 症状
- 需要永久设置环境变量

### 常见原因
- 临时 set 只在当前会话生效

### 检查命令
- set / echo %变量%

### 解决思路
- 图形界面：系统属性 → 环境变量
- 命令行：setx 变量名 值
