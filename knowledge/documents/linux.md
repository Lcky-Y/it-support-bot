# Linux 故障知识库

## Permission denied 权限拒绝

### 别名
linux 没权限 permission denied 权限不够 无法访问 拒绝访问

### 平台
linux

### 技术栈
linux shell

### 故障类型
权限问题

### 错误类型
linux_permission_denied

### 关键词
permission denied 权限 denied 拒绝 没权限

### 症状
- bash: ./xxx: Permission denied
- 打开/写入文件报 Permission denied

### 常见原因
- 文件属主或权限不对
- 当前用户无读写执行权限
- 目录权限不足

### 检查命令
- ls -l 文件
- id 查看当前用户

### 解决思路
- chmod 调整权限（如 chmod +x 或 chmod 755）
- chown 修改属主
- 需要时用 sudo

## sudo 提示不在 sudoers 中

### 别名
sudo 不能用 not in sudoers 提示无权限 没有 sudo 权限

### 平台
linux

### 技术栈
linux sudo

### 故障类型
权限问题

### 错误类型
linux_sudo_sudoers

### 关键词
sudo sudoers not in the sudoers file 权限

### 症状
- xxx is not in the sudoers file. This incident will be reported

### 常见原因
- 用户不在 sudoers 列表
- 未加入 wheel/sudo 组

### 检查命令
- id 查看所在组

### 解决思路
- 用 root 执行 usermod -aG sudo 用户名
- 或用 visudo 添加用户

## chmod 修改文件权限

### 别名
修改文件权限 设置权限 chmod 命令 数字权限 755

### 平台
linux

### 技术栈
linux shell

### 故障类型
权限问题

### 错误类型
linux_chmod

### 关键词
chmod 权限 755 644 数字

### 症状
- 需要给文件/目录设置读写执行权限

### 常见原因
- 权限设置不当

### 检查命令
- ls -l

### 解决思路
- chmod 755 文件 或 chmod 644 文件
- 目录加执行位 chmod +x

## chown 修改文件属主

### 别名
修改属主 文件所有者 chown 归属 改成谁

### 平台
linux

### 技术栈
linux shell

### 故障类型
权限问题

### 错误类型
linux_chown

### 关键词
chown 属主 所有者 owner 归属

### 症状
- 文件属主需要变更
- 提示 Operation not permitted

### 常见原因
- 文件属主与运行用户不一致

### 检查命令
- ls -l

### 解决思路
- chown 用户:组 文件
- 递归：chown -R 用户 目录

## 运行脚本报 Permission denied

### 别名
脚本没执行权限 执行不了脚本 shell 脚本权限 不能运行

### 平台
linux

### 技术栈
linux shell bash

### 故障类型
权限问题

### 错误类型
linux_script_exec_perm

### 关键词
脚本 执行 权限 permission denied bash

### 症状
- 运行 ./run.sh 报 Permission denied

### 常见原因
- 脚本没有执行位

### 检查命令
- ls -l run.sh

### 解决思路
- chmod +x run.sh
- 或 bash run.sh 直接执行

## 文件系统只读无法写入

### 别名
只读 无法写入 read-only filesystem 磁盘只读 写不进去

### 平台
linux

### 技术栈
linux

### 故障类型
存储问题

### 错误类型
linux_readonly_fs

### 关键词
read-only filesystem 只读 无法写入 mount

### 症状
- 写入文件报 Read-only file system

### 常见原因
- 分区以只读方式挂载
- 磁盘故障触发只读保护

### 检查命令
- mount | grep 挂载点

### 解决思路
- 重新挂载为读写：mount -o remount,rw /
- 检查磁盘健康（dmesg）

## 无法删除文件 Operation not permitted

### 别名
删不掉文件 operation not permitted 无法删除 删除被拒

### 平台
linux

### 技术栈
linux

### 故障类型
权限问题

### 错误类型
linux_rm_operation_not_permitted

### 关键词
operation not permitted rm 删除 无法删除 immutable

### 症状
- rm 文件报 Operation not permitted

### 常见原因
- 文件带 immutable 属性
- 目录权限不足

### 检查命令
- lsattr 文件

### 解决思路
- chattr -i 文件 去掉 immutable
- 检查父目录写权限

## apt 安装找不到包

