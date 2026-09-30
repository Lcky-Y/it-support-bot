# MySQL 故障知识库

## Access denied for user 认证失败

### 别名
mysql 认证失败 access denied 密码错误 登录失败 1045 权限

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
认证失败

### 错误类型
mysql_access_denied

### 关键词
Access denied for user ERROR 1045 密码 认证 登录

### 症状
- ERROR 1045 (28000): Access denied for user 'xxx'@'localhost'

### 常见原因
- 密码错误
- 用户无该主机访问权限
- 用户不存在或未授权

### 检查命令
- mysql -u 用户 -p 尝试登录

### 解决思路
- 核对密码
- 用 root 授权：GRANT ALL ON 库.* TO '用户'@'主机'
- 检查用户是否存在

## Can't connect to MySQL server

### 别名
mysql 连接被拒 连接不上 10061 2003 服务未启动

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
网络问题

### 错误类型
mysql_connection_refused

### 关键词
Can't connect to MySQL server connection refused ERROR 2003 10061 服务

### 症状
- ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost' (10061)
- 连接被拒绝

### 常见原因
- MySQL 服务未启动
- 端口不对或防火墙拦截
- 主机地址错误

### 检查命令
- 确认服务已启动
- netstat -ano | findstr 3306

### 解决思路
- 启动 MySQL 服务
- 核对端口与主机
- 检查防火墙放行 3306

## Unknown database

### 别名
mysql 数据库不存在 1049 库不存在 数据库找不到

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
配置错误

### 错误类型
mysql_unknown_database

### 关键词
Unknown database ERROR 1049 数据库 不存在

### 症状
- ERROR 1049 (42000): Unknown database 'xxx'

### 常见原因
- 数据库名拼写错误
- 数据库未创建

### 检查命令
- SHOW DATABASES;

### 解决思路
- 核对数据库名
- CREATE DATABASE 创建
- 确认连接的是正确实例

## Table doesn't exist 表不存在

### 别名
mysql 表不存在 1146 表找不到 表没有

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_table_not_found

### 关键词
Table doesn't exist ERROR 1146 表 不存在

### 症状
- ERROR 1146 (42S02): Table 'xxx' doesn't exist

### 常见原因
- 表名拼写错误
- 连错数据库
- 表被删除

### 检查命令
- SHOW TABLES;

### 解决思路
- 核对表名与当前库
- USE 正确数据库
- 确认表已创建

## SQL 语法错误

### 别名
mysql sql 语法错误 1064 写错了 查询报错

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_syntax_error

### 关键词
ERROR 1064 SQL syntax 语法 错误 query

### 症状
- ERROR 1064 (42000): You have an error in your SQL syntax

### 常见原因
- SQL 语法写错
- 关键字/引号/逗号问题

### 检查命令
- 查看报错附近语句

### 解决思路
- 检查关键字拼写
- 检查引号与逗号
- 核对 SQL 语法

## 中文乱码字符集

### 别名
mysql 乱码 字符集 utf8mb4 中文 问号 编码

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
配置错误

### 错误类型
mysql_charset

### 关键词
utf8mb4 字符集 charset 乱码 中文 编码

### 症状
- 中文显示为乱码或问号

### 常见原因
- 字符集不一致
- 未用 utf8mb4

### 检查命令
- SHOW VARIABLES LIKE 'character%'

### 解决思路
- 库表字段统一 utf8mb4
- 连接串加 characterEncoding=utf8
- 改默认字符集

## 死锁 deadlock

### 别名
mysql 死锁 deadlock 1213 锁冲突 事务

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_deadlock

### 关键词
Deadlock found ERROR 1213 死锁 事务 锁

### 症状
- ERROR 1213 (40001): Deadlock found when trying to get lock

### 常见原因
- 多个事务相互等待锁
- 加锁顺序不一致

### 检查命令
- SHOW ENGINE INNODB STATUS

### 解决思路
- 统一加锁顺序
- 缩短事务
- 捕获重试

## Lock wait timeout exceeded

### 别名
mysql 锁等待超时 1205 锁超时 等锁

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_lock_wait

### 关键词
Lock wait timeout exceeded ERROR 1205 锁 超时

### 症状
- ERROR 1205 (HY000): Lock wait timeout exceeded

### 常见原因
- 事务长时间未提交占锁
- 长事务阻塞

### 检查命令
- SHOW PROCESSLIST 查看占用

### 解决思路
- 结束长时间未提交的事务
- 优化事务时长
- 增大 innodb_lock_wait_timeout

## mysqld command not found

### 别名
mysqld 命令找不到 mysql 命令找不到 服务 找不到 未安装

### 平台
linux macos

### 技术栈
mysql database

### 故障类型
环境依赖

### 错误类型
mysql_command_not_found

### 关键词
mysqld command not found mysql 未安装 PATH

### 症状
- mysqld: command not found
- mysql: command not found

