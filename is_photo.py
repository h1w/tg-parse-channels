from PIL import Image
import os
import mimetypes

root = input('Type absolute path to photos directory: ')
remove_list = []

def check_image_with_pil(path):
    try:
        img = Image.open(path)
        img.close()
    except:
        return False
    return True

# Check with mimetype if file is image/jpeg
def mimetype_check():
    for filename in os.listdir(root):
        file_abspath = os.path.join(root, filename)
        if mimetypes.guess_type(file_abspath)[0] != 'image/jpeg':
            remove_list.append(file_abspath)

# Pillow Check
def pillow_check():
    for filename in os.listdir(root):
        file_abspath = os.path.join(root, filename)
        check = check_image_with_pil(file_abspath)
        if check is False:
            remove_list.append(file_abspath)

# Remove error images
def remove_from_list():
    for file_abspath in remove_list:
        os.remove(file_abspath)

mimetype_check()
pillow_check()

print(len(remove_list), "files to remove:\n", *remove_list)
confirm = input('type YES for delete: ')
if confirm == 'YES':
    remove_from_list()
else:
    print("Exit without removing files")
    quit()