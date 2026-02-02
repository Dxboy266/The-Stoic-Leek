"""
《韭菜的自我修养》The Stoic Leek
主应用入口
"""

import streamlit as st
from core import get_user, sign_in, sign_out, sign_up, try_restore_session
from core import get_supabase, load_user_data, save_user_data, call_ai, generate_share_card
from config import DEFAULT_EXERCISES, MODELS

# ========== 页面配置 ==========
st.set_page_config(
    page_title="韭菜的自我修养",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== 样式 ==========
st.markdown("""
<style>
* { font-family: 'Inter', 'Noto Sans SC', -apple-system, sans-serif; }
.stApp { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 30%, #f0fdf4 70%, #faf5ff 100%); }
.block-container { max-width: 55% !important; min-width: 520px !important; padding: 1rem 2rem !important; padding-top: 0 !important; }

/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
header { display: none !important; }

/* 输入框磨砂玻璃效果 */
.stTextInput > div > div {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div:focus-within {
    background: rgba(255, 255, 255, 0.85) !important;
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
}
.stNumberInput > div > div {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
}

/* 按钮样式 - 胶囊渐变 */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
/* 次要按钮 */
.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.8) !important;
    color: #475569 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.95) !important;
}

/* 下载按钮特殊样式 */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 25px !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
}

/* Tabs 样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.5);
    padding: 4px;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 指标卡片阴影 */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    backdrop-filter: blur(10px);
}

.header { text-align: center; padding: 0.5rem 0 1.5rem 0; }
.app-icon { font-size: 4rem; display: block; }
.header h1 { font-size: 2.25rem; font-weight: 700; background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
.header h1 a { text-decoration: none; background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.header .slogan-en { font-size: 0.875rem; color: #94a3b8; letter-spacing: 0.05em; margin-top: 0.5rem; font-style: italic; }
.header .slogan-cn { font-size: 1rem; color: #64748b; margin-top: 0.25rem; }
.header .desc { font-size: 0.9375rem; color: #475569; line-height: 1.8; max-width: 500px; margin: 1rem auto 0; }
.page-title { font-size: 1.75rem; font-weight: 700; color: #1e293b; text-align: center; margin: 1rem 0 0.5rem; }
.page-desc { font-size: 0.9375rem; color: #64748b; text-align: center; margin-bottom: 2rem; }
.section-title { font-size: 1.0625rem; font-weight: 600; color: #1e293b; margin: 1.5rem 0 0.75rem; }
.exercise-chip { display: inline-flex; padding: 6px 12px; margin: 4px; background: rgba(255,255,255,0.8); border: 1px solid #e2e8f0; border-radius: 16px; font-size: 14px; color: #475569; backdrop-filter: blur(5px); }
.result-card { background: rgba(255,255,255,0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 18px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
.result-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.875rem; margin-bottom: 1.25rem; }
.result-item { background: rgba(248,250,252,0.8); border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; text-align: center; }
.result-value { font-size: 1.375rem; font-weight: 700; color: #0f172a; }
.result-value.profit { color: #ef4444; }
.result-value.loss { color: #10b981; }
.exercise-card { background: rgba(248,250,252,0.8); border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
.exercise-title { text-align: center; font-size: 0.75rem; color: #64748b; margin-bottom: 0.75rem; font-weight: 500; }
.exercise-list { text-align: left; padding: 0 0.5rem; }
.exercise-item { font-size: 1.125rem; font-weight: 600; color: #0f172a; padding: 0.25rem 0; }
.exercise-item.rest { color: #64748b; font-weight: 500; text-align: center; }
.result-label { font-size: 0.75rem; color: #64748b; }
.advice-box { background: linear-gradient(135deg, rgba(240,249,255,0.9), rgba(224,242,254,0.9)); border-radius: 12px; padding: 1rem; border-left: 4px solid #0ea5e9; backdrop-filter: blur(5px); }
.advice-title { font-size: 0.75rem; font-weight: 600; color: #0369a1; margin-bottom: 0.5rem; }
.advice-text { font-size: 0.9375rem; color: #0c4a6e; line-height: 1.7; }
.footer { text-align: center; padding: 2rem 0 1rem; color: #94a3b8; font-size: 0.875rem; }
.stats { display: flex; justify-content: center; gap: 2rem; padding: 1rem; background: rgba(248,250,252,0.8); border-radius: 12px; margin: 1rem 0; backdrop-filter: blur(5px); }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #8b5cf6; }
.stat-label { font-size: 0.75rem; color: #64748b; }

@media (max-width: 768px) {
    .block-container { max-width: 100% !important; padding: 0.75rem !important; min-width: unset !important; }
    .header { padding: 0.25rem 0 1rem 0; }
    .header h1 { font-size: 1.75rem; }
    .header .slogan-en { font-size: 0.75rem; }
    .header .slogan-cn { font-size: 0.875rem; }
    .app-icon { font-size: 3rem; }
    .result-grid { grid-template-columns: 1fr; gap: 0.5rem; }
    .result-item { padding: 0.75rem; }
    .result-value { font-size: 1.25rem; }
    .exercise-card { padding: 0.75rem; }
    .exercise-item { font-size: 1rem; }
    .advice-box { padding: 0.75rem; }
    .advice-text { font-size: 0.875rem; }
    .section-title { font-size: 1rem; margin: 1rem 0 0.5rem; }
    .footer { padding: 1.5rem 0 0.5rem; font-size: 0.75rem; }
    .stButton > button { padding: 0.5rem 1rem !important; font-size: 0.875rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ========== 初始化（懒加载）==========
def _get_supabase():
    """懒加载 Supabase"""
    if 'supabase' not in st.session_state:
        st.session_state['supabase'] = get_supabase()
    return st.session_state['supabase']

# 尝试恢复登录状态
user = try_restore_session(_get_supabase()) or st.session_state.get('user')

# ========== 页面组件 ==========
def show_auth_page():
    """登录/注册页面 - 单体式现代卡片"""
    
    # 精修样式 - 紫/白/灰三色统一
    st.markdown('''<style>
    /* ===== 1. 实心白卡片 - 强边界感 ===== */
    div[data-testid="column"]:nth-of-type(2) > div {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem 2rem 1.5rem 2rem !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 0.95) !important;
    }
    
    /* ===== 2. 极简输入框 ===== */
    div[data-testid="column"]:nth-of-type(2) .stTextInput > div > div {
        background: #f5f5f7 !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTextInput > div > div:focus-within {
        border-color: #667eea !important;
        background: #fff !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.12) !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTextInput input {
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTextInput {
        margin-bottom: 0.75rem;
    }
    
    /* ===== 3. Tabs - 强制紫色，消灭红色 ===== */
    div[data-testid="column"]:nth-of-type(2) .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 0 !important;
        border-bottom: 1px solid #e5e7eb !important;
        justify-content: center;
        margin-top: -8px !important;
        margin-bottom: 1.25rem;
        padding: 0 !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTabs [data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 500;
        color: #9ca3af !important;
        padding: 0.6rem 1.75rem !important;
        border-radius: 0 !important;
        background: transparent !important;
        border-bottom: 2px solid transparent !important;
        margin-bottom: -1px;
    }
    div[data-testid="column"]:nth-of-type(2) .stTabs [data-baseweb="tab"]:hover {
        color: #667eea !important;
    }
    /* 选中状态 - 紫色文字+紫色下划线 */
    div[data-testid="column"]:nth-of-type(2) .stTabs [aria-selected="true"] {
        color: #667eea !important;
        background: transparent !important;
        box-shadow: none !important;
        border-bottom-color: #667eea !important;
        font-weight: 600;
    }
    /* 彻底隐藏 Streamlit 默认红色高亮 */
    div[data-testid="column"]:nth-of-type(2) .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
        background-color: transparent !important;
        height: 0 !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    /* 覆盖所有可能的红色来源 */
    div[data-testid="column"]:nth-of-type(2) .stTabs button[data-baseweb="tab"]::before,
    div[data-testid="column"]:nth-of-type(2) .stTabs button[data-baseweb="tab"]::after {
        background-color: #667eea !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stTabs [role="tablist"] > div:last-child {
        background-color: #667eea !important;
    }
    
    /* ===== 4. Logo 区域 - 紧凑 ===== */
    .auth-logo {
        text-align: center;
        margin-bottom: 0.25rem;
        padding-bottom: 0;
    }
    .auth-logo .icon {
        font-size: 2.75rem;
        display: block;
        margin-bottom: 0.4rem;
    }
    .auth-logo h1 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 0.2rem 0;
        letter-spacing: -0.02em;
    }
    .auth-logo p {
        color: #9ca3af;
        font-size: 0.78rem;
        margin: 0;
    }
    
    /* ===== 5. 底部链接 ===== */
    .auth-footer {
        text-align: center;
        margin-top: 1.25rem;
        padding-top: 0.75rem;
        border-top: 1px solid #f0f0f0;
        font-size: 0.72rem;
        color: #9ca3af;
    }
    .auth-footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    .auth-footer a:hover {
        text-decoration: underline;
    }
    
    /* ===== 6. 按钮 - 紫色渐变 ===== */
    div[data-testid="column"]:nth-of-type(2) .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.7rem 1rem !important;
        margin-top: 0.5rem;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.45) !important;
    }
    </style>''', unsafe_allow_html=True)
    
    # 三列布局 - 中间列自动成为卡片
    _, col2, _ = st.columns([1, 1.2, 1])
    
    with col2:
        # Logo - 在卡片内
        st.markdown('''<div class="auth-logo">
            <span class="icon">🌱</span>
            <h1>韭菜的自我修养</h1>
            <p>市场涨跌皆虚妄，唯有酸痛最真实</p>
        </div>''', unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2 = st.tabs(["登录", "注册"])
        
        with tab1:
            email = st.text_input("邮箱", key="login_email", label_visibility="collapsed", placeholder="邮箱")
            password = st.text_input("密码", type="password", key="login_pwd", label_visibility="collapsed", placeholder="密码")
            
            is_loading = st.session_state.get('login_loading', False)
            
            if st.button(
                "登录中..." if is_loading else "登录",
                use_container_width=True,
                disabled=is_loading,
                key="login_btn",
                type="primary"
            ):
                if email and password:
                    st.session_state['login_loading'] = True
                    st.session_state['login_data'] = (email, password)
                    st.rerun()
                else:
                    st.warning("请填写邮箱和密码")
            
            if is_loading and 'login_data' in st.session_state:
                email, password = st.session_state['login_data']
                try:
                    supabase = _get_supabase()
                    if not supabase:
                        st.error("数据库未配置")
                    else:
                        ok, msg = sign_in(supabase, email, password)
                        if ok:
                            st.session_state['login_loading'] = False
                            del st.session_state['login_data']
                            st.rerun()
                        else:
                            st.error(msg)
                except Exception as e:
                    st.error(f"连接失败：{str(e)}")
                st.session_state['login_loading'] = False
                if 'login_data' in st.session_state:
                    del st.session_state['login_data']
        
        with tab2:
            email2 = st.text_input("邮箱", key="reg_email", label_visibility="collapsed", placeholder="邮箱")
            password2 = st.text_input("密码", type="password", key="reg_pwd", label_visibility="collapsed", placeholder="密码（至少6位）")
            password3 = st.text_input("确认", type="password", key="reg_pwd2", label_visibility="collapsed", placeholder="确认密码")
            
            is_reg_loading = st.session_state.get('reg_loading', False)
            
            if st.button(
                "注册中..." if is_reg_loading else "注册",
                use_container_width=True,
                disabled=is_reg_loading,
                key="reg_btn",
                type="primary"
            ):
                if not email2 or not password2:
                    st.warning("请填写邮箱和密码")
                elif len(password2) < 6:
                    st.warning("密码至少6位")
                elif password2 != password3:
                    st.warning("两次密码不一致")
                else:
                    st.session_state['reg_loading'] = True
                    st.session_state['reg_data'] = (email2, password2)
                    st.rerun()
            
            if is_reg_loading and 'reg_data' in st.session_state:
                email2, password2 = st.session_state['reg_data']
                try:
                    supabase = _get_supabase()
                    if not supabase:
                        st.error("数据库未配置")
                    else:
                        ok, msg = sign_up(supabase, email2, password2)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                except Exception as e:
                    st.error(f"连接失败：{str(e)}")
                st.session_state['reg_loading'] = False
                if 'reg_data' in st.session_state:
                    del st.session_state['reg_data']
        
        # 底部
        st.markdown('''<div class="auth-footer">
            <a href="https://github.com/Dxboy266/The-Stoic-Leek" target="_blank">GitHub</a>
            <span style="margin: 0 0.5rem">·</span>
            <a href="https://siliconflow.cn" target="_blank">获取 API Key</a>
        </div>''', unsafe_allow_html=True)


def show_home_page(user):
    """首页"""
    st.markdown('''<div class="header">
        <span class="app-icon">🌱</span>
        <h1><a href="https://github.com/Dxboy266/The-Stoic-Leek" target="_blank" style="text-decoration:none;color:inherit;">韭菜的自我修养</a></h1>
        <p class="slogan-en">Market volatility is noise; Muscle pain is real.</p>
        <p class="slogan-cn">市场涨跌皆虚妄，唯有酸痛最真实。</p>
    </div>''', unsafe_allow_html=True)
    
    # 判断当前视图：有结果就显示结果页，否则显示输入页
    has_result = 'result' in st.session_state
    is_generating = st.session_state.get('generating', False)
    
    if has_result and not is_generating:
        # ===== 结果页 =====
        r = st.session_state['result']
        amt = r['amount']
        roi = r.get('roi', 0)
        color = "profit" if amt > 0 else ("loss" if amt < 0 else "")
        amt_str = f"+¥{amt:.2f}" if amt > 0 else (f"-¥{abs(amt):.2f}" if amt < 0 else "¥0.00")
        roi_str = f"+{roi:.2f}%" if roi > 0 else f"{roi:.2f}%"
        
        # 解析运动列表
        exercise_raw = r['exercise'].strip()
        if not exercise_raw or exercise_raw in ['0', '无', '休息', '休息日']:
            exercise_html = '<div class="exercise-item rest">今日休息，养精蓄锐 🧘</div>'
        else:
            exercises = [e.strip() for e in exercise_raw.replace('，', ',').split(',') if e.strip() and e.strip() != '0']
            if exercises:
                exercise_html = ''.join([f'<div class="exercise-item">· {ex}</div>' for ex in exercises])
            else:
                exercise_html = '<div class="exercise-item rest">今日休息，养精蓄锐 🧘</div>'
        
        st.markdown(f'''<div class="result-card">
            <div class="result-grid">
                <div class="result-item"><div class="result-value {color}">{amt_str}</div><div class="result-label">今日盈亏</div></div>
                <div class="result-item"><div class="result-value {color}">{roi_str}</div><div class="result-label">收益率</div></div>
                <div class="result-item"><div class="result-value">{r['mood']}</div><div class="result-label">心情状态</div></div>
            </div>
            <div class="exercise-card"><div class="exercise-title">运动处方</div><div class="exercise-list">{exercise_html}</div></div>
            <div class="advice-box"><div class="advice-title">AI 建议</div><div class="advice-text">{r['advice']}</div></div>
        </div>''', unsafe_allow_html=True)
        
        # 按钮区 - 水平并排
        card_bytes = generate_share_card(
            amount=r['amount'],
            roi=r.get('roi', 0),
            exercise=r['exercise'],
            advice=r['advice']
        )
        
        col_regen, col_download = st.columns([1, 1.5])
        with col_regen:
            if st.button("🔄 重新生成", use_container_width=True, type="secondary"):
                st.session_state['generating'] = True
                st.session_state['gen_data'] = (r['amount'], r['total_assets'])
                st.session_state['is_regenerate'] = True
                st.rerun()
        with col_download:
            st.download_button(
                label="📤 下载分享卡片",
                data=card_bytes,
                file_name="韭菜处方单.png",
                mime="image/png",
                use_container_width=True,
                type="primary"
            )
    
    else:
        # ===== 输入页 =====
        if not st.session_state.get('api_key'):
            st.warning("请先前往「设置」页面配置 API 密钥")
        
        st.markdown('<div class="section-title">📊 输入今日投资情况</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            saved_assets = st.session_state.get('total_assets')
            total_assets = st.number_input(
                "本金（元）", 
                value=float(saved_assets) if saved_assets else None,
                min_value=1.0,
                step=1000.0,
                placeholder="请输入本金",
                help="你的投资本金总额，保存后下次自动填充"
            )
            if total_assets and total_assets != saved_assets:
                st.session_state['total_assets'] = total_assets
                save_user_data(user['id'])
        
        with col2:
            amount = st.number_input("今日盈亏（元）", value=None, step=100.0, placeholder="正数盈利，负数亏损")
        
        # 收益率预览
        if amount is not None and total_assets and total_assets > 0:
            roi = (amount / total_assets) * 100
            roi_color = "#ef4444" if roi > 0 else ("#10b981" if roi < 0 else "gray")
            roi_str = f"+{roi:.2f}%" if roi > 0 else f"{roi:.2f}%"
            st.markdown(f'<div style="text-align:center;color:{roi_color};font-size:1.2rem;margin:0.5rem 0">收益率：{roi_str}</div>', unsafe_allow_html=True)
        
        btn_label = "生成中..." if is_generating else "生成处方"
        
        if st.button(btn_label, use_container_width=True, disabled=is_generating):
            if not total_assets:
                st.warning("请先输入本金")
            elif amount is None:
                st.warning("请先输入盈亏金额")
            elif not st.session_state.get('api_key'):
                st.info("请先配置 API 密钥")
            else:
                st.session_state['generating'] = True
                st.session_state['gen_data'] = (amount, total_assets)
                st.session_state['is_regenerate'] = False
                st.rerun()
        
        # 执行生成
        if is_generating and 'gen_data' in st.session_state:
            amount, total_assets = st.session_state['gen_data']
            is_regen = st.session_state.get('is_regenerate', False)
            try:
                result = call_ai(
                    st.session_state['api_key'],
                    st.session_state['model'],
                    amount,
                    total_assets,
                    st.session_state['exercises']
                )
                roi = round((amount / total_assets) * 100, 2) if total_assets > 0 else 0
                st.session_state['result'] = {
                    'amount': amount,
                    'total_assets': total_assets,
                    'roi': roi,
                    **result
                }
                # 只有首次生成才更新本金
                if not is_regen:
                    new_assets = total_assets + amount
                    st.session_state['total_assets'] = new_assets
                    save_user_data(user['id'])
            except Exception as e:
                st.error(str(e))
            st.session_state['generating'] = False
            if 'gen_data' in st.session_state:
                del st.session_state['gen_data']
            if 'is_regenerate' in st.session_state:
                del st.session_state['is_regenerate']
            st.rerun()
    
    st.markdown('<div class="footer">保持理性 · 保持运动 · 保持韭菜的自我修养</div>', unsafe_allow_html=True)


def show_exercises_page(user):
    """动作池页面"""
    st.markdown('<div class="page-title">💪 动作池管理</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-desc">自定义健身动作，AI 将从中推荐</div>', unsafe_allow_html=True)
    
    exercises = st.session_state.get('exercises', DEFAULT_EXERCISES)
    st.markdown(f'''<div class="stats">
        <div><div class="stat-value">{len(exercises)}</div><div class="stat-label">当前动作</div></div>
        <div><div class="stat-value">{len(DEFAULT_EXERCISES)}</div><div class="stat-label">默认动作</div></div>
    </div>''', unsafe_allow_html=True)
    
    st.markdown("### 当前动作池")
    if exercises:
        chips = ''.join([f'<span class="exercise-chip">{ex}</span>' for ex in exercises])
        st.markdown(f'<div style="margin:12px 0">{chips}</div>', unsafe_allow_html=True)
        to_del = st.selectbox("删除动作", [""] + exercises, format_func=lambda x: "选择要删除的动作" if x == "" else f"× {x}")
        if to_del:
            st.session_state['exercises'].remove(to_del)
            save_user_data(user['id'])
            st.rerun()
    else:
        st.info("动作池为空")
    
    st.markdown("---")
    st.markdown("### 添加动作")
    new_ex = st.text_input("动作名称", placeholder="如：引体向上")
    if st.button("添加", use_container_width=True):
        if new_ex and new_ex.strip():
            if new_ex.strip() not in st.session_state['exercises']:
                st.session_state['exercises'].append(new_ex.strip())
                save_user_data(user['id'])
                st.rerun()
            else:
                st.warning("已存在")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("恢复默认", use_container_width=True):
            st.session_state['exercises'] = DEFAULT_EXERCISES.copy()
            save_user_data(user['id'])
            st.rerun()
    with c2:
        if st.button("清空", use_container_width=True):
            st.session_state['exercises'] = []
            save_user_data(user['id'])
            st.rerun()


def show_settings_page(user):
    """设置页面"""
    st.markdown('<div class="page-title">⚙️ 设置</div>', unsafe_allow_html=True)
    
    if st.session_state.get('db_error'):
        st.error(f"数据库错误: {st.session_state['db_error']}")
    
    # API 密钥
    st.markdown("### API 密钥")
    st.info("[硅基流动](https://siliconflow.cn) 注册获取免费密钥")
    
    current_key = st.session_state.get('api_key', '')
    
    if current_key and not st.session_state.get('show_key'):
        st.success(f"✅ 已配置（{current_key[:8]}...）")
        if st.button("更换密钥"):
            st.session_state['show_key'] = True
            st.rerun()
    else:
        new_key = st.text_input("API 密钥", type="password", value="" if st.session_state.get('show_key') else current_key)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("保存密钥", use_container_width=True):
                if new_key and new_key.strip():
                    st.session_state['api_key'] = new_key.strip()
                    save_user_data(user['id'])
                    st.session_state['show_key'] = False
                    st.success("已保存")
                    st.rerun()
                else:
                    st.warning("请输入密钥")
        with c2:
            if st.session_state.get('show_key') and st.button("取消", use_container_width=True):
                st.session_state['show_key'] = False
                st.rerun()
    
    # 模型选择
    st.markdown("---")
    st.markdown("### 模型选择")
    cur = st.session_state.get('model_name', 'DeepSeek-V3 (免费)')
    sel = st.selectbox("模型", list(MODELS.keys()), index=list(MODELS.keys()).index(cur) if cur in MODELS else 0)
    if sel != cur:
        st.session_state['model_name'] = sel
        st.session_state['model'] = MODELS[sel]
        save_user_data(user['id'])
        st.rerun()
    
    # 账户
    st.markdown("---")
    st.markdown("### 账户")
    st.info(f"当前账户：{user['email']}")
    if st.button("退出登录", use_container_width=True):
        sign_out(_get_supabase())
        st.rerun()
    
    # 关于
    st.markdown("---")
    st.markdown("### 关于")
    st.markdown("**韭菜的自我修养** v1.0\n\n[GitHub](https://github.com/Dxboy266/The-Stoic-Leek)")


# ========== 主逻辑 ==========
if not user:
    show_auth_page()
else:
    # 加载用户数据
    if not st.session_state.get('data_loaded'):
        load_user_data(user['id'])
        st.session_state['data_loaded'] = True
    
    # 导航 Tabs
    tab_home, tab_exercises, tab_settings = st.tabs(["🏠 首页", "💪 动作池", "⚙️ 设置"])
    
    with tab_home:
        show_home_page(user)
    
    with tab_exercises:
        show_exercises_page(user)
    
    with tab_settings:
        show_settings_page(user)
