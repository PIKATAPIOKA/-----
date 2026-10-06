import random
import string
import threading
import streamlit as st


# ============================================================
# 全体データ
# ============================================================

@st.cache_resource
def get_store():

    return {
        "rooms": {},
        "lock": threading.Lock(),
    }


store = get_store()


# ============================================================
# ミーティングコード生成
# ============================================================

def make_code(length=6):

    chars = string.ascii_uppercase + string.digits

    while True:

        code = "".join(
            random.choices(
                chars,
                k=length,
            )
        )

        if code not in store["rooms"]:

            return code


# ============================================================
# 部屋作成
# ============================================================

def create_room(
    code=None,
    name=None,
):

    with store["lock"]:

        code = code or make_code()

        if code in store["rooms"]:

            return None

        store["rooms"][code] = {

            "members": {
                name
            },

            "messages": [],

        }

        return code


# ============================================================
# 部屋参加
# ============================================================

def join_room(
    code,
    name,
):

    with store["lock"]:

        if code not in store["rooms"]:

            return False

        store["rooms"][code]["members"].add(
            name
        )

        return True


# ============================================================
# 部屋取得
# ============================================================

def get_room(code):

    return store["rooms"].get(code)


# ============================================================
# 部屋退出
# ============================================================

def leave_room(
    code,
    name,
):

    with store["lock"]:

        room = store["rooms"].get(code)

        if room is None:

            return

        room["members"].discard(
            name
        )

        # 誰もいなくなったら削除
        if not room["members"]:

            del store["rooms"][code]