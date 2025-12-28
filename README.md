# 《韭菜的自我修养》The Stoic Leek 🌱

一个帮助投资者通过健身任务管理情绪的 Web 应用。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stoic-leek.streamlit.app)
[![GitHub](https://img.shields.io/github/license/Dxboy266/The-Stoic-Leek)](https://github.com/Dxboy266/The-Stoic-Leek/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Dxboy266/The-Stoic-Leek)](https://github.com/Dxboy266/The-Stoic-Leek/stargazers)

## ✨ 特性

- 🔐 **用户系统**：支持注册登录，数据云端同步
- 🤖 **AI 驱动建议**：使用大语言模型生成个性化的运动处方
- 💪 **动作池管理**：自定义健身动作，AI 从中智能推荐
- 😌 **情绪识别**：根据盈亏金额自动判断心情状态
- 📱 **响应式设计**：完美支持 PC 和移动设备
- ☁️ **云端存储**：基于 Supabase，数据安全持久化

## 🎯 工作原理

1. **注册/登录**：创建账户，数据云端同步
2. **输入盈亏金额**：正数表示盈利，负数表示亏损
3. **AI 分析心情**：
   - 10元以下 → 平淡 → 休息
   - 10-100元 → 平淡 → 轻运动
   - 100-1000元 → 适量运动
   - 1000元+ → 需要运动（多动作组合）
4. **生成运动处方**：从你的动作池中智能推荐

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
- **AI**：硅基流动 API (DeepSeek/Qwen)

## 📁 项目结构

```
the-stoic-leek/
├── .streamlit/
│   ├── config.toml          # Streamlit 配置
│   └── secrets.toml         # 密钥配置（不提交）
├── app.py                   # 主应用程序
├── requirements.txt         # Python 依赖
├── README.md                # 项目说明
├── LICENSE                  # MIT 许可证
└── .gitignore               # Git 忽略配置
```

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - Python Web 框架
- [Supabase](https://supabase.com/) - 开源 Firebase 替代
- [硅基流动](https://siliconflow.cn) - 免费 AI API 服务

---

**免责声明**：本应用仅供娱乐和情绪管理参考，不构成任何投资建议。投资有风险，入市需谨慎。
