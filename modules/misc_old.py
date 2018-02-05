import cakebot_config
from .helpers import is_integer

# Used for !timedcats. May be extended for use with other commands in the future.
# Returns a tuple (times, duration_str)
def parse_duration_str(args):
    # Defaults to 5 m if no duration string is given
    times = 5
    duration_str = 'm'

    if len(args) > 1:
        arg_times = args[1]
        if is_integer(arg_times):
            if int(arg_times) <= 60:
                times = int(arg_times)

        if len(args) > 2:
            arg_duration = args[2]
            if arg_duration in cakebot_config.time_map:
                duration_str = arg_duration
    return times, duration_str
