"""
《韭菜的自我修养》The Stoic Leek
"""

import streamlit as st
import requests
import json
import os
from supabase import create_client, Client

DEFAULT_EXERCISES = ["深蹲", "俯卧撑", "卷腹", "高抬腿", "波比跳", "开合跳", "平板支撑", "拉伸", "靠墙静蹲", "仰卧起坐", "跳绳", "原地跑"]

MODELS = {
    "DeepSeek-V3 (免费)": "deepseek-ai/DeepSeek-V3",
    "DeepSeek-V2.5 (免费)": "deepseek-ai/DeepSeek-V2.5",
    "Qwen2.5-7B (免费)": "Qwen/Qwen2.5-7B-Instruct",
    "Qwen2.5-72B (免费)": "Qwen/Qwen2.5-72B-Instruct",
}

st.set_page_config(page_title="韭菜的自我修养", page_icon="🌱", layout="centered", initial_sidebar_state="collapsed")

# Supabase 配置
SUPABASE_URL = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")

@st.cache_resource
def get_supabase() -> Client:
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = get_supabase()

# ========== 用户认证 ==========
def get_user():
    return st.session_state.get('user')

def sign_up(email, password):
    try:
        resp = supabase.auth.sign_up({"email": email, "password": password})
        if resp.user:
            return True, "注册成功！请查收验证邮件"
        return False, "注册失败"
    except Exception as e:
        msg = str(e)
        if "already registered" in msg:
            return False, "该邮箱已注册"
        return False, msg

def sign_in(email, password):
    try:
        resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if resp.user:
            st.session_state['user'] = {"id": resp.user.id, "email": resp.user.email}
            st.session_state['data_loaded'] = False  # 重新加载数据
            return True, "登录成功"
        return False, "登录失败"
    except Exception as e:
        msg = str(e)
        if "Invalid login" in msg:
            return False, "邮箱或密码错误"
        if "Email not confirmed" in msg:
            return False, "请先验证邮箱"
        return False, msg

def sign_out():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.clear()

# ========== 数据存储 ==========
def load_data():
    if 'data_loaded' in st.session_state and st.session_state['data_loaded']:
        return
    
    # 默认值
    st.session_state['exercises'] = DEFAULT_EXERCISES.copy()
    st.session_state['model'] = "deepseek-ai/DeepSeek-V3"
    st.session_state['model_name'] = "DeepSeek-V3 (免费)"
    st.session_state['api_key'] = ""
    
    user = get_user()
    if supabase and user:
        try:
            resp = supabase.table("user_settings").select("*").eq("id", user['id']).execute()
            if resp.data and len(resp.data) > 0:
                data = resp.data[0]
                if data.get('exercises'):
                    st.session_state['exercises'] = data['exercises']
                if data.get('model'):
                    st.session_state['model'] = data['model']
                if data.get('model_name'):
                    st.session_state['model_name'] = data['model_name']
                if data.get('api_key'):
                    st.session_state['api_key'] = data['api_key']
        except Exception as e:
            st.session_state['db_error'] = str(e)
    
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    st.session_state['data_loaded'] = True

def save_to_db():
    user = get_user()
    if not supabase or not user:
        return False
    try:
        supabase.table("user_settings").upsert({
            "id": user['id'],
            "api_key": st.session_state.get('api_key', ''),
            "exercises": st.session_state.get('exercises', DEFAULT_EXERCISES),
            "model": st.session_state.get('model', 'deepseek-ai/DeepSeek-V3'),
            "model_name": st.session_state.get('model_name', 'DeepSeek-V3 (免费)')
        }).execute()
        return True
    except Exception as e:
        st.session_state['db_error'] = str(e)
        return False

