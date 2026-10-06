import streamlit as st

from components.room import create_room, join_room, leave_room, get_room
from components.chat import send_message, show_messages
from components.reactions import add_reaction
from components.files import save_uploaded_file
from components.call import show_call


st.set_page_config(
    page_title="連絡ツール",
    page_icon="💬",
    layout="wide",
)


# ============================================================
# 初期化
# ============================================================

if "room" not in st.session_state:
    st.session_state.room = None

if "name" not in st.session_state:
    st.session_state.name = None


# ============================================================
# ログイン・部屋作成画面
# ============================================================

if st.session_state.room is None:

    st.title("💬 連絡ツール")

    st.write(
        "ミーティングコードを使って部屋を作成・参加できます。"
    )

    name = st.text_input(
        "名前",
        placeholder="例：Kan",
    )

    code = st.text_input(
        "ミーティングコード",
        placeholder="作成するときは空欄でOK",
    ).strip().upper()

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 部屋作成
    # --------------------------------------------------------

    with col1:
        if st.button(
            "➕ 部屋を作成",
            use_container_width=True,
        ):

            if not name.strip():

                st.error("名前を入力してください。")

            else:

                new_code = create_room(
                    code=code,
                    name=name.strip(),
                )

                if new_code is None:

                    st.error(
                        "そのミーティングコードはすでに使われています。"
                    )

                else:

                    st.session_state.room = new_code
                    st.session_state.name = name.strip()

                    st.rerun()

    # --------------------------------------------------------
    # 部屋参加
    # --------------------------------------------------------

    with col2:

        if st.button(
            "🚪 部屋に参加",
            use_container_width=True,
        ):

            if not name.strip():

                st.error("名前を入力してください。")

            elif not code:

                st.error("ミーティングコードを入力してください。")

            elif join_room(
                code=code,
                name=name.strip(),
            ):

                st.session_state.room = code
                st.session_state.name = name.strip()

                st.rerun()

            else:

                st.error(
                    "そのミーティングコードの部屋がありません。"
                )

    st.stop()


# ============================================================
# 部屋情報
# ============================================================

room_code = st.session_state.room
user_name = st.session_state.name

room = get_room(room_code)


if room is None:

    st.error(
        "部屋が見つかりません。"
        "サーバーが再起動された可能性があります。"
    )

    st.session_state.room = None
    st.session_state.name = None

    st.rerun()


# ============================================================
# サイドバー
# ============================================================

with st.sidebar:

    st.title("💬 連絡ツール")

    st.subheader("ミーティングコード")

    st.code(
        room_code,
        language=None,
    )

    st.caption(
        "このコードを相手に伝えてください。"
    )

    st.divider()

    st.subheader("👥 参加者")

    for member in sorted(room["members"]):

        if member == user_name:

            st.write(
                f"🟢 {member}（あなた）"
            )

        else:

            st.write(
                f"🟢 {member}"
            )

    st.divider()

    if st.button(
        "🚪 退出",
        use_container_width=True,
    ):

        leave_room(
            room_code,
            user_name,
        )

        st.session_state.room = None
        st.session_state.name = None

        st.rerun()


# ============================================================
# メイン画面
# ============================================================

st.title(
    f"💬 ミーティング {room_code}"
)

st.caption(
    f"ログイン中：{user_name}"
)


# ============================================================
# タブ
# ============================================================

chat_tab, call_tab = st.tabs(
    [
        "💬 チャット",
        "📹 通話",
    ]
)


# ============================================================
# チャット
# ============================================================

with chat_tab:

    show_messages(
        room_code,
        user_name,
    )

    st.divider()

    # --------------------------------------------------------
    # ファイル
    # --------------------------------------------------------

    uploaded_file = st.file_uploader(
        "📎 ファイル・画像を送信",
        type=[
            "png",
            "jpg",
            "jpeg",
            "gif",
            "webp",
            "pdf",
            "txt",
            "zip",
            "csv",
        ],
    )

    if uploaded_file is not None:

        if st.button("📤 ファイルを送信"):

            save_uploaded_file(
                room_code,
                user_name,
                uploaded_file,
            )

            st.success(
                "ファイルを送信しました。"
            )

            st.rerun()

    # --------------------------------------------------------
    # メッセージ
    # --------------------------------------------------------

    message = st.chat_input(
        "メッセージを入力..."
    )

    if message:

        send_message(
            room_code,
            user_name,
            message,
        )

        st.rerun()


# ============================================================
# 通話
# ============================================================

with call_tab:

    show_call(
        room_code,
        user_name,
    )