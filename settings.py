# Settings file.
tg_sec = {
    'api_id': <api_id>,
    'api_hash': '<api_hash>'
}

parser = {
    'only_photo': True, # If "True", the script will download ONLY photos from channels
    'only_unread': True # If "True", the script will by download ONLY UNREAD messages from channels
}

download_root = '<absolute path to download root(directory)>'

# Set list of channels for unread only parse method. See parser['only_unread'] mast be "True"
channels_unread_only = [
    <channel-id-1>,
    <channel-id-2>,
    <channel-id-3>,
    <channel-id-4>,
    <...>
]

# Set list of channels for parse not only unread method. See parser['only_unread'] mast be "False"
channels_all = [
    <channel-id-1>,
    <channel-id-2>,
    <channel-id-3>,
    <channel-id-4>,
    <...>
]