### 别名
apt 找不到包 找不到这个包 装软件找不到 装软件提示找不到 无法定位软件包 install 没有候选 unable to locate package

### 平台
linux

### 技术栈
apt debian ubuntu

### 故障类型
安装失败

### 错误类型
linux_apt_package_not_found

### 关键词
apt install unable to locate package 找不到包

### 症状
- E: Unable to locate package xxx

### 常见原因
- 包名拼写错误
- 未更新软件源索引
- 源里不含该包

### 检查命令
- apt search 关键字

### 解决思路
- apt update 更新索引后再装
- 核对包名或换源

## apt update 失败

### 别名
apt update 报错 更新源失败 软件源更新不了

### 平台
linux

### 技术栈
apt debian ubuntu

### 故障类型
网络问题

### 错误类型
linux_apt_update_failed

### 关键词
apt update 失败 源 网络 超时 failed to fetch

### 症状
- E: Failed to fetch http://... Temporary failure resolving
- 更新源卡住或报错

### 常见原因
- 网络不通 / DNS 问题
- 软件源地址失效

### 检查命令
- ping 源地址

### 解决思路
- 检查网络与 DNS
- 更换软件源镜像

## apt 依赖冲突

### 别名
apt 依赖冲突 依赖问题 broken packages 无法安装依赖

### 平台
linux

### 技术栈
apt debian ubuntu

### 故障类型
安装失败

### 错误类型
linux_apt_dependency

### 关键词
apt 依赖 dependency unmet broken packages 冲突

### 症状
- E: Unmet dependencies
- 提示 broken packages

### 常见原因
- 包版本冲突
- 源版本不一致

### 检查命令
- apt check

### 解决思路
- apt --fix-broken install 修复
- 检查是否混用多个源版本

## dpkg 被锁 / 锁错误

### 别名
dpkg 锁 被锁住 unable to lock 另一个进程占用 安装卡住

### 平台
linux

### 技术栈
apt dpkg debian ubuntu

### 故障类型
安装失败

### 错误类型
linux_dpkg_lock

### 关键词
dpkg lock unable to lock 锁 占用

### 症状
- Could not get lock /var/lib/dpkg/lock

### 常见原因
- 另一个安装进程在运行
- 上次安装中断残留锁

### 检查命令
- ps aux | grep apt

### 解决思路
- 等待其它安装完成
- 确认无进程后删除锁文件（谨慎）

## apt 下载慢 / 换源

### 别名
apt 换源 下载慢 更新源 镜像源 国内源

### 平台
linux

### 技术栈
apt debian ubuntu

### 故障类型
网络问题

### 错误类型
linux_apt_mirror

### 关键词
apt 源 镜像 慢 换源 sources.list

### 症状
- apt 下载速度慢

### 常见原因
- 默认源在国外

### 检查命令
- cat /etc/apt/sources.list

### 解决思路
- 更换为国内镜像源（如清华、阿里源）
- 改后 apt update

## yum / dnf 安装失败

### 别名
yum 安装失败 dnf 报错 红帽安装包 centos 装不了

### 平台
linux

### 技术栈
yum dnf centos rhel fedora

### 故障类型
安装失败

### 错误类型
linux_yum_install

### 关键词
yum dnf install 失败 依赖 centos

### 症状
- yum install 报错
- Error: Unable to find a match

### 常见原因
- 包不存在或源未同步
- 依赖冲突

### 检查命令
- yum search 关键字

### 解决思路
- 核对包名
- 换源或 yum update 后重试

## 源码编译 make 失败

### 别名
make 编译失败 源码安装 编译报错 gcc 错误

### 平台
linux

### 技术栈
make gcc linux

### 故障类型
安装失败

### 错误类型
linux_make_failed

### 关键词
make gcc 编译 error 源码 构建

### 症状
- make 报 error
- 提示缺头文件或库

### 常见原因
- 缺少编译依赖
- 缺少开发库头文件

### 检查命令
- gcc --version

### 解决思路
- 安装 build-essential 等编译工具
- 补齐缺失的 -dev 依赖包

## systemctl 服务启动失败

### 别名
服务启动失败 systemctl 起不来 服务起不来 启动报错

### 平台
linux

### 技术栈
systemd systemctl linux

### 故障类型
服务启动失败

### 错误类型
linux_systemctl_start_failed

