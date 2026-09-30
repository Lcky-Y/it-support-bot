# Node.js / npm 故障知识库

## npm 找不到包

### 别名
npm 找不到包 E404 404 装不上 缺包 缺了个包 包找不到

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_package_not_found

### 关键词
npm ERR E404 404 Not Found registry

### 症状
- npm ERR! code E404
- 404 Not Found - GET https://registry.npmjs.org/xxx

### 常见原因
- 包名拼写错误
- 私有包未配置对应 registry 或未登录
- 包已被下架或改名

### 检查命令
- npm view <包名> versions

### 解决思路
- 核对包名拼写
- 私有包用 .npmrc 配置 scope registry 并 npm login
- 换用正确包名或镜像

## npm ERESOLVE 依赖冲突

### 别名
npm 依赖冲突 ERESOLVE 依赖树 unable to resolve dependency tree 版本冲突

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_eresolve

### 关键词
ERESOLVE could not resolve dependency tree 依赖 冲突 版本 npm install

### 症状
- npm ERR! code ERESOLVE
- ERESOLVE unable to resolve dependency tree
- Could not resolve dependency

### 常见原因
- 依赖版本互相冲突
- package.json 版本约束过死
- 使用了不一致的 lock 文件

### 检查命令
- npm ls 查看依赖树

### 解决思路
- npm install --legacy-peer-deps 绕过（谨慎）
- 调整 package.json 版本约束
- 删除 node_modules 与 lock 后重装

## npm peer dependency 冲突

### 别名
peer dependency 冲突 peerDependencies 缺失 对等依赖 版本不满足

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_peer_dependency

### 关键词
peer dependency peerDependencies requires a peer of unmet 依赖 冲突

### 症状
- npm ERR! peer dep missing
- xxx requires a peer of yyy@^2.0.0

### 常见原因
- 插件与主库要求的 peer 依赖版本不一致
- 多个包对同一 peer 依赖版本要求冲突

### 检查命令
- npm ls 查看依赖层级

### 解决思路
- 安装满足要求的 peer 依赖版本
- 或用 --legacy-peer-deps 临时绕过
- 升级/降级相关包版本

## npm EACCES 权限不足

### 别名
npm 权限不足 权限不够 没权限 装东西 提示权限不够 全局安装失败

### 平台
linux macos

### 技术栈
npm node

### 故障类型
权限问题

### 错误类型
npm_eacces

### 关键词
npm EACCES permission denied 全局 安装 sudo

### 症状
- npm ERR! code EACCES
- Permission denied 安装全局包失败

### 常见原因
- 全局安装目录无写权限
- 使用 root 安装后普通用户无权限

### 检查命令
- npm config get prefix
- ls -l $(npm config get prefix)

### 解决思路
- 全局安装加 sudo（或修改 prefix 到用户目录）
- 配置 prefix 到 ~/.npm-global
- 或使用 nvm 管理 node

## npm EPERM 权限错误

### 别名
npm EPERM operation not permitted Windows 占用 杀毒

### 平台
windows

### 技术栈
npm node

### 故障类型
权限问题

### 错误类型
npm_eperm

### 关键词
npm EPERM operation not permitted Windows 占用 杀毒

### 症状
- npm ERR! code EPERM
- npm ERR! syscall rename 或 unlink

### 常见原因
- 文件被其它进程占用（如编辑器、杀毒软件）
- 无管理员权限

### 检查命令
- 关闭占用 node_modules 的程序

### 解决思路
- 关闭 VS Code / 杀毒软件后重试
- 以管理员身份运行终端
- 删除 node_modules 后重装

## npm ENOENT 文件不存在

### 别名
npm 找不到文件 目录不存在 路径错误 no such file or directory

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_enoent

### 关键词
npm ENOENT no such file or directory 路径 目录

### 症状
- npm ERR! code ENOENT
- ENOENT: no such file or directory

