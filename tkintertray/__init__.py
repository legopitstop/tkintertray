import pystray
import threading
import tkinter
from PIL import Image, ImageFile

def _convert_menu(menu:tkinter.Menu):
    """Converts the list of menus to pystray.MenuItem"""
    def set_state():
        def inner(icon, item):
            print('set', icon, item)
            return True
        return inner

    def get_state():
        def inner(item):
            print('get', item)
            return True
        return inner

    def callback(icon:pystray.Icon, item:pystray.MenuItem):
        # Handle the callback from the pytray.MenuItem
        index = cmds.get(str(item))
        if index: menu.invoke(index)

    menus = []
    last = menu.index('end')
    cmds = {}
    for i in range(1, last+1):
        match menu.type(i):
            case 'cascade': 
                label = menu.entrycget(i, 'label')
                state = menu.entrycget(i, 'state')
                enabled = True
                if state=='disabled': enabled = False
                _menu = menu.winfo_children()
                if len(_menu) >= 0:
                    action = _convert_menu(_menu[0])
                    item = pystray.MenuItem(text=label, action=action, enabled=enabled)
                    menus.append(item)

            case 'command':
                label = menu.entrycget(i, 'label')
                state = menu.entrycget(i, 'state')
                enabled = True
                if state=='disabled': enabled = False
                cmds[str(label)] = i
                item = pystray.MenuItem(text=label, action=callback, enabled=enabled)
                menus.append(item)

            case 'checkbutton':
                state = False
                label = menu.entrycget(i, 'label')
                state = menu.entrycget(i, 'state')
                enabled = True
                if state=='disabled': enabled = False
                item = pystray.MenuItem(text=label, action=set_state(), checked=get_state(), enabled=enabled)
                menus.append(item)
                
            case 'radiobutton':
                state = False
                label = menu.entrycget(i, 'label')
                state = menu.entrycget(i, 'state')
                enabled = True
                if state=='disabled': enabled = False

                item = pystray.MenuItem(text=label, action=set_state(), checked=get_state(), radio=True, enabled=enabled)
                menus.append(item)


            case _:
                print(f'Unknown tkinter.Menu type "{menu.type(i)}"')

    return pystray.Menu(*menus)

class Tray():
    def __init__(self, master=None, image=None, menu=None):
        self._tray = pystray.Icon('.!tray')

        if master == None:  master = tkinter._get_default_root()
        self.wm_title(master.title())
        self.image = None
        self.menu = None

        self.configure(
            image=image,
            menu=menu
        )

    @property
    def title(self):
        return self._tray.title
    
    def wm_title(self, string:str):
        self._tray.title = str(string)
    title=wm_title

    @property
    def image(self):
        return self._tray.icon
    
    @image.setter
    def image(self, value:ImageFile.ImageFile):
        if value==None: self.image = Image.open('icon.png')
        elif isinstance(value, ImageFile.ImageFile): self._tray.icon = value
        else: raise TypeError(f'Expected PIL.ImageFile.ImageFile but got {value.__class__.__name__} instead.')
        
    @property
    def menu(self):
        return self._tray.menu
    
    @menu.setter
    def menu(self, value:tkinter.Menu):
        if value==None: pass
        elif isinstance(value, tkinter.Menu): self._tray.menu = _convert_menu(value)
        else: raise TypeError(f'Expected tkinter.Menu but got {value.__class__.__name__} instead.')

    def configure(self, **kw):
        if 'text' in kw and kw['text']!=None: self.text = kw.pop('text')
        if 'image' in kw and kw['image']!=None: self.image = kw.pop('image')
        if 'menu' in kw and kw['menu']!=None: self.menu = kw.pop('menu')
        return self

    def run(self):
        thread = threading.Thread(target=self._tray.run)
        thread.start()
        return self
    
    def destory(self):
        self._tray.stop()

    def notify(self, message:str, title:str=None):
        self._tray.notify(message, title)

class TrayToplevel():
    def __init__(self):
        pass