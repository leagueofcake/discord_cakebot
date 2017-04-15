from datetime import datetime
from .helpers import get_full_username, temp_message


def get_log_channel_id(c, server_id):
    c.execute("SELECT channel_id FROM log_channel WHERE server_id = ?", (server_id, ))
    res = c.fetchone()
    if res:
        return res[0]
    return None


def add_log_channel(c, server_id, channel_id):
    c.execute("INSERT INTO log_channel(server_id, channel_id) VALUES (?, ?)", (server_id, channel_id))


def update_log_channel(c, server_id, channel_id):
    c.execute("UPDATE log_channel SET channel_id = ? WHERE server_id = ?", (channel_id, server_id))


def gen_edit_message_log(before, after):
    before_content = before.clean_content
    after_content = after.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")

    if before.attachments:
        before_content += ' ' + before.attachments[0]['proxy_url']
    if after.attachments:
        after_content += ' ' + after.attachments[0]['proxy_url']

    log_message = '[{}] {} *edited their message in* {}\n' \
                  'Before: {}\n' \
                  'After+: {}'.format(local_message_time, get_full_username(before.author), before.channel.mention,
                                      before_content, after_content)
    return log_message


def gen_delete_message_log(message):
    clean_content = message.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")
    username = get_full_username(message.author)

    if message.attachments:
        clean_content += ' ' + message.attachments[0]['proxy_url']

    return '[{}] {} *deleted their message in* {}\n' \
           '{}'.format(local_message_time, username, message.channel.mention, clean_content)

async def purge_messages(message, client, purge_user, num):
    if 1 <= num <= 100:
        to_delete = []
        async for log in client.logs_from(message.channel, limit=500):
            if log.author.id == purge_user.id:
                to_delete.append(log)
            if len(to_delete) == num:  # Found num amount of messages
                break

        if len(to_delete) == 1:
            await client.delete_message(to_delete[0])
        else:
            await client.delete_messages(to_delete)
        await temp_message(client, message.channel,
                           "Purged {} messages from {}.".format(len(to_delete),
                                                                purge_user))
    else:
        await temp_message(client, message.channel, "Please specify a valid number of messages to purge. (1-100)")

async def auto_rename_voice_channel(client, before, after):
    if before.server.id in ("139345703800406016", "178312027041824768"):  # Only use on main/dev server
        default_list = ["Gaming Channel 1", "Gaming Channel 2", "Gaming Channel 3", "Music Channel"]

        if after.voice_channel:
            game_count = {}
            voice_members = after.voice_channel.voice_members

            for member in voice_members:
                if member.game:
                    if member.game.name not in game_count:
                        game_count[member.game.name] = 1
                    else:
                        game_count[member.game.name] += 1
            if game_count:
                new_channel_names = [key for m in [max(game_count.values())] for key,val in game_count.items() if val == m]
                for new_channel_name in new_channel_names:
                    if new_channel_name:  # Non-blank new channel name
                        await client.edit_channel(after.voice_channel, name=new_channel_name)
            else:
                default_name = default_list[after.voice_channel.position]
                await client.edit_channel(after.voice_channel, name=default_name)

            if before.voice_channel:
                if len(before.voice_channel.voice_members) == 0:  # No more members, reset to default name
                    default_name = default_list[before.voice_channel.position]
                    await client.edit_channel(before.voice_channel, name=default_name)

        # If voice channel being left has no more members, reset to default name
        if before.voice_channel:
            if len(before.voice_channel.voice_members) == 0:
                default_name = default_list[before.voice_channel.position]
                await client.edit_channel(before.voice_channel, name=default_name)