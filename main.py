import settings

import logging
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon import functions, types
from telethon.utils import pack_bot_file_id

download_root = settings.download_root

logging.basicConfig(level=logging.INFO)

api_id = settings.tg_sec['api_id']
api_hash = settings.tg_sec['api_hash']
client = TelegramClient('tgparse', api_id, api_hash)


# Printing download progress
def progress_callback(current, total):
    print('Downloaded progress', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))

async def ParseOnlyUnread():
    channels_ids = settings.channels_unread_only
    channels_count = 1
    channels_total = len(channels_ids)

    for channel_id in channels_ids:
        channel_entity = await client.get_entity(PeerChannel(channel_id))
        
        dialog = await client(functions.messages.GetPeerDialogsRequest(
            peers=[channel_id]
        ))
        dialog = dialog.dialogs[0]
        
        unread_messages = []
        count=1
        
        logging.info(f'One moment. Counting messages in the {channel_entity.title} channel')
        async for message in client.iter_messages(channel_id):
            if count > dialog.unread_count:
                break
            unread_messages.append(message)
            count+=1
        
        if len(unread_messages) == 0:
            logging.info(f'No read messages in {channel_entity.title} channel')
        elif len(unread_messages) > 0: # Is unread messages
            m_readed_count = 1
            m_total = len(unread_messages)
            
            for msg in unread_messages[::-1]:
                if not msg.media == None:
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                    filename = '{}{}'.format(download_root, timestamp)
                    path = None
                    
                    if getattr(msg.media, 'photo', None):
                        path = await msg.download_media(filename, progress_callback=progress_callback, thumb=-1)
                    
                    elif getattr(msg.media, 'document', None) and settings.parser['only_photo'] == False: # if only_photo is True, will download only photo, not documents(video, gifs, files)
                        path = await msg.download_media(download_root+timestamp, progress_callback=progress_callback)
                    
                    # Log download event
                    if not path == None:
                        logging.info(f'[Channels: {channels_count}/{channels_total}] [Progress: {m_readed_count}/{m_total}] [DOWNLOAD] media from {channel_entity.title} to ' + path)
                
                await msg.mark_read()

                m_readed_count+=1

        channels_count+=1

async def ParseAll():
    channels_ids = settings.channels_all
    channels_count = 1
    channels_total = len(channels_ids)
    
    for channel_id in channels_ids:
        channel_entity = await client.get_entity(PeerChannel(channel_id))
        
        dialog = await client(functions.messages.GetPeerDialogsRequest(
            peers=[channel_id]
        ))
        dialog = dialog.dialogs[0]
        
        m_readed_count = 1
        m_total = 0
        
        logging.info(f'One moment. Counting messages in the {channel_entity.title} channel')
        async for msg in client.iter_messages(channel_id):
            m_total+=1
        
        async for msg in client.iter_messages(channel_id):
            if not msg.media == None:
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                filename = '{}{}'.format(download_root, timestamp)
                path = None
                
                if getattr(msg.media, 'photo', None):
                    path = await msg.download_media(filename, progress_callback=progress_callback, thumb=-1)
                
                elif getattr(msg.media, 'document', None) and settings.parser['only_photo'] == False: # if only_photo is True, will download only photo, not documents(video, gifs, files)
                    path = await msg.download_media(download_root+timestamp, progress_callback=progress_callback)
                
                # Log download event
                if not path == None:
                    logging.info(f'[Channels: {channels_count}/{channels_total}] [Progress: {m_readed_count}/{m_total}] [DOWNLOAD] media from {channel_entity.title} to ' + path)
            
            await msg.mark_read()

            m_readed_count+=1

        channels_count+=1

async def Main():
    if settings.parser['only_unread'] == True:
        await ParseOnlyUnread()
    else:
        await ParseAll()

with client:
    client.loop.run_until_complete(Main())