### 常见原因
- 路径拼写错误
- package.json 或入口文件缺失
- 在错误目录执行命令

### 检查命令
- ls / dir 确认目录内容

### 解决思路
- cd 到项目根目录
- 确认 package.json 存在
- 核对脚本中的文件路径

## npm 安装超时

### 别名
npm 安装超时 网络请求失败 下不动 一直卡 下载慢 连不上

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
网络问题

### 错误类型
npm_timeout

### 关键词
npm network request failed ETIMEDOUT timeout 超时 连接

### 症状
- npm ERR! network request failed
- reason: connect ETIMEDOUT
- 安装长时间无响应

### 常见原因
- 默认 registry 访问慢
- 网络不稳定或代理限制

### 检查命令
- npm config get registry

### 解决思路
- 切换国内镜像源（npmmirror）
- 检查并配置代理
- 重试 npm install

## npm 国内镜像源配置

### 别名
npm 换源 镜像源 淘宝源 npmmirror 加速 慢 registry 配置

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
网络问题

### 错误类型
npm_registry_mirror

### 关键词
registry 镜像 源 换源 淘宝 npmmirror 加速 慢 npm config

### 症状
- npm 安装缓慢或超时

### 常见原因
- 默认 registry.npmjs.org 国内访问慢

### 检查命令
- npm config get registry

### 解决思路
- npm config set registry https://registry.npmmirror.com
- 或临时 --registry=https://registry.npmmirror.com
- 改后 npm install 重试

## npm SSL 证书错误

### 别名
npm 证书错误 自签名 证书是自签名的 无法验证

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
网络问题

### 错误类型
npm_ssl_error

### 关键词
npm self-signed UNABLE_TO_VERIFY_LEAF_SIGNATURE certificate verify 证书验证 验证失败

### 症状
- self-signed certificate in certificate chain
- UNABLE_TO_VERIFY_LEAF_SIGNATURE
- certificate has expired

### 常见原因
- 公司代理/防火墙替换证书
- 系统时间错误
- 使用自签名私有 registry

### 检查命令
- npm config get registry
- 校正系统时间

### 解决思路
- 校正系统时间
- 私有 registry 配 strict-ssl=false（仅可信源）
- 检查代理是否替换证书

## npm 代理设置

### 别名
npm 代理 走代理 翻墙 设置代理 加速

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
网络问题

### 错误类型
npm_proxy

### 关键词
npm proxy https-proxy 7890 config 走代理

### 症状
- npm 拉取缓慢或超时

### 常见原因
- 需要代理访问 registry

### 检查命令
- npm config get proxy

### 解决思路
- npm config set proxy http://127.0.0.1:7890
- npm config set https-proxy http://127.0.0.1:7890
- 取消：npm config delete proxy

## npm cache 清理

### 别名
npm cache 清理 缓存 清缓存 verify 安装报错 缓存损坏

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_cache_clean

### 关键词
cache clean 缓存 清理 verify 损坏 npm install 报错

### 症状
- 安装报错疑似缓存损坏

### 常见原因
- 缓存损坏或不完整

### 检查命令
- npm cache verify

### 解决思路
- npm cache clean --force 强制清理
- 再 npm cache verify 重建
- 重新安装

## npm cache 校验失败

### 别名
npm cache verify 失败 缓存校验 校验错误 安装中断

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_cache_verify

### 关键词
cache verify 校验 缓存 失败 corrupted 中断 npm install

### 症状
- npm cache verify 报错
- 安装因缓存问题中断

### 常见原因
- 缓存文件损坏
- 磁盘空间不足

### 检查命令
- npm cache verify

### 解决思路
- npm cache clean --force 后重装
- 检查磁盘空间

## npm ELIFECYCLE 脚本失败

### 别名
npm 脚本执行失败 ELIFECYCLE build 失败 生命周期 命令报错

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
运行异常

### 错误类型
npm_elifecycle