def call_ai(api_key, model, amount, exercises):
    if not api_key:
        raise Exception("请先配置 API 密钥")
    exercise_str = ', '.join(exercises) if exercises else '休息'
    abs_amt = abs(amount)
    level = "微小" if abs_amt < 10 else ("小额" if abs_amt < 100 else ("中等" if abs_amt < 1000 else "较大"))
    
    prompt = f"""用户今日盈亏：{amount:.2f} 元（{level}波动）
规则：10元以下=平淡+休息，10-100=平淡+轻运动，100-1000=适量运动，1000+=需要运动
可选运动：{exercise_str}
输出（30字内，务实不夸张）：
【心情】：焦虑/兴奋/平淡
【运动】：动作×数量 或 休息
【建议】：一句话"""

    resp = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.6},
        timeout=15
    )
    if resp.status_code == 401:
        raise Exception("API 密钥无效")
    resp.raise_for_status()
    text = resp.json()['choices'][0]['message']['content'].strip()
    
    mood, exercise, advice = "平淡", "休息", text
    for line in text.split('\n'):
        if '【心情】' in line:
            m = line.split('】')[-1].strip().strip('：:')
            mood = "焦虑" if "焦虑" in m else ("兴奋" if "兴奋" in m else "平淡")
        elif '【运动】' in line:
            exercise = line.split('】')[-1].strip().strip('：:')
        elif '【建议】' in line:
            advice = line.split('】')[-1].strip().strip('：:')
    return {"mood": mood, "exercise": exercise, "advice": advice, "full": text}


