# CUDA / GPU 故障知识库

## nvidia-smi 无法显示显卡

### 关键词
nvidia-smi 无法显示 显卡 驱动 not recognized GPU 识别

### 症状
- nvidia-smi 不是内部或外部命令
- nvidia-smi 不显示显卡

### 常见原因
- 显卡驱动未安装或损坏
- 驱动未加入 PATH
- 显卡未正确连接

### 检查命令
- nvidia-smi

### 解决思路
- 重新安装最新 NVIDIA 驱动
- 确认驱动目录在 PATH
- 检查显卡硬件连接

## 显卡驱动安装 / 更新

### 关键词
显卡驱动 安装 更新 NVIDIA driver 驱动 官网 更新驱动

### 症状
- GPU 无法使用或性能异常

### 常见原因
- 驱动过旧或不兼容

### 检查命令
- nvidia-smi

### 解决思路
- 从 NVIDIA 官网下载最新驱动
- 选择 Game Ready 或 Studio 版本
- 干净安装后重启

## CUDA Toolkit 与驱动版本对应

### 关键词
CUDA Toolkit 驱动 版本 对应 兼容 nvidia driver CUDA 版本

### 症状
- 编译/运行 CUDA 程序报版本错误

### 常见原因
- CUDA Toolkit 要求的驱动版本高于当前驱动

### 检查命令
- nvidia-smi 查看驱动版本
- nvcc --version

### 解决思路
- 升级驱动以满足 Toolkit 要求
- 或安装较低版本的 Toolkit

## cuDNN 配置

### 关键词
cuDNN 配置 cudnn 深度学习 库 安装 环境变量

### 症状
- 深度学习框架报 cuDNN 相关错误

### 常见原因
- cuDNN 未安装或版本不匹配

### 检查命令
- 检查 cuDNN 文件是否在 CUDA 目录

### 解决思路
- 下载对应版本的 cuDNN
- 解压复制到 CUDA 安装目录
- 核对 CUDA 与 cuDNN 版本匹配

## CUDA 版本查询

### 关键词
CUDA 版本 查询 nvcc version 查看 torch.version.cuda 驱动

### 症状
- 需要确认当前 CUDA 版本

### 常见原因
- 不了解如何查看 CUDA 版本

### 检查命令
- nvcc --version
- nvidia-smi
- python -c "import torch; print(torch.version.cuda)"

### 解决思路
- nvcc --version 查看 Toolkit 版本
- nvidia-smi 查看驱动支持的最高 CUDA

## 驱动与 PyTorch 兼容

### 关键词
驱动 PyTorch 兼容 CUDA 版本 驱动版本 不匹配 GPU

### 症状
- PyTorch 检测不到 CUDA
- 运行时报 CUDA 版本错误

### 常见原因
- 驱动过旧，不支持 PyTorch 所需的 CUDA

### 检查命令
- nvidia-smi
- python -c "import torch; print(torch.version.cuda)"

### 解决思路
- 更新驱动到支持对应 CUDA 的版本
- 按官方表匹配 PyTorch 与 CUDA

## CUDA_HOME 环境变量

### 关键词
CUDA_HOME 环境变量 路径 配置 编译 cmake 找不到 CUDA

### 症状
- 编译时报找不到 CUDA 或 CUDA_HOME

### 常见原因
- 未设置 CUDA_HOME 环境变量

### 检查命令
- echo %CUDA_HOME%

### 解决思路
- 设置 CUDA_HOME 为 CUDA Toolkit 安装目录
- 或 CUDA_PATH 指向对应版本

## 多 CUDA 版本共存

### 关键词
多版本 CUDA 共存 切换 PATH 环境变量 版本 选择

### 症状
- 系统装了多个 CUDA 版本导致混乱

### 常见原因
- 多个 Toolkit 版本共存
- PATH 顺序错误

### 检查命令
- nvcc --version

### 解决思路
- 调整 PATH 中 CUDA 目录顺序
- 用 CUDA_PATH 指定目标版本
- 只保留需要的版本
