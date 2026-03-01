import streamlit as st
import feedparser
from datetime import datetime

# 页面配置
st.set_page_config(page_title="全球财经看板", page_icon="💰")

st.title("💰 实时财经新闻快讯")
st.write("数据源：Google News (中文财经频道)")

# 核心功能：获取新闻
def fetch_finance_news():
    # 这是 Google 新闻“商业”板块的中文 RSS 地址，稳定性极高
    rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVd3U0FtVnpHZ0pWVXlnQVAB?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    
    try:
        # 解析 RSS
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            return None
        return feed.entries
    except Exception as e:
        return None

# 侧边栏：刷新按钮
if st.sidebar.button('🔄 点击手动刷新'):
    st.cache_data.clear()
    st.rerun()

# 加载并显示新闻
with st.spinner('正在同步全球财经数据...'):
    news_entries = fetch_finance_news()

if news_entries:
    st.success(f"已更新！当前共有 {len(news_entries[:20])} 条头条资讯")
    
    for entry in news_entries[:20]: # 只取最新的20条
        with st.container():
            # 标题变蓝色加粗
            st.markdown(f"### [{entry.title}]({entry.link})")
            
            # 显示发布来源和日期
            col1, col2 = st.columns([1, 1])
            with col1:
                st.caption(f"📢 来源：{entry.source.get('title', '未知媒体')}")
            with col2:
                # 尝试格式化时间
                st.caption(f"⏰ 发布时间：{entry.published[:16] if 'published' in entry else '刚刚'}")
            
            st.divider() # 画线
else:
    st.error("哎呀，服务器连接有点阻塞，请点击左侧按钮刷新试试。")

st.sidebar.markdown("---")
st.sidebar.write("💡 **小贴士**：点击标题可直接跳转至媒体原文阅读。")
