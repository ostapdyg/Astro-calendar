from modules.application import *


class EventWindow:
    def __init__(self, event_widget):
        event = event_widget.event
        self.master = tk.Toplevel()
        self.master.title('About event')
        self.frame = tk.Frame(self.master, bg='white')
        title = tk.Label(self.frame, text=event.event_type, font='Arial 14', bg='white')
        text = tk.Text(self.frame, height=3, width='50', font='Arial 12', relief='flat', bg='white')
        text.insert('end', event.description+'\n')
        text.insert('end', event.url)
        title.pack(side='top', fill='x', expand=True)
        text.pack(side='top', fill='x', expand=True)
        tk.Button(self.frame, width=5, height=1, text='Close',
                  command=self.master.destroy).pack(side='right', padx=20)
        self.frame.pack(fill='both', expand=True)

