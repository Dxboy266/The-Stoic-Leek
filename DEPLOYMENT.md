# 部署指南

本应用支持多种免费部署方式，推荐使用 Streamlit Cloud（最简单）。

## 方案 1：Streamlit Cloud（推荐）⭐

**优点**：
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 自动部署（推送代码即更新）
- ✅ PC 和移动端完美支持
- ✅ 无需服务器管理

**步骤**：

### 1. 准备 GitHub 仓库

```bash
# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 关联远程仓库
git remote add origin https://github.com/Dxboy266/The-Stoic-Leek.git

# 推送到 GitHub
git push -u origin main
```

### 2. 部署到 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择您的仓库：`Dxboy266/The-Stoic-Leek`
5. 主文件路径：`app.py`
6. 点击 "Deploy"

### 3. 等待部署完成

- 首次部署需要 2-5 分钟
- 部署完成后会获得一个 URL：`https://stoic-leek.streamlit.app`
- 这个 URL 可以在任何设备上访问

### 4. 更新应用

只需推送代码到 GitHub，Streamlit Cloud 会自动重新部署：

```bash
git add .
git commit -m "Update features"
git push
```

## 方案 2：Hugging Face Spaces

**优点**：
- ✅ 免费
- ✅ 支持 Streamlit
- ✅ 良好的社区支持

**步骤**：

1. 访问 [Hugging Face Spaces](https://huggingface.co/spaces)
2. 创建新 Space，选择 Streamlit SDK
3. 上传代码文件
4. 等待部署完成

## 方案 3：Railway

**优点**：
- ✅ 每月 $5 免费额度
- ✅ 支持自定义域名
- ✅ 自动 HTTPS

**步骤**：

1. 访问 [Railway](https://railway.app)
2. 连接 GitHub 仓库
3. 添加环境变量（如需要）
4. 部署

## 方案 4：Render

**优点**：
- ✅ 免费套餐
- ✅ 自动 HTTPS
- ✅ 支持自定义域名

**步骤**：

1. 访问 [Render](https://render.com)
2. 创建新 Web Service
3. 连接 GitHub 仓库
4. 构建命令：`pip install -r requirements.txt`
5. 启动命令：`streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 移动端访问

所有部署方案都支持移动端访问：

1. **响应式设计**：应用已针对移动设备优化
2. **直接访问**：在手机浏览器中输入部署 URL
3. **添加到主屏幕**：
   - iOS：Safari → 分享 → 添加到主屏幕
   - Android：Chrome → 菜单 → 添加到主屏幕

## 自定义域名（可选）

如果您有自己的域名：

### Streamlit Cloud
1. 在 Streamlit Cloud 设置中添加自定义域名
2. 在域名 DNS 设置中添加 CNAME 记录

### 其他平台
参考各平台的自定义域名文档

## 环境变量配置

如果需要预设 API 密钥（不推荐，有安全风险）：

1. 在部署平台添加环境变量：`SILICONFLOW_API_KEY`
2. 修改 `app.py` 读取环境变量

**注意**：不建议在公开部署中硬编码 API 密钥。

## 性能优化

### 1. 缓存优化

在 `app.py` 中添加缓存：

```python
@st.cache_resource
def get_ai_client(api_key):
    return AIClient(api_key)
```

### 2. 限流保护

添加请求频率限制，避免 API 滥用。

### 3. 错误监控

集成错误追踪服务（如 Sentry）。

## 成本估算

### 免费方案
- **Streamlit Cloud**：完全免费，无限制
- **Hugging Face**：完全免费
- **Railway**：$5/月免费额度
- **Render**：免费套餐（有休眠限制）

### API 成本
- **硅基流动**：提供免费额度
- 个人使用通常不会超出免费额度

## 监控和维护

### 1. 检查应用状态
定期访问应用确保正常运行

### 2. 查看日志
在部署平台查看应用日志

### 3. 更新依赖
定期更新 `requirements.txt` 中的包版本

## 故障排查

### 应用无法启动
1. 检查 `requirements.txt` 是否正确
2. 查看部署日志
3. 确认 Python 版本兼容性

### API 调用失败
1. 检查 API 密钥是否有效
2. 确认网络连接
3. 查看 API 服务状态

### 移动端显示异常
1. 清除浏览器缓存
2. 检查 CSS 样式
3. 测试不同浏览器

## 推荐配置

**最佳实践**：
- ✅ 使用 Streamlit Cloud 部署
- ✅ 启用 HTTPS（自动）
- ✅ 定期更新依赖
- ✅ 监控 API 使用量
- ✅ 备份代码到 GitHub

---

**部署完成后，记得更新 README.md 中的在线演示链接！**
