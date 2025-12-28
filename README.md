# 《韭菜的自我修养》The Stoic Leek 🌱

一个帮助投资者通过健身任务管理情绪的 Web 应用。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stoic-leek.streamlit.app)
[![GitHub](https://img.shields.io/github/license/Dxboy266/The-Stoic-Leek)](https://github.com/Dxboy266/The-Stoic-Leek/blob/main/LICENSE)

## ✨ 特性

- 🔐 **用户系统**：支持注册登录，会话自动保持
- 🤖 **AI 驱动**：斯多葛风格的毒舌健身教练
- 💪 **动作池管理**：自定义健身动作
- ☁️ **云端存储**：基于 Supabase，数据安全持久化

## 🎯 工作原理

1. **登录账户** → 数据云端同步
2. **输入盈亏** → AI 分析心情
3. **生成处方** → 运动 + 毒舌建议

## 📁 项目结构

```
the-stoic-leek/
├── app.py                   # 主应用入口
├── config/                  # 配置（纯数据）
│   ├── __init__.py          # 配置加载器
│   ├── config.yaml          # 动作池 + 模型配置
│   └── prompt.txt           # AI Prompt
├── core/                    # 核心逻辑
│   ├── __init__.py
│   ├── ai.py                # AI 调用
│   ├── auth.py              # 用户认证
│   └── db.py                # 数据库操作
├── .streamlit/
│   ├── config.toml          # Streamlit 配置
│   └── secrets.toml         # 密钥配置（不提交）
├── requirements.txt         # Python 依赖
└── README.md
```

## 🚀 快速开始

### 在线体验

访问 [在线演示](https://stoic-leek.streamlit.app)

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/Dxboy266/The-Stoic-Leek.git
cd The-Stoic-Leek
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 Supabase**

创建 `.streamlit/secrets.toml`：
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

4. **创建数据库表**

在 Supabase SQL Editor 运行：
```sql
CREATE TABLE user_settings (
    id TEXT PRIMARY KEY,
    api_key TEXT,
    exercises TEXT[],
    model TEXT DEFAULT 'deepseek-ai/DeepSeek-V3',
    model_name TEXT DEFAULT 'DeepSeek-V3 (免费)',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

5. **启动应用**
```bash
streamlit run app.py
```

## 📦 技术栈

- **前端**：Streamlit
- **后端**：Python
- **数据库**：Supabase (PostgreSQL)
- **认证**：Supabase Auth
- **AI**：硅基流动 API

## 📝 许可证

MIT License

## 🙏 致谢

- [Streamlit](https://streamlit.io/)
- [Supabase](https://supabase.com/)
- [硅基流动](https://siliconflow.cn)

---

**免责声明**：本应用仅供娱乐和情绪管理参考，不构成任何投资建议。
