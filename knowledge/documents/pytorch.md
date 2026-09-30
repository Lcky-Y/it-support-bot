# PyTorch 故障知识库

## torch.cuda.is_available() 返回 False

### 关键词
torch cuda is_available False 检测不到 GPU 显卡 不可用 cu118 cu121 cpu

### 症状
- torch.cuda.is_available() 返回 False
- nvidia-smi 能显示显卡但 PyTorch 检测不到

### 常见原因
- 安装了 CPU 版 PyTorch
- 显卡驱动过旧
- PyTorch 与 CUDA 版本不匹配

### 检查命令
- nvidia-smi
- python -c "import torch; print(torch.__version__)"
- python -c "import torch; print(torch.version.cuda)"

### 解决思路
- 安装对应 CUDA 版：python -m pip install torch --index-url https://download.pytorch.org/whl/cu121
- 更新显卡驱动
- 核对 torch.__version__ 是否含 +cuXXX

## CUDA out of memory

### 关键词
CUDA out of memory OOM 显存不足 memory batch 模型 释放

### 症状
- CUDA out of memory
- 训练/推理时显存不足

### 常见原因
- batch size 过大
- 模型过大
- 显存被其他进程占用

### 检查命令
- nvidia-smi

### 解决思路
- 减小 batch size
- torch.cuda.empty_cache()
- 使用混合精度 AMP

## CUDA 运行时错误

### 关键词
CUDA error device-side assert illegal memory kernel launch 报错

### 症状
- CUDA error: device-side assert triggered
- CUDA error: illegal memory access

### 常见原因
- 驱动与 PyTorch 版本不匹配
- 索引越界或数据不合法
- 多进程并发冲突

### 检查命令
- nvidia-smi
- python -c "import torch; print(torch.version.cuda)"

### 解决思路
- 更新显卡驱动
- 检查数据索引是否越界
- 重启 Python 进程

## PyTorch 安装 CPU / CUDA

### 关键词
安装 torch pytorch install CPU CUDA 官网 cu121 命令

### 症状
- 需要安装 PyTorch

### 常见原因
- 需按是否有 NVIDIA 显卡选择版本

### 检查命令
- nvidia-smi

### 解决思路
- CPU：python -m pip install torch
- CUDA：python -m pip install torch --index-url https://download.pytorch.org/whl/cu121
- 安装后验证 torch.cuda.is_available()

## torch 与 CUDA 版本不匹配

### 关键词
版本不匹配 version mismatch torch cuda 兼容 torchvision 版本

### 症状
- torch 加载 CUDA 报错
- torchvision 与 torch 版本不兼容

### 常见原因
- PyTorch 的 CUDA 版本与驱动不匹配
- torch 与 torchvision 版本不对应

### 检查命令
- python -c "import torch; print(torch.__version__, torch.version.cuda)"

### 解决思路
- 按 PyTorch 官网选择匹配版本重装
- torchvision 版本与 torch 对应

## 模型加载失败

### 关键词
模型 加载 失败 load_state_dict checkpoint 权重 keys mismatch map_location

### 症状
- 加载模型权重报错
- state_dict keys mismatch

### 常见原因
- checkpoint 路径错误或损坏
- 模型结构变化
- 保存/加载设备不一致

### 检查命令
- 确认文件存在与大小
- print(model.state_dict().keys())

### 解决思路
- torch.load(path, map_location='cpu')
- 用 strict=False 忽略不匹配的键
- 核对模型结构

## 多卡 / DataParallel

### 关键词
多卡 DataParallel DistributedDataParallel DDP 多GPU device 显卡

### 症状
- 多 GPU 训练报错或速度不理想

### 常见原因
- 设备分配错误
- 单卡多卡用法不同

### 检查命令
- nvidia-smi 确认可用 GPU

### 解决思路
- 单卡：model.to('cuda')
- 多卡：nn.DataParallel 或 DDP
- 显存不足时减小 batch

## 梯度未释放 / 缓存

### 关键词
梯度 释放 detach requires_grad 缓存 empty_cache 内存增长

### 症状
- 显存持续增长不释放

### 常见原因
- 中间变量保留计算图
- 未清理缓存

### 检查命令
- nvidia-smi 观察显存

### 解决思路
- 用 torch.no_grad() 包裹推理
- 及时 .detach() 中间变量
- torch.cuda.empty_cache()

## torch 与 torchvision 版本对应

### 关键词
torchvision torch 版本 对应 不兼容 install 依赖

### 症状
- 安装 torchvision 后 import 报错

### 常见原因
- torchvision 版本与 torch 不匹配

### 检查命令
- python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"

### 解决思路
- 按官方对应关系安装匹配版本
- 重新安装 torch 与 torchvision
