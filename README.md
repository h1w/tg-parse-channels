# Parse Telegram Channels
_Script to download media from telegram channels._

### Run script
Before run, set Telegram credentials and Parser settings in file `settings.py`.

Create virtual environment
```
python3 -m venv venv
```

Enter to `venv`
```
. venv/bin/activate
```

Install python modules from requirements.txt
```
pip install -r requirements.txt
```

Start script
```
python3 main.py
```

### Check images for integrity and correctness
Example
```
python3 is_photo.py

Type absolute path to photos directory: <input absolute path to photos directory>

<count> files to remove:
<list of files>

type YES for delete: <type YES or something for keep files>
```
