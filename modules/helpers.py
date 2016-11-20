def parse_command_args(command):
    return command.split(' ')


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


def find_permissions(perms, word):
    if perms:
        for perm in perms:
            if word == perm:
                return True
    return False