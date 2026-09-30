# Java 故障知识库

## java command not found

### 别名
java 命令找不到 java 不存在 未安装 java 找不到

### 平台
linux macos

### 技术栈
java jdk

### 故障类型
环境依赖

### 错误类型
java_command_not_found

### 关键词
java command not found 未安装 PATH

### 症状
- bash: java: command not found

### 常见原因
- 未安装 JDK/JRE
- java 不在 PATH 中

### 检查命令
- which java
- java -version

### 解决思路
- 安装 JDK 并配置 JAVA_HOME 与 PATH
- 重新加载 shell 配置
- 确认 PATH 含 JDK 的 bin 目录

## java 不是内部或外部命令

### 别名
java 不是内部或外部命令 Windows 无法识别 java 找不到

### 平台
windows

### 技术栈
java jdk

### 故障类型
环境依赖

### 错误类型
java_not_recognized_windows

### 关键词
java 不是内部或外部命令 Windows 无法识别 PATH

### 症状
- 'java' 不是内部或外部命令，也不是可运行的程序或批处理文件

### 常见原因
- 未安装 JDK
- PATH 未包含 JDK bin 目录
- 安装后未重开终端

### 检查命令
- where java

### 解决思路
- 安装 JDK
- 将 JDK bin 目录加入 PATH
- 重开终端

## javac command not found

### 别名
javac 命令找不到 编译器找不到 找不到编译器 编译不了

### 平台
windows linux macos

### 技术栈
java jdk javac

### 故障类型
环境依赖

### 错误类型
javac_command_not_found

### 关键词
javac command not found 未安装 PATH 编译

### 症状
- javac: command not found
- 只装了 JRE 没有编译器

### 常见原因
- 只装了 JRE 未装 JDK
- javac 不在 PATH

### 检查命令
- which javac
- java -version

### 解决思路
- 安装完整 JDK（含 javac）
- 配置 JAVA_HOME 与 PATH

## JAVA_HOME 配置

### 别名
JAVA_HOME 没配 设置 java home 环境变量 java 环境

### 平台
windows linux macos

### 技术栈
java jdk

### 故障类型
配置错误

### 错误类型
java_home

### 关键词
JAVA_HOME 环境变量 配置 找不到 设置

### 症状
- 程序报 JAVA_HOME 未设置或指向错误

### 常见原因
- 未设置 JAVA_HOME
- 指向了 JRE 而非 JDK

### 检查命令
- echo %JAVA_HOME%（Windows）或 echo $JAVA_HOME

### 解决思路
- 设置 JAVA_HOME 指向 JDK 根目录
- 将 %JAVA_HOME%\bin 或 $JAVA_HOME/bin 加入 PATH

## JDK 与 JRE 区别

### 别名
JDK JRE 区别 装哪个 编译 运行 区别

### 平台
windows linux macos

### 技术栈
java jdk jre

### 故障类型
排查方法

### 错误类型
java_jdk_jre

### 关键词
JDK JRE 区别 javac java 编译 运行 装哪个

### 症状
- 不确定装 JDK 还是 JRE

### 常见原因
- 两者用途不同

### 检查命令
- 判断是否需要编译（javac）

### 解决思路
- 开发/编译需装 JDK（含 JRE + javac）
- 只运行程序可只装 JRE
- 生产运行一般用 JRE 或精简 JDK

## UnsupportedClassVersionError

### 别名
class version 不匹配 编译版本过高 运行不了 major minor 版本太高 类版本太高 版本不一致

### 平台
windows linux macos

### 技术栈
java jdk

### 故障类型
版本不兼容

### 错误类型
java_unsupported_class_version

### 关键词
UnsupportedClassVersionError class file version 版本 不匹配 major minor

### 症状
- java.lang.UnsupportedClassVersionError
- class file version 61.0，当前只能运行 52.0

### 常见原因
- 用高版本 JDK 编译，低版本 JRE 运行

### 检查命令
- java -version
- javac -version

