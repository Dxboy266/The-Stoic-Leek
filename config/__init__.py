"""
配置模块 - 从 YAML 和 TXT 文件加载配置
"""

import yaml
from pathlib import Path

_config_dir = Path(__file__).parent

# 加载 YAML 配置
with open(_config_dir / "config.yaml", "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f)

# 加载 Prompt
with open(_config_dir / "prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().strip()

# 导出配置
DEFAULT_EXERCISES = _config["exercises"]
MODELS = _config["models"]
DEFAULT_MODEL = _config["default_model"]
DEFAULT_MODEL_NAME = _config["default_model_name"]
API_URL = _config["api"]["url"]
API_TIMEOUT = _config["api"]["timeout"]
API_TEMPERATURE = _config["api"]["temperature"]
MOOD_KEYWORDS = _config["mood_keywords"]


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
