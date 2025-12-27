"""
《韭菜的自我修养》The Stoic Leek
一个帮助投资者通过健身任务管理情绪的 Streamlit 应用
"""

import streamlit as st
import random
import requests
import json

# 健身动作配置
EXERCISE_CONFIG = {
    "loss": ["深蹲", "俯卧撑", "卷腹", "高抬腿"],
    "profit": ["波比跳", "深蹲", "俯卧撑", "开合跳"],
    "neutral": ["平板支撑", "拉伸", "靠墙静蹲"]
}

# 计算系数
LOSS_DIVISOR = 10    # 亏损金额除数
PROFIT_DIVISOR = 20  # 盈利金额除数


def determine_mood(amount: float) -> str:
    """
    根据盈亏金额自动判断心情状态
    
    Args:
        amount: 盈亏金额（正数为盈利，负数为亏损，零为持平）
    
    Returns:
        str: 心情状态（"焦虑"、"兴奋"或"平淡"）
    """
    if amount < 0:
        return "焦虑"
    elif amount > 0:
        return "兴奋"
    else:
        return "平淡"


def calculate_exercise_task(amount: float) -> tuple[str, int]:
    """
    根据盈亏金额计算健身任务
    
    Args:
        amount: 盈亏金额（正数为盈利，负数为亏损，零为持平）
    
    Returns:
        tuple: (动作名称, 动作数量)
    """
    if amount < 0:
        # 亏损：abs(amount) // 10，最小为 1
        count = max(1, int(abs(amount) // LOSS_DIVISOR))
        exercise = random.choice(EXERCISE_CONFIG["loss"])
    elif amount > 0:
        # 盈利：amount // 20，最小为 1
        count = max(1, int(amount // PROFIT_DIVISOR))
        exercise = random.choice(EXERCISE_CONFIG["profit"])
    else:
        # 持平：固定数量
        count = 30  # 平板支撑 30 秒或拉伸 30 秒
        exercise = random.choice(EXERCISE_CONFIG["neutral"])
    
    return exercise, count


def build_prompt(amount: float, mood: str, exercise: str, count: int) -> str:
    """
    构建 AI Prompt
    
    Args:
        amount: 盈亏金额
        mood: 心情状态
        exercise: 健身动作
        count: 动作数量
    
    Returns:
        str: 完整的 prompt 文本
    """
    if amount < 0:
        # 亏损场景：幽默嘲讽 + 斯多葛哲学
        prompt = f"""你是一位幽默风趣且富有哲学智慧的投资顾问。用户今天亏损了 {abs(amount):.2f} 元，心情{mood}。

请用幽默嘲讽的语气，结合斯多葛哲学的智慧，给用户一段简短的建议（100字以内）。要点：
1. 用轻松幽默的方式嘲讽一下用户的亏损
2. 引用斯多葛哲学的观点（如爱比克泰德、马可·奥勒留的思想），提醒用户专注于可控之事
3. 鼓励用户通过完成 {count} 个{exercise}来发泄情绪、重获理性

语气要轻松诙谐，但不失智慧。"""

    elif amount > 0:
        # 盈利场景：打击嚣张 + 风险警示
        prompt = f"""你是一位冷静理性的投资顾问。用户今天盈利了 {amount:.2f} 元，心情{mood}。

请用略带打击的幽默语气，给用户一段简短的警示建议（100字以内）。要点：
1. 提醒用户不要过度兴奋，市场随时可能反转
2. 强调风险管理和保持谦逊的重要性
3. 建议用户通过完成 {count} 个{exercise}来冷静头脑、保持理性

语气要幽默但犀利，让用户保持清醒。"""

    else:
        # 持平场景：平常心鼓励
        prompt = f"""你是一位温和智慧的投资顾问。用户今天盈亏为零，心情{mood}。

请用温和鼓励的语气，给用户一段简短的建议（100字以内）。要点：
1. 肯定用户保持平常心的态度
2. 鼓励用户继续保持理性和耐心
3. 建议用户通过 {count} 秒的{exercise}来保持身心平衡

语气要温和友善，传递正能量。"""

    return prompt


class AIClient:
    """硅基流动 SiliconFlow API 客户端"""
    
    def __init__(self, api_key: str):
        """
        初始化客户端
        
        Args:
            api_key: SiliconFlow API 密钥
        """
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1"
        self.model = "Qwen/Qwen2.5-7B-Instruct"
    
    def generate_advice(self, amount: float, mood: str, exercise: str, count: int) -> str:
        """
        生成投资建议文本
        
        Args:
            amount: 盈亏金额
            mood: 心情状态
            exercise: 健身动作
            count: 动作数量
        
        Returns:
            str: AI 生成的建议文本
        
        Raises:
            Exception: API 调用失败
        """
        # 构建 prompt
        prompt = build_prompt(amount, mood, exercise, count)
        
        # 准备请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.8,
            "max_tokens": 500
        }
        
        try:
            # 发送请求
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            
            # 检查响应
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            advice = result['choices'][0]['message']['content']
            
            return advice.strip()
            
        except requests.exceptions.Timeout:
            raise Exception("API 请求超时，请稍后重试")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("API 密钥无效，请检查配置")
            elif response.status_code == 429:
                raise Exception("请求过于频繁，请稍后重试")
            else:
                raise Exception(f"API 调用失败: {str(e)}")
        except Exception as e:
            raise Exception(f"生成建议时出错: {str(e)}")

# 页面配置
st.set_page_config(
    page_title="《韭菜的自我修养》The Stoic Leek",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/your-username/the-stoic-leek',
        'Report a bug': "https://github.com/your-username/the-stoic-leek/issues",
        'About': "# 《韭菜的自我修养》\n通过健身任务管理投资情绪的 AI 应用"
    }
)

# 添加自定义 CSS 以优化移动端体验
st.markdown("""
<style>
    /* 移动端优化 */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            font-size: 16px;
            padding: 12px;
        }
        
        .stNumberInput input {
            font-size: 16px;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.4rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
    }
    
    /* 通用样式优化 */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.title("《韭菜的自我修养》")
st.subheader("The Stoic Leek")

# 应用说明
st.markdown("""
通过"对冲焦虑的肉体惩罚/奖励机制"帮助投资者管理情绪。
将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。
""")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    st.markdown("### API 密钥设置")
    st.info("请在 [硅基流动](https://siliconflow.cn) 注册并获取免费 API 密钥")
    
    api_key = st.text_input(
        "SiliconFlow API 密钥",
        type="password",
        help="输入您的 API 密钥以使用 AI 生成功能"
    )
    
    # 存储 API 密钥到 session state
    if api_key:
        st.session_state['api_key'] = api_key

# 主输入区域
st.markdown("---")
st.header("📊 输入今日投资情况")

amount = st.number_input(
    "盈亏金额（元）",
    value=0.0,
    step=100.0,
    help="正数表示盈利，负数表示亏损，系统将自动判断您的心情状态"
)

# 生成处方按钮
if st.button("🎯 生成处方", type="primary", use_container_width=True):
    # 检查 API 密钥
    if 'api_key' not in st.session_state or not st.session_state['api_key']:
        st.info("💡 请先在侧边栏配置 API 密钥")
    else:
        # 输入验证
        if abs(amount) > 1000000:
            st.warning("⚠️ 金额似乎过大，请确认输入正确")
        
        # 显示加载动画
        with st.spinner("🤖 AI 正在生成您的专属处方..."):
            try:
                # 自动判断心情状态
                mood = determine_mood(amount)
                
                # 计算健身任务
                exercise, count = calculate_exercise_task(amount)
                
                # 调用 AI 生成建议
                ai_client = AIClient(st.session_state['api_key'])
                advice = ai_client.generate_advice(amount, mood, exercise, count)
                
                # 存储处方到 session state
                st.session_state['prescription'] = {
                    'amount': amount,
                    'mood': mood,
                    'exercise': exercise,
                    'count': count,
                    'advice': advice
                }
                
                st.success("✅ 处方生成成功！")
                
            except Exception as e:
                st.error(f"❌ 生成处方失败: {str(e)}")
                st.info("💡 请检查 API 密钥是否正确，或稍后重试")

# 显示处方
if 'prescription' in st.session_state:
    st.markdown("---")
    st.header("📋 您的投资处方")
    
    prescription = st.session_state['prescription']
    amount = prescription['amount']
    exercise = prescription['exercise']
    count = prescription['count']
    advice = prescription['advice']
    
    # 根据盈亏类型选择颜色和 emoji
    if amount < 0:
        color = "red"
        emoji = "📉"
        status_text = f"亏损 {abs(amount):.2f} 元"
    elif amount > 0:
        color = "green"
        emoji = "📈"
        status_text = f"盈利 {amount:.2f} 元"
    else:
        color = "gray"
        emoji = "➖"
        status_text = "持平"
    
    # 显示盈亏状态
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label=f"{emoji} 今日盈亏",
            value=status_text
        )
    with col2:
        st.metric(
            label="💪 健身任务",
            value=f"{exercise} x {count}"
        )
    
    # 显示 AI 建议
    st.markdown("### 🧠 AI 建议")
    st.info(advice)
    
    # 重新生成按钮
    if st.button("🔄 重新生成", type="secondary", use_container_width=True):
        with st.spinner("🤖 AI 正在重新生成处方..."):
            try:
                # 使用相同的金额，心情会自动重新判断（结果相同）
                mood = determine_mood(amount)
                
                # 重新计算健身任务（随机选择新动作）
                exercise, count = calculate_exercise_task(amount)
                
                # 调用 AI 生成新建议
                ai_client = AIClient(st.session_state['api_key'])
                advice = ai_client.generate_advice(amount, mood, exercise, count)
                
                # 更新处方
                st.session_state['prescription'] = {
                    'amount': amount,
                    'mood': mood,
                    'exercise': exercise,
                    'count': count,
                    'advice': advice
                }
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ 重新生成失败: {str(e)}")

# 页脚
st.markdown("---")
st.caption("💪 保持理性，保持运动，保持韭菜的自我修养")
