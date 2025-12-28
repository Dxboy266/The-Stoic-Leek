"""
认证模块 - 处理用户登录、注册
"""

import streamlit as st


def try_restore_session(supabase) -> dict | None:
    """尝试恢复会话"""
    # 已登录直接返回
    if st.session_state.get('user'):
        return st.session_state['user']
    
    # 尝试从 Supabase 获取当前 session
    if supabase:
        try:
            session = supabase.auth.get_session()
            if session and session.user:
                user = {"id": session.user.id, "email": session.user.email}
                st.session_state['user'] = user
                return user
        except:
            pass
    
    return None


def sign_up(supabase, email: str, password: str) -> tuple[bool, str]:
    """注册新用户"""
    try:
        resp = supabase.auth.sign_up({"email": email, "password": password})
        if resp.user:
            return True, "注册成功！"
        return False, "注册失败"
    except Exception as e:
        msg = str(e)
        if "already registered" in msg:
            return False, "该邮箱已注册"
        return False, msg


def sign_in(supabase, email: str, password: str) -> tuple[bool, str]:
    """用户登录"""
    try:
        resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if resp.user and resp.session:
            st.session_state['user'] = {"id": resp.user.id, "email": resp.user.email}
            st.session_state['data_loaded'] = False
            return True, "登录成功"
        return False, "登录失败"
    except Exception as e:
        msg = str(e)
        if "Invalid login" in msg:
            return False, "邮箱或密码错误"
        if "Email not confirmed" in msg:
            return False, "请先验证邮箱"
        return False, msg


def sign_out(supabase):
    """退出登录"""
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.clear()


def get_user() -> dict | None:
    """获取当前登录用户"""
    return st.session_state.get('user')
