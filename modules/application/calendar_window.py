from modules.adt import Calendar
from modules.application import *


class CalendarWindow:
    def __init__(self, master, app=None, filename=None):
        self.app = app
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(expand=True, side='left', fill='both')
        self.frame = ScrolledFrame(self.top_frame)
        self.frame.pack(expand=True, side='left', fill='both')
        self.events = []
        self.filename = filename
        self.calendar = Calendar()
        if self.filename:
            self.calendar.add_from_file(filename)
        self.update_events()

    def update_events(self):
        for event_widget in self.events:
            if event_widget.removed:
                self.calendar.remove_event(event_widget.event)
            event_widget.pack_forget()
            event_widget.destroy()
        for event in self.calendar:
            self.events.append(EventWidget(self.frame, event, self))

    def load(self):
        pass

    def save(self):
        filename = filedialog.asksaveasfilename(title='Save as...',
                                                defaultextension=".cal",
                                                filetypes=[('Calendar files',
                                                           '*.cal'),
                                                           ('All files',
                                                            '*.*')])
        if filename:
            self.calendar.write_to_file(filename)


class EventWidget(tk.Frame):
    BG = '#ffe7dc'
    BG_REMOVED = '#ceceb6'

    def __init__(self, master, event_obj, window, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.window = window
        self.base = tk.Frame(self, bg=self.BG,
                             relief='groove', bd=2)
        self.config(bd=0, bg='red')
        self.pack(fill='x', expand=False, side='top')
        self.base.pack(fill='x', expand=True)
        if event_obj:
            self.event = event_obj
            self.text = self.event.event_type
            self.date = self.event.start_time
        self.text_label = tk.Label(self.base, text=self.text, bg = self.BG,
                                   font='arial 15')
        self.text_label.pack(side='top', anchor='nw')
        self.date_label = tk.Label(self.base, text=self.date, bg=self.BG)
        self.date_label.pack(side='top', anchor='nw')
        self.base.bind('<Button>', self.on_click)
        self.remove_button = tk.Button(self.base, text='Remove', bg=self.BG)
        self.remove_button.pack(side='left', anchor='se')
        self.remove_button.bind('<Button>', self.on_remove)
        self.removed = False

    def on_click(self, event=None):
        EventWindow(self)

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


class CalendarMenu:
    def __init__(self, master, window):
        self.master = master
        self.window = window
        self.main_menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.master.quit)
        self.file_menu.add_command(label='Load', command=self.window.load)
        self.file_menu.add_command(label='Save', command = self.window.save)

        self.help_menu.add_command(label='Help Index', command=HelpIndex)
        self.help_menu.add_command(label='About...', command=About)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Help', menu=self.help_menu)
        self.main_menu.add_command(label='Refresh events',
                                   command=self.window.update_events)
        self.master.configure(menu=self.main_menu)
