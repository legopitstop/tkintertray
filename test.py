import pystray
from PIL import Image
import os

PATH = os.path.dirname(os.path.realpath(__file__))

image = Image.open(os.path.join(PATH, 'icon.png'))


def on_clicked(icon, item):
    if str(item) == 'Hello':
        print('Hellpo world')
    elif str(item) == 'Exit':
        icon.stop()

menu2 = pystray.Menu(
    pystray.MenuItem('Hello', on_clicked)
)

menu = pystray.Menu(
    pystray.MenuItem('Hello', on_clicked),
    pystray.MenuItem('More', menu2),
    pystray.MenuItem('Exit', on_clicked)
)


icon = pystray.Icon("Test", image, menu=menu)
icon.title = 'Worked'
# name
# icon
# title
# menu
# visible

# notify(messgae, title)
icon.run()