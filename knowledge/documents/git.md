# Git 故障知识库

## git 认证失败

### 关键词
Authentication failed fatal Authentication 认证 密码 token 401 登录 credential

### 症状
- fatal: Authentication failed
- 推送/拉取时提示认证失败

### 常见原因
- 用户名/密码错误
- GitHub 需用 token 代替密码
- 凭据缓存中的旧密码失效

### 检查命令
- git config --list

### 解决思路
- GitHub 使用 Personal Access Token
- 更新 Windows 凭据管理器
- SSH 方式：ssh -T git@github.com 测试

## git 仓库不存在

### 关键词
repository not found Remote not found 仓库 不存在 404 clone remote

### 症状
- remote: Repository not found
- clone 时提示找不到仓库

### 常见原因
- 仓库地址拼写错误
- 仓库为私有且无权限
- 仓库被删除或改名

### 检查命令
- 浏览器打开仓库 URL

### 解决思路
- 核对仓库地址大小写与用户名
- 确认账号有访问权限
- git remote set-url origin <正确地址>

## git 合并冲突

### 关键词
merge conflict CONFLICT 合并冲突 Automatic merge failed 冲突 <<<<<<<

### 症状
- CONFLICT (content)
- Automatic merge failed

### 常见原因
- 两个分支修改了同一文件的同一部分

### 检查命令
- git status

### 解决思路
- 编辑冲突文件，保留正确内容
- 删除冲突标记 <<<<<<< ======= >>>>>>>
- git add 后 git commit

## git 推送被拒绝

### 关键词
push rejected non-fast-forward 推送 拒绝 fetch first failed to push

### 症状
- push rejected
- non-fast-forward updates were rejected

### 常见原因
- 远程有本地没有的新提交
- 没有推送权限

### 检查命令
- git status
- git log --oneline

### 解决思路
- git pull --rebase origin <分支>
- 解决冲突后再推送
- 确认有推送权限

## 不是 git 仓库

### 关键词
not a git repository 不是 git 仓库 fatal init 目录

### 症状
- fatal: not a git repository

### 常见原因
- 在非仓库目录运行 git 命令
- 忘记 git init 或 clone

### 检查命令
- pwd / cd 到仓库根目录

### 解决思路
- cd 到仓库目录
- git init 初始化
- 或 git clone <地址>

## git 分支操作

### 关键词
branch 分支 checkout switch detached HEAD 上游 upstream 切换

### 症状
- 分支不存在或无法切换
- detached HEAD 状态

### 常见原因
- 分支名冲突或不存在
- 处于 detached HEAD
- 未设置上游分支

### 检查命令
- git branch -a

### 解决思路
- git switch -c <新分支>
- 设置上游：git push -u origin <分支>
- 退出 detached HEAD：git switch <分支>

## git 撤销操作

### 关键词
撤销 reset revert checkout -- 回退 commit 误操作

### 症状
- 需要撤销错误的提交或修改

### 常见原因
- 误提交、误修改文件

### 检查命令
- git log --oneline

### 解决思路
- 撤销未暂存修改：git checkout -- <文件>
- 撤销最近提交（保留修改）：git reset --soft HEAD~1
- 生成反向提交：git revert <commit>

## git 忽略文件 .gitignore

### 关键词
gitignore 忽略 ignore 排除 敏感文件 __pycache__ .env

### 症状
- 不需要的文件被纳入版本控制

### 常见原因
- 未配置 .gitignore

### 检查命令
- 查看仓库根目录 .gitignore

### 解决思路
- 在根目录创建 .gitignore
- 添加 __pycache__/、.env 等规则
- 已跟踪文件需 git rm --cached

## git 代理设置

### 关键词
proxy 代理 http.proxy git config 7890 翻墙 加速

### 症状
- git 拉取/推送缓慢或超时

### 常见原因
- 需要走代理访问 GitHub

### 检查命令
- git config --global --list

### 解决思路
- git config --global http.proxy http://127.0.0.1:7890
- 取消：git config --global --unset http.proxy

## git 远程地址切换

### 关键词
remote set-url origin HTTPS SSH 切换 远程 地址

### 症状
- 需要在 HTTPS 与 SSH 之间切换

### 常见原因
- 认证方式调整

### 检查命令
- git remote -v

### 解决思路
- 查看：git remote -v
- 切换：git remote set-url origin <新地址>