### 解决思路
- 统一编译与运行版本
- 或用 javac --release 指定较低版本编译
- 升级运行时 JDK

## ClassNotFoundException

### 别名
找不到类 类找不到 类没有加载 class 找不到 类未定义

### 平台
windows linux macos

### 技术栈
java

### 故障类型
运行异常

### 错误类型
java_class_not_found

### 关键词
ClassNotFoundException 找不到类 classpath 类路径

### 症状
- java.lang.ClassNotFoundException: xxx

### 常见原因
- 类不在 classpath 中
- 依赖 jar 缺失
- 反射加载的类名写错

### 检查命令
- 检查 classpath 与依赖 jar

### 解决思路
- 确认依赖 jar 已加入 classpath
- 核对全限定类名
- 检查 JDBC 驱动等动态加载的类

## NoClassDefFoundError

### 别名
类定义找不到 运行时找不到类 类加载失败 缺少依赖

### 平台
windows linux macos

### 技术栈
java

### 故障类型
运行异常

### 错误类型
java_no_class_def

### 关键词
NoClassDefFoundError 找不到类定义 运行时 classpath

### 症状
- java.lang.NoClassDefFoundError: xxx

### 常见原因
- 编译时存在、运行时类缺失
- 依赖版本不一致
- 静态初始化失败

### 检查命令
- 检查运行 classpath 与依赖版本

### 解决思路
- 补齐缺失的运行时依赖
- 统一依赖版本
- 排查静态块异常

## NoSuchMethodError

### 别名
方法找不到 方法不存在 版本不对 方法报错

### 平台
windows linux macos

### 技术栈
java

### 故障类型
版本不兼容

### 错误类型
java_no_such_method

### 关键词
NoSuchMethodError 方法不存在 版本 不兼容

### 症状
- java.lang.NoSuchMethodError

### 常见原因
- 依赖库版本不匹配
- 编译与运行使用的版本不同

### 检查命令
- 检查依赖 jar 版本

### 解决思路
- 统一依赖版本
- 排除冲突的旧版 jar
- 用 mvn dependency:tree 排查

## 编译错误 cannot find symbol

### 别名
编译不过 找不到符号 变量未定义 编译报错 symbol

### 平台
windows linux macos

### 技术栈
java javac

### 故障类型
运行异常

### 错误类型
java_cannot_find_symbol

### 关键词
cannot find symbol 编译 错误 javac 找不到符号

### 症状
- error: cannot find symbol

### 常见原因
- 变量或方法名拼写错误
- 缺少 import
- 依赖 jar 未加入编译 classpath

### 检查命令
- 查看报错行定位符号

### 解决思路
- 核对拼写与 import
- 补充 import 或依赖
- 检查方法签名

## OutOfMemoryError Java heap space

### 别名
内存溢出 堆内存不够 oom 爆内存 堆溢出

### 平台
windows linux macos

### 技术栈
java jvm

### 故障类型
性能问题

### 错误类型
java_heap_oom

### 关键词
OutOfMemoryError Java heap space Xmx 堆内存 溢出

### 症状
- java.lang.OutOfMemoryError: Java heap space

### 常见原因
- 堆内存不足
- 数据量过大或内存泄漏

### 检查命令
- jmap -heap 查看堆使用

### 解决思路
- 增大堆：-Xmx 调大
- 排查内存泄漏（jmap / jstat）
- 优化数据处理

## OutOfMemoryError Metaspace

### 别名
元空间溢出 metaspace oom 永久代 类加载过多

### 平台
windows linux macos

### 技术栈
java jvm

### 故障类型
性能问题

### 错误类型
java_metaspace_oom

### 关键词
OutOfMemoryError Metaspace PermGen 元空间 永久代

### 症状
- java.lang.OutOfMemoryError: Metaspace
- 老版本 PermGen space

### 常见原因
- 加载类过多（动态代理/热部署）
- Metaspace 默认上限偏小

### 检查命令
- 观察类加载数量

