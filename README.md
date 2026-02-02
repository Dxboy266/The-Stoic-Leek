# 《韭菜的自我修养》The Stoic Leek 🌱

一个帮助投资者通过健身任务管理情绪的 Web 应用。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。

**💡 核心理念：市场的涨跌是不可控的外部变量，只有肌肉的酸痛才是你唯一能掌控的真实。**

## ✨ 项目特性

- 🛡️ **Local-First 架构**：数据存储在本地浏览器（LocalStorage），无须担心隐私泄露，无需数据库。
- 🤖 **AI 驱动**：集成 DeepSeek R1/V3，提供斯多葛风格的毒舌健身方案。
- 📊 **市场概览**：集成北向资金、热门板块等金融数据，助你洞察全局。
- 💪 **身心对冲**：根据盈亏百分比（ROI）动态生成健身任务，用肉体痛苦抵消财务焦虑。
- 📱 **现代 UI**：基于 Next.js + Tailwind CSS + Shadcn UI 构建的高颜值界面。

## 🚀 快速开始

项目采用前后端分离架构，你需要分别启动后端和前端服务。

### 1. 后端服务 (Python / FastAPI)

后端主要负责 AI 调用代理和金融数据抓取。

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境 (建议)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端 (默认端口 8000)
uvicorn app.main:app --reload
```

### 2. 前端服务 (Next.js)

前端负责所有 UI 面板交互和数据本地化存储。

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端 (默认端口 3000)
npm run dev
```

启动后，访问 [http://localhost:3000](http://localhost:3000) 即可开始使用。

## 📁 存储说明

**现在数据保存在哪里？**

由于移除了云端数据库，本项目目前采用 **Local-First** 架构：
- **所有的个人设置**（API Key、选中的模型、自定义动作池）
- **所有的投资记录**（本金、今日盈亏）
- **生成的处方建议**

这些数据全部保存在你浏览器的 **LocalStorage** 中（键名为 `stoic-leek-storage`）。
这意味着数据仅存在于当前浏览器，更换浏览器或清除网站缓存会导致数据丢失。后端仅作为辅助工具（AI 代理、市场数据），不持久化任何用户信息。

## 🛠️ 技术栈

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Shadcn UI, Zustand (Persist)
- **Backend**: FastAPI, AkShare, Uvicorn, httpx
- **AI**: DeepSeek V3/R1 (via SiliconFlow or other providers)

## 📝 许可证

MIT License

---

**免责声明**：本应用仅供娱乐和情绪管理参考，不构成任何投资建议。
