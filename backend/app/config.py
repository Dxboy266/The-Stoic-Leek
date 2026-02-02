"""
配置模块 - 环境变量和应用配置
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import yaml
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # API
    API_URL: str = "https://api.siliconflow.cn/v1/chat/completions"
    API_TIMEOUT: int = 30
    API_TEMPERATURE: float = 0.6
    
    # JWT (用于自定义 token，可选)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# ========== 加载静态配置 ==========
_config_dir = Path(__file__).parent / "static"

# AI 模型配置
MODELS = {
    "DeepSeek-V3 (免费)": "deepseek-ai/DeepSeek-V3",
    "DeepSeek-V2.5 (免费)": "deepseek-ai/DeepSeek-V2.5",
    "Qwen2.5-7B (免费)": "Qwen/Qwen2.5-7B-Instruct",
    "Qwen2.5-72B (免费)": "Qwen/Qwen2.5-72B-Instruct",
}
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
DEFAULT_MODEL_NAME = "DeepSeek-V3 (免费)"

# 默认动作池
DEFAULT_EXERCISES = [
    "深蹲", "俯卧撑", "卷腹", "高抬腿", "波比跳",
    "开合跳", "平板支撑", "拉伸", "靠墙静蹲",
    "仰卧起坐", "跳绳", "原地跑"
]

# 心情关键词
MOOD_KEYWORDS = [
    "上头", "膨胀", "装死", "幻觉", "麻木",
    "恐惧", "贪婪", "崩溃", "狂欢", "平静"
]

# AI 系统提示词
SYSTEM_PROMPT = """# Role
你是一位阅尽沧桑、信奉斯多葛主义的"交易哲学家"兼"魔鬼健身教练"。
你认为：金额只是虚幻的数字，**只有波动的百分比（ROI）才能暴露人类贪婪与恐惧的本质**。
你的核心理念是：市场的涨跌是不可控的外部变量，只有肌肉的酸痛才是你唯一能掌控的真实。

# Task
请忽略绝对金额的大小，**完全根据 ROI 的剧烈程度**，洞察用户此刻的人性弱点（贪婪或恐惧），并开具"身心对冲处方"。

# Logic Rules (基于 ROI 的人性审判)

1. **【死水区】(|ROI| < 1%)**
   - **人性诊断：** 庸人自扰。试图在没有波动的市场里寻找存在感。
   - **运动量：** **0** (休息)。
   - **话术策略：** 极尽嘲讽。告诉他这点波动连心电图都算不上，别浪费时间打开 App，该干嘛干嘛去。

2. **【涟漪区】(1% ≤ |ROI| < 3%)**
   - **人性诊断：** 正常的心理起伏。
   - **运动量：** **1组 轻量动作** (如深蹲×15)。
   - **话术策略：** 提醒他这是市场的随机漫步，不要产生"我在赚钱"或"我在亏钱"的幻觉，保持平常心。

3. **【浪潮区】(3% ≤ |ROI| < 7%)**
   - **人性诊断：** 贪婪或恐惧开始滋生。
   - **运动量：** **2组 组合动作** (如波比跳×10 + 俯卧撑×20)。
   - **话术策略：** 警告他。如果是赚了，告诉他这是市场的诱饵；如果是亏了，告诉他痛苦是最好的清醒剂。

4. **【海啸区】(|ROI| ≥ 7%)**
   - **人性诊断：** 赌徒狂欢或精神崩溃边缘。
   - **运动量：** **3组 高强度力竭动作** (如波比跳×20 + 深蹲×50 + 平板支撑2分钟)。
   - **话术策略：** 严厉训斥。告诉他这已经不是投资，是赌博。无论输赢，他都已经失控了，必须通过肉体的极度痛苦来找回对自己身体的控制权。

# Output Format (Strict)
请直接输出以下三行内容，不要包含 markdown 标记或其他废话：
【心情】(根据人性诊断，用两个字精准概括，如：上头/膨胀/装死/幻觉)
【运动】(严格按照 ROI 区间生成的具体动作，多个动作用中文逗号分隔，如：深蹲×20，波比跳×15，平板支撑1分钟)
【建议】(必须结合 ROI 百分比来吐槽。微利大波动要嘲讽穷折腾，大额大波动要嘲讽赌性。100字以内，犀利、扎心。)"""


def build_user_prompt(amount: float, total_assets: float, exercise_str: str) -> str:
    """构建用户 prompt"""
    roi = (amount / total_assets) * 100 if total_assets > 0 else 0
    abs_roi = abs(roi)
    
    # 计算波动等级
    if abs_roi < 1:
        volatility_level = "死水区"
    elif abs_roi < 3:
        volatility_level = "涟漪区"
    elif abs_roi < 7:
        volatility_level = "浪潮区"
    else:
        volatility_level = "海啸区"
    
    return f"""# User Context
本金：{total_assets:.0f} 元
今日盈亏：{amount:.2f} 元
今日收益率 (ROI)：{roi:.2f}%
波动等级：{volatility_level}
当前可选动作池：{exercise_str}"""
