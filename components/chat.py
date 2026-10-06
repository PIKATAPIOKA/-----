from datetime import datetime

import streamlit as st

from components.room import get_room


def send_message(room_code, sender, text):
    room = get_room(room_code)

    if room is None:
        return

    room["messages"].append(
        {
            "type": "text",
            "sender": sender,
            "text": text,
            "time": datetime.now().strftime("%H:%M"),
            "read_by": set(),
            # 絵文字ごとに「誰が押したか」を保存
            "reactions": {},
        }
    )


@st.fragment(run_every=2)
def show_messages(room_code, user_name):
    room = get_room(room_code)

    if room is None:
        return

    messages = room["messages"]

    if not messages:
        st.info("まだメッセージがありません。")
        return

    for index, msg in enumerate(messages):
        sender = msg["sender"]
        is_me = sender == user_name

        # 相手のメッセージを見たら既読にする
        if not is_me:
            msg["read_by"].add(user_name)

        with st.chat_message("user" if is_me else "assistant"):
            st.markdown(f"**{sender}**　`{msg['time']}`")

            # テキストメッセージ
            if msg["type"] == "text":
                st.write(msg["text"])

            # ファイルメッセージ
            elif msg["type"] == "file":
                show_file_message(msg)

            # リアクション
            show_reactions(msg, index, user_name)

            # 自分のメッセージなら既読表示
            if is_me:
                others = room["members"] - {user_name}

                if not others:
                    st.caption("相手の参加待ち")

                elif msg["read_by"]:
                    st.caption(
                        " 既読："
                        + ", ".join(sorted(msg["read_by"]))
                    )

                else:
                    st.caption("未読")


def show_file_message(msg):
    file_name = msg.get("file_name", "ファイル")
    file_data = msg.get("file_data")
    mime_type = msg.get(
        "mime_type",
        "application/octet-stream",
    )

    if not file_data:
        st.warning("ファイルデータがありません。")
        return

    # 画像なら表示
    if mime_type.startswith("image/"):
        st.image(
            file_data,
            caption=file_name,
        )

    # ダウンロード
    st.download_button(
        "📥 ダウンロード",
        data=file_data,
        file_name=file_name,
        mime=mime_type,
        key=f"download_{id(msg)}",
    )


def show_reactions(msg, index, user_name):
    emojis = [
        "( ¯꒳¯ )ｂ",
        "♡(˘︶˘).｡.:*♡",
        "ꉂꉂ(˃ᗜ˂*)ｱﾊﾊ",
        "(lll-ω-)",
        "(ꐦ°᷄д°᷅)",
        "(๑•̀ㅂ•́)و✧",
    ]

    # reactionsの形式
    #
    # {
    #     "👍": {"Kan", "Taro"},
    #     "❤️": {"Kan"}
    # }
    #
    # 「誰が押したか」を保存することで、
    # 1人1個までにできる。

    reactions = msg.setdefault("reactions", {})

    cols = st.columns(len(emojis))

    for col, emoji in zip(cols, emojis):

        # このリアクションを押した人
        users = reactions.setdefault(emoji, set())

        # 自分が押しているか
        reacted = user_name in users

        # 現在の人数
        count = len(users)

        # ボタン表示
        if reacted:
            button_text = f"☑️ {emoji} {count}"
        else:
            button_text = f"{emoji} {count if count else ''}"

        if col.button(
            button_text,
            key=f"reaction_{index}_{emoji}_{user_name}",
        ):

            # すでに押している → 取り消す
            if reacted:
                users.remove(user_name)

            # まだ押していない → 追加
            else:
                users.add(user_name)

            st.rerun()