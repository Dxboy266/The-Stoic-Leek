# 《韭菜的自我修养》5分钟部署指南

## 准备工作（30秒）

**服务器信息：**
- IP: 81.70.55.132
- 系统: Ubuntu 22.04
- Docker: 已安装（版本 26）

---

## 步骤 1：打包项目（1分钟）

在本地电脑打开 PowerShell，执行：

```powershell
# 确保在项目根目录
# D:/res/project/The Stoic Leek/The-Stoic-Leek
tar --exclude=stoic-leek.tar.gz --exclude=node_modules --exclude=.git --exclude=__pycache__ --exclude=.next --exclude="*.pyc" --exclude=venv --exclude=.venv -czf stoic-leek.tar.gz .
```

---

## 步骤 2：上传到服务器（2分钟）

### 方式 A：使用腾讯云控制台（推荐）

1. 打开 [腾讯云轻量应用服务器控制台](https://console.cloud.tencent.com/lighthouse/instance/detail?rid=5&id=lhins-ltwuur60)
2. 点击 **文件** → 进入 `/opt/` 目录
3. 创建文件夹 `stoic-leek` (如果不存在)
4. 将本地生成的 `stoic-leek.tar.gz` 拖拽上传到 `/opt/stoic-leek/` 目录中

### 方式 B：使用命令行 (SCP)

```powershell
scp stoic-leek.tar.gz root@81.70.55.132:/opt/
# 注意：你需要知道服务器 root 密码或有 SSH key
```

---

## 步骤 3：服务器部署（1.5分钟）

登录服务器（通过控制台远程登录 或 SSH），执行以下命令：

```bash
# 1. 准备目录并解压
mkdir -p /opt/stoic-leek
cd /opt/stoic-leek

# 如果文件在 /opt/ 下
mv /opt/stoic-leek.tar.gz . 2>/dev/null || true
# 或者如果文件在 /tmp/ 下
# mv /tmp/stoic-leek.tar.gz .

tar -xzf stoic-leek.tar.gz

# 2. 开放防火墙端口 (Ubuntu ufw)
ufw allow 3001/tcp
ufw allow 8000/tcp

# 3. 构建并启动容器
# 注意：第一次构建可能需要几分钟下载镜像
docker-compose build --no-cache
docker-compose up -d

# 4. 查看运行状态
docker-compose ps
```

---

## 步骤 4：访问应用（30秒）

部署成功后，浏览器访问：

- **前端页面**: http://81.70.55.132:3001
- **后端 API**: http://81.70.55.132:8000
- **API 文档**: http://81.70.55.132:8000/docs

---

## 常见问题排查

### Q: 访问不了页面？
1. 检查腾讯云控制台的 **防火墙** 规则，确保 3001 和 8000 端口已添加“允许 TCP”。
2. 查看容器日志：
   ```bash
   docker-compose logs -f
   ```

### Q: 如何更新代码？
1. 本地重新打包 `tar`。
2. 上传覆盖服务器上的压缩包。
3. 服务器执行：
   ```bash
   cd /opt/stoic-leek
   tar -xzf stoic-leek.tar.gz
   docker-compose up -d --build
   ```

### Q: 如何完全重置？
```bash
docker-compose down
docker system prune -a -f
# 然后重新构建
docker-compose up -d --build
```
