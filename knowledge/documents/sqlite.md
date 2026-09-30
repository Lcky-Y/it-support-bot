# SQLite 故障知识库

## database is locked

### 别名
sqlite 数据库被锁 database locked 锁定 被占用 锁

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_locked

### 关键词
database is locked SQLite 锁 锁定 占用

### 症状
- sqlite3.OperationalError: database is locked

### 常见原因
- 多个连接同时写
- 事务未提交

### 检查命令
- 检查是否有未提交事务

### 解决思路
- 提交/回滚未完成事务
- 减少并发写
- 设置 busy_timeout 等待

## no such table

### 别名
sqlite 表不存在 no such table 表找不到 表没有

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_no_such_table

### 关键词
no such table SQLite 表 不存在

### 症状
- sqlite3.OperationalError: no such table

### 常见原因
- 表名拼写错误
- 连错数据库文件
- 表未创建

### 检查命令
- 列出表 .tables

### 解决思路
- 核对表名
- 确认数据库文件路径正确
- 执行建表语句

## unable to open database file

### 别名
sqlite 打不开数据库文件 无法打开 数据库文件打不开 权限 路径

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
权限问题

### 错误类型
sqlite_cannot_open

### 关键词
unable to open database file SQLite 打开 权限 路径

### 症状
- sqlite3.OperationalError: unable to open database file

### 常见原因
- 文件路径不存在或错误
- 目录无写权限
- 文件被占用

### 检查命令
- 确认路径与目录权限

### 解决思路
- 检查路径是否存在
- 确保目录可写
- 确认文件未被占用

## malformed database

### 别名
sqlite 数据库损坏 文件损坏 malformed

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_malformed

### 关键词
malformed SQLite 数据库 损坏

### 症状
- DatabaseError: file is not a database
- malformed database

### 常见原因
- 文件损坏
- 文件不是 SQLite 数据库

### 检查命令
- file 数据库文件 查看类型

### 解决思路
- 从备份恢复
- 确认文件类型正确
- 避免异常中断写入

## OperationalError 线程

### 别名
sqlite 线程错误 same thread OperationalError 多线程

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_thread

### 关键词
OperationalError SQLite thread 线程 same thread 连接

### 症状
- SQLite objects created in a thread can only be used in that same thread

### 常见原因
- 跨线程使用同一连接

### 检查命令
- 检查连接使用位置

### 解决思路
- 每线程独立连接
- 或 connect 加 check_same_thread=False
- 用连接池管理

## busy 锁等待

### 别名
sqlite busy 忙 锁等待 超时 并发写

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_busy

### 关键词
SQLite busy timeout 锁 等待 并发 写

### 症状
- database table is locked / busy

### 常见原因
- 并发写冲突

### 检查命令
- 检查并发写入

### 解决思路
- 设置 busy_timeout
- 串行化写操作
- 用 WAL 模式

## 只读 / 文件权限

### 别名
sqlite 只读 权限 read-only 不能写 写入失败

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
权限问题

### 错误类型
sqlite_readonly

### 关键词
read-only SQLite 只读 权限 写 失败

### 症状
- attempt to write a readonly database

### 常见原因
- 文件或目录只读
- 权限不足

### 检查命令
- 检查文件权限

### 解决思路
- 修改文件/目录权限
- 确保可写

## 文件路径问题

### 别名
sqlite 相对路径 文件路径 目录 路径错误

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
配置错误

### 错误类型
sqlite_path

### 关键词
SQLite 路径 相对 文件路径 目录

### 症状
- 连错数据库文件

### 常见原因
- 相对路径解析到错误目录

### 检查命令
- 确认数据库文件绝对路径

### 解决思路
- 使用绝对路径
- 确认工作目录
- 检查路径拼写

## 表结构变更 migration

### 别名
sqlite 表结构 迁移 加字段 改表 列 不存在

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
配置错误

### 错误类型
sqlite_migration

### 关键词
SQLite 表结构 迁移 加字段 列 改表

### 症状
- 报列不存在或表结构不符

### 常见原因
- 表结构变更未同步

### 检查命令
- 查看表结构 PRAGMA table_info

### 解决思路
- 执行迁移脚本
- 用 ALTER TABLE 加列
- 用 ORM 的 migration 工具

## 磁盘 I/O 错误

### 别名
sqlite 磁盘 io 错误 空间不足 写入失败 disk

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
存储问题

### 错误类型
sqlite_io_error

### 关键词
SQLite disk I/O error 磁盘 空间 不足 写

### 症状
- disk I/O error
- 写入失败

### 常见原因
- 磁盘空间不足
- 磁盘故障

### 检查命令
- df -h 检查磁盘

### 解决思路
- 释放磁盘空间
- 检查磁盘健康
- 换存储位置

## no such column

### 别名
sqlite 列不存在 no such column 字段 找不到 列 没有

### 平台
windows linux macos

### 技术栈
sqlite database

### 故障类型
运行异常

### 错误类型
sqlite_no_such_column

### 关键词
no such column SQLite 列 字段 不存在

### 症状
- sqlite3.OperationalError: no such column

### 常见原因
- 列名拼写错误
- 表结构已变更

### 检查命令
- PRAGMA table_info 查看列

### 解决思路
- 核对列名
- 检查表结构是否变更
- 修正 SQL