### 解决思路
- 调大 -XX:MaxMetaspaceSize
- 排查类加载泄漏（热部署框架）

## StackOverflowError

### 别名
栈溢出 递归太深 爆栈 死循环 递归

### 平台
windows linux macos

### 技术栈
java jvm

### 故障类型
运行异常

### 错误类型
java_stack_overflow

### 关键词
StackOverflowError 栈溢出 递归 死循环

### 症状
- java.lang.StackOverflowError

### 常见原因
- 递归无终止条件
- 递归层数过深

### 检查命令
- 查看堆栈定位递归调用

### 解决思路
- 检查递归终止条件
- 递归改循环
- 或增大 -Xss 栈大小

## NullPointerException

### 别名
空指针 npe 空指针异常 null 报错

### 平台
windows linux macos

### 技术栈
java

### 故障类型
运行异常

### 错误类型
java_null_pointer

### 关键词
NullPointerException NPE 空指针 null

### 症状
- java.lang.NullPointerException

### 常见原因
- 对象未初始化就调用
- 集合里取出 null

### 检查命令
- 查看堆栈定位空引用行

### 解决思路
- 调用前判空
- 用 Optional 或默认值
- 定位为 null 的对象来源

## ClassCastException

### 别名
类型转换失败 强转报错 类型转换 异常

### 平台
windows linux macos

### 技术栈
java

### 故障类型
运行异常

### 错误类型
java_class_cast

### 关键词
ClassCastException 类型转换 强转 失败

### 症状
- java.lang.ClassCastException

### 常见原因
- 强制类型转换的目标类型不匹配

### 检查命令
- 查看堆栈定位强转处

### 解决思路
- 强转前用 instanceof 判断
- 使用泛型避免强转
- 检查实际对象类型

## jar 打包与运行

### 别名
打 jar 包 运行 jar 找不到主类 manifest 打包

### 平台
windows linux macos

### 技术栈
java jar

### 故障类型
排查方法

### 错误类型
java_jar

### 关键词
jar 打包 运行 manifest main-class 主类

### 症状
- 需要打包或运行 jar

### 常见原因
- 未指定 Main-Class

### 检查命令
- jar tf 查看内容

### 解决思路
- 打包：jar cfe app.jar MainClass 类文件
- 运行：java -jar app.jar
- 清单需含 Main-Class 项

## 找不到或无法加载主类

### 别名
找不到主类 无法加载主类 main class 找不到 主类错误

### 平台
windows linux macos

### 技术栈
java

### 故障类型
配置错误

### 错误类型
java_main_class

### 关键词
Could not find or load main class 主类 classpath

### 症状
- 错误: 找不到或无法加载主类 xxx
- Could not find or load main class

### 常见原因
- 类名含包名未写全
- classpath 不含编译输出目录
- 当前目录不对

### 检查命令
- ls 确认 .class 文件位置

### 解决思路
- 使用全限定类名
- java -cp . 类名 指定 classpath
- 确认 .class 输出目录

## classpath 配置

### 别名
classpath 设置 类路径 找不到 -cp 依赖 类路径

### 平台
windows linux macos

### 技术栈
java

### 故障类型
配置错误

### 错误类型
java_classpath

### 关键词
classpath 类路径 配置 -cp 依赖

### 症状
- 运行报找不到类

### 常见原因
- classpath 未包含依赖 jar

### 检查命令
- echo %CLASSPATH% 或 echo $CLASSPATH

### 解决思路
- java -cp 依赖.jar:主类 运行
- 或用构建工具管理依赖

## 端口占用 BindException

### 别名
端口被占用 bind 失败 启动报端口 address already in use 端口冲突

### 平台
windows linux macos

### 技术栈
java

### 故障类型
配置错误

### 错误类型
java_bind_exception

### 关键词
BindException Address already in use 端口 占用

### 症状
- java.net.BindException: Address already in use

### 常见原因
- 端口已被其它进程占用

### 检查命令
- netstat -ano | findstr 端口（Windows）或 ss -tlnp