### 关键词
systemctl start failed 服务 启动 失败 unit

### 症状
- systemctl start xxx 报 failed
- Job for xxx failed

### 常见原因
- 配置错误
- 依赖服务未启动
- 程序本身崩溃

### 检查命令
- systemctl status xxx
- journalctl -u xxx -xe

### 解决思路
- 查看 status 与日志定位
- 修正配置后 daemon-reload

## systemctl 命令不可用

### 别名
systemctl 找不到 不是 systemd 容器里没有 systemctl

### 平台
linux

### 技术栈
systemd systemctl linux docker

### 故障类型
环境依赖

### 错误类型
linux_systemctl_not_found

### 关键词
systemctl not found 不存在 容器 不是 systemd

### 症状
- System has not been booted with systemd as init system
- systemctl: command not found

### 常见原因
- 容器内无 systemd
- 系统用其它 init

### 检查命令
- ps 1

### 解决思路
- 容器内改用 service 或直接运行程序
- 确认 PID1 是否为 systemd

## 查看进程 ps

### 别名
查看进程 进程列表 查进程 ps 命令

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_ps

### 关键词
ps 进程 查看 列表 aux

### 症状
- 需要查看运行中的进程

### 常见原因
- 无

### 检查命令
- ps aux

### 解决思路
- ps aux 查看全部进程
- ps aux | grep 关键字 过滤

## kill 结束进程

### 别名
杀掉进程 结束进程 kill 命令 关闭程序

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_kill

### 关键词
kill 进程 结束 杀掉 pid 终止

### 症状
- 需要结束某个进程

### 常见原因
- 无

### 检查命令
- ps aux | grep 进程名

### 解决思路
- kill PID 正常结束
- kill -9 PID 强制结束

## 进程杀不掉 / 僵尸进程

### 别名
进程杀不掉 僵尸进程 kill 不掉 defunct

### 平台
linux

### 技术栈
linux

### 故障类型
运行异常

### 错误类型
linux_zombie

### 关键词
zombie defunct 僵尸 杀不掉 kill 无效

### 症状
- 进程状态显示 Z（defunct）
- kill 后进程仍存在

### 常见原因
- 父进程未回收子进程
- 进程处于不可中断状态 D

### 检查命令
- ps aux | grep Z

### 解决思路
- 结束父进程以回收僵尸进程
- D 状态通常等 IO 完成或重启

## 服务开机自启

### 别名
开机自启 开机启动 服务自动启动 enable 自启

### 平台
linux

### 技术栈
systemd systemctl linux

### 故障类型
配置错误

### 错误类型
linux_service_enable

### 关键词
enable 开机自启 启动 自启动 systemctl

### 症状
- 服务重启后没有自动启动

### 常见原因
- 未 enable

### 检查命令
- systemctl is-enabled xxx

### 解决思路
- systemctl enable xxx 设置开机自启
- systemctl disable 关闭

## journalctl 查看日志

### 别名
查看系统日志 journalctl 服务日志 日志报错

### 平台
linux

### 技术栈
systemd journalctl linux

### 故障类型
排查方法

### 错误类型
linux_journalctl

### 关键词
journalctl 日志 log 查看 systemd

### 症状
- 需要查看服务日志排查问题

### 常见原因
- 无

### 检查命令
- journalctl -u 服务名 -xe

### 解决思路
- journalctl -u 服务名 查看指定服务日志
- -f 实时跟踪

## 进程占用高排查

### 别名
cpu 占用高 内存占用高 进程占用 排查 卡顿

### 平台
linux

### 技术栈
linux shell

### 故障类型
性能问题

### 错误类型
linux_top_process

### 关键词
top cpu 内存 占用 高 进程 卡顿

### 症状
- 服务器 CPU 或内存占用过高

### 常见原因
- 某个进程异常
- 内存泄漏

### 检查命令
- top
- free -h

### 解决思路
- top 按 CPU/内存排序定位进程
- 定位后 kill 或优化

## 端口被占用

### 别名
端口被占用 address already in use 端口冲突 起服务报端口

### 平台
linux

### 技术栈
linux shell

### 故障类型
配置错误

### 错误类型
linux_port_conflict

### 关键词
port already in use 端口 占用 冲突 bind

### 症状
- bind: address already in use
- 启动服务提示端口被占用

