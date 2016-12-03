#!/usr/bin/env python3.5
from cakebot_help import help_dict
with open('README.md', 'w') as f:
    sorted_keys = sorted(help_dict)
    f.write("# discord_cakebot\n")
    f.write("General-purpose bot for discord.\n\n")
    f.write("## Command List\n")
    for command in sorted_keys:
        f.write(help_dict[command].get_markdown())