# Docker 故障知识库

## Docker daemon 未运行

### 别名
docker 启动失败 无法连接 docker daemon 守护进程没起来 docker 服务未启动

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
服务启动失败

### 错误类型
docker_daemon_not_running

### 关键词
docker daemon cannot connect 连接失败 守护进程 is the docker daemon running

### 症状
- Cannot connect to the Docker daemon at unix:///var/run/docker.sock
- error during connect: Get http://%2F%2F.%2Fpipe%2Fdocker_engine: open //./pipe/docker_engine: 系统找不到指定的文件
- docker ps 报错连接不上

### 常见原因
- Docker 服务未启动
- Docker Desktop 未运行
- 当前用户无权限访问 docker.sock

### 检查命令
- docker info
- systemctl status docker
- docker ps

### 解决思路
- 启动服务：systemctl start docker（Linux）
- 打开 Docker Desktop 并等待其就绪（Windows / macOS）
- 将用户加入 docker 组后重新登录

## Docker Desktop 启动失败

### 别名
docker desktop 打不开 docker 客户端启动报错

### 平台
windows macos

### 技术栈
docker

### 故障类型
服务启动失败

### 错误类型
docker_desktop_start_failed

### 关键词
docker desktop 启动失败 打不开 无法启动 engine

### 症状
- Docker Desktop 启动后一直转圈
- 提示 Docker Desktop failed to start
- 报错 Docker Engine stopped

### 常见原因
- 虚拟化 / WSL2 未启用
- 版本与系统不兼容
- 残留进程占用端口

### 检查命令
- wsl --status
- 任务管理器查看 Docker 进程

### 解决思路
- 启用虚拟化（BIOS 中开启）与 WSL2
- 重启 Docker Desktop 或完全退出后重启
- 升级或重装 Docker Desktop

## 拉取镜像超时或缓慢

### 别名
docker pull 慢 拉镜像 拉镜像卡住 下载镜像超时 pull 不动 拉不下来

### 平台
windows linux macos

### 技术栈
docker registry

### 故障类型
网络问题

### 错误类型
docker_pull_timeout

### 关键词
docker pull timeout 超时 慢 卡住 下载 retrying

### 症状
- Get https://registry-1.docker.io/v2/: dial tcp: i/o timeout
- 拉取镜像一直 retrying in Xs
- 下载速度极慢

### 常见原因
- 默认 Docker Hub 源在国内访问慢
- 网络代理 / 防火墙影响
- DNS 解析问题

### 检查命令
- docker info | grep Registry
- curl https://registry-1.docker.io/v2/

### 解决思路
- 配置国内镜像加速器（在 daemon.json 里加 registry-mirrors）
- 重启 docker 服务后重试
- 配置代理或更换网络

## 拉取镜像认证失败

### 别名
docker pull 认证失败 拉镜像 401 unauthorized 登录过期

### 平台
windows linux macos

### 技术栈
docker registry

### 故障类型
认证失败

### 错误类型
docker_pull_auth_failed

### 关键词
pull unauthorized 401 authentication required 认证失败 login

### 症状
- unauthorized: authentication required
- 拉取私有镜像提示 401
- Error response from daemon: pull access denied

### 常见原因
- 未登录私有仓库
- 凭证过期或错误
- 仓库权限不足

### 检查命令
- docker login <registry>
- docker info

### 解决思路
- 先 docker login 指定仓库地址
- 确认账号密码 / token 正确
- 联系管理员开通仓库拉取权限

## 镜像不存在或无法找到

### 别名
docker 镜像不存在 pull 找不到 manifest 未找到 tag 不存在

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
资源不存在

### 错误类型
docker_image_not_found

### 关键词
pull not found manifest unknown 镜像不存在 tag

### 症状
- manifest unknown
- Error: No such image
- Error response from daemon: pull access denied / not found