### 关键词
ELIFECYCLE script 脚本 build 失败 exit code 生命周期

### 症状
- npm ERR! code ELIFECYCLE
- npm run build 报错退出

### 常见原因
- 脚本命令本身出错
- 依赖缺失或环境不满足

### 检查命令
- 直接运行脚本里的命令定位

### 解决思路
- 查看上方具体报错定位脚本命令
- 补齐依赖或修正脚本
- 检查 node 版本是否满足

## npm ETARGET 版本不存在

### 别名
npm 版本不存在 找不到这个版本 ETARGET No matching version

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_etarget

### 关键词
npm ETARGET No matching version found 版本 不存在

### 症状
- npm ERR! code ETARGET
- No matching version found for xxx

### 常见原因
- 指定版本号不存在
- 拼写错误或未发布该版本

### 检查命令
- npm view <包> versions

### 解决思路
- 核对版本号或去掉版本约束
- 用 npm view 查看可用版本

## npm EINTEGRITY 校验失败

### 别名
npm 完整性校验失败 EINTEGRITY integrity checksum 校验 不一致

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_eintegrity

### 关键词
EINTEGRITY integrity checksum sha512 校验 失败 不一致

### 症状
- npm ERR! code EINTEGRITY
- integrity checksum failed

### 常见原因
- 下载包被篡改或损坏
- lock 文件中的 hash 过期

### 检查命令
- 检查 package-lock.json

### 解决思路
- npm cache clean --force 后重装
- 删除 node_modules 与 lock 重新生成
- 检查是否走代理导致内容被改

## npm command not found

### 别名
npm 命令找不到 命令找不到了 npm not found 未安装 不在 PATH

### 平台
linux macos

### 技术栈
npm node

### 故障类型
环境依赖

### 错误类型
npm_command_not_found

### 关键词
npm command not found 未安装 PATH

### 症状
- bash: npm: command not found

### 常见原因
- 未安装 node/npm
- npm 不在 PATH 中

### 检查命令
- which npm
- node -v

### 解决思路
- 安装 node（自带 npm）
- 用 nvm 安装并切换
- 确认 PATH 包含 node 安装目录

## npm 不是内部或外部命令

### 别名
npm 不是内部或外部命令 Windows npm 找不到 命令 无法识别

### 平台
windows

### 技术栈
npm node

### 故障类型
环境依赖

### 错误类型
npm_not_recognized_windows

### 关键词
npm 不是内部或外部命令 Windows 无法识别 PATH 批处理文件

### 症状
- 'npm' 不是内部或外部命令，也不是可运行的程序或批处理文件

### 常见原因
- 未安装 Node.js
- PATH 未包含 Node 安装目录
- 安装后未重开终端

### 检查命令
- where npm

### 解决思路
- 安装 Node.js
- 重开终端刷新 PATH
- 手动将 Node 目录加入 PATH

## node command not found

### 别名
node 命令找不到 node 不存在 未安装

### 平台
windows linux macos

### 技术栈
node

### 故障类型
环境依赖

### 错误类型
node_command_not_found

### 关键词
node command not found 未安装 PATH

### 症状
- node: command not found

### 常见原因
- 未安装 Node.js
- node 不在 PATH 中

### 检查命令
- which node

### 解决思路
- 安装 Node.js
- 用 nvm 安装并切换版本
- 检查 PATH

## Windows PATH 配置 node npm

### 别名
Windows PATH 配置 node npm 环境变量 命令找不到 无法识别

### 平台
windows

### 技术栈
node npm

### 故障类型
配置错误

### 错误类型
node_windows_path

### 关键词
PATH 环境变量 Windows node npm 配置 命令 找不到

### 症状
- 安装 node 后命令仍无法识别

### 常见原因
- Node 安装目录未加入系统 PATH
- 环境变量未生效

### 检查命令
- echo %PATH%

