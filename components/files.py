from datetime import datetime

from components.room import get_room


def save_uploaded_file(
    room_code,
    sender,
    uploaded_file,
):

    room = get_room(
        room_code
    )

    if room is None:

        return False

    file_bytes = uploaded_file.read()

    message = {

        "type": "file",

        "sender": sender,

        "text": "",

        "time": datetime.now().strftime(
            "%H:%M"
        ),

        "read_by": set(),

        "reactions": {},

        "file_name": uploaded_file.name,

        "file_data": file_bytes,

        "mime_type": uploaded_file.type
        or "application/octet-stream",

    }

    room[
        "messages"
    ].append(
        message
    )

    return True