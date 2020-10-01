from bot.modules.HelpEntry import HelpEntry

_perms_desc = "Gets or sets the cakebot permissions for a given user."
_perms_usage = (
    "NOTE: This does NOT set server permissions but only permissions for cakebot commands.\n"
    "Permissions are required for:\n"
    "!musicprefix (set)\n"
    "!permissions (set)\n"
    "!logchannel (set)\n\n"
    "!permissions - displays your current cakebot permissions\n"
    "!permissions <user mention> - displays current cakebot permissions for the mentioned user.\n"
    "!permissions <user mention> <command|commands> - add permissions to the given user. Requires "
    "manage_guild permission."
)
_perms_example = (
    "Give Clyde musicprefix permissions: !permissions @Clyde#1234 musicprefix\n"
    "Give Clyde musicprefix and logchannel permissions: !permissions @Clyde#1234 musicprefix logchannel"
)

help_entries = {
    "permissions": HelpEntry(
        "!permissions", _perms_desc, _perms_usage, "permissions", _perms_example
    ),
}
