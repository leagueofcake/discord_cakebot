from discord.abc import User


def is_integer(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False


# Returns a string in the form username#descriptor e.g. Clyde#1234
def get_full_username(user: User) -> str:
    return "{}#{}".format(user.name, user.discriminator)
