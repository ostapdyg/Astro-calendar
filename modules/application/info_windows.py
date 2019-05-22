from modules.application import *


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
