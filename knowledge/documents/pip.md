# pip 故障知识库

## pip 找不到可安装的包

### 关键词
Could not find a version that satisfies No matching distribution pip install 找不到包 包名

### 症状
- ERROR: Could not find a version that satisfies the requirement xxx
- ERROR: No matching distribution found for xxx

### 常见原因
- 包名拼写错误
- 当前源没有该包（私有包需指定源）
- Python 版本不兼容

### 检查命令
- python --version
- python -m pip search <包名>（旧版）

### 解决思路
- 核对包名拼写
- 指定国内镜像源
- 确认 Python 版本满足要求

## pip 依赖冲突

### 关键词
conflicting dependencies dependency conflict 版本冲突 incompatible resolver 依赖

### 症状
- 安装时提示 conflicting dependencies
- 多个包要求同一依赖的不同版本

### 常见原因
- 包版本要求互相冲突
- requirements.txt 版本固定过死
- 已安装版本与需求不兼容

### 检查命令
- python -m pip check

### 解决思路
- 用 pip check 查看冲突
- 调整 requirements.txt 版本约束
- 使用虚拟环境隔离

## pip SSL 证书错误

### 关键词
SSL SSLError CERTIFICATE_VERIFY_FAILED 证书 verify pip install 镜像 trusted-host

### 症状
- SSLError: CERTIFICATE_VERIFY_FAILED
- pip 安装时报 SSL 证书错误

### 常见原因
- 公司代理/防火墙替换证书
- 系统时间不对
- 镜像源证书不受信任

### 检查命令
- 校正系统时间

### 解决思路
- 使用国内镜像源
- 加 --trusted-host 跳过校验（仅可信源）
- 校正系统时间

## pip 安装超时

### 关键词
timed out ReadTimeout ConnectTimeout 超时 pip install 下载 镜像 慢

### 症状
- pip 安装时长时间无响应或超时

### 常见原因
- 默认源访问慢
- 网络不稳定或代理限制
- 包体积大

### 检查命令
- 检查网络与代理设置

### 解决思路
- 切换国内镜像源
- 增大超时 --default-timeout=100
- 检查代理配置

## pip 权限错误

### 关键词
Permission denied Access is denied 权限 拒绝 --user 管理员 WinError 5

### 症状
- Permission denied / Access is denied
- 向系统目录安装包失败

### 常见原因
- 无管理员权限
- 目标目录只读或被占用

### 检查命令
- 确认是否以管理员运行终端

### 解决思路
- 以管理员身份运行终端
- 使用 pip install --user <包>
- 在虚拟环境内安装

## pip 国内镜像源配置

### 关键词
镜像 源 换源 清华 阿里 index-url pypi.tuna 加速 慢

### 症状
- pip 安装缓慢或超时

### 常见原因
- 默认 PyPI 源在国内访问慢

### 检查命令
- pip config list

### 解决思路
- 临时：pip install -i <镜像>
- 永久：pip config set global.index-url <镜像>
- 清华：https://pypi.tuna.tsinghua.edu.cn/simple

## pip 与 python 环境不一致

### 关键词
环境不一致 python pip 不同环境 where python 解释器 装错

### 症状
- 安装了包但 import 仍报 ModuleNotFoundError
- pip 与 python 指向不同解释器

### 常见原因
- 系统存在多个 Python
- 虚拟环境未激活
- IDE 使用不同解释器

### 检查命令
- where python
- python -m pip --version

### 解决思路
- 始终用 python -m pip 安装
- 激活目标虚拟环境
- IDE 选择正确解释器

## requirements.txt 安装

### 关键词
requirements.txt 依赖 requirements install -r 批量安装

### 症状
- 需要批量安装项目依赖

### 常见原因
- 不知道如何安装 requirements.txt

### 检查命令
- 查看 requirements.txt 内容

### 解决思路
- python -m pip install -r requirements.txt
- 在虚拟环境内执行

## pip 升级自身

### 关键词
pip 升级 upgrade pip 版本 self-update 更新

### 症状
- pip 版本过旧导致功能异常

### 常见原因
- 长期未更新 pip

### 检查命令
- python -m pip --version

### 解决思路
- python -m pip install --upgrade pip

## wheel 安装失败

### 关键词
wheel whl 安装失败 离线安装 .whl 平台

### 症状
- 安装 .whl 文件报错

### 常见原因
- wheel 与 Python 版本或平台不匹配
- 文件名标签不对应

### 检查命令
- 查看 .whl 文件名中的 cp 与平台标签

### 解决思路
- 选择匹配的 wheel（cp311 / win_amd64 等）
- pip install <文件路径>.whl
