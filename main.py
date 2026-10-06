import streamlit as st
from datetime import datetime

st.set_page_config(page_title="連絡ツール", page_icon="💬")

# 全ユーザーで共有されるデータ
@st.cache_resource
def get_store():
    return {"messages": []}

store = get_store()

# ユーザー名の入力
name = st.sidebar.text_input("あなたの名前", key="name")
if not name:
    st.info("左のサイドバーで名前を入力してください")
    st.stop()

st.title("💬 連絡ツール")

# 2秒ごとに自動更新される表示部分
@st.fragment(run_every=2)
def show_messages():
    for msg in store["messages"]:
        # 自分以外のメッセージを見たら既読にする
        if msg["sender"] != name:
            msg["read_by"].add(name)

        is_me = msg["sender"] == name
        with st.chat_message("user" if is_me else "assistant"):
            st.markdown(f"**{msg['sender']}**  `{msg['time']}`")
            st.write(msg["text"])
            if is_me:
                if msg["read_by"]:
                    st.caption("✅ 既読: " + ", ".join(sorted(msg["read_by"])))
                else:
                    st.caption("未読")

show_messages()

# 送信
if text := st.chat_input("メッセージを入力"):
    store["messages"].append({
        "sender": name,
        "text": text,
        "time": datetime.now().strftime("%H:%M"),
        "read_by": set(),
    })
    st.rerun()