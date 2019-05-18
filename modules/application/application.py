import tkinter as tk
from modules.adt import Calendar, Event



class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("430x400")
        self.main_menu = MainMenu(self.master, self)
        self.frame = ScrolledFrame(self.master)
        self.frame.pack(expand=True, fill='both')
        self.events = []
        self.calendar = Calendar().create_from_file('ical_2020.php')
        self.update_events()

    def update_events(self):
        for event_widget in self.events:
            if event_widget.removed:
                self.calendar.remove_event(event_widget.event)
            event_widget.pack_forget()
            event_widget.destroy()
        for event in self.calendar:
            self.events.append(EventWidget(self.frame, event))


class EventWidget(tk.Frame):
    BG = '#ffe7dc'
    BG_REMOVED='#ceceb6'

    def __init__(self, master, event_obj=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.base = tk.Frame(self, width=400, height=100, bg=self.BG,
                             relief='groove', bd=2)
        self.config(bd=0, bg='red')
        self.pack(fill='x', expand=True, anchor='w')
        self.base.pack_propagate(0)
        self.base.pack(fill='x', expand=True)
        if event_obj:
            self.event = event_obj
            self.text = self.event.event_type
            self.date = self.event.start_time
        self.text_label = tk.Label(self.base, text=self.text, bg = self.BG,
                                   font='arial 15')
        self.text_label.pack(side='left', anchor='nw')
        self.date_label = tk.Label(self.base, text=self.date, bg=self.BG)
        self.date_label.pack(side='top', anchor='nw')
        self.base.bind('<Button>', self.on_click)
        self.remove_button = tk.Button(self.base, text='Remove', bg=self.BG)
        self.remove_button.pack(side='right')
        self.remove_button.bind('<Button>', self.on_remove)
        self.removed = False


    def on_click(self, event=None):
        EventWindow(self.event)


    def on_remove(self, event):
        if not self.removed:
            self.removed = True
            self.base.config(bg=self.BG_REMOVED)
            self.text_label.config(bg=self.BG_REMOVED)
            self.date_label.config(bg=self.BG_REMOVED)
            self.remove_button.config(text='Cancel', bg=self.BG_REMOVED)
        else:
            self.removed = False
            self.base.config(bg=self.BG)
            self.text_label.config(bg=self.BG)
            self.date_label.config(bg=self.BG)
            self.remove_button.config(text='Remove', bg=self.BG)

class MainMenu:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.main_menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.master.quit)
        self.help_menu.add_command(label='Help Index', command=HelpIndex)
        self.help_menu.add_command(label='About...', command=About)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Help', menu=self.help_menu)
        self.main_menu.add_command(label='Refresh events',
                                   command=self.app.update_events)
        self.master.configure(menu=self.main_menu)

class EventWindow:
    def __init__(self, event):
        self.master = tk.Toplevel()
        self.master.title('About event')
        self.frame = tk.Frame(self.master, bg='white')
        title = tk.Label(self.frame, text=event.event_type, font='Arial 14', bg='white')
        text = tk.Text(self.frame, height=3, width='50', font='Arial 12', relief='flat', bg='white')
        text.insert('end', event.description+'\n')
        text.insert('end', event.url)
        title.pack(side='top',fill='x', expand=True)
        text.pack(side='top', fill='x', expand=True)
        tk.Button(self.frame, width=5, height=1, text='Close', command=self.master.destroy).pack(side='right', padx=20)
        self.frame.pack(fill='both', expand=True)



class HelpIndex:
    def __init__(self, master=None):
        self.master = tk.Toplevel(master)
        self.master.title('Help')
        self.master.geometry('400x500')
        self.frame = ScrolledFrame(self.master)
        text = tk.Message(self.frame, text='Some useful text. '*1000)
        text.pack(side='left', expand=True)
        self.frame.pack(fill='both', expand=True)

class About:
    def __init__(self, master=None):
        self.master = tk.Toplevel(master)
        self.master.title('About')
        self.master.geometry('400x500')
        self.frame = ScrolledFrame(self.master)
        text = tk.Message(self.frame, text='Text about the program. '*1000)
        text.pack(side='left', expand=True)
        self.frame.pack(fill='both', expand=True)


class ScrolledFrame:
    """
    A frame with the scrollbar attached to the right side.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.top_frame = tk.Frame(master, **kwargs)
        self.scroll = tk.Scrollbar(self.top_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self.top_frame, width=width, height=height,
                                bg=bg, yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.canvas.yview)
        self.scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame = tk.Frame(self.canvas, bg=bg)
        self.canvas.create_window(4, 4, window=self.main_frame, anchor='nw')
        self.main_frame.bind("<Configure>", self._reconf)
        self.top_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        """
        Some attributes like width refer to the top-level frame while others
        refer to the main frame
        """
        if item in self.top_attr:
            return getattr(self.top_frame, item)
        else:
            return getattr(self.main_frame, item)

    def _reconf(self, event=None):
        """
        Helper function to keep canvas size constant
        """
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion=(0, 0, x2, max(y2, height)))


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()