### 常见原因
- 端口已被其它进程占用

### 检查命令
- ss -tlnp | grep 端口

### 解决思路
- 找到占用进程并结束
- 或换一个端口

## 查看端口占用 ss / netstat

### 别名
查看端口 谁占用端口 查端口 ss netstat 端口号

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_port_check

### 关键词
ss netstat 端口 查看 占用 监听

### 症状
- 需要查看端口监听与占用情况

### 常见原因
- 无

### 检查命令
- ss -tlnp

### 解决思路
- ss -tlnp 查看监听端口
- netstat -tlnp 也可以

## ping 不通

### 别名
ping 不通 无法 ping 网络不通 连接不上主机

### 平台
linux

### 技术栈
linux shell

### 故障类型
网络问题

### 错误类型
linux_ping_fail

### 关键词
ping 不通 网络 timeout unreachable 主机

### 症状
- ping 目标无响应

### 常见原因
- 网络不通
- 防火墙禁 ping
- 目标不可达

### 检查命令
- ping 目标
- ip route

### 解决思路
- 检查网络与路由
- 确认防火墙是否禁 ICMP

## DNS 解析失败

### 别名
dns 解析不了 域名解析失败 解析不到 域名 ping 不通

### 平台
linux

### 技术栈
linux shell

### 故障类型
网络问题

### 错误类型
linux_dns

### 关键词
dns 解析 域名 resolve 失败 getaddrinfo

### 症状
- ping 域名失败但 ping IP 成功
- Temporary failure in name resolution

### 常见原因
- /etc/resolv.conf 配置错误
- DNS 服务器不可用

### 检查命令
- cat /etc/resolv.conf

### 解决思路
- 修改 /etc/resolv.conf 添加可用 DNS（如 8.8.8.8）
- 检查网络与 DNS 服务

## curl 报 SSL 证书错误

### 别名
curl 证书错误 ssl 证书 验证失败 https 报错

### 平台
linux

### 技术栈
curl linux

### 故障类型
网络问题

### 错误类型
linux_curl_ssl

### 关键词
curl ssl certificate 证书 verify 验证失败

### 症状
- SSL certificate problem: unable to get local issuer certificate

### 常见原因
- 证书链不完整
- 系统时间不对
- 自签名证书

### 检查命令
- date
- curl -v 目标

### 解决思路
- 检查系统时间
- 自签名/内网可加 -k（仅调试用）

## curl 连接失败

### 别名
curl 连接失败 连不上 拒绝连接 could not connect

### 平台
linux

### 技术栈
curl linux

### 故障类型
网络问题

### 错误类型
linux_curl_connection

### 关键词
curl connect 连接失败 refused 拒绝 could not connect

### 症状
- curl: (7) Failed to connect ... Connection refused

### 常见原因
- 目标服务未启动
- 端口不对
- 防火墙拦截

### 检查命令
- ss -tlnp 看目标端口

### 解决思路
- 确认服务已启动并监听
- 检查端口与防火墙

## 查看 IP 地址

### 别名
查看 ip 本机 ip ifconfig ip addr 网卡地址

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_ip_addr

### 关键词
ip addr ifconfig 查看 ip 地址 网卡

### 症状
- 需要查看本机 IP

### 常见原因
- 无

### 检查命令
- ip addr

### 解决思路
- ip addr 或 ip a 查看
- 老系统可用 ifconfig（需 net-tools）

## 服务器无法访问外网

### 别名
无法上网 不能访问外网 网络不通 出不了网

### 平台
linux

### 技术栈
linux

### 故障类型
网络问题

### 错误类型
linux_no_internet

### 关键词
外网 上网 无法访问 网络 不通 路由

### 症状
- 服务器 ping 不通外网
- 只能访问内网

### 常见原因
- 网关 / 路由配置错误
- DNS 问题
- 防火墙规则

### 检查命令
- ip route
- ping 8.8.8.8

### 解决思路
- 检查默认网关与路由
- 检查 DNS 与防火墙

## 服务监听但外部访问不了

### 别名
服务访问不了 监听 外部连不上 防火墙拦截 端口不通

### 平台
linux

### 技术栈
linux shell

### 故障类型
网络问题

### 错误类型
linux_port_listen

### 关键词
监听 访问不了 连接 端口 防火墙 拒绝

