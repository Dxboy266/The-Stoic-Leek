# 《韭菜的自我修养》The Stoic Leek 💪

一个帮助投资者通过健身任务管理情绪的 Web 应用。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stoic-leek.streamlit.app)
[![GitHub](https://img.shields.io/github/license/Dxboy266/The-Stoic-Leek)](https://github.com/Dxboy266/The-Stoic-Leek/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Dxboy266/The-Stoic-Leek)](https://github.com/Dxboy266/The-Stoic-Leek/stargazers)

## ✨ 特性

- 🤖 **AI 驱动建议**：使用大语言模型生成个性化的投资建议
- 💪 **健身任务系统**：根据盈亏金额自动计算健身任务
- 😌 **情绪管理**：通过斯多葛哲学和幽默语气帮助管理投资情绪
- 📱 **响应式设计**：完美支持 PC 和移动设备
- 🔄 **重新生成**：不满意？一键重新生成新的建议

## 🎯 工作原理

1. **输入盈亏金额**：正数表示盈利，负数表示亏损
2. **自动判断心情**：
   - 亏损 → 焦虑 → 幽默嘲讽 + 斯多葛哲学安慰
   - 盈利 → 兴奋 → 打击嚣张 + 风险警示
   - 持平 → 平淡 → 平常心鼓励
3. **计算健身任务**：
   - 亏损：abs(金额) ÷ 10 个动作（深蹲、俯卧撑、卷腹等）
   - 盈利：金额 ÷ 20 个动作（波比跳、开合跳等）
   - 持平：30 秒轻量运动（平板支撑、拉伸等）
4. **AI 生成建议**：结合心情和健身任务生成个性化建议

## 🚀 快速开始

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

3. **启动应用**
```bash
streamlit run app.py
```

4. **配置 API 密钥**
   - 访问 [硅基流动](https://siliconflow.cn) 注册并获取免费 API 密钥
   - 在应用侧边栏输入 API 密钥

### 在线体验

访问 [在线演示](https://stoic-leek.streamlit.app)

## 📦 依赖

- Python 3.8+
- Streamlit
- Requests
- 其他依赖见 `requirements.txt`

## 📁 项目结构

```
the-stoic-leek/
├── .streamlit/
│   └── config.toml          # Streamlit 配置
├── app.py                   # 主应用程序
├── requirements.txt         # Python 依赖
├── packages.txt             # 系统依赖
├── README.md                # 项目说明
├── LICENSE                  # MIT 许可证
├── CONTRIBUTING.md          # 贡献指南
├── USAGE.md                 # 使用文档
├── DEPLOYMENT.md            # 部署指南
└── .gitignore               # Git 忽略配置
```

## 🎨 截图

### PC 端
![PC Screenshot](docs/images/pc-screenshot.png)

### 移动端
![Mobile Screenshot](docs/images/mobile-screenshot.png)

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的 Python Web 框架
- [硅基流动](https://siliconflow.cn) - 提供免费的 AI API 服务
- 斯多葛哲学 - 提供智慧的指引

## 📧 联系方式

如有问题或建议，请提交 [Issue](https://github.com/Dxboy266/The-Stoic-Leek/issues)

---

**免责声明**：本应用仅供娱乐和情绪管理参考，不构成任何投资建议。投资有风险，入市需谨慎。
