from modules.adt import Calendar
from modules.application import *
import os
MIN_YEAR = 1980
MAX_YEAR = 2050


class CalendarWindow:
    def __init__(self, master, app=None, filename=None, num=0):
        self.app = app
        self.master = master
        self.num = num
        if filename:
            self.name = r'/'.join(filename.split('/')[-2:])
        else:
            self.name = 'New calendar'
        self.top_frame = tk.Frame(self.master, borderwidth=2, relief='ridge')
        self.menu = CalendarMenu(self.top_frame, self)
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
            event_widget.pack_forget()
            event_widget.destroy()
        for event in self.calendar:
            self.events.append(EventWidget(self.frame, event, self))

    def delete_events(self):
        for event_widget in self.events:
            if event_widget.selected:
                self.calendar.remove_event(event_widget.event)
        self.update_events()

    def select_all(self, event=None):
        for event_widget in self.events:
            if not event_widget.selected:
                event_widget.select()

    def unselect_all(self, event=None):
        for event_widget in self.events:
            if event_widget.selected:
                event_widget.select()

    def load(self):
        filename = filedialog.askopenfilename(title='Load...',
                                              defaultextension=".cal",
                                              filetypes=[('Calendar files',
                                                         '*.cal')],
                                              initialdir=os.path.abspath(
                                                  'user_cals'))
        if filename:
            self.calendar = self.calendar.create_from_file(filename)
            self.update_events()
            self.name = r'/'.join(filename.split('/')[-2:])
            self.menu.name_label.config(text=self.name)

    def new_cal(self):
        self.calendar = Calendar()
        self.update_events()
        self.menu.name_label.config(text='New calendar')

    def save(self):
        filename = filedialog.asksaveasfilename(title='Save as...',
                                                defaultextension=".cal",
                                                filetypes=[('Calendar files',
                                                           '*.cal'),
                                                           ('All files',
                                                            '*.*')],
                                                initialdir=os.path.abspath(
                                                    'user_cals'))
        if filename:
            self.calendar.write_to_file(filename)
            self.name = r'/'.join(filename.split('/')[-2:])
            self.menu.name_label.config(text=self.name)

    def load_all(self, from_year, to_year=0):
        if not to_year:
            to_year = from_year
        self.calendar = Calendar()
        for year in range(from_year, to_year+1):
            self.calendar.add_from_file('data/ical_{}.php'.format(str(year)))
        self.update_events()
        self.name = 'Events {} to {}'.format(from_year, to_year)
        self.menu.name_label.config(text=self.name)

    def add_to_other(self):
        other_num = (self.num+1)%2
        for event_widget in self.events:
            if event_widget.selected:
                self.app.cals[other_num].calendar.add_event(event_widget.event)
        self.app.cals[other_num].update_events()
        self.unselect_all()



