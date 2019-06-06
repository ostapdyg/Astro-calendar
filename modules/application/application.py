from modules.application import *


class Application:
    def __init__(self, root):
        self.main_menu = MainMenu(root, self)
        self.cals = [None, None]
        self.cals[0] = CalendarWindow(root, self, 'data/ical_2020.php', 0)
        self.cals[1] = CalendarWindow(root, self, 'user_cals/defaultcal.cal',
                                      1)


class MainMenu:
    def __init__(self, master, window):
        self.master = master
        self.window = window
        self.main_menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_separator()
        self.help_menu.add_command(label='Help Index', command=HelpIndex)
        self.help_menu.add_command(label='About...', command=About)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Help', menu=self.help_menu)
        self.file_menu.add_command(label='Quit', command=self.master.quit)
        self.master.configure(menu=self.main_menu)


def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
