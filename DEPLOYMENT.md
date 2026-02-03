# 部署指南 (Deployment Guide)

本项目推荐使用 Docker Compose 进行一键部署。

## 前置要求

- 服务器已安装 Docker 和 Docker Compose。
- 确保端口 `8000` (后端) 和 `3001` (前端) 未被占用。

## 部署步骤

### 1. 配置环境

1.  **修改 `docker-compose.yml`**:
    
    打开 `docker-compose.yml` 文件，找到 `frontend` 服务下的 `NEXT_PUBLIC_API_URL` 参数。
    将其修改为你服务器的公网 IP 地址或域名。
    
    ```yaml
    # docker-compose.yml
    
    frontend:
      # ...
      args:
        # 将此处 IP 改为你的服务器公网 IP
        NEXT_PUBLIC_API_URL: http://YOUR_SERVER_IP:8000
    ```

2.  **配置后端环境变量**:
    
    确保 `backend/.env` 文件存在，并配置了必要的环境变量（如数据库连接、API Key 等）。
    如果不存在，可以复制 `backend/.env.template` (如果有) 或参考项目文档创建。

### 2. 启动服务

在项目根目录下执行以下命令：

```bash
# 构建并启动服务（后台运行）
docker-compose up -d --build
```

### 3. 本地验证

等待构建完成后，检查容器状态：

```bash
docker-compose ps
```

如果状态均为 `Up`，则部署成功。你可以通过浏览器访问：

- 前端: `http://YOUR_SERVER_IP:3001`
- 后端 API 文档: `http://YOUR_SERVER_IP:8000/docs`

### 4. 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 注意事项

- **数据持久化**: 
  如果你希望在容器删除后保留数据（如数据库、日志），请在 `docker-compose.yml` 中取消注释并配置 `volumes` 部分。
  目前后端使用了 SQLite (假设)，数据文件通常在 `backend/` 目录下。如果在生产环境使用 Docker，建议将数据目录挂载到宿主机。
  
- **API Key 安全**:
  建议在服务器的环境变量中配置敏感信息，而不是直接写在代码或 Dockerfile 中。
