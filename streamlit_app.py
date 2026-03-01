import streamlit as st
import akshare as ak
import pandas as pd
from datetime import datetime

# 设置网页标题和图标
st.set_page_config(page_title="每日财经早报", page_icon="📈")

st.title("🛡️ 每日财经实时快讯")
st.caption(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 添加一个刷新按钮
if st.button('刷新获取最新新闻'):
    st.rerun()

# 获取数据的函数
@st.cache_data(ttl=600) # 缓存10分钟，避免频繁抓取被封IP
def get_news():
    try:
        # 获取财联社电报数据
        df = ak.stock_telegraph_cls()
        return df.head(15) # 只取最新的15条
    except:
        return None

news_data = get_news()

if news_data is not None:
    for index, row in news_data.iterrows():
        # 用卡片形式展示新闻
        with st.expander(f"⏰ {row['publish_time']} - {row['title']}", expanded=True):
            st.write(row['content'])
            st.info("来源：财联社")
else:
    st.error("暂时无法获取新闻，请稍后再试。")

# 侧边栏说明
st.sidebar.header("关于本站")
st.sidebar.write("这是一个自动抓取最新财经快讯的极简演示站。")
st.sidebar.write("数据来源：财联社 (通过 AkShare 接口)")