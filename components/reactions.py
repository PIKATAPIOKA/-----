from components.room import get_room


REACTIONS = [
    "👍",
    "❤️",
    "😂",
    "😮",
    "😢",
    "🎉",
]


def add_reaction(
    room_code,
    message_index,
    emoji,
):

    if emoji not in REACTIONS:

        return False

    room = get_room(
        room_code
    )

    if room is None:

        return False

    messages = room[
        "messages"
    ]

    if (
        message_index < 0
        or message_index >= len(messages)
    ):

        return False

    message = messages[
        message_index
    ]

    reactions = message[
        "reactions"
    ]

    reactions[emoji] = (
        reactions.get(
            emoji,
            0,
        )
        + 1
    )

    return True