### 解决思路
- 结束占用进程
- 或更换端口
- 检查是否重复启动

## JDBC 驱动找不到

### 别名
数据库驱动找不到 jdbc 驱动 mysql 驱动 数据库连接失败

### 平台
windows linux macos

### 技术栈
java jdbc mysql

### 故障类型
运行异常

### 错误类型
java_jdbc_driver

### 关键词
ClassNotFoundException com.mysql jdbc Driver 数据库

### 症状
- ClassNotFoundException: com.mysql.jdbc.Driver

### 常见原因
- 未添加 JDBC 驱动依赖
- 驱动类名写错

### 检查命令
- 检查依赖里是否有驱动 jar

### 解决思路
- 添加对应数据库驱动依赖
- 新版本驱动类名改为 com.mysql.cj.jdbc.Driver

## 多 JDK 版本切换

### 别名
切换 jdk 版本 装了好几个 java 版本 java -version 不对

### 平台
windows linux macos

### 技术栈
java jdk

### 故障类型
配置错误

### 错误类型
java_switch_version

### 关键词
JDK 版本 切换 多个 java -version 环境变量

### 症状
- java -version 显示的不是期望版本

### 常见原因
- 系统装了多个 JDK，PATH 顺序不对

### 检查命令
- java -version
- where java（Windows）

### 解决思路
- 调整 PATH 中 JDK 顺序
- 或用工具（如 jenv）管理版本
- 确保 JAVA_HOME 与 PATH 一致

## java 版本过旧升级

### 别名
升级 java 版本 更新 jdk java 过旧 下载 jdk

### 平台
windows linux macos

### 技术栈
java jdk

### 故障类型
版本不兼容

### 错误类型
java_upgrade

### 关键词
java 版本 过旧 升级 更新 jdk 下载

### 症状
- 程序需要更高 Java 版本

### 常见原因
- 本地 JDK 过旧

### 检查命令
- java -version

### 解决思路
- 下载安装新版 JDK
- 更新 JAVA_HOME 与 PATH
- 确认新版本生效

## Spring Boot 启动失败

### 别名
spring 启动失败 起不来 bean 报错 启动就退出 应用上下文

### 平台
windows linux macos

### 技术栈
java spring springboot

### 故障类型
运行异常

### 错误类型
java_spring_boot_failed

### 关键词
Spring Boot ApplicationContext 启动 失败 Bean 创建

### 症状
- Application run failed
- 启动时 Bean 创建失败

### 常见原因
- Bean 配置或依赖注入错误
- 配置项错误

### 检查命令
- 查看启动堆栈与最后异常

### 解决思路
- 定位最后一个 Caused by
- 检查 @Configuration / 依赖注入
- 核对 application.yml 配置

## Spring Boot 端口冲突

### 别名
spring 端口占用 8080 被占 spring 端口冲突 起服务报端口

### 平台
windows linux macos

### 技术栈
java spring springboot

### 故障类型
配置错误

### 错误类型
java_spring_port

### 关键词
Spring Boot Port already in use 端口 占用 启动

### 症状
- Port 8080 was already in use
- Spring Boot 启动报端口冲突

### 常见原因
- 端口被占用

### 检查命令
- netstat -ano | findstr 8080

### 解决思路
- 结束占用进程
- 改端口：server.port=8081
- 检查是否重复启动

## 文件编码乱码

### 别名
编译乱码 中文乱码 编码不对 javac 编码 乱码

### 平台
windows linux macos

### 技术栈
java javac

### 故障类型
配置错误

### 错误类型
java_encoding

### 关键词
javac -encoding 乱码 GBK UTF-8 编码

### 症状
- 编译报错或中文乱码

### 常见原因
- 源文件编码与编译编码不一致

### 检查命令
- 检查源文件编码

### 解决思路
- javac -encoding UTF-8 编译
- 统一源文件编码为 UTF-8
- 运行加 -Dfile.encoding=UTF-8