### 常见原因
- 镜像名或 tag 拼写错误
- 镜像确实不存在或已删除
- 平台架构不匹配（arm64 vs amd64）

### 检查命令
- docker images
- 到 Docker Hub 搜索确认镜像名

### 解决思路
- 核对镜像名与 tag 是否正确
- 换用官方存在的 tag
- 指定平台：docker pull --platform linux/amd64 <镜像>

## 容器启动后立即退出

### 别名
docker 容器一闪而过 启动就退出 一启动就退出 启动就没了 一启动就没了 exited 容器跑不起来 秒退 程序没了

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
运行异常

### 错误类型
docker_container_exit_immediately

### 关键词
container exited 容器 退出 exited 0 启动失败

### 症状
- docker run 后容器立即 Exited (0)
- docker ps -a 里容器状态是 Exited

### 常见原因
- 容器内主进程正常结束（无前台常驻进程）
- 启动命令错误
- 依赖服务未就绪导致崩溃

### 检查命令
- docker logs <容器>
- docker ps -a

### 解决思路
- 查看 docker logs 定位崩溃原因
- 确保有前台进程（如 nginx -g 'daemon off;'）
- 交互式调试：docker run -it <镜像> sh

## 端口被占用

### 别名
docker 端口冲突 端口被占用 bind address already in use 端口映射失败

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
配置错误

### 错误类型
docker_port_conflict

### 关键词
port is already allocated bind address already in use 端口占用 冲突

### 症状
- Bind for 0.0.0.0:8080 failed: port is already allocated
- Error starting userland proxy: listen tcp 0.0.0.0:8080: bind: address already in use

### 常见原因
- 宿主机该端口已被其它程序占用
- 多个容器映射了同一宿主机端口

### 检查命令
- netstat -ano | findstr 8080（Windows）
- lsof -i :8080（Linux/macOS）

### 解决思路
- 换一个未占用端口：-p 8081:80
- 结束占用端口的进程
- 检查其它容器是否已映射该端口

## 容器内权限不足 Permission denied

### 别名
docker permission denied 容器内没权限 挂载目录没权限 运行不了

### 平台
linux macos

### 技术栈
docker

### 故障类型
权限问题

### 错误类型
docker_permission_denied

### 关键词
permission denied 权限 denied 没权限

### 症状
- 容器内执行命令报 Permission denied
- 挂载的目录无法读写

### 常见原因
- 以非 root 用户运行但文件属 root
- 挂载目录宿主机权限不足
- SELinux / AppArmor 限制

### 检查命令
- ls -l 查看文件属主
- docker run --user root

### 解决思路
- 用 --user 指定合适用户
- 修改挂载目录属主或权限
- 关闭或调整 SELinux（临时 setenforce 0）

## Linux 下 docker 需 sudo 或 socket 权限

### 别名
docker 需要 sudo 权限被拒绝 socket 权限 加入 docker 组

### 平台
linux

### 技术栈
docker

### 故障类型
权限问题

### 错误类型
docker_socket_permission

### 关键词
permission denied docker.sock sudo 权限 group

### 症状
- Got permission denied while trying to connect to the Docker daemon socket
- 普通用户运行 docker 报错

### 常见原因
- 用户不在 docker 组
- docker.sock 权限不对

### 检查命令
- id
- ls -l /var/run/docker.sock

### 解决思路
- sudo usermod -aG docker $USER 后重新登录
- 或临时用 sudo docker

## 数据卷挂载失败

### 别名
docker 挂载失败 数据卷没生效 -v 不生效 文件没同步

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
存储问题

### 错误类型
docker_volume_mount_failed

### 关键词
mount volume -v 挂载 数据卷 不生效 丢失

### 症状
- 挂载后容器内看不到宿主机文件
- 修改宿主机文件容器内不同步

### 常见原因
- 挂载路径拼写错误
- 使用相对路径而非绝对路径
- 挂载目标是空目录或不存在