### 解决思路
- 将 Node 安装目录加入系统 PATH
- 重开终端或注销重登生效
- 重新安装 Node 勾选 Add to PATH

## node 版本不兼容 engines

### 别名
node 版本不兼容 engines 要求 版本 不满足 升级 node

### 平台
windows linux macos

### 技术栈
node npm

### 故障类型
版本不兼容

### 错误类型
node_engines

### 关键词
engines node 版本 不兼容 不满足 要求 升级 unsupported

### 症状
- 包要求 node >= xx 当前版本不满足
- Unsupported engine warning

### 常见原因
- 本地 node 版本过旧
- 包要求更高 node 版本

### 检查命令
- node -v

### 解决思路
- 升级 node 到满足的版本
- 用 nvm 切换版本
- 或降级包版本

## npm 版本过旧升级

### 别名
npm 升级 版本过旧 npm 更新 upgrade 过时

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
版本不兼容

### 错误类型
npm_upgrade

### 关键词
npm 升级 upgrade 版本 过旧 更新 outdated

### 症状
- npm 功能异常或版本过旧

### 常见原因
- 长期未更新 npm

### 检查命令
- npm -v

### 解决思路
- npm install -g npm@latest
- 或随 node 一起升级

## node 版本过旧升级

### 别名
node 升级 版本过旧 更新 node 版本 升级 nodejs

### 平台
windows linux macos

### 技术栈
node nvm

### 故障类型
版本不兼容

### 错误类型
node_upgrade

### 关键词
node 升级 版本 过旧 更新 nvm 新版本

### 症状
- 项目要求更高 node 版本

### 常见原因
- 本地 node 过旧

### 检查命令
- node -v

### 解决思路
- 官网下载新版本安装
- 或用 nvm install <版本> 并 nvm use

## nvm 切换 node 版本

### 别名
nvm 切换 node 版本 安装 node 管理版本 use 切换失败

### 平台
windows linux macos

### 技术栈
nvm node

### 故障类型
环境依赖

### 错误类型
nvm_use_version

### 关键词
nvm use install 切换 node 版本 管理 安装

### 症状
- 需要安装或切换 node 版本

### 常见原因
- 项目需要不同 node 版本

### 检查命令
- nvm list

### 解决思路
- nvm install <版本> 安装
- nvm use <版本> 切换
- nvm alias default <版本> 设默认

## nvm command not found

### 别名
nvm 命令找不到 nvm 不存在 未安装 无法识别

### 平台
windows linux macos

### 技术栈
nvm node

### 故障类型
环境依赖

### 错误类型
nvm_command_not_found

### 关键词
nvm command not found 未安装 PATH

### 症状
- nvm: command not found

### 常见原因
- 未安装 nvm
- nvm 未加入 PATH 或未 source

### 检查命令
- 重开终端测试 nvm --version

### 解决思路
- 安装 nvm
- 确保 shell 配置里 source 了 nvm 脚本
- Windows 用 nvm-windows

## package-lock.json 冲突

### 别名
package-lock 冲突 lock 文件冲突 合并冲突 lock 版本不一致

### 平台
windows linux macos

### 技术栈
npm node git

### 故障类型
配置错误

### 错误类型
npm_lock_conflict

### 关键词
package-lock.json 冲突 lock merge conflict 版本 不一致 git

### 症状
- package-lock.json 出现合并冲突

### 常见原因
- 多人同时修改依赖导致 lock 冲突

### 检查命令
- git status

### 解决思路
- 手动解决冲突保留正确版本
- 或放弃本地 lock 重新 npm install 生成
- 团队统一 node/npm 版本减少冲突

## package-lock 不同步 npm ci 失败

### 别名
package-lock 不同步 npm ci 失败 lock 与 package.json 不一致

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_lock_out_of_sync

### 关键词
package-lock npm ci 不同步 不一致 package.json out of sync

### 症状
- npm ci 报 lock 与 package.json 不一致