# CSS
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
.user-bar { display: flex; justify-content: flex-end; align-items: center; gap: 12px; padding: 8px 0; font-size: 14px; color: #64748b; }
.auth-box { max-width: 360px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
.auth-title { font-size: 1.5rem; font-weight: 700; text-align: center; margin-bottom: 1.5rem; color: #1e293b; }
@media (max-width: 768px) { .block-container { max-width: 100% !important; padding: 1rem !important; min-width: unset !important; } .result-grid { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

# ========== 登录页面 ==========
def show_auth_page():
    st.markdown('''<div class="header"><span class="app-icon">🌱</span><h1>《韭菜的自我修养》</h1><p class="subtitle">THE STOIC LEEK</p></div>''', unsafe_allow_html=True)
    
    if not supabase:
        st.error("数据库未配置")
        return
    
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("邮箱", key="login_email")
            password = st.text_input("密码", type="password", key="login_pwd")
            if st.form_submit_button("登录", use_container_width=True):
                if email and password:
                    ok, msg = sign_in(email, password)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("请填写邮箱和密码")
    
    with tab2:
        with st.form("register_form"):
            email = st.text_input("邮箱", key="reg_email")
            password = st.text_input("密码（至少6位）", type="password", key="reg_pwd")
            password2 = st.text_input("确认密码", type="password", key="reg_pwd2")
            if st.form_submit_button("注册", use_container_width=True):
                if not email or not password:
                    st.warning("请填写邮箱和密码")
                elif len(password) < 6:
                    st.warning("密码至少6位")
                elif password != password2:
                    st.warning("两次密码不一致")
                else:
                    ok, msg = sign_up(email, password)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

# ========== 主应用 ==========
user = get_user()

if not user:
    show_auth_page()
else:
    load_data()
    
    # 用户栏
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button(f"退出 ({user['email'][:10]}...)", use_container_width=True):
            sign_out()
            st.rerun()
    
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

    # 首页
    if st.session_state['page'] == 'home':
        st.markdown('''<div class="header"><span class="app-icon">🌱</span><h1>《韭菜的自我修养》</h1><p class="subtitle">THE STOIC LEEK</p><p class="desc">通过"对冲焦虑的肉体惩罚/奖励机制"帮助投资者管理情绪。将投资盈亏转化为健身任务，用幽默且带有斯多葛哲学意味的方式平衡心理波动。</p></div>''', unsafe_allow_html=True)
        
        if not st.session_state.get('api_key'):
            st.warning("请先前往「设置」页面配置 API 密钥")
        
        st.markdown('<div class="section-title">📊 输入今日投资情况</div>', unsafe_allow_html=True)
        amount = st.number_input("盈亏金额（元）", value=None, step=100.0, placeholder="请输入金额")
        
        if st.button("生成处方", use_container_width=True):
            if amount is None:
                st.warning("请先输入金额")
            elif not st.session_state.get('api_key'):
                st.info("请先配置 API 密钥")
            else:
                with st.spinner("AI 分析中..."):
                    try:
                        result = call_ai(st.session_state['api_key'], st.session_state['model'], amount, st.session_state['exercises'])
                        st.session_state['result'] = {'amount': amount, **result}
                    except Exception as e:
                        st.error(str(e))
        
        if 'result' in st.session_state:
            r = st.session_state['result']
            amt = r['amount']
            color = "green" if amt > 0 else ("red" if amt < 0 else "")
            amt_str = f"+¥{amt:.2f}" if amt > 0 else (f"-¥{abs(amt):.2f}" if amt < 0 else "¥0.00")
            st.markdown(f'''<div class="result-card"><div class="result-grid"><div class="result-item"><div class="result-value {color}">{amt_str}</div><div class="result-label">今日盈亏</div></div><div class="result-item"><div class="result-value">{r['mood']}</div><div class="result-label">心情状态</div></div><div class="result-item"><div class="result-value">{r['exercise']}</div><div class="result-label">运动建议</div></div></div><div class="advice-box"><div class="advice-title">🧠 AI 建议</div><div class="advice-text">{r['advice']}</div></div></div>''', unsafe_allow_html=True)
            
            if st.button("重新生成", use_container_width=True):
                try:
                    result = call_ai(st.session_state['api_key'], st.session_state['model'], amt, st.session_state['exercises'])
                    st.session_state['result'] = {'amount': amt, **result}
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
        
        st.markdown('<div class="footer">保持理性 · 保持运动 · 保持韭菜的自我修养</div>', unsafe_allow_html=True)

    # 动作池
    elif st.session_state['page'] == 'exercises':
        st.markdown('<div class="page-title">💪 动作池管理</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-desc">自定义健身动作，AI 将从中推荐</div>', unsafe_allow_html=True)
        
        exercises = st.session_state.get('exercises', DEFAULT_EXERCISES)
        st.markdown(f'<div class="stats"><div><div class="stat-value">{len(exercises)}</div><div class="stat-label">当前动作</div></div><div><div class="stat-value">{len(DEFAULT_EXERCISES)}</div><div class="stat-label">默认动作</div></div></div>', unsafe_allow_html=True)
        
        st.markdown("### 当前动作池")
        if exercises:
            chips = ''.join([f'<span class="exercise-chip">{ex}</span>' for ex in exercises])
            st.markdown(f'<div style="margin:12px 0">{chips}</div>', unsafe_allow_html=True)
            to_del = st.selectbox("删除动作", [""] + exercises, format_func=lambda x: "选择要删除的动作" if x == "" else f"× {x}")
            if to_del:
                st.session_state['exercises'].remove(to_del)
                save_to_db()
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
                    save_to_db()
                    st.rerun()
                else:
                    st.warning("已存在")
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("恢复默认", use_container_width=True):
                st.session_state['exercises'] = DEFAULT_EXERCISES.copy()
                save_to_db()
                st.rerun()
        with c2:
            if st.button("清空", use_container_width=True):
                st.session_state['exercises'] = []
                save_to_db()
                st.rerun()

    # 设置
    elif st.session_state['page'] == 'settings':
        st.markdown('<div class="page-title">⚙️ 设置</div>', unsafe_allow_html=True)
        
        if st.session_state.get('db_error'):
            st.error(f"数据库错误: {st.session_state['db_error']}")
        
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
                        save_to_db()
                        st.session_state['show_key'] = False
                        st.success("已保存")
                        st.rerun()
                    else:
                        st.warning("请输入密钥")
            with c2:
                if st.session_state.get('show_key') and st.button("取消", use_container_width=True):
                    st.session_state['show_key'] = False
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 模型选择")
        cur = st.session_state.get('model_name', 'DeepSeek-V3 (免费)')
        sel = st.selectbox("模型", list(MODELS.keys()), index=list(MODELS.keys()).index(cur) if cur in MODELS else 0)
        if sel != cur:
            st.session_state['model_name'] = sel
            st.session_state['model'] = MODELS[sel]
            save_to_db()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 关于")
        st.markdown("**韭菜的自我修养** v1.0\n\n[GitHub](https://github.com/Dxboy266/The-Stoic-Leek)")