### 检查命令
- docker inspect <容器> 查看 Mounts
- 确认宿主机路径存在

### 解决思路
- 使用绝对路径挂载
- 检查路径是否拼写正确
- 用命名卷：docker volume create 再挂载

## 数据卷权限与属主问题

### 别名
docker 挂载目录权限 数据卷属主 root 写入失败

### 平台
linux macos

### 技术栈
docker

### 故障类型
权限问题

### 错误类型
docker_volume_permission

### 关键词
volume permission 挂载 权限 属主 write

### 症状
- 挂载后容器内无权限写入
- 文件属主变成 root

### 常见原因
- 容器内运行用户与宿主机属主不一致
- 命名卷权限默认 root

### 检查命令
- docker exec <容器> ls -l

### 解决思路
- 用 --user 匹配宿主机 UID
- 在 Dockerfile 中 chown 目录
- 调整宿主机目录权限

## 镜像构建失败

### 别名
docker build 失败 镜像构建报错 build 不成功

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
构建失败

### 错误类型
docker_build_failed

### 关键词
build failed 构建失败 error building dockerfile

### 症状
- docker build 中途报错退出
- failed to solve / build failed

### 常见原因
- Dockerfile 指令错误
- 基础镜像拉取失败
- 构建步骤内命令执行失败

### 检查命令
- docker build -t test . 查看完整输出

### 解决思路
- 按输出定位失败的那一步
- 确认基础镜像能正常拉取
- 用 --no-cache 重新构建排查

## Dockerfile 找不到或 COPY 失败

### 别名
dockerfile not found copy 失败 文件找不到 build 上下文没有文件

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
构建失败

### 错误类型
dockerfile_not_found

### 关键词
dockerfile not found COPY failed 找不到 no such file

### 症状
- unable to prepare context: unable to evaluate symlinks in Dockerfile path
- COPY failed: no such file or directory

### 常见原因
- Dockerfile 不在构建上下文中
- COPY 源路径写错
- .dockerignore 把文件排除了

### 检查命令
- ls 确认 Dockerfile 位置

### 解决思路
- 用 -f 指定 Dockerfile 路径
- 检查 COPY 源路径与上下文
- 检查 .dockerignore 是否误排除

## 构建上下文过大

### 别名
docker build 卡住 上下文太大 sending build context 大

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
性能问题

### 错误类型
docker_build_context_too_large

### 关键词
build context 上下文 大 sending 慢

### 症状
- Sending build context 到 docker daemon 非常慢
- 上下文几个 GB 导致卡住

### 常见原因
- 把 node_modules、.git、日志等大目录打进上下文

### 检查命令
- 查看目录大小

### 解决思路
- 配置 .dockerignore 排除无关目录
- 减小构建上下文目录

## 优化 .dockerignore

### 别名
dockerignore 配置 排除文件 减小镜像

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
构建失败

### 错误类型
docker_dockerignore

### 关键词
dockerignore 忽略 排除 build context

### 症状
- 构建上下文包含大量无关文件
- 镜像体积过大

### 常见原因
- 未配置 .dockerignore

### 检查命令
- cat .dockerignore

### 解决思路
- 新建 .dockerignore，排除 .git、node_modules、__pycache__、日志等

## 构建缓存问题

### 别名
docker build 缓存 缓存失效 每次重新下载

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
构建失败

### 错误类型
docker_build_cache

### 关键词
cache 缓存 invalidated 失效 layer

### 症状
- 每次构建都重新拉取或重跑
- 缓存层失效

### 常见原因
- Dockerfile 指令顺序不佳
- 源文件变化导致缓存失效

### 检查命令
- docker build 观察 cache 命中

### 解决思路
- 把不常变的指令放前面（先 COPY 依赖再 COPY 源码）
- 必要时 --no-cache 强制重建

## docker-compose 语法错误

### 别名
compose 语法错误 yaml 报错 compose up 解析失败

### 平台
windows linux macos