### 常见原因
- 手动改了 package.json 未更新 lock

### 检查命令
- npm install 重新生成 lock

### 解决思路
- 删除 package-lock.json 重新 npm install
- 或运行 npm install 同步 lock
- 再执行 npm ci

## 删除 node_modules 重装

### 别名
node_modules 删除 重装 清依赖 重新安装 依赖损坏

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
安装失败

### 错误类型
npm_reinstall

### 关键词
node_modules 删除 重装 清空 重新安装 依赖 损坏 rm

### 症状
- 依赖损坏导致运行异常

### 常见原因
- node_modules 损坏或不完整

### 检查命令
- 查看 node_modules 是否完整

### 解决思路
- Windows：rmdir /s /q node_modules
- Linux：rm -rf node_modules
- 删除后 npm install 重装

## npm ci 与 npm install 区别

### 别名
npm ci install 区别 用哪个 干净安装 lock 严格

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
排查方法

### 错误类型
npm_ci_install

### 关键词
npm ci install 区别 干净 严格 lock 用哪个

### 症状
- 不确定用 npm ci 还是 npm install

### 常见原因
- 两者行为差异

### 检查命令
- 查看 package-lock.json 是否存在

### 解决思路
- npm ci 严格按 lock 干净安装（CI 环境用）
- npm install 会更新 lock（本地开发用）
- CI 部署优先 npm ci

## npm run script not found

### 别名
npm run 脚本找不到 script 不存在 missing script 命令不存在

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
配置错误

### 错误类型
npm_script_not_found

### 关键词
npm run script missing 脚本 找不到 不存在 package.json

### 症状
- npm run xxx 报 missing script
- npm ERR! Missing script

### 常见原因
- package.json 里没有该脚本
- 脚本名拼写错误

### 检查命令
- 查看 package.json scripts 字段

### 解决思路
- 核对 scripts 中的脚本名
- 在 package.json 添加对应脚本
- 用 npm run 查看全部脚本

## npm run 脚本执行策略

### 别名
npm run 脚本执行策略 Windows PowerShell 禁止运行 权限

### 平台
windows

### 技术栈
npm node powershell

### 故障类型
权限问题

### 错误类型
npm_script_policy

### 关键词
执行策略 PowerShell 禁止运行脚本 policy npm run 无法加载

### 症状
- 无法加载脚本，因为在此系统上禁止运行脚本

### 常见原因
- PowerShell 执行策略 Restricted

### 检查命令
- Get-ExecutionPolicy

### 解决思路
- Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
- 或改用 cmd 终端运行 npm

## node-gyp 编译失败

### 别名
node-gyp 编译失败 原生模块 编译 native addon 安装失败 gyp

### 平台
windows linux macos

### 技术栈
node-gyp node npm

### 故障类型
安装失败

### 错误类型
node_gyp_failed

### 关键词
node-gyp gyp ERR 编译 失败 native addon 原生模块 构建

### 症状
- npm install 时 node-gyp rebuild 失败
- gyp ERR! stack / build error

### 常见原因
- 缺少编译工具链
- 原生模块需要本地编译

### 检查命令
- node-gyp 版本与编译环境

### 解决思路
- 安装所需编译工具
- 用预编译二进制或换版本
- 查看 gyp ERR 具体错误定位

## node-gyp 缺 Python 或 VS

### 别名
node-gyp 缺 python visual studio windows 构建工具 编译环境

### 平台
windows

### 技术栈
node-gyp node npm

### 故障类型
环境依赖

### 错误类型
node_gyp_env_windows

### 关键词
node-gyp python visual studio build tools windows 编译 环境 缺失

### 症状
- gyp ERR! find Python
- 提示需要 Visual Studio Build Tools

### 常见原因
- 缺少 Python 或 VS 构建工具

### 检查命令
- 是否安装 VS Build Tools 与 Python