### 症状
- 服务本地可访问，外部访问不了

### 常见原因
- 监听在 127.0.0.1
- 防火墙拦截

### 检查命令
- ss -tlnp 看监听地址

### 解决思路
- 让服务监听 0.0.0.0
- 放行对应端口

## 磁盘空间满

### 别名
磁盘满了 空间不足 no space left 磁盘占用 df

### 平台
linux

### 技术栈
linux shell

### 故障类型
存储问题

### 错误类型
linux_disk_full

### 关键词
no space left 磁盘 满 空间 不足 df

### 症状
- No space left on device
- 写文件失败提示空间不足

### 常见原因
- 磁盘被日志/大文件占满
- 分区规划不合理

### 检查命令
- df -h

### 解决思路
- df -h 定位满的分区
- 清理日志或大文件

## 查看目录大小 du

### 别名
查看目录大小 du 目录占用 谁占空间 大文件

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_du

### 关键词
du 目录 大小 占用 空间 磁盘

### 症状
- 需要定位哪个目录占空间大

### 常见原因
- 无

### 检查命令
- du -sh 目录

### 解决思路
- du -sh * 查看各子项大小
- du -h --max-depth=1 逐层排查

## 挂载 mount

### 别名
挂载 mount 磁盘挂载 分区挂载 挂载点

### 平台
linux

### 技术栈
linux shell

### 故障类型
存储问题

### 错误类型
linux_mount

### 关键词
mount 挂载 分区 磁盘 挂载点 umount

### 症状
- 磁盘/分区无法访问，需要挂载

### 常见原因
- 未挂载或挂载配置错误

### 检查命令
- lsblk
- mount

### 解决思路
- mount /dev/xxx /mnt 挂载
- 写入 /etc/fstab 实现开机自动挂载

## 软链接 ln -s

### 别名
软链接 符号链接 ln -s 快捷方式 链接

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_symlink

### 关键词
ln -s 软链接 符号链接 symlink 链接

### 症状
- 需要创建文件软链接

### 常见原因
- 无

### 检查命令
- ls -l

### 解决思路
- ln -s 目标 链接名 创建软链接
- 删除用 unlink 或 rm

## find 查找文件

### 别名
查找文件 find 搜索文件 找文件

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_find

### 关键词
find 查找 搜索 文件 名字

### 症状
- 需要按名字/条件查找文件

### 常见原因
- 无

### 检查命令
- find / -name 文件名

### 解决思路
- find 路径 -name 文件名 按名查找
- 按类型/时间加参数过滤

## inode 耗尽

### 别名
inode 满了 不能创建文件 大量小文件 磁盘没满但写不了

### 平台
linux

### 技术栈
linux

### 故障类型
存储问题

### 错误类型
linux_inode_full

### 关键词
inode 耗尽 满了 创建文件 小文件 写不了

### 症状
- 磁盘有空间但无法创建文件
- No space left on device 但 df 显示有空间

### 常见原因
- 大量小文件耗尽 inode

### 检查命令
- df -i

### 解决思路
- df -i 确认 inode 使用
- 清理大量小文件（如缓存/临时文件）

## 磁盘分区 fdisk

### 别名
磁盘分区 fdisk 分区 新磁盘 未分区

### 平台
linux

### 技术栈
linux shell

### 故障类型
排查方法

### 错误类型
linux_fdisk

### 关键词
fdisk 分区 磁盘 新盘 分区表

### 症状
- 新磁盘需要分区

### 常见原因
- 无

### 检查命令
- lsblk

### 解决思路
- fdisk /dev/xxx 交互分区
- 分区后 mkfs 格式化并挂载

## ssh 连接被拒绝

### 别名
ssh 连不上 连接被拒 refused 拒绝连接 ssh 失败

### 平台
linux

### 技术栈
ssh linux

### 故障类型
网络问题

### 错误类型
linux_ssh_refused

### 关键词
ssh refused 拒绝 connection 连接失败

### 症状
- ssh: connect to host port 22: Connection refused

### 常见原因
- sshd 服务未启动
- 端口不是 22
- 防火墙拦截

### 检查命令
- systemctl status sshd

### 解决思路
- 启动 sshd 服务
- 检查端口与防火墙

## ssh 认证失败 publickey

