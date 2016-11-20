def parse_command_args(command):
    return command.split(' ')

def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False