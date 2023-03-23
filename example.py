from tkintertray import Tray
from PIL import Image
import tkinter

root = tkinter.Tk()

tray = Tray(root, image=Image.open('icon.png'))
tray.title('Tkinter Tray')

def callback1(): print('callback 1')
def callback2(): print('callback 2')

menu = tkinter.Menu(root)
menu2 = tkinter.Menu(menu)
menu2.add_command(label='command 1', command=callback1)
menu2.add_command(label='command 2', command=callback2)
menu2.add_checkbutton(label='checkbutton')
# menu2.add_radiobutton(label='radiobutton')

menu.add_cascade(label='Submenu', menu=menu2)
menu.add_command(label='Exit', command=root.destroy)

tray.configure(menu=menu)

tray.run()


root.mainloop()
tray.destory() # End loop