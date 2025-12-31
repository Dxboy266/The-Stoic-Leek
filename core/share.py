"""
分享卡片模块 - A股风格双皮肤（红红火火 vs 关灯吃面）
"""

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os

# 分享链接
SHARE_URL = "https://github.com/Dxboy266/The-Stoic-Leek"


def _get_font(size: int):
    """获取字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    try:
        return ImageFont.load_default(size=size)
    except:
        return ImageFont.load_default()


def _draw_gradient(img: Image.Image, color_top: tuple, color_bottom: tuple):
    """绘制垂直线性渐变背景"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def _draw_translucent_rect(img: Image.Image, xy: tuple, radius: int, color: tuple, alpha: int):
    """绘制半透明圆角矩形"""
    x1, y1, x2, y2 = xy
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=(*color, alpha))
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'), (0, 0))


def _wrap_text(text: str, font, max_width: int, draw) -> list:
    """文字换行"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def _parse_exercises(exercise_str: str) -> list:
    """解析运动列表"""
    exercise_str = exercise_str.strip()
    if not exercise_str or exercise_str in ['0', '无', '休息', '休息日']:
        return []
    exercises = exercise_str.replace('，', ',').split(',')
    return [e.strip() for e in exercises if e.strip() and e.strip() != '0']


def _generate_qrcode(url: str, size: int, dark_mode: bool = False) -> Image.Image:
    """生成二维码"""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        if dark_mode:
            # 深色模式：白色二维码，透明背景
            qr_img = qr.make_image(fill_color="white", back_color="black")
        else:
            qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
        return qr_img
    except ImportError:
        color = (200, 200, 200) if not dark_mode else (80, 80, 80)
        placeholder = Image.new('RGB', (size, size), color)
        return placeholder


def generate_share_card(amount: float, roi: float, exercise: str, advice: str, quote: str = "") -> bytes:
    """生成分享卡片图片 - A股风格双皮肤"""
    
    width = 540
    padding = 32
    content_width = width - padding * 2
    
    # 根据盈亏选择主题
    is_loss = amount < 0
    
    if is_loss:
        # 【韭菜护眼版】关灯吃面 - 赛博朋克风
        gradient_top = (10, 25, 47)      # 深蓝
        gradient_bottom = (5, 15, 25)    # 更深的蓝黑
        text_primary = (255, 255, 255)   # 白色
        text_secondary = (160, 180, 200) # 浅银蓝
        accent_color = (0, 255, 100)     # 荧光绿
        card_color = (20, 40, 60)        # 深蓝灰
        card_alpha = 180
        quote_color = (40, 60, 80)
        divider_color = (40, 60, 80)
    else:
        # 【红红火火版】喜庆温暖
        gradient_top = (255, 245, 238)   # 极淡暖橙
        gradient_bottom = (255, 255, 255) # 白色
        text_primary = (51, 51, 51)      # 深灰
        text_secondary = (128, 128, 128) # 灰色
        accent_color = (255, 51, 51)     # 正红色
        card_color = (255, 250, 245)     # 暖白
        card_alpha = 220
        quote_color = (255, 230, 220)
        divider_color = (240, 230, 225)
    
    # 字体
    font_title = _get_font(26)
    font_large = _get_font(40)
    font_medium = _get_font(17)
    font_small = _get_font(14)
    font_tiny = _get_font(12)
    font_quote = _get_font(50)
    
    # 解析运动列表
    exercises = _parse_exercises(exercise)
    
    # 临时画布计算高度
    temp = Image.new('RGB', (width, 1200), (255, 255, 255))
    temp_draw = ImageDraw.Draw(temp)
    
    advice_lines = _wrap_text(advice, font_small, content_width - 70, temp_draw)
    
    # 计算高度
    header_h = 100
    amount_h = 80
    exercise_h = 40 + max(len(exercises), 1) * 28 + 20
    advice_h = 65 + min(len(advice_lines), 6) * 22 + 35
    footer_h = 75
    
    total_h = padding + header_h + amount_h + 16 + exercise_h + 12 + advice_h + 16 + footer_h + padding
    
    # 正式画布 - 渐变背景
    img = Image.new('RGB', (width, total_h), gradient_top)
    _draw_gradient(img, gradient_top, gradient_bottom)
    draw = ImageDraw.Draw(img)
    
    y = padding
    
    # ===== 头部 =====
    today = datetime.now().strftime("%m/%d")
    draw.text((width - padding, y + 4), today, font=font_small, anchor="rt", fill=text_secondary)
    
    draw.text((padding, y), "韭菜处方单", font=font_title, fill=text_primary)
    y += 36
    
    draw.text((padding, y), "市场涨跌皆虚妄，唯有酸痛最真实", font=font_tiny, fill=text_secondary)
    y += 50
    
    # ===== 金额区 =====
    if amount > 0:
        prefix = "+"
        label = "今日收益"
    elif amount < 0:
        prefix = ""
        label = "今日亏损"
    else:
        prefix = ""
        label = "今日持平"
    
    draw.text((padding, y), label, font=font_tiny, fill=text_secondary)
    y += 20
    
    amount_str = f"{prefix}¥{amount:,.2f}"
    draw.text((padding, y), amount_str, font=font_large, fill=accent_color)
    
    amt_bbox = draw.textbbox((padding, y), amount_str, font=font_large)
    roi_str = f"{roi:+.2f}%"
    draw.text((amt_bbox[2] + 12, y + 16), roi_str, font=font_small, fill=accent_color)
    
    y += 55
    
    # ===== 运动处方卡片（半透明）=====
    card_y1 = y
    card_y2 = y + exercise_h
    _draw_translucent_rect(img, (padding, card_y1, width - padding, card_y2), 12, card_color, card_alpha)
    draw = ImageDraw.Draw(img)  # 重新获取 draw
    
    draw.text((width // 2, card_y1 + 14), "运动处方", font=font_tiny, anchor="mt", fill=text_secondary)
    
    ex_y = card_y1 + 38
    if exercises:
        for ex in exercises[:5]:
            draw.text((padding + 20, ex_y), f"·  {ex}", font=font_medium, fill=text_primary)
            ex_y += 28
    else:
        draw.text((width // 2, ex_y + 8), "今日休息，养精蓄锐", font=font_medium, anchor="mt", fill=text_secondary)
    
    y = card_y2 + 12
    
    # ===== AI点评卡片（半透明）=====
    card_y1 = y
    card_y2 = y + advice_h
    _draw_translucent_rect(img, (padding, card_y1, width - padding, card_y2), 12, card_color, card_alpha)
    draw = ImageDraw.Draw(img)
    
    draw.text((width // 2, card_y1 + 14), "AI 建议", font=font_tiny, anchor="mt", fill=text_secondary)
    
    # 左上角大引号
    draw.text((padding + 16, card_y1 + 32), '"', font=font_quote, fill=quote_color)
    
    # 建议文字
    adv_y = card_y1 + 50
    for line in advice_lines[:6]:
        draw.text((padding + 36, adv_y), line, font=font_small, fill=text_primary)
        adv_y += 22
    
    # 右下角大引号
    draw.text((width - padding - 45, adv_y - 12), '"', font=font_quote, fill=quote_color)
    
    y = card_y2 + 16
    
    # ===== 底部 =====
    draw.line([(padding, y), (width - padding, y)], fill=divider_color, width=1)
    y += 14
    
    draw.text((padding, y), "韭菜的自我修养", font=font_small, fill=text_primary)
    draw.text((padding, y + 20), "The Stoic Leek", font=font_tiny, fill=text_secondary)
    
    # 二维码
    qr_size = 48
    qr_img = _generate_qrcode(SHARE_URL, qr_size, dark_mode=is_loss)
    qr_x = width - padding - qr_size
    qr_y = y + 3
    img.paste(qr_img, (qr_x, qr_y))
    
    # 输出
    buffer = BytesIO()
    img.save(buffer, format='PNG', quality=95)
    buffer.seek(0)
    return buffer.getvalue()
