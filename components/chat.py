from datetime import datetime

import streamlit as st

from components.room import get_room


# ============================================================
# メッセージ送信
# ============================================================

def send_message(
    room_code,
    sender,
    text,
):

    room = get_room(room_code)

    if room is None:

        return

    room["messages"].append(

        {

            "type": "text",

            "sender": sender,

            "text": text,

            "time": datetime.now().strftime(
                "%H:%M"
            ),

            "read_by": set(),

            "reactions": {},

        }

    )


# ============================================================
# メッセージ表示
# ============================================================

@st.fragment(run_every=2)
def show_messages(
    room_code,
    user_name,
):

    room = get_room(room_code)

    if room is None:

        return

    messages = room["messages"]

    if not messages:

        st.info(
            "まだメッセージがありません。"
        )

        return

    for index, msg in enumerate(messages):

        sender = msg["sender"]

        is_me = sender == user_name

        # ----------------------------------------------------
        # 既読
        # ----------------------------------------------------

        if not is_me:

            msg["read_by"].add(
                user_name
            )

        # ----------------------------------------------------
        # チャット表示
        # ----------------------------------------------------

        with st.chat_message(
            "user" if is_me else "assistant"
        ):

            st.markdown(
                f"**{sender}**　`{msg['time']}`"
            )

            if msg["type"] == "text":

                st.write(
                    msg["text"]
                )

            elif msg["type"] == "file":

                show_file_message(
                    msg
                )

            # ------------------------------------------------
            # 既読
            # ------------------------------------------------

            if is_me:

                others = (
                    room["members"]
                    - {user_name}
                )

                if not others:

                    st.caption(
                        "相手の参加待ち"
                    )

                elif msg["read_by"]:

                    st.caption(
                        "✅ 既読："
                        + ", ".join(
                            sorted(
                                msg["read_by"]
                            )
                        )
                    )

                else:

                    st.caption(
                        "未読"
                    )

            # ------------------------------------------------
            # リアクション
            # ------------------------------------------------

            show_reactions(
                msg,
                index,
            )


# ============================================================
# ファイルメッセージ
# ============================================================

def show_file_message(msg):

    file_name = msg.get(
        "file_name",
        "ファイル",
    )

    file_data = msg.get(
        "file_data"
    )

    mime_type = msg.get(
        "mime_type",
        "application/octet-stream",
    )

    if not file_data:

        st.warning(
            "ファイルデータがありません。"
        )

        return

    if mime_type.startswith(
        "image/"
    ):

        st.image(
            file_data,
            caption=file_name,
        )

    st.download_button(
        "📥 ダウンロード",
        data=file_data,
        file_name=file_name,
        mime=mime_type,
        key=f"download_{id(msg)}",
    )


# ============================================================
# リアクション
# ============================================================

def show_reactions(
    msg,
    index,
):

    emojis = [
        "👍",
        "❤️",
        "😂",
        "😮",
        "😢",
        "🎉",
    ]

    cols = st.columns(
        len(emojis)
    )

    for col, emoji in zip(
        cols,
        emojis,
    ):

        count = msg[
            "reactions"
        ].get(
            emoji,
            0,
        )

        if col.button(
            f"{emoji} {count if count else ''}",
            key=f"reaction_{index}_{emoji}",
        ):

            msg[
                "reactions"
            ][emoji] = count + 1

            st.rerun()