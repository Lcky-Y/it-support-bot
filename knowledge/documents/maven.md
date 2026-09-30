# Maven 故障知识库

## mvn command not found

### 别名
mvn 命令找不到 maven 找不到 未安装 mvn 不存在

### 平台
linux macos

### 技术栈
maven mvn

### 故障类型
环境依赖

### 错误类型
maven_command_not_found

### 关键词
mvn command not found 未安装 PATH maven

### 症状
- bash: mvn: command not found

### 常见原因
- 未安装 Maven
- mvn 不在 PATH

### 检查命令
- which mvn
- mvn -version

### 解决思路
- 安装 Maven 并配置 PATH
- 或使用 IDE 内置 Maven

## mvn 不是内部或外部命令

### 别名
mvn 找不到 maven 无法识别 Windows mvn 命令

### 平台
windows

### 技术栈
maven mvn

### 故障类型
环境依赖

### 错误类型
maven_not_recognized_windows

### 关键词
mvn 不是内部或外部命令 Windows 无法识别 PATH

### 症状
- 'mvn' 不是内部或外部命令，也不是可运行的程序或批处理文件

### 常见原因
- 未安装 Maven
- PATH 未包含 Maven bin 目录

### 检查命令
- where mvn

### 解决思路
- 安装 Maven
- 将 Maven bin 目录加入 PATH
- 重开终端

## mvn 报 JAVA_HOME 未设置

### 别名
mvn 报 java home maven 需要 java JAVA_HOME 未设置 无法运行

### 平台
windows linux macos

### 技术栈
maven java jdk

### 故障类型
配置错误

### 错误类型
maven_java_home

### 关键词
JAVA_HOME 未设置 mvn JAVA_HOME is not defined

### 症状
- JAVA_HOME is not defined
- mvn 无法启动

### 常见原因
- 未设置 JAVA_HOME
- JAVA_HOME 指向错误

### 检查命令
- echo $JAVA_HOME 或 echo %JAVA_HOME%

### 解决思路
- 设置 JAVA_HOME 指向 JDK
- 确认路径存在

## Could not resolve dependencies

### 别名
依赖解析失败 依赖下载不下来 依赖拉不下来 依赖解析不了 下载不下来 拉依赖

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_dependency_resolve

### 关键词
Could not resolve dependencies 依赖 解析 失败

### 症状
- Could not resolve dependencies for project xxx

### 常见原因
- 依赖不在仓库中
- 网络/仓库源问题
- 版本号错误

### 检查命令
- mvn dependency:resolve

### 解决思路
- 核对依赖坐标与版本
- 检查 settings.xml 的镜像/仓库
- 用 mvn -X 查看详细解析过程

## Maven 找不到依赖 404

### 别名
依赖找不到 下载依赖 404 找不到这个依赖 依赖不存在

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_dependency_not_found

### 关键词
Could not find artifact 404 Not Found 依赖

### 症状
- Could not find artifact xxx
- 404 Not Found 下载依赖失败

### 常见原因
- 依赖坐标或版本错误
- 私有依赖未配置私服
- 仓库里没有该包

### 检查命令
- 到仓库搜索该依赖是否存在

### 解决思路
- 核对 groupId/artifactId/version
- 私有依赖配置私服地址
- 换用存在的版本

## Maven 镜像源配置

### 别名
maven 换源 阿里源 镜像加速 下载慢 中央仓库慢

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
网络问题

### 错误类型
maven_mirror

### 关键词
maven mirror 阿里云 镜像 源 settings.xml 下载慢

### 症状
- Maven 下载依赖缓慢或超时

### 常见原因
- 默认中央仓库访问慢

### 检查命令
- 查看 settings.xml

### 解决思路
- settings.xml 配置阿里云镜像
- mirrorOf 设为 central
- 改后重新构建

## Maven SSL 证书错误 PKIX

### 别名
证书链验证失败 ssl 证书报错 PKIX 验证失败

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
网络问题

### 错误类型
maven_ssl_pkix

### 关键词
maven PKIX path building failed certificate SunCertPathBuilderException 证书验证

### 症状
- PKIX path building failed
- sun.security.provider.certpath.SunCertPathBuilderException

### 常见原因
- 公司代理替换了证书
- 私有仓库证书不受信任

### 检查命令
- 确认仓库地址与证书

### 解决思路
- 导入证书到 JDK 信任库（keytool -import）
- 检查代理是否拦截
- 或改用 http 镜像（不推荐）

