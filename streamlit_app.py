import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# 设置网页
st.set_page_config(page_title="全球财经快讯", page_icon="🌐")

st.title("🌐 全球财经实时快讯")
st.subheader("稳定版 - 自动抓取主流财经媒体")

# 定义新闻源（这里选了新浪财经，非常稳定）
NEWS_SOURCES = {
    "新浪财经-国内新闻": "https://finance.sina.com.cn/realtime/china/index.xml",
    "新浪财经-国际新闻": "https://finance.sina.com.cn/realtime/global/index.xml",
    "新浪财经-证券新闻": "https://finance.sina.com.cn/realtime/stock/index.xml"
}

# 选择新闻源
source_name = st.sidebar.selectbox("选择新闻频道", list(NEWS_SOURCES.keys()))
source_url = NEWS_SOURCES[source_name]

def get_rss_news(url):
    try:
        # 解析 RSS 数据
        feed = feedparser.parse(url)
        news_list = []
        for entry in feed.entries[:20]: # 取前20条
            news_list.append({
                "标题": entry.title,
                "链接": entry.link,
                "发布时间": entry.published if 'published' in entry else "刚刚",
                "摘要": entry.summary if 'summary' in entry else ""
            })
        return news_list
    except Exception as e:
        st.error(f"解析出错: {e}")
        return None

# 刷新按钮
if st.button('🔄 刷新获取最新新闻'):
    st.cache_data.clear()
    st.rerun()

# 获取并显示新闻
with st.spinner('正在连接财经服务器...'):
    news = get_rss_news(source_url)

if news:
    for item in news:
        with st.container():
            # 显示标题
            st.markdown(f"### [{item['标题']}]({item['链接']})")
            # 显示时间
            st.caption(f"📅 {item['发布时间']}")
            # 显示摘要（去掉HTML标签）
            import re
            clean_summary = re.sub('<[^<]+?>', '', item['摘要']) 
            st.write(clean_summary[:200] + "...") 
            st.divider()
else:
    st.warning("暂未获取到数据，请尝试切换频道或稍后刷新。")

# 侧边栏
st.sidebar.info("提示：此版本使用 RSS 技术，解决了海外服务器访问受限的问题。")