### 技术栈
docker docker-compose compose

### 故障类型
配置错误

### 错误类型
docker_compose_syntax_error

### 关键词
compose yaml syntax error 语法错误 validation

### 症状
- ERROR: The Compose file is invalid
- yaml: line X: mapping values are not allowed here

### 常见原因
- YAML 缩进错误
- 关键字拼写错误
- 版本不匹配

### 检查命令
- docker-compose config

### 解决思路
- docker-compose config 校验并定位错误行
- 检查缩进（不要混用 tab 和空格）

## docker-compose 服务无法启动

### 别名
compose up 失败 服务起不来 compose 启动报错

### 平台
windows linux macos

### 技术栈
docker docker-compose compose

### 故障类型
服务启动失败

### 错误类型
docker_compose_up_failed

### 关键词
compose up failed 启动失败 服务 exited

### 症状
- docker-compose up 后服务退出
- 提示某服务 exited

### 常见原因
- 依赖服务未就绪
- 端口冲突
- 镜像构建失败

### 检查命令
- docker-compose logs

### 解决思路
- 用 depends_on + 健康检查控制启动顺序
- 查看 docker-compose logs 定位

## compose 版本不兼容

### 别名
compose 版本 不兼容 version 报错 compose 版本问题

### 平台
windows linux macos

### 技术栈
docker docker-compose compose

### 故障类型
版本不兼容

### 错误类型
docker_compose_version

### 关键词
compose version 不兼容 unsupported version

### 症状
- Version is unsupported
- 提示版本过低或过高

### 常见原因
- compose 文件 version 与 docker-compose 版本不匹配

### 检查命令
- docker-compose version

### 解决思路
- 调整 compose 文件 version 字段
- 升级 docker-compose

## 容器间无法通信

### 别名
docker 容器互相访问不了 网络不通 容器连不上

### 平台
windows linux macos

### 技术栈
docker docker-compose

### 故障类型
网络问题

### 错误类型
docker_container_network

### 关键词
network 容器 通信 连接失败 访问

### 症状
- 容器 A 无法访问容器 B
- ping 不通其它容器

### 常见原因
- 容器不在同一网络
- 使用了容器 IP 而非服务名

### 检查命令
- docker network ls
- docker network inspect

### 解决思路
- 加入同一自定义网络：docker network create 后连接
- compose 里用服务名互相访问

## 容器 DNS 解析失败

### 别名
docker 容器 dns 解析不了 域名解析失败

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
网络问题

### 错误类型
docker_dns

### 关键词
dns 解析失败 域名 resolve lookup

### 症状
- 容器内 ping 域名失败但 ping IP 成功
- getaddrinfo failed / name resolution error

### 常见原因
- 容器 DNS 配置错误
- 宿主机 DNS 问题

### 检查命令
- docker run --dns 8.8.8.8 测试

### 解决思路
- 用 --dns 指定 DNS
- 检查 /etc/resolv.conf

## 桥接网络或 IP 冲突

### 别名
docker 网络冲突 桥接 网段冲突 ip 冲突

### 平台
linux

### 技术栈
docker

### 故障类型
网络问题

### 错误类型
docker_network_conflict

### 关键词
bridge 网段 冲突 ip range subnet

### 症状
- 报网段冲突
- 容器 IP 与局域网冲突

### 常见原因
- 默认 bridge 网段与公司网络重叠

### 检查命令
- docker network inspect bridge

### 解决思路
- 修改 daemon.json 中的 bip 网段
- 创建自定义网络指定子网

## 磁盘空间不足

### 别名
docker 磁盘满了 no space left on device 空间不足 清理

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
资源不足

### 错误类型
docker_no_space

### 关键词
no space left on device 磁盘 空间 不足 full

### 症状
- no space left on device
- 拉取镜像失败提示空间不足

### 常见原因
- 镜像、容器、数据卷堆积
- 未及时清理无用镜像