## Maven 代理设置

### 别名
maven 走代理 翻墙 设置代理 下载慢 maven 代理设置

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
网络问题

### 错误类型
maven_proxy

### 关键词
maven proxy settings.xml 走代理 7890

### 症状
- Maven 下载缓慢或超时

### 常见原因
- 需要走代理访问仓库

### 检查命令
- 查看 settings.xml 的 proxy 配置

### 解决思路
- settings.xml 配置 <proxy> 指向本地代理
- 或配置镜像源
- 改后重新构建

## maven-compiler-plugin 版本

### 别名
编译插件版本 maven compiler 插件 source target 编译

### 平台
windows linux macos

### 技术栈
maven java

### 故障类型
版本不兼容

### 错误类型
maven_compiler_plugin

### 关键词
maven-compiler-plugin source target 编译 版本 release

### 症状
- 编译版本与 JDK 不匹配
- 需要指定编译版本

### 常见原因
- 未配置编译插件版本
- 默认版本与 JDK 不匹配

### 检查命令
- mvn help:effective-pom 查看插件版本

### 解决思路
- pom.xml 配置 maven-compiler-plugin
- 设置 source/target 或 release
- 指定插件版本

## source/target 不匹配

### 别名
编译版本不对 1.7 1.8 source target 版本 编译报错

### 平台
windows linux macos

### 技术栈
maven java

### 故障类型
版本不兼容

### 错误类型
maven_source_target

### 关键词
source target release 编译 版本 不匹配 maven compiler

### 症状
- 编译提示 source/target 版本不支持
- 需要更高 JDK 编译

### 常见原因
- pom 里 source/target 高于本地 JDK
- 默认编译版本过低

### 检查命令
- java -version 与 pom 配置对比

### 解决思路
- 调整 source/target 匹配 JDK
- 或升级 JDK
- 建议用 <release> 属性

## pom.xml 语法错误

### 别名
pom 报错 xml 语法错误 解析失败 pom 格式错误

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
配置错误

### 错误类型
maven_pom_syntax

### 关键词
pom.xml XML 解析 失败 parse 语法错误

### 症状
- 构建报 XML 解析失败
- 提示标签未闭合

### 常见原因
- pom.xml 标签写错或未闭合
- 编码问题

### 检查命令
- 用编辑器检查 XML 格式

### 解决思路
- 修正 XML 标签
- 用 IDE 校验 pom.xml
- 检查 BOM 或编码

## Plugin not found 插件解析失败

### 别名
插件找不到 plugin 下载失败 插件解析不了 插件不存在

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_plugin_not_found

### 关键词
Plugin not found plugin 插件 解析 失败 maven

### 症状
- Plugin xxx not found
- 插件解析或下载失败

### 常见原因
- 插件版本不存在
- 仓库未同步该插件

### 检查命令
- 查看具体插件坐标

### 解决思路
- 核对插件版本
- 检查镜像/私服配置
- 指定存在的插件版本

## .m2/repository 清理

### 别名
本地仓库清理 依赖损坏 m2 仓库 重新下载依赖

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_m2_clean

### 关键词
.m2 repository 本地仓库 清理 损坏

### 症状
- 依赖下载一半损坏导致构建失败

### 常见原因
- 本地仓库依赖损坏或不完整

### 检查命令
- 查看 ~/.m2/repository 下对应目录

### 解决思路
- 删除损坏依赖目录重新下载
- 或删整个 repository 重下
- 换镜像源后重试

## mvn package 打包失败

### 别名
打包失败 build 失败 编译不过 mvn 打包 报错

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_package_failed

### 关键词
mvn package 打包 失败 build failure

### 症状
- BUILD FAILURE
- 打包过程报错

### 常见原因
- 编译错误
- 测试失败
- 插件问题

### 检查命令
- mvn package -DskipTests 快速定位

### 解决思路
- 查看报错定位编译或测试问题
- 加 -e 查看完整堆栈
- 修好后重新打包

## mvn test 失败

### 别名
测试失败 surefire 跑不过 单元测试失败 mvn 测试

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
运行异常

### 错误类型
maven_test_failed

### 关键词
mvn test 失败 surefire 测试 报错

### 症状
- mvn test 报测试失败

### 常见原因
- 测试断言失败
- 测试依赖缺失

### 检查命令
- 查看 surefire 报告

### 解决思路
- 查看失败测试的堆栈
- 修正测试或用 -Dmaven.test.skip=true 跳过
- 检查测试依赖

