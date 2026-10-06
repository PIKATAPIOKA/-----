import random
import string
import threading
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="連絡ツール", page_icon="💬")


# 全ユーザーで共有されるデータ(サーバー再起動で消えます)
@st.cache_resource
def get_store():
    return {"rooms": {}, "lock": threading.Lock()}


store = get_store()


def make_code(length=6):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choices(chars, k=length))
        if code not in store["rooms"]:
            return code


# ---------- 入室画面 ----------
if "room" not in st.session_state:
    st.title("💬 連絡ツール")
    st.write("ミーティングコードを入力して参加、または新しく作成してください。")

    name = st.text_input("あなたの名前")
    code_input = st.text_input(
        "ミーティングコード", help="作成時は空欄でOK(自動で発行されます)"
    ).strip().upper()

    col1, col2 = st.columns(2)

    if col1.button("➕ 作成", use_container_width=True):
        if not name.strip():
            st.error("名前を入力してください")
        else:
            with store["lock"]:
                code = code_input or make_code()
                if code in store["rooms"]:
                    st.error("そのコードはすでに使われています")
                else:
                    store["rooms"][code] = {"messages": [], "members": {name.strip()}}
                    st.session_state.room = code
                    st.session_state.name = name.strip()
                    st.rerun()

    if col2.button("🚪 参加", use_container_width=True):
        if not name.strip():
            st.error("名前を入力してください")
        elif code_input not in store["rooms"]:
            st.error("そのコードの部屋は見つかりません")
        else:
            with store["lock"]:
                store["rooms"][code_input]["members"].add(name.strip())
            st.session_state.room = code_input
            st.session_state.name = name.strip()
            st.rerun()

    st.stop()


# ---------- チャット画面 ----------
code = st.session_state.room
name = st.session_state.name
room = store["rooms"].get(code)

if room is None:
    st.warning("この部屋は存在しません(サーバーが再起動された可能性があります)")
    del st.session_state["room"]
    st.stop()

with st.sidebar:
    st.subheader("ミーティングコード")
    st.code(code, language=None)
    st.caption("このコードを相手に伝えてください")


    @st.fragment(run_every=2)
    def show_members():
        st.write("**参加者**")
        for m in sorted(room["members"]):
            st.write(("🟢 " if m == name else "👤 ") + m)


    show_members()

    if st.button("退出"):
        del st.session_state["room"]
        del st.session_state["name"]
        st.rerun()

st.title(f"💬 {code}")


@st.fragment(run_every=2)
def show_messages():
    others = room["members"] - {name}
    for msg in room["messages"]:
        is_me = msg["sender"] == name

        # 他人のメッセージを表示した時点で既読にする
        if not is_me:
            msg["read_by"].add(name)

        with st.chat_message("user" if is_me else "assistant"):
            st.markdown(f"**{msg['sender']}**  `{msg['time']}`")
            st.write(msg["text"])
            if is_me:
                if not others:
                    st.caption("相手の参加待ち")
                elif msg["read_by"]:
                    st.caption("✅ 既読: " + ", ".join(sorted(msg["read_by"])))
                else:
                    st.caption("未読")


show_messages()

if text := st.chat_input("メッセージを入力"):
    with store["lock"]:
        room["messages"].append(
            {
                "sender": name,
                "text": text,
                "time": datetime.now().strftime("%H:%M"),
                "read_by": set(),
            }
        )
    st.rerun()