class EventWidget(tk.Frame):
    BG = '#ffe7dc'
    BG_SELECTED = '#ceceb6'

    def __init__(self, master, event_obj, window, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.window = window
        self.selected = False
        self.base = tk.Frame(self, bg=self.BG,
                             relief='groove', bd=2)
        self.config(bd=0, bg='red')
        self.pack(fill='x', expand=False, side='top')
        self.base.pack(fill='x', expand=True)
        if event_obj:
            self.event = event_obj
            self.text = self.event.event_type
            self.date = self.event.start_time
        self.sb_var = tk.BooleanVar()
        self.sb_var.set(False)
        self.select_button = tk.Checkbutton(self.base, variable=self.sb_var,
                                            bg=self.BG,
                                            onvalue=True,
                                            offvalue=False,
                                            command=self.select)
        self.select_button.pack(side='left', anchor='e')
        self.text_label = tk.Label(self.base, text=self.text, bg=self.BG,
                                   font='arial 15')
        self.text_label.pack(side='top', anchor='nw')
        self.date_label = tk.Label(self.base, text=self.date, bg=self.BG)
        self.date_label.pack(side='top', anchor='nw')
        self.base.bind('<Button>', self.on_click)

    def on_click(self, event=None):
        EventWindow(self)

    def select(self, event=None):
        print(self)
        if not self.selected:
            if not self.sb_var.get():
                self.sb_var.set(True)
            self.selected = True
            self.base.config(bg=self.BG_SELECTED)
            self.text_label.config(bg=self.BG_SELECTED)
            self.date_label.config(bg=self.BG_SELECTED)
            self.select_button.config(bg=self.BG_SELECTED)
        else:
            if self.sb_var.get():
                self.sb_var.set(False)
            self.selected = False
            self.base.config(bg=self.BG)
            self.text_label.config(bg=self.BG)
            self.date_label.config(bg=self.BG)
            self.select_button.config(bg=self.BG)


class CalendarMenu(tk.Frame):
    def __init__(self, master, window, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(relief='ridge', borderwidth=1, height=20)
        self.window = window
        self.load_all_events_window = None
        self.name_label = tk.Label(self, text=self.window.name, width=20)
        file_menu = tk.Menubutton(self, text='File  ', anchor='nw',
                                  relief='raised', underline=0, borderwidth=1)
        file_menu.menu = tk.Menu(file_menu)
        file_menu['menu'] = file_menu.menu
        file_menu.menu.add_command(label='New', command=self.window.new_cal)
        file_menu.menu.add_command(label='Save...', command=self.window.save)
        file_menu.menu.add_command(label='Load...', command=self.window.load)
        file_menu.menu.add_command(label="Load years...",
                                   command=self.on_load_all)
        self.delete_im = tk.PhotoImage(file="images/delete.gif")
        delete_button = tk.Button(self, image=self.delete_im, height=21,
                                  width=21,
                                  borderwidth=0,
                                  command=self.window.update_events)
        self.copy_im = tk.PhotoImage(file="images/copy.gif")
        copy_button = tk.Button(self, image=self.copy_im, height=21,
                                width=21,
                                borderwidth=0,
                                command=self.window.add_to_other)
        self.select_button = tk.Button(self, text='Select all', borderwidth=0,
                                       command=self.on_select_all, width=8,
                                       relief='ridge', height=1)

        self.pack(fill='x', expand=True)
        file_menu.pack(side='left', fill='x', anchor='nw')
        # self.select_button.pack(side='left', fill='none')
        delete_button.pack(side='left', fill='none')
        copy_button.pack(side='left', fill='none')
        self.name_label.pack(anchor='ne')

    def on_load_all(self):
        if not self.load_all_events_window:
            self.load_all_events_window = LoadAllEventsWindow(self.window)

    def on_select_all(self, event=None):
        self.select_button.config(text='Deselect all',
                                  command=self.on_unselect_all)
        self.window.select_all()

    def on_unselect_all(self, event=None):
        self.select_button.config(text='Select all',
                                  command=self.on_select_all)
        self.window.unselect_all()


class LoadAllEventsWindow:
    def __init__(self, main_window):
        self.window = main_window
        self.master = tk.Toplevel()
        self.master.title("Choose time period")
        self.master.geometry('300x150')
        self.frame = tk.Frame()
        self.from_scale = tk.Scale(self.master, from_=MIN_YEAR, to=MAX_YEAR,
                                   orient='horizontal', length=130)
        self.from_scale.config(command=self.on_from_scale)
        self.from_scale.pack(anchor='e')
        self.to_scale = tk.Scale(self.master, from_=MIN_YEAR, to=MAX_YEAR,
                                 orient='horizontal', length=130)
        self.to_scale.pack(anchor='e')
        self.bt_ok = tk.Button(self.master,
                               text='Ok', command=self.load_events)
        self.bt_cancel = tk.Button(self.master,
                                   text='Cancel', command=self.close)

        self.bt_ok.pack(side='right', anchor='se', padx=20, pady=3)
        self.bt_cancel.pack(side='left', anchor='sw', padx=20, pady=3)

        self.frame.pack(fill='both', expand=True)

    def load_events(self):
            # self.window.load_all(self.from_scale.get(), self.to_scale.get())
            self.window.load_all(self.from_scale.get(), self.from_scale.get())
            self.close()

    def close(self, event=None):
        self.master.destroy()
        self.master = None
        del self

    def __bool__(self):
        return self.master is not None

    def on_from_scale(self, event):
        f = self.from_scale.get()
        self.to_scale.set(max(self.to_scale.get(), f))
        self.to_scale.config(from_=f,
                             length=int(100*(MAX_YEAR-f)/(MAX_YEAR-MIN_YEAR))+
                             self.to_scale['sliderlength'], to=f+1)