### 别名
ssh 认证失败 登录失败 permission denied publickey 密码错误

### 平台
linux

### 技术栈
ssh linux

### 故障类型
认证失败

### 错误类型
linux_ssh_auth_failed

### 关键词
ssh permission denied publickey 认证 失败 登录

### 症状
- Permission denied (publickey,password)

### 常见原因
- 密码错误
- 密钥不匹配
- 禁止密码登录

### 检查命令
- ssh -v 用户@主机 查看详细

### 解决思路
- 核对密码或密钥
- 检查 authorized_keys 配置

## ssh 密钥权限 too open

### 别名
ssh 密钥权限问题 too open 权限太开放 私钥权限

### 平台
linux

### 技术栈
ssh linux

### 故障类型
权限问题

### 错误类型
linux_ssh_key_perm

### 关键词
ssh key too open permissions 权限 私钥 密钥

### 症状
- Permissions 0644 for 'id_rsa' are too open

### 常见原因
- 私钥文件权限过于开放

### 检查命令
- ls -l ~/.ssh/id_rsa

### 解决思路
- chmod 600 ~/.ssh/id_rsa
- 目录 chmod 700 ~/.ssh

## known_hosts 冲突

### 别名
known_hosts 冲突 host key 变了 中间人攻击 密钥变更

### 平台
linux

### 技术栈
ssh linux

### 故障类型
认证失败

### 错误类型
linux_ssh_known_hosts

### 关键词
known_hosts host key 冲突 变更 remote host identification

### 症状
- REMOTE HOST IDENTIFICATION HAS CHANGED

### 常见原因
- 目标主机密钥变更（重装/换机）
- 存在中间人风险

### 检查命令
- cat ~/.ssh/known_hosts

### 解决思路
- 确认安全后删除旧记录：ssh-keygen -R 主机
- 重新连接

## ssh 连接超时

### 别名
ssh 超时 连接不上 卡住 无响应 ssh 慢

### 平台
linux

### 技术栈
ssh linux

### 故障类型
网络问题

### 错误类型
linux_ssh_timeout

### 关键词
ssh timeout 超时 连接 卡 无响应

### 症状
- ssh 连接一直无响应或超时

### 常见原因
- 网络不通或防火墙
- DNS 反查慢

### 检查命令
- ping 目标主机

### 解决思路
- 检查网络与防火墙
- 服务端关闭 UseDNS 加速

## scp 传输失败

### 别名
scp 传输失败 拷贝失败 文件传输 上传失败

### 平台
linux

### 技术栈
ssh scp linux

### 故障类型
网络问题

### 错误类型
linux_scp

### 关键词
scp 传输 拷贝 上传 下载 失败

### 症状
- scp 复制文件失败

### 常见原因
- 路径错误
- 权限不足
- 网络中断

### 检查命令
- ssh 主机 先确认连通

### 解决思路
- 核对源/目标路径
- 检查目标目录写权限

## 命令未找到 command not found

### 别名
命令找不到 command not found 不是命令 未安装

### 平台
linux

### 技术栈
linux shell

### 故障类型
环境依赖

### 错误类型
linux_command_not_found

### 关键词
command not found 命令 找不到 未安装

### 症状
- xxx: command not found

### 常见原因
- 未安装该命令
- 不在 PATH 中

### 检查命令
- which 命令
- echo $PATH

### 解决思路
- 安装对应软件包
- 把路径加入 PATH

## PATH 环境变量

### 别名
PATH 环境变量 配置 path 命令找不到 环境变量

### 平台
linux

### 技术栈
linux shell bash

### 故障类型
配置错误

### 错误类型
linux_path

### 关键词
PATH 环境变量 path 命令 配置 找不到

### 症状
- 程序不在 PATH 导致命令找不到

### 常见原因
- PATH 未包含程序目录

### 检查命令
- echo $PATH

### 解决思路
- export PATH=$PATH:/新目录
- 写入 .bashrc 永久生效

## 环境变量永久生效

### 别名
环境变量 永久生效 配置环境变量 export 不生效

### 平台
linux

### 技术栈
linux shell bash

### 故障类型
配置错误

### 错误类型
linux_env_var

### 关键词
环境变量 export 永久 生效 bashrc profile

### 症状
- 临时 export 的变量重开后丢失