### 解决思路
- 安装 Visual Studio Build Tools（含 C++ 工具集）
- 安装 Python 并加入 PATH
- 或 npm config set python 指定路径

## npm 全局安装的包命令找不到

### 别名
npm 全局安装 全局包命令找不到 global bin 全局包

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
环境依赖

### 错误类型
npm_global_bin

### 关键词
npm global bin 全局 安装 PATH prefix

### 症状
- npm install -g 后命令仍找不到

### 常见原因
- 全局 bin 目录不在 PATH 中
- 环境变量未刷新

### 检查命令
- npm config get prefix

### 解决思路
- 将 prefix 的 bin 目录加入 PATH
- 重开终端
- 检查是否用了 nvm 的 prefix

## npm 全局安装权限 prefix

### 别名
npm 全局安装 无权限 全局目录 prefix 目录

### 平台
linux macos

### 技术栈
npm node

### 故障类型
权限问题

### 错误类型
npm_global_prefix

### 关键词
npm prefix 全局 目录 无权限 EACCES

### 症状
- 全局安装报权限错误

### 常见原因
- 全局目录在系统目录需 root

### 检查命令
- npm config get prefix

### 解决思路
- 设 prefix 到用户目录 ~/.npm-global
- 并把其 bin 加入 PATH
- 或使用 nvm 管理

## npm deprecated 警告

### 别名
npm deprecated 弃用 警告 过时包 deprecated 提示

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
排查方法

### 错误类型
npm_deprecated

### 关键词
deprecated 弃用 警告 过时 outdated npm install

### 症状
- 安装时提示 xxx is deprecated

### 常见原因
- 依赖包已被弃用

### 检查命令
- npm outdated

### 解决思路
- 通常仅警告，可先忽略
- 长期看替换为维护中的包
- npm outdated 查看可更新包

## npm audit 安全漏洞

### 别名
npm audit 漏洞 安全 修复 vulnerabilities 审计

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
排查方法

### 错误类型
npm_audit

### 关键词
audit 漏洞 安全 vulnerabilities 修复 审计 high

### 症状
- 提示存在安全漏洞

### 常见原因
- 依赖存在已知漏洞

### 检查命令
- npm audit

### 解决思路
- npm audit fix 自动修复
- npm audit fix --force 大版本修复（谨慎）
- 升级有漏洞的依赖

## npx command not found

### 别名
npx 命令找不到 未安装 无法识别

### 平台
windows linux macos

### 技术栈
npx npm node

### 故障类型
环境依赖

### 错误类型
npx_command_not_found

### 关键词
npx command not found 未安装

### 症状
- npx: command not found

### 常见原因
- node/npm 过旧
- npx 不在 PATH

### 检查命令
- npm -v

### 解决思路
- 升级 npm（npx 随 npm 提供）
- 或用 npm exec 代替

## node 内存溢出

### 别名
node 内存溢出 内存爆了 爆了 内存就爆了 内存不够 内存不足 JavaScript 堆

### 平台
windows linux macos

### 技术栈
node

### 故障类型
运行异常

### 错误类型
node_oom

### 关键词
node heap out of memory 内存 溢出 JavaScript heap limit FATAL

### 症状
- JavaScript heap out of memory
- FATAL ERROR: Reached heap limit

### 常见原因
- 处理数据量过大
- 内存泄漏

### 检查命令
- 观察进程内存占用

### 解决思路
- 增大内存：node --max-old-space-size=4096
- 优化数据处理方式
- 排查内存泄漏

## Cannot find module 模块未找到

### 别名
Cannot find module MODULE_NOT_FOUND 模块找不到 找不到模块 require 失败

### 平台
windows linux macos

### 技术栈
node npm

### 故障类型
运行异常

### 错误类型
node_module_not_found

### 关键词
Cannot find module MODULE_NOT_FOUND 模块 require 导入

