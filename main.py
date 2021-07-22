import settings

import logging
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon import functions, types
from telethon.utils import pack_bot_file_id

download_root = '/home/bpqvg/Desktop/BoxThread/Media/'

logging.basicConfig(level=logging.INFO)

api_id = settings.tg_sec['api_id']
api_hash = settings.tg_sec['api_hash']
client = TelegramClient('tgparse', api_id, api_hash)

async def Main():
    channels_ids = settings.channels
    
    for channel_id in channels_ids:
        channel_entity = await client.get_entity(PeerChannel(channel_id))
        dialog = await client(functions.messages.GetPeerDialogsRequest(
            peers=[channel_id]
        ))
        dialog = dialog.dialogs[0]
        unread_messages = []
        count=1
        async for message in client.iter_messages(channel_id):
            if count > dialog.unread_count:
                break
            unread_messages.append(message)
            count+=1
        if len(unread_messages) > 0: # Is unread messages
            for msg in unread_messages[::-1]:
                if not msg.media == None:
                    try:
                        if msg.media.photo:
                            filename = f"{download_root}%s.jpg" % datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                            path = await msg.download_media(filename)
                            logging.info(f'[DOWNLOAD] image from {channel_entity.username} to ' + path)
                    except:
                        path = await msg.download_media(filename)
                        logging.info(f'[DOWNLOAD] image from {channel_entity.username} to ' + path)
                await msg.mark_read()
        

with client:
    client.loop.run_until_complete(Main())