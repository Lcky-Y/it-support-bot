# PostgreSQL 故障知识库

## peer authentication failed

### 别名
postgres peer 认证失败 认证失败 登录失败 密码 本地

### 平台
linux

### 技术栈
postgresql database

### 故障类型
认证失败

### 错误类型
postgres_peer_auth

### 关键词
peer authentication failed FATAL 认证 本地 失败

### 症状
- FATAL: Peer authentication failed for user "postgres"

### 常见原因
- 本地 socket 用 peer 认证，系统用户与库用户不一致

### 检查命令
- 用 psql -U 用户 -d 库 测试

### 解决思路
- 改用密码登录：psql -h 127.0.0.1
- 或改 pg_hba.conf 为 md5/scram
- 或用匹配的系统用户

## password authentication failed

### 别名
postgres 密码错误 密码认证失败 登录失败 password 不对

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
认证失败

### 错误类型
postgres_password_auth

### 关键词
password authentication failed FATAL 密码 认证 失败

### 症状
- FATAL: password authentication failed for user

### 常见原因
- 密码错误
- pg_hba.conf 认证方式不匹配

### 检查命令
- 核对密码与 pg_hba.conf

### 解决思路
- 核对密码
- 检查 pg_hba.conf 认证方式
- ALTER USER 重置密码

## connection refused 服务未启动

### 别名
postgres 连接被拒 服务未启动 连不上 拒绝连接

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
网络问题

### 错误类型
postgres_connection_refused

### 关键词
connection refused postgres 服务 未启动 拒绝 连接

### 症状
- connection refused
- could not connect to server

### 常见原因
- 服务未启动
- 端口不对或防火墙拦截

### 检查命令
- 确认服务已启动
- netstat -ano | findstr 5432

### 解决思路
- 启动 PostgreSQL 服务
- 核对端口与防火墙
- 检查监听地址

## database does not exist

### 别名
postgres 数据库不存在 库不存在 数据库找不到

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
配置错误

### 错误类型
postgres_db_not_exist

### 关键词
database does not exist 数据库 不存在

### 症状
- FATAL: database "xxx" does not exist

### 常见原因
- 数据库名拼写错误
- 未创建

### 检查命令
- \l 列出数据库

### 解决思路
- 核对数据库名
- createdb 创建

## relation does not exist 表不存在

### 别名
postgres 表不存在 relation 表找不到 表没有

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
运行异常

### 错误类型
postgres_table_not_found

### 关键词
relation does not exist 表 不存在

### 症状
- ERROR: relation "xxx" does not exist

### 常见原因
- 表名拼写错误
- 未加 schema 前缀
- 表未创建

### 检查命令
- \dt 列出表

### 解决思路
- 核对表名与 schema
- 用 public.表名 或指定 schema
- 确认表已创建

## psql command not found

### 别名
psql 命令找不到 postgres 命令找不到 未安装 客户端

### 平台
linux macos

### 技术栈
postgresql database

### 故障类型
环境依赖

### 错误类型
psql_command_not_found

### 关键词
psql command not found 未安装 PATH postgres

### 症状
- psql: command not found

### 常见原因
- 未安装 PostgreSQL 客户端
- bin 目录不在 PATH

### 检查命令
- which psql

### 解决思路
- 安装 postgresql-client
- 将 bin 加入 PATH

## PostgreSQL 启动失败

### 别名
postgres 启动失败 服务起不来 启动报错 pg_ctl 起不来

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
服务启动失败

### 错误类型
postgres_start_failed

### 关键词
postgres 启动 失败 服务 起不来 pg_ctl 日志

### 症状
- PostgreSQL 服务无法启动

### 常见原因
- 配置错误
- 数据目录权限问题

### 检查命令
- 查看日志与 pg_ctl status

### 解决思路
- 查看日志定位
- 检查数据目录权限
- 检查配置

## pg_hba.conf 配置

### 别名
pg_hba 认证配置 访问控制 连接被拒 pg_hba.conf 认证

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
配置错误

### 错误类型
postgres_pg_hba

### 关键词
pg_hba.conf 认证 访问 控制 host

### 症状
- 连接被认证策略拒绝

### 常见原因
- pg_hba.conf 规则不允许

### 检查命令
- 查看 pg_hba.conf

### 解决思路
- 添加 host 规则（md5/scram）
- 修改后 reload 生效

## 端口 5432 被占用

### 别名
postgres 端口被占用 5432 端口冲突 启动报端口

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
配置错误

### 错误类型
postgres_port

### 关键词
5432 端口 占用 冲突 bind address already in use

### 症状
- 启动报端口 5432 被占用

### 常见原因
- 已有进程占用 5432

### 检查命令
- netstat -ano | findstr 5432

### 解决思路
- 结束占用进程
- 或改端口

## permission denied for table

### 别名
postgres 表权限 denied 权限不足 无权限 对表没权限 操作拒绝

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
权限问题

### 错误类型
postgres_permission

### 关键词
permission denied for table 表

### 症状
- ERROR: permission denied for table xxx

### 常见原因
- 用户对表无操作权限

### 检查命令
- \dp 查看表权限

### 解决思路
- GRANT SELECT/INSERT ON 表 TO 用户
- 检查表 owner

## duplicate key value

### 别名
postgres 重复键 主键冲突 唯一键 重复 值

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
运行异常

### 错误类型
postgres_duplicate_key

### 关键词
duplicate key value 主键 唯一 冲突 重复

### 症状
- ERROR: duplicate key value violates unique constraint

### 常见原因
- 主键或唯一约束重复

### 检查命令
- 查看冲突值

### 解决思路
- 用 ON CONFLICT 处理
- 检查序列与数据
- 修正重复数据

## encoding 字符集

### 别名
postgres 字符集 encoding 编码 乱码 中文

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
配置错误

### 错误类型
postgres_encoding

### 关键词
encoding 字符集 编码 UTF8 乱码 中文

### 症状
- 中文乱码或编码不匹配

### 常见原因
- 数据库与客户端编码不一致

### 检查命令
- SHOW server_encoding

### 解决思路
- 统一 UTF8 编码
- 客户端设置 client_encoding

## 远程连接被拒 listen_addresses

### 别名
postgres 远程连接 连不上 外部访问 listen 监听

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
网络问题

### 错误类型
postgres_listen

### 关键词
listen_addresses 远程 连接 监听 外部 访问

### 症状
- 远程无法连接 PostgreSQL

### 常见原因
- 只监听 localhost
- pg_hba.conf 未放行

### 检查命令
- SHOW listen_addresses

### 解决思路
- 设置 listen_addresses='*'
- pg_hba.conf 放行远程
- 检查防火墙

## 版本升级

### 别名
postgres 版本 升级 旧版本 迁移 更新

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
版本不兼容

### 错误类型
postgres_version

### 关键词
postgres 版本 升级 更新 迁移 旧

### 症状
- 需要升级 PostgreSQL 版本

### 常见原因
- 版本过旧

### 检查命令
- psql --version

### 解决思路
- 用 pg_upgrade 或 pg_dump 迁移
- 备份后升级

## role does not exist

### 别名
postgres 角色不存在 用户不存在 role 用户 登录

### 平台
windows linux macos

### 技术栈
postgresql database

### 故障类型
认证失败

### 错误类型
postgres_role_not_exist

### 关键词
role does not exist 角色 用户 不存在

### 症状
- FATAL: role "xxx" does not exist

### 常见原因
- 用户/角色未创建
- 用户名拼写错误

### 检查命令
- \du 列出角色

### 解决思路
- CREATE ROLE 创建用户
- 核对用户名