### 常见原因
- 只写在当前 shell，未持久化

### 检查命令
- echo $变量

### 解决思路
- 写入 ~/.bashrc 或 ~/.profile
- source 使其立即生效

## shell 脚本语法错误

### 别名
shell 脚本报错 语法错误 bash 脚本语法 脚本不执行

### 平台
linux

### 技术栈
bash shell linux

### 故障类型
运行异常

### 错误类型
linux_shell_syntax

### 关键词
bash 脚本 语法错误 syntax error 报错

### 症状
- script.sh: line 1: syntax error near unexpected token

### 常见原因
- 语法写错
- 中文标点或空格问题
- 编码问题

### 检查命令
- bash -n 脚本

### 解决思路
- bash -n 脚本 检查语法
- 检查引号与括号配对

## 中文乱码 / 编码问题

### 别名
中文乱码 编码问题 locale 字符集 显示乱码

### 平台
linux

### 技术栈
linux shell

### 故障类型
配置错误

### 错误类型
linux_locale

### 关键词
乱码 编码 locale 字符集 utf8 中文

### 症状
- 终端中文显示乱码
- 文件编码不符

### 常见原因
- locale 未设置为 UTF-8
- 文件编码与查看方式不符

### 检查命令
- locale

### 解决思路
- 设置 LANG=en_US.UTF-8 或 zh_CN.UTF-8
- 转换文件编码（iconv）

## bashrc / profile 不生效

### 别名
bashrc 不生效 profile 配置了没生效 环境变量没加载

### 平台
linux

### 技术栈
bash shell linux

### 故障类型
配置错误

### 错误类型
linux_bashrc

### 关键词
bashrc profile 不生效 配置 加载 source

### 症状
- 修改 .bashrc 后重开终端未生效

### 常见原因
- 未 source
- 改错文件（如 .profile 不用于交互 shell）

### 检查命令
- source ~/.bashrc

### 解决思路
- source ~/.bashrc 使其生效
- 交互 shell 用 .bashrc，登录 shell 用 .profile

## ufw 防火墙放行端口

### 别名
ufw 放行端口 防火墙 ubuntu 开放端口 防火墙规则

### 平台
linux

### 技术栈
ufw linux ubuntu

### 故障类型
配置错误

### 错误类型
linux_ufw

### 关键词
ufw 防火墙 端口 放行 allow 开放

### 症状
- 端口被 ufw 拦截无法访问

### 常见原因
- 未放行端口

### 检查命令
- ufw status

### 解决思路
- ufw allow 端口/服务
- ufw enable 启用（注意别把自己锁外面）

## firewalld 防火墙

### 别名
firewalld 防火墙 centos 端口 放行 开放端口 firewall-cmd

### 平台
linux

### 技术栈
firewalld linux centos

### 故障类型
配置错误

### 错误类型
linux_firewalld

### 关键词
firewalld firewall-cmd 端口 放行 开放 防火墙

### 症状
- 端口被 firewalld 拦截

### 常见原因
- 未开放端口

### 检查命令
- firewall-cmd --list-ports

### 解决思路
- firewall-cmd --add-port=端口/tcp --permanent
- 然后 --reload

## 防火墙导致服务无法访问

### 别名
防火墙拦截 服务访问不了 端口被拦 防火墙导致连不上

### 平台
linux

### 技术栈
ufw firewalld iptables linux

### 故障类型
网络问题

### 错误类型
linux_firewall_block

### 关键词
防火墙 拦截 端口 访问不了 拒绝 屏蔽

### 症状
- 服务端口无法从外部访问

### 常见原因
- 防火墙规则拦截
- 安全组未放行

### 检查命令
- ufw status 或 firewall-cmd --list-all

### 解决思路
- 放行对应端口
- 云主机检查安全组规则

## iptables 配置

### 别名
iptables 规则 配置防火墙 端口转发 防火墙规则

### 平台
linux

### 技术栈
iptables linux

### 故障类型
配置错误

### 错误类型
linux_iptables

### 关键词
iptables 规则 防火墙 配置 端口 转发

### 症状
- 需要配置 iptables 规则

### 常见原因
- 无

### 检查命令
- iptables -L -n

### 解决思路
- iptables -A INPUT -p tcp --dport 端口 -j ACCEPT
- 注意规则顺序与持久化