### 检查命令
- docker system df

### 解决思路
- docker system prune -a 清理无用资源
- 删除无标签镜像

## 容器内存不足被 OOM

### 别名
docker 内存不足 oom 容器被杀 内存超限

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
资源不足

### 错误类型
docker_oom

### 关键词
out of memory oom killed 内存 不足

### 症状
- 容器突然退出，状态 OOMKilled
- 日志出现 out of memory

### 常见原因
- 应用内存占用超过限制
- 未设置内存限制导致宿主机内存耗尽

### 检查命令
- docker inspect <容器> 查看 OOMKilled

### 解决思路
- 用 -m 设置内存限制
- 优化应用内存占用

## 容器退出码 137

### 别名
docker exit 137 容器被 kill oomkilled 退出码

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
资源不足

### 错误类型
docker_exit_137

### 关键词
exit 137 oomkilled 退出码 killed

### 症状
- 容器 Exited (137)
- docker inspect 显示 OOMKilled: true

### 常见原因
- 内存超出限制被 OOM 杀掉
- 系统或用户主动 kill

### 检查命令
- docker inspect -f '{{.State.OOMKilled}}'

### 解决思路
- 提高内存限制或优化内存
- 检查是否有外部 kill

## OCI runtime 错误

### 别名
docker oci runtime error 容器启动报错 runtime 错误

### 平台
linux

### 技术栈
docker

### 故障类型
运行异常

### 错误类型
docker_oci_runtime_error

### 关键词
oci runtime error container process caused

### 症状
- OCI runtime create failed
- container_linux.go: ... caused "process_linux.go"

### 常见原因
- 启动命令错误
- 文件系统或 cgroup 配置问题

### 检查命令
- docker run -it <镜像> sh 测试

### 解决思路
- 检查启动命令
- 重启 docker 服务

## 容器反复重启

### 别名
docker 容器一直重启 restart loop 重启循环 起不来

### 平台
windows linux macos

### 技术栈
docker docker-compose

### 故障类型
运行异常

### 错误类型
docker_restart_loop

### 关键词
restart loop 反复重启 restarting exited

### 症状
- 容器状态 Restarting 循环
- compose 里服务不断重启

### 常见原因
- 启动即崩溃
- 配置错误或依赖未就绪

### 检查命令
- docker logs --tail 50 <容器>

### 解决思路
- 查看 logs 定位崩溃原因
- 用 restart: unless-stopped 并修正配置

## 查看容器日志

### 别名
docker logs 看日志 排查 容器日志

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
排查方法

### 错误类型
docker_logs

### 关键词
logs 日志 查看 排查 tail

### 症状
- 需要定位容器运行问题

### 常见原因
- 无

### 检查命令
- docker logs <容器>
- docker logs -f <容器>

### 解决思路
- docker logs --tail 100 查看最近日志
- docker logs -f 实时跟踪

## 进入运行中的容器

### 别名
docker exec 进入容器 attach 交互 shell

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
排查方法

### 错误类型
docker_exec_it

### 关键词
exec -it attach 进入 shell 交互

### 症状
- 需要进入容器内排查

### 常见原因
- 无

### 检查命令
- docker exec -it <容器> sh

### 解决思路
- 用 docker exec -it <容器> bash（或 sh）进入
- 排查文件、进程、网络

## 清理磁盘占用

### 别名
docker 清理 删除无用镜像 释放空间 prune

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
资源不足

### 错误类型
docker_cleanup

### 关键词
prune 清理 删除 空间 镜像 无标签

### 症状
- 磁盘占用越来越大

### 常见原因
- 无用镜像、停止容器、悬空卷堆积

### 检查命令
- docker system df

### 解决思路
- docker system prune -a 清理
- docker volume prune 清理卷

## Windows 需要 WSL2

### 别名
docker 需要 wsl2 windows 下 docker 报 wsl 内核 未启用

### 平台
windows

### 技术栈
docker wsl