### 常见原因
- 未安装 MySQL
- bin 目录不在 PATH

### 检查命令
- which mysql

### 解决思路
- 安装 MySQL
- 将 bin 目录加入 PATH

## MySQL 启动失败

### 别名
mysql 启动失败 服务起不来 启动报错 mysqld 起不来

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
服务启动失败

### 错误类型
mysql_start_failed

### 关键词
mysqld 启动 失败 服务 起不来 日志

### 症状
- MySQL 服务无法启动

### 常见原因
- 配置错误
- 数据目录权限或损坏

### 检查命令
- 查看 MySQL 错误日志

### 解决思路
- 查看错误日志定位
- 检查 my.cnf / my.ini 配置
- 检查数据目录权限

## caching_sha2_password 认证

### 别名
mysql 认证插件 caching_sha2 连接报错 8.0 驱动

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
认证失败

### 错误类型
mysql_auth_plugin

### 关键词
caching_sha2_password 认证 插件 驱动 连接

### 症状
- 连接报认证插件错误
- 客户端不支持 caching_sha2_password

### 常见原因
- MySQL 8 默认认证插件与老驱动不兼容

### 检查命令
- 查看驱动版本

### 解决思路
- 升级驱动
- 或改用户认证为 mysql_native_password
- 或改默认认证插件

## 连接超时 / 慢

### 别名
mysql 连接超时 连不上 慢 连接卡住 卡着 一直卡

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
网络问题

### 错误类型
mysql_connection_timeout

### 关键词
MySQL 连接 超时 timeout 慢 网络

### 症状
- 连接 MySQL 长时间无响应或超时

### 常见原因
- 网络不通
- DNS 反查慢
- 连接数满

### 检查命令
- 检查网络与连通性

### 解决思路
- 检查网络与防火墙
- 关闭 skip-name-resolve 反查
- 检查最大连接数

## Duplicate entry 重复键

### 别名
mysql 重复键 1062 主键冲突 唯一键 重复

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_duplicate_key

### 关键词
Duplicate entry ERROR 1062 主键 唯一 重复

### 症状
- ERROR 1062 (23000): Duplicate entry 'xxx' for key

### 常见原因
- 主键或唯一键重复

### 检查命令
- 查看冲突键值

### 解决思路
- 改用 INSERT ... ON DUPLICATE KEY UPDATE
- 或 INSERT IGNORE
- 检查数据是否重复

## 外键约束失败

### 别名
mysql 外键约束 1452 约束失败 外键报错

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_foreign_key

### 关键词
foreign key constraint ERROR 1452 外键 约束

### 症状
- ERROR 1452 (23000): Cannot add or update a child row

### 常见原因
- 外键引用的父记录不存在

### 检查命令
- 核对关联表数据

### 解决思路
- 先插入父记录
- 或关闭外键检查（临时）
- 核对关联数据一致性

## 表损坏 repair

### 别名
mysql 表损坏 repair 修复 表坏了 崩溃

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_table_corrupt

### 关键词
table corrupt repair 表 损坏 修复 crash

### 症状
- 查询报表损坏或崩溃

### 常见原因
- 异常断电或磁盘问题

### 检查命令
- CHECK TABLE 表名

### 解决思路
- REPAIR TABLE 表名
- 从备份恢复
- 检查磁盘

## 端口 3306 被占用

### 别名
mysql 端口被占用 3306 端口冲突 启动报端口

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
配置错误

### 错误类型
mysql_port

### 关键词
3306 端口 占用 冲突 bind address already in use

### 症状
- MySQL 启动报端口 3306 被占用

### 常见原因
- 已有进程占用 3306

### 检查命令
- netstat -ano | findstr 3306

### 解决思路
- 结束占用进程
- 或改端口
- 检查是否重复启动

## 用户授权 grant

### 别名
mysql 授权 grant 权限 用户 访问权限 远程访问

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
配置错误

### 错误类型
mysql_grant

### 关键词
GRANT 授权 用户 远程

### 症状
- 用户无权限或无法远程访问

### 常见原因
- 未授权
- 用户限定 localhost

### 检查命令
- SHOW GRANTS FOR 用户

### 解决思路
- GRANT ALL ON 库.* TO '用户'@'%'
- FLUSH PRIVILEGES
- 允许远程主机

## Too many connections

### 别名
mysql 连接数太多 1040 连接数满 连不上 连接超限

### 平台
windows linux macos

### 技术栈
mysql database

### 故障类型
运行异常

### 错误类型
mysql_too_many_connections

### 关键词
Too many connections ERROR 1040 连接数 满

### 症状
- ERROR 1040 (08004): Too many connections

### 常见原因
- 连接数达到上限
- 连接未释放

### 检查命令
- SHOW VARIABLES LIKE 'max_connections'

### 解决思路
- 调大 max_connections
- 释放空闲连接
- 用连接池
