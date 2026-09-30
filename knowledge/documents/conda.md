# Conda 故障知识库

## conda 创建环境

### 关键词
conda create 创建环境 env python= name 环境 新建

### 症状
- 需要创建隔离的 conda 环境

### 常见原因
- 命令参数错误
- 网络慢导致下载失败

### 检查命令
- conda env list

### 解决思路
- conda create -n myenv python=3.10 -y
- 网络慢可配置清华 channel

## conda 激活环境失败

### 关键词
conda activate 激活 失败 CommandNotFoundError conda init powershell 执行策略

### 症状
- conda activate 报错或无效
- CommandNotFoundError: conda

### 常见原因
- conda 未初始化到当前 shell
- PowerShell 执行策略限制
- 环境名拼写错误

### 检查命令
- conda env list

### 解决思路
- conda init powershell 后重启终端
- Set-ExecutionPolicy RemoteSigned
- 核对环境名

## conda 依赖冲突 Solving environment

### 关键词
Solving environment PackagesNotFoundError 冲突 conda 依赖 resolving 慢

### 症状
- Solving environment 卡住或失败
- PackagesNotFoundError

### 常见原因
- conda 与 pip 混用导致冲突
- channel 之间包版本不一致

### 检查命令
- conda info

### 解决思路
- 优先 conda-forge：conda install -c conda-forge <包>
- 避免 conda 与 pip 反复混装
- conda update conda

## conda 命令未找到

### 关键词
conda not recognized 不是内部 命令 找不到 PATH 未安装

### 症状
- conda 不是内部或外部命令
- conda is not recognized

### 常见原因
- conda 未加入 PATH
- 安装后未重启终端

### 检查命令
- where conda

### 解决思路
- 使用 Anaconda Prompt
- 将 conda 目录加入 PATH
- 重启终端

## conda channel 慢 / 镜像

### 关键词
CondaHTTPError channel 慢 镜像 清华 conda config add channels 超时

### 症状
- CondaHTTPError
- conda 下载缓慢或超时

### 常见原因
- 默认源访问慢
- channel 配置不当

### 检查命令
- conda config --show channels

### 解决思路
- conda config --add channels 清华镜像
- 删除失效的 channel

## conda 与 pip 混用

### 关键词
conda pip 混用 冲突 环境 依赖 不一致

### 症状
- conda 环境里 pip 安装导致依赖混乱

### 常见原因
- 同一环境反复用 conda 和 pip 安装

### 检查命令
- conda list

### 解决思路
- 优先 conda 安装，缺少的再 pip
- 尽量在一个环境内保持单一安装来源

## conda 环境列表与删除

### 关键词
conda env list 删除环境 remove 环境 管理

### 症状
- 需要查看或删除 conda 环境

### 常见原因
- 环境冗余需要清理

### 检查命令
- conda env list
- conda env remove -n <环境名>

### 解决思路
- conda env list 查看
- conda env remove -n <环境名> 删除

## conda 更新与导出

### 关键词
conda update 更新 export environment.yml 导出 迁移

### 症状
- 需要更新 conda 或导出环境

### 常见原因
- conda 版本过旧
- 需要迁移/复现环境

### 检查命令
- conda update conda

### 解决思路
- conda update conda
- conda env export > environment.yml