### 故障类型
环境依赖

### 错误类型
docker_wsl2_required

### 关键词
wsl2 内核 wsl --update 需要 启用

### 症状
- 提示需要 WSL2 内核更新
- Docker Desktop 依赖 WSL2 无法运行

### 常见原因
- WSL2 未安装或未启用
- 内核版本过旧

### 检查命令
- wsl --status
- wsl --update

### 解决思路
- wsl --install 安装 WSL2
- wsl --update 更新内核

## WSL 内 docker 报错

### 别名
wsl docker 报错 wsl 里不能用 docker 子系统

### 平台
windows linux

### 技术栈
docker wsl

### 故障类型
环境依赖

### 错误类型
docker_wsl_error

### 关键词
wsl docker 报错 子系统 不支持

### 症状
- WSL 里运行 docker 报错
- 提示无法连接

### 常见原因
- WSL 发行版未启用 docker 集成
- 服务未启动

### 检查命令
- wsl --list -v

### 解决思路
- 在 Docker Desktop 设置中启用 WSL 集成
- 重启 WSL 与 Docker Desktop

## 虚拟化未启用

### 别名
docker 需要虚拟化 virtualization 未开启 bios

### 平台
windows

### 技术栈
docker

### 故障类型
环境依赖

### 错误类型
docker_virtualization

### 关键词
virtualization 虚拟化 bios 未启用 hyper-v

### 症状
- Docker Desktop 提示 virtualization 未启用

### 常见原因
- BIOS 中虚拟化未开启
- Hyper-V 未启用

### 检查命令
- 任务管理器查看虚拟化状态

### 解决思路
- BIOS 开启 VT-x/AMD-V
- 启用 Hyper-V 或 WSL2 后端

## docker 命令未找到

### 别名
docker 命令找不到 not found 不是内部命令 未安装

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
环境依赖

### 错误类型
docker_command_not_found

### 关键词
command not found 不是内部 命令 未安装

### 症状
- docker: command not found
- docker 不是内部或外部命令

### 常见原因
- 未安装 docker
- PATH 未包含 docker

### 检查命令
- which docker
- docker --version

### 解决思路
- 安装 Docker
- 把 docker 加入 PATH 并重开终端

## 私有仓库搭建与访问

### 别名
docker 私有仓库 registry 自建仓库 局域网镜像

### 平台
linux

### 技术栈
docker registry

### 故障类型
配置错误

### 错误类型
docker_private_registry

### 关键词
registry 私有仓库 自建 insecure push

### 症状
- 推送私有仓库报 http: server gave HTTP response to HTTPS client
- 无法访问自建 registry

### 常见原因
- 未配置 insecure-registries
- 仓库未加认证

### 检查命令
- docker login <registry>

### 解决思路
- daemon.json 配置 insecure-registries
- 用 docker run -d -p 5000:5000 registry 启动

## 容器时区不对

### 别名
docker 容器时区 时间不对 时区错误 差了八小时

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
配置错误

### 错误类型
docker_timezone

### 关键词
时区 timezone 时间 不对 UTC 八小时

### 症状
- 容器内时间与本地差 8 小时
- 日志时间戳不对

### 常见原因
- 容器默认使用 UTC 时区

### 检查命令
- docker exec <容器> date

### 解决思路
- 挂载 -v /etc/localtime:/etc/localtime:ro
- 设置环境变量 TZ=Asia/Shanghai

## 镜像导出与导入

### 别名
docker save load 导出镜像 离线安装镜像 迁移

### 平台
windows linux macos

### 技术栈
docker

### 故障类型
排查方法

### 错误类型
docker_save_load

### 关键词
save load 导出 导入 离线 迁移 tar

### 症状
- 需要离线迁移镜像

### 常见原因
- 无

### 检查命令
- docker images

### 解决思路
- 导出：docker save -o image.tar <镜像>
- 导入：docker load -i image.tar
