from modules.application import *


class ScrolledFrame:
    """
    A frame with the scrollbar attached to the right side.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.top_frame = tk.Frame(master, **kwargs)
        self.scroll = tk.Scrollbar(self.top_frame, orient='vertical')
        self.canvas = tk.Canvas(self.top_frame, width=width, height=height,
                                bg=bg, yscrollcommand=self.scroll.set,
                                yscrollincrement='5')
        self.scroll.configure(command=self.canvas.yview)
        self.scroll.pack(fill='y', side='right')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.main_frame = tk.Frame(self.canvas, bg=bg)
        self.canvas.create_window(4, 4, window=self.main_frame, anchor='nw')
        self.main_frame.bind("<Configure>", self._reconf)
        self.top_attr = set(dir(tk.Widget))
        self.canvas.bind("<Enter>", self._bind_wheel)
        self.canvas.bind("<Leave>", self._unbind_wheel)

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

    def _on_wheel(self, event):
        if event.delta < 0:
            self.canvas.yview_scroll(1, 'units')
        if event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')

    def _bind_wheel(self, event=None):
        self.canvas.bind_all("<4>", self._on_wheel)
        self.canvas.bind_all("<5>", self._on_wheel)
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)

    def _unbind_wheel(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
