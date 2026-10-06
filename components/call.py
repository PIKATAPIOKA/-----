import streamlit as st

try:

    from streamlit_webrtc import (
        webrtc_streamer,
        WebRtcMode,
    )

    WEBRTC_AVAILABLE = True

except ImportError:

    WEBRTC_AVAILABLE = False


def show_call(
    room_code,
    user_name,
):

    st.subheader("📹 ビデオ通話")

    st.write(
        f"参加者：{user_name}"
    )

    if not WEBRTC_AVAILABLE:

        st.error(
            "streamlit-webrtc がインストールされていません。"
        )

        st.code(
            "pip install streamlit-webrtc av"
        )

        return

    st.info(
        "カメラ・マイクの使用許可を求められたら許可してください。"
    )

    # --------------------------------------------------------
    # 通話
    # --------------------------------------------------------

    webrtc_streamer(

        key=f"meeting-{room_code}",

        mode=WebRtcMode.SENDRECV,

        media_stream_constraints={

            "video": True,

            "audio": True,

        },

        async_processing=True,

    )

    st.divider()

    st.caption(
        "カメラやマイクのON/OFFは、"
        "ブラウザ側の通話コントロールから操作できます。"
    )

    st.warning(
        "現在の通話機能はWebRTCの基本機能です。"
        "Zoomのような複数人通話・画面共有を完全に実現するには、"
        "別途シグナリングサーバーやTURNサーバーが必要です。"
    )