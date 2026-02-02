# 韭菜的自我修养 v2.0 实施方案

## 项目概述

**The Stoic Leek** - 一个用运动对冲投资焦虑的 AI 应用

### 核心理念
> 市场涨跌皆虚妄，唯有酸痛最真实。

---

## 🏗️ 技术架构

### 前端 (待实施)
- **框架**: Next.js 14+ (React)
- **样式**: Tailwind CSS + Shadcn/UI
- **图表**: Recharts / Tremor
- **动画**: Framer Motion

### 后端 ✅ (已完成)
- **框架**: FastAPI (Python)
- **数据库**: Supabase (PostgreSQL)
- **金融数据**: AkShare
- **AI**: SiliconFlow API (DeepSeek)

---

## 📅 实施阶段

### 第一阶段：后端重构 ✅ 完成

#### 已完成内容

1. **项目结构搭建**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py           # FastAPI 入口
   │   ├── config.py         # 配置管理
   │   ├── schemas.py        # 数据模型
   │   ├── routers/          # API 路由
   │   │   ├── auth.py       # 认证
   │   │   ├── prescription.py # 处方生成
   │   │   ├── settings.py   # 用户设置
   │   │   └── market.py     # 市场数据
   │   └── services/         # 业务逻辑
   │       ├── auth.py
   │       ├── ai.py
   │       ├── database.py
   │       └── market.py     # 北向资金/热门板块
   ├── requirements.txt
   ├── .env.example
   └── README.md
   ```

2. **API 接口实现**
   
   | 端点 | 方法 | 说明 | 状态 |
   |------|------|------|------|
   | `/` | GET | API 根路由 | ✅ |
   | `/health` | GET | 健康检查 | ✅ |
   | `/auth/register` | POST | 用户注册 | ✅ |
   | `/auth/login` | POST | 用户登录 | ✅ |
   | `/auth/logout` | POST | 退出登录 | ✅ |
   | `/prescription/generate` | POST | 生成处方（需登录） | ✅ |
   | `/prescription/generate-anonymous` | POST | 匿名生成处方 | ✅ |
   | `/settings` | GET/PUT | 用户设置 | ✅ |
   | `/settings/models` | GET | 获取模型列表 | ✅ |
   | `/settings/exercises/default` | GET | 默认动作列表 | ✅ |
   | `/market/northbound` | GET | 北向资金数据 | ✅ |
   | `/market/hot-sectors` | GET | 热门板块 | ✅ |
   | `/market/daily-summary` | GET | 每日 AI 总结 | ✅ |
   | `/market/health` | GET | 市场服务健康检查 | ✅ |

3. **数据源验证**
   - ✅ AkShare 1.18.19 安装成功
   - ✅ 北向资金接口 (`stock_hsgt_hist_em`) 可用
   - ✅ 行业板块接口 (`stock_board_industry_spot_em`) 可用
   - ✅ 龙虎榜接口可用

---

### 第二阶段：前端重塑 🔵 待开始

#### 计划内容

1. **初始化 Next.js 项目**
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint
   cd frontend
   npx shadcn-ui@latest init
   ```

2. **核心页面**
   - [ ] 登录/注册页
   - [ ] Dashboard（盈亏输入 + 结果展示）
   - [ ] 设置页
   - [ ] 行情看板页

3. **组件开发**
   - [ ] 输入卡片
   - [ ] 结果卡片
   - [ ] 运动处方展示
   - [ ] 分享卡片生成

---

### 第三阶段：新功能落地 🟢 待开始

#### Priority 1: 每日大佬实操 & AI 总结
- [ ] 北向资金趋势图
- [ ] 热门板块热力图
- [ ] 每日 AI 市场辣评
- [ ] 定时任务（每日15:30自动生成）

#### Priority 2: 投资学习指南
- [ ] 内容管理系统
- [ ] 闯关式学习进度
- [ ] 成就勋章系统

#### Priority 3: 基金选型 AI Chat
- [ ] 向量数据库搭建
- [ ] RAG 检索服务
- [ ] 对话界面

---

## 🚀 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填写 SUPABASE_URL 和 SUPABASE_KEY

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📊 数据源说明

### 北向资金
使用 AkShare 的 `stock_hsgt_hist_em(symbol="北向资金")` 接口获取：
- 日期
- 沪股通净流入
- 深股通净流入
- 北向资金合计

### 热门板块
使用 AkShare 的 `stock_board_industry_spot_em()` 接口获取：
- 板块名称
- 涨跌幅
- 领涨股票（可选）

---

## 🔗 相关链接

- [AkShare 文档](https://akshare.akfamily.xyz/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Supabase 文档](https://supabase.com/docs)
- [Next.js 文档](https://nextjs.org/docs)
- [Shadcn/UI](https://ui.shadcn.com/)

---

## 📝 更新日志

### 2026-01-25
- ✅ 后端 FastAPI 架构搭建完成
- ✅ 核心 API 接口实现
- ✅ AkShare 数据源集成
- ✅ 市场数据服务上线
