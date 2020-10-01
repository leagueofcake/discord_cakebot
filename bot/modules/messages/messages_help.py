from bot.modules.HelpEntry import HelpEntry

_hello_desc = "cakebot says hello! Use to check if cakebot is online. "
_hello_usage = "!hello"

_redirect_desc = "Redirects a message to another channel."
_redirect_usage = "!redirect <channel mention> <message>"
_redirect_example = (
    "Redirects message to #alt: !redirect #alt Hi guys, from the main channel!"
)

_say_desc = "Makes cakebot talk!"
_say_usage = "!say <room> <message> - makes cakebot say a message in the specified room"

help_entries = {
    "hello": HelpEntry("!hello", _hello_desc, _hello_usage, "miscellaneous"),
    "redirect": HelpEntry(
        "!redirect", _redirect_desc, _redirect_usage, "general", _redirect_example
    ),
    "say": HelpEntry("!say", _say_desc, _say_usage, "miscellaneous"),
}