### 症状
- Error: Cannot find module 'xxx'
- MODULE_NOT_FOUND

### 常见原因
- 依赖未安装
- 路径错误
- 未在 node_modules 中

### 检查命令
- ls node_modules 确认安装

### 解决思路
- npm install <包> 安装缺失依赖
- 核对 require/import 路径
- 删除 node_modules 重装

## npm 网络 EAI_AGAIN 无法解析

### 别名
npm 网络错误 EAI_AGAIN ENOTFOUND getaddrinfo 域名 解析失败

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
网络问题

### 错误类型
npm_dns

### 关键词
EAI_AGAIN ENOTFOUND getaddrinfo 域名 解析 失败 网络 registry

### 症状
- getaddrinfo EAI_AGAIN
- ENOTFOUND registry.npmjs.org

### 常见原因
- DNS 解析失败
- 网络不通

### 检查命令
- ping registry 域名

### 解决思路
- 检查 DNS 与网络
- 切换镜像源
- 配置 hosts 或更换 DNS

## npm registry 配置错误

### 别名
npm registry 配置错误 ERR_INVALID_URL 地址 错误 无法安装

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
配置错误

### 错误类型
npm_registry_invalid

### 关键词
ERR_INVALID_URL registry 地址 错误 配置 无效 invalid

### 症状
- ERR_INVALID_URL
- npm install 报 registry 地址无效

### 常见原因
- .npmrc 中 registry 地址写错

### 检查命令
- npm config get registry

### 解决思路
- 修正 registry 地址
- npm config delete registry 恢复默认
- 检查 .npmrc 配置

## npm 私有仓库 scope 配置

### 别名
npm 私有仓库 scope 私有源 公司 内部包 registry 配置

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
配置错误

### 错误类型
npm_private_registry

### 关键词
scope 私有 仓库 内部 包 registry 公司 私服 .npmrc

### 症状
- 私有包安装失败或 404

### 常见原因
- 私有 scope 未配置对应 registry

### 检查命令
- 查看 .npmrc

### 解决思路
- .npmrc 配置 @scope:registry=私有源
- npm login 登录私有仓库
- 校验 token 是否有效

## npm link 本地包

### 别名
npm link 本地包 调试 本地开发 软链接 全局链接

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
排查方法

### 错误类型
npm_link

### 关键词
npm link 本地 包 调试 软链接 开发 全局 链接

### 症状
- 本地开发需调试未发布的包

### 常见原因
- 包未发布到 registry

### 检查命令
- npm link 查看已链接包

### 解决思路
- 在包目录 npm link
- 在使用处 npm link <包名>
- 用后 npm unlink <包名>

## node 服务端口被占用

### 别名
node 端口被占用 EADDRINUSE address already in use 端口冲突

### 平台
windows linux macos

### 技术栈
node

### 故障类型
配置错误

### 错误类型
node_port_in_use

### 关键词
EADDRINUSE address already in use 端口 占用 冲突 服务 启动

### 症状
- Error: listen EADDRINUSE
- address already in use

### 常见原因
- 端口已被其它进程占用

### 检查命令
- netstat -ano | findstr 端口（Windows）或 ss -tlnp

### 解决思路
- 结束占用进程
- 或更换服务端口
- 检查是否重复启动

## package.json 语法错误

### 别名
package.json 语法错误 JSON 解析失败 格式错误 逗号 括号

### 平台
windows linux macos

### 技术栈
npm node

### 故障类型
配置错误

### 错误类型
npm_package_json_syntax

### 关键词
package.json JSON 语法 错误 解析 parse 格式 逗号 括号

### 症状
- npm install 报 JSON 解析失败
- Unexpected token in JSON

### 常见原因
- package.json 语法错误（多余逗号等）

### 检查命令
- 用 JSON 校验工具检查

### 解决思路
- 修正 JSON 语法
- 用编辑器格式化检查
- 删除多余逗号或补全括号