## 依赖冲突 Dependency convergence

### 别名
依赖冲突 版本冲突 依赖重复 omitted 依赖不一致

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
安装失败

### 错误类型
maven_dependency_conflict

### 关键词
mvn Dependency convergence omitted for conflict 依赖 冲突 版本

### 症状
- Dependency convergence error
- 多个版本被省略（omitted for conflict）

### 常见原因
- 传递依赖版本不一致

### 检查命令
- mvn dependency:tree

### 解决思路
- 用 dependencyManagement 统一版本
- 排除冲突依赖 exclusion
- 升级到兼容版本

## Maven 下载超时

### 别名
下载慢 超时 卡住 maven 下载 依赖下载不动

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
网络问题

### 错误类型
maven_timeout

### 关键词
Maven timeout 下载 慢 超时 网络

### 症状
- 依赖下载长时间无响应或超时

### 常见原因
- 默认中央仓库慢
- 网络不稳定

### 检查命令
- 检查网络与镜像配置

### 解决思路
- 配置阿里云镜像
- 检查代理
- 重试构建

## dependency:tree 排查

### 别名
查看依赖树 排查依赖 依赖树 dependency tree 分析依赖

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
排查方法

### 错误类型
maven_dependency_tree

### 关键词
dependency tree 依赖树 排查 冲突 mvn dependency

### 症状
- 需要查看依赖关系定位冲突

### 常见原因
- 依赖冲突或重复

### 检查命令
- mvn dependency:tree

### 解决思路
- mvn dependency:tree 查看依赖树
- 加 -Dincludes 过滤
- 定位冲突后排除或统一版本

## settings.xml 配置

### 别名
settings 全局配置 maven 本地仓库 镜像

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
配置错误

### 错误类型
maven_settings

### 关键词
settings.xml maven 镜像 profile localRepository

### 症状
- 需要配置镜像、代理或本地仓库路径

### 常见原因
- 默认配置不满足需求

### 检查命令
- 查看 ~/.m2/settings.xml

### 解决思路
- 配置镜像 mirror
- 配置 localRepository 路径
- 配置 profile 与激活

## Maven 私服

### 别名
私服 nexus 私有仓库 公司仓库 私有源 内部仓库

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
配置错误

### 错误类型
maven_private_repo

### 关键词
私服 nexus 私有仓库 repository 公司

### 症状
- 私有依赖下载失败或 404

### 常见原因
- 未配置私服地址
- 未登录私服

### 检查命令
- 查看 settings.xml 的 server 与仓库配置

### 解决思路
- settings.xml 配置私服仓库地址
- 配置 server 认证凭据
- 校验账号密码

## Spring Boot Maven 打包 repackage

### 别名
spring boot 打包 可执行 jar 打不了包 打包报错 spring 打包

### 平台
windows linux macos

### 技术栈
maven java spring springboot

### 故障类型
安装失败

### 错误类型
maven_spring_repackage

### 关键词
spring-boot-maven-plugin repackage 打包 可执行 jar

### 症状
- 打出的 jar 无法直接运行
- 找不到主类

### 常见原因
- 未配置 spring-boot-maven-plugin
- 未执行 repackage

### 检查命令
- 查看 pom.xml 插件配置

### 解决思路
- 配置 spring-boot-maven-plugin
- 执行 mvn package 生成可执行 jar
- 用 java -jar 运行

## mvn 版本过旧升级

### 别名
升级 maven 版本 更新 mvn maven 过旧 mvn 升级

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
版本不兼容

### 错误类型
maven_upgrade

### 关键词
mvn 版本 过旧 升级 maven 下载 更新

### 症状
- Maven 功能异常或版本过旧

### 常见原因
- 长期未更新 Maven

### 检查命令
- mvn -version

### 解决思路
- 下载新版 Maven 解压
- 更新 PATH
- 或升级 IDE 内置 Maven

## Maven 多模块构建

### 别名
多模块 parent module 构建失败 聚合构建 reactor

### 平台
windows linux macos

### 技术栈
maven

### 故障类型
配置错误

### 错误类型
maven_multi_module

### 关键词
多模块 reactor module 构建 聚合 parent

### 症状
- 多模块项目构建失败

### 常见原因
- 模块间依赖或父子关系配置错误
- 打包顺序问题

### 检查命令
- mvn -pl -am 查看模块关系

### 解决思路
- 检查 parent 与 module 配置
- 用 -pl/-am 指定构建模块
- 统一版本管理
