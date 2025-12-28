"""
《韭菜的自我修养》The Stoic Leek
主应用入口
"""

import streamlit as st
from core import get_user, sign_in, sign_out, sign_up
from core import get_supabase, load_user_data, save_user_data, call_ai
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
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
header { display: none !important; }
.header { text-align: center; padding: 0.5rem 0 1.5rem 0; }
.app-icon { font-size: 4rem; display: block; }
.header h1 { font-size: 2.25rem; font-weight: 700; background: linear-gradient(135deg, #0ea5e9, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
.header .subtitle { font-size: 1rem; color: #64748b; letter-spacing: 0.15em; }
.header .desc { font-size: 0.9375rem; color: #475569; line-height: 1.8; max-width: 500px; margin: 1rem auto 0; }
.page-title { font-size: 1.75rem; font-weight: 700; color: #1e293b; text-align: center; margin: 1rem 0 0.5rem; }
.page-desc { font-size: 0.9375rem; color: #64748b; text-align: center; margin-bottom: 2rem; }
.section-title { font-size: 1.0625rem; font-weight: 600; color: #1e293b; margin: 1.5rem 0 0.75rem; }
.exercise-chip { display: inline-flex; padding: 6px 12px; margin: 4px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; font-size: 14px; color: #475569; }
.result-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
.result-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.875rem; margin-bottom: 1.25rem; }
.result-item { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; text-align: center; }
.result-value { font-size: 1.375rem; font-weight: 700; color: #0f172a; }
.result-value.green { color: #10b981; }
.result-value.red { color: #ef4444; }
.result-label { font-size: 0.75rem; color: #64748b; }
.advice-box { background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 12px; padding: 1rem; border-left: 4px solid #f59e0b; }
.advice-title { font-size: 0.75rem; font-weight: 600; color: #92400e; margin-bottom: 0.5rem; }
.advice-text { font-size: 0.9375rem; color: #78350f; line-height: 1.7; }
.footer { text-align: center; padding: 2rem 0 1rem; color: #94a3b8; font-size: 0.875rem; }
.stats { display: flex; justify-content: center; gap: 2rem; padding: 1rem; background: #f8fafc; border-radius: 12px; margin: 1rem 0; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #8b5cf6; }
.stat-label { font-size: 0.75rem; color: #64748b; }
@media (max-width: 768px) { .block-container { max-width: 100% !important; padding: 1rem !important; min-width: unset !important; } .result-grid { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

# ========== 初始化（懒加载）==========
def _get_supabase():
    """懒加载 Supabase"""
    if 'supabase' not in st.session_state:
        st.session_state['supabase'] = get_supabase()
    return st.session_state['supabase']

user = st.session_state.get('user')

# ========== 页面组件 ==========
def show_auth_page():
    """登录/注册页面"""
    st.markdown('''<div class="header"><span class="app-icon">🌱</span><h1>《韭菜的自我修养》</h1><p class="subtitle">THE STOIC LEEK</p></div>''', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    with tab1:
        email = st.text_input("邮箱", key="login_email")
        password = st.text_input("密码", type="password", key="login_pwd")
        
        is_loading = st.session_state.get('login_loading', False)
        
        if st.button(
            "登录中..." if is_loading else "登录",
            use_container_width=True,
            disabled=is_loading,
            key="login_btn"
        ):
            if email and password:
                st.session_state['login_loading'] = True
                st.session_state['login_data'] = (email, password)
                st.rerun()
            else:
                st.warning("请填写邮箱和密码")
        
        # 执行登录
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
                        if 'login_data' in st.session_state:
                            del st.session_state['login_data']
                        st.rerun()
                    else:
                        st.error(msg)
            except Exception as e:
                st.error(f"连接失败：{str(e)}")
            # 无论成功失败都重置状态
            st.session_state['login_loading'] = False
            if 'login_data' in st.session_state:
                del st.session_state['login_data']
    
    with tab2:
        email2 = st.text_input("邮箱", key="reg_email")
        password2 = st.text_input("密码（至少6位）", type="password", key="reg_pwd")
        password3 = st.text_input("确认密码", type="password", key="reg_pwd2")
        
        is_reg_loading = st.session_state.get('reg_loading', False)
        
        if st.button(
            "注册中..." if is_reg_loading else "注册",
            use_container_width=True,
            disabled=is_reg_loading,
            key="reg_btn"
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
        
        # 执行注册
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
            # 无论成功失败都重置状态
            st.session_state['reg_loading'] = False
            if 'reg_data' in st.session_state:
                del st.session_state['reg_data']


def show_home_page(user):
    """首页"""
    st.markdown('''<div class="header"><span class="app-icon">🌱</span><h1>《韭菜的自我修养》</h1><p class="subtitle">THE STOIC LEEK</p><p class="desc">通过"对冲焦虑的肉体惩罚/奖励机制"帮助投资者管理情绪。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。</p></div>''', unsafe_allow_html=True)
    
    if not st.session_state.get('api_key'):
        st.warning("请先前往「设置」页面配置 API 密钥")
    
    st.markdown('<div class="section-title">📊 输入今日投资情况</div>', unsafe_allow_html=True)
    
    # 本金和盈亏输入
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
        # 本金变化时保存
        if total_assets and total_assets != saved_assets:
            st.session_state['total_assets'] = total_assets
            save_user_data(user['id'])
    
    with col2:
        amount = st.number_input("今日盈亏（元）", value=None, step=100.0, placeholder="正数盈利，负数亏损")
    
    # 显示收益率预览
    if amount is not None and total_assets and total_assets > 0:
        roi = (amount / total_assets) * 100
        roi_color = "green" if roi > 0 else ("red" if roi < 0 else "gray")
        roi_str = f"+{roi:.2f}%" if roi > 0 else f"{roi:.2f}%"
        st.markdown(f'<div style="text-align:center;color:{roi_color};font-size:1.2rem;margin:0.5rem 0">收益率：{roi_str}</div>', unsafe_allow_html=True)
    
    # 按钮逻辑
    has_result = 'result' in st.session_state
    is_generating = st.session_state.get('generating', False)
    
    if has_result:
        btn_label = "重新生成中..." if is_generating else "重新生成"
    else:
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
            st.rerun()
    
    # 执行生成
    if is_generating and 'gen_data' in st.session_state:
        amount, total_assets = st.session_state['gen_data']
        try:
            result = call_ai(
                st.session_state['api_key'],
                st.session_state['model'],
                amount,
                total_assets,
                st.session_state['exercises']
            )
            roi = (amount / total_assets) * 100 if total_assets > 0 else 0
            st.session_state['result'] = {
                'amount': amount,
                'total_assets': total_assets,
                'roi': roi,
                **result
            }
        except Exception as e:
            st.error(str(e))
        st.session_state['generating'] = False
        if 'gen_data' in st.session_state:
            del st.session_state['gen_data']
        st.rerun()
    
    if has_result:
        r = st.session_state['result']
        amt = r['amount']
        roi = r.get('roi', 0)
        color = "green" if amt > 0 else ("red" if amt < 0 else "")
        amt_str = f"+¥{amt:.2f}" if amt > 0 else (f"-¥{abs(amt):.2f}" if amt < 0 else "¥0.00")
        roi_str = f"+{roi:.2f}%" if roi > 0 else f"{roi:.2f}%"
        
        st.markdown(f'''<div class="result-card">
            <div class="result-grid">
                <div class="result-item"><div class="result-value {color}">{amt_str}</div><div class="result-label">今日盈亏</div></div>
                <div class="result-item"><div class="result-value {color}">{roi_str}</div><div class="result-label">收益率</div></div>
                <div class="result-item"><div class="result-value">{r['mood']}</div><div class="result-label">心情状态</div></div>
            </div>
            <div class="result-item" style="margin-bottom:1rem"><div class="result-value">{r['exercise']}</div><div class="result-label">运动处方</div></div>
            <div class="advice-box"><div class="advice-title">🧠 AI 建议</div><div class="advice-text">{r['advice']}</div></div>
        </div>''', unsafe_allow_html=True)
    
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
    
    # 导航
    page = st.session_state.get('page', 'home')
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏠 首页", use_container_width=True, type="primary" if page == 'home' else "secondary"):
            st.session_state['page'] = 'home'
            st.rerun()
    with c2:
        if st.button("💪 动作池", use_container_width=True, type="primary" if page == 'exercises' else "secondary"):
            st.session_state['page'] = 'exercises'
            st.rerun()
    with c3:
        if st.button("⚙️ 设置", use_container_width=True, type="primary" if page == 'settings' else "secondary"):
            st.session_state['page'] = 'settings'
            st.rerun()
    
    # 页面路由
    if page == 'home':
        show_home_page(user)
    elif page == 'exercises':
        show_exercises_page(user)
    elif page == 'settings':
        show_settings_page(user)
