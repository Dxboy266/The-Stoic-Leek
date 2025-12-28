"""
数据库模块 - 处理 Supabase 数据存储（懒加载）
"""

import streamlit as st
import os

# 延迟导入，避免启动时加载 supabase
_supabase_client = None


def get_supabase():
    """获取 Supabase 客户端（懒加载单例）"""
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client
    
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")
    
    if url and key:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        return _supabase_client
    
    return None


def _get_defaults():
    """获取默认配置（懒加载）"""
    from config import DEFAULT_EXERCISES, DEFAULT_MODEL, DEFAULT_MODEL_NAME
    return DEFAULT_EXERCISES, DEFAULT_MODEL, DEFAULT_MODEL_NAME


def load_user_data(user_id: str):
    """从数据库加载用户数据"""
    DEFAULT_EXERCISES, DEFAULT_MODEL, DEFAULT_MODEL_NAME = _get_defaults()
    supabase = get_supabase()
    
    # 设置默认值
    st.session_state.setdefault('exercises', DEFAULT_EXERCISES.copy())
    st.session_state.setdefault('model', DEFAULT_MODEL)
    st.session_state.setdefault('model_name', DEFAULT_MODEL_NAME)
    st.session_state.setdefault('api_key', "")
    st.session_state.setdefault('total_assets', None)
    st.session_state.setdefault('page', 'home')
    
    if not supabase or not user_id:
        return
    
    try:
        resp = supabase.table("user_settings").select("*").eq("id", user_id).execute()
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
            if data.get('total_assets'):
                st.session_state['total_assets'] = float(data['total_assets'])
    except Exception as e:
        st.session_state['db_error'] = str(e)


def save_user_data(user_id: str) -> bool:
    """保存用户数据到数据库"""
    DEFAULT_EXERCISES, DEFAULT_MODEL, DEFAULT_MODEL_NAME = _get_defaults()
    supabase = get_supabase()
    
    if not supabase or not user_id:
        return False
    
    try:
        supabase.table("user_settings").upsert({
            "id": user_id,
            "api_key": st.session_state.get('api_key', ''),
            "exercises": st.session_state.get('exercises', DEFAULT_EXERCISES),
            "model": st.session_state.get('model', DEFAULT_MODEL),
            "model_name": st.session_state.get('model_name', DEFAULT_MODEL_NAME),
            "total_assets": st.session_state.get('total_assets')
        }).execute()
        return True
    except Exception as e:
        st.session_state['db_error'] = str(e)
        return False
