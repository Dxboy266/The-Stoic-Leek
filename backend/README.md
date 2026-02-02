# 韭菜的自我修养 v2.0 - Backend

FastAPI 后端服务，提供 RESTful API。

## 快速开始

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件，填写你的配置
```

### 4. 启动服务

```bash
# 开发模式（热重载）
uvicorn app.main:app --reload --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 概览

### 认证
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 退出登录

### 处方
- `POST /prescription/generate` - 生成韭菜处方（需登录）
- `POST /prescription/generate-anonymous` - 生成处方（匿名）

### 设置
- `GET /settings` - 获取用户设置
- `PUT /settings` - 更新用户设置
- `GET /settings/models` - 获取可用模型列表
- `GET /settings/exercises/default` - 获取默认动作列表
- `POST /settings/exercises/reset` - 重置动作池

### 市场数据 (新功能!)
- `GET /market/northbound` - 北向资金数据
- `GET /market/hot-sectors` - 热门板块
- `GET /market/daily-summary` - 每日 AI 市场总结
- `GET /market/health` - 市场数据服务健康检查

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 入口
│   ├── config.py         # 配置
│   ├── schemas.py        # 数据模型
│   ├── routers/          # API 路由
│   │   ├── auth.py
│   │   ├── prescription.py
│   │   ├── settings.py
│   │   └── market.py
│   └── services/         # 业务逻辑
│       ├── auth.py
│       ├── ai.py
│       ├── database.py
│       └── market.py
├── requirements.txt
├── .env.example
└── README.md
```

## 技术栈

- **FastAPI** - 现代高性能 Web 框架
- **Pydantic** - 数据验证
- **Supabase** - 数据库和认证
- **AkShare** - 金融数据
- **httpx** - 异步 HTTP 客户端
