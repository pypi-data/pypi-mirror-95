import tkinter as tk
from pyrustic.viewable import Viewable


# Components
BODY = "body"
CANVAS = "canvas"
BOX = "box"
HSB = "hsb"
VSB = "vsb"

# Orient
BOTH = "both"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"


class Scrollbox(Viewable):
    """
    Scrollbox is a scrollable surface. You just need to use its property "box" as
    your layout's parent.

    Example:

        import tkinter as tk
        from pyrustic.widget.scrollbox import Scrollbox

        root = tk.Tk()
        scrollbox = Scrollbox(root)
        scrollbox.build_pack()
        # Pack 50 Label on the box
        for i in range(50):
            label = tk.Label(scrollbox.box, text="Label {}".format(i))
            label.pack(anchor=tk.W)
        root.mainloop()

    """
    def __init__(self,
                 master=None,
                 orient=VERTICAL,
                 box_sticky="nswe",
                 resizable_box=True,
                 options=None):
        """
        - master: widget parent. Example: an instance of tk.Frame

        - orient: could be one of: VERTICAL, HORIZONTAL, BOTH

        - options: dictionary of widgets options
            The widgets keys are: BODY, CANVAS, BOX, HSB, VSB
            Example: Assume that you want to set the CANVAS background to red
                options = {CANVAS: {"background": "red"}}
        """
        self._master = master
        self._orient = orient
        self._box_sticky = box_sticky
        self._resizable_box = resizable_box
        self._options = {} if options is None else options
        self._body_options = None
        self._canvas_options = None
        self._box_options = None
        self._vsb_options = None
        self._hsb_options = None
        self._parse_options(self._options)
        self._body = None
        self._canvas = None
        self._box = None
        self._box_id = None
        self._vsb = None
        self._hsb = None
        self._hsb_under_mouse = False
        self._is_scrollable = False
        self._components = {}

    # ==============================================
    #                   PROPERTIES
    # ==============================================

    @property
    def master(self):
        return self._master

    @property
    def body(self):
        return self._body

    @property
    def box(self):
        return self._box

    @property
    def orient(self):
        return self._orient

    @property
    def options(self):
        return self._options

    @property
    def components(self):
        """
        Get the components (widgets instances) used to build this scrollbox.

        This property returns a dict. The keys are:
            BODY, CANVAS, BOX, HSB, VSB

        Warning: check the presence of key before usage. Example,
        the widget linked to the HSB key may be missing because
        only VSB is used
        """
        return self._components

    # ==============================================
    #                 PUBLIC METHODS
    # ==============================================

    def xview_moveto(self, fraction):
        """
        Calls canvas's method 'xview_moveto'
        Set:
            - 0: to scroll to left
            - 1: to scroll to right
        """
        if self._canvas:
            self._body.update_idletasks()
            self._canvas.xview_moveto(fraction)

    def yview_moveto(self, fraction):
        """
        Calls canvas's method 'yview_moveto'
        Set:
            - 0: to scroll to top
            - 1: to scroll to bottom
        """
        if self._canvas:
            self._body.update_idletasks()
            self._canvas.yview_moveto(fraction)

    def box_config(self, **options):
        """
        As the BOX is an item compared to CANVAS, some
        the options concerning the BOX can be edited only via
        CANVAS "itemconfig" method.
        Use this method to edit these options.
        itemconfig options are: anchor, state, height, width.

        Warning: these options are not the same as the arguments
         of BOX's own constructor !
        """
        if self._box:
            self._canvas.itemconfig(self._box_id, cnf=options)

    def clear(self):
        """
        Clears the Scrollbox.
        This method doesn't destruct this object but BOX's children
        """
        if self._box:
            for x in self._box.winfo_children():
                x.destroy()

    # ==============================================
    #                 PRIVATE METHODS
    # ==============================================

    def _on_build(self):
        self._body = tk.Frame(self._master,
                              class_="Scrollbox",
                              cnf=self._body_options)
        self._components[BODY] = self._body
        self._body.bind("<Enter>", self._on_enter_body, "+")
        self._body.bind("<Leave>", self._on_leave_body, "+")
        self._body.bind("<Unmap>", self._on_unmap_body, "+")
        self._body.bind("<Destroy>", self._on_destroy_body, "+")
        self._body.bind_all("<MouseWheel>", self._on_mouse_wheel, "+")
        self._body.bind_all("<Button-4>", self._on_mouse_wheel, "+")
        self._body.bind_all("<Button-5>", self._on_mouse_wheel, "+")
        self._body.columnconfigure(0, weight=1, uniform=1)
        self._body.rowconfigure(0, weight=1, uniform=1)
        self._body.winfo_toplevel().bind("<Configure>",
                                         self._on_configure_box_canvas, "+")
        # canvas
        self._canvas = tk.Canvas(self._body,
                                 name=CANVAS,
                                 width=0,
                                 height=0,
                                 cnf=self._canvas_options)
        self._components[CANVAS] = self._canvas
        self._canvas.grid(row=0, column=0, sticky=self._box_sticky)
        # box
        self._box = tk.Frame(self._canvas,
                             name=BOX,
                             cnf=self._box_options)
        self._components[BOX] = self._box
        self._box_id = self._canvas.create_window(0, 0, window=self._box, anchor="nw")
        self._box.bind("<Configure>", self._on_configure_box_canvas, "+")
        # scrollbar
        self._set_scrollbars()

    def _on_display(self):
        if not self._master:
            self._master = self._body.master

    def _on_destroy(self):
        if self._body:
            self._unbind_funcs()

    def _on_mouse_wheel(self, event):
        if not self._orient or not self._is_scrollable:
            return
        # scroll down   (value: 1)   ->  event.num = 5   or  event.delta < 0
        # scroll up     (value: -1)  ->  event.num = 4   or  event.delta >= 0
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        if self._orient in ("horizontal", "x", "h"):
            self._canvas.xview_scroll(scroll, "units")
        elif self._orient in ("both", "vertical", "y", "v"):
            if self._hsb_under_mouse:
                self._canvas.xview_scroll(scroll, "units")
            else:
                self._canvas.yview_scroll(scroll, "units")

    def _set_scrollbars(self):
        if self._orient in ("both", "horizontal", "h", "x"):
            self._hsb = tk.Scrollbar(self._body, orient="horizontal",
                                     name=HSB,
                                     command=self._canvas.xview,
                                     cnf=self._hsb_options)
            self._components[HSB] = self._hsb
            self._hsb.grid(row=1, column=0, columnspan=2, sticky="swe")
            self._canvas.config(xscrollcommand=self._hsb.set)
            self._bind_enter_leave_to_hsb()
        if self._orient in ("both", "vertical", "v", "y"):
            self._vsb = tk.Scrollbar(self._body, orient="vertical",
                                     name=VSB,
                                     command=self._canvas.yview,
                                     cnf=self._vsb_options)
            self._components[VSB] = self._vsb
            self._vsb.grid(row=0, column=1, sticky=self._box_sticky)
            self._canvas.config(yscrollcommand=self._vsb.set)

    def _bind_enter_leave_to_hsb(self):
        def enter_hsb(event):
            self._hsb_under_mouse = True
        def leave_hsb(event):
            self._hsb_under_mouse = False
        self._hsb.bind('<Enter>', enter_hsb, "+")
        self._hsb.bind('<Leave>', leave_hsb, "+")

    def _on_configure_box_canvas(self, event):
        if self._box:
            if self._orient in ("horizontal", "h", "x"):
                if self._resizable_box:
                    self._canvas.itemconfig(self._box_id,
                                            height=self._canvas.winfo_height())
                else:
                    self._canvas.config(height=self._box.winfo_height())
            elif self._orient in ("vertical", "v", "y"):
                if self._resizable_box:
                    self._canvas.itemconfig(self._box_id,
                                            width=self._canvas.winfo_width())
                else:
                    self._canvas.config(width=self._box.winfo_width())
            self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _on_enter_body(self, event):
        self._is_scrollable = True

    def _on_leave_body(self, event):
        self._is_scrollable = False

    def _on_unmap_body(self, event):
        self._is_scrollable = False

    def _on_destroy_body(self, event):
        self._is_scrollable = False

    def _unbind_funcs(self):
        try:
            for val in ("<Enter>", "<Leave>",
                        "<Unmap>", "<Destroy>",
                        "<MouseWheel>", "<Button-4>",
                        "<Button-5>", "<Configure>"):
                self._body.unbind(val)
        except Exception as e:
            pass

    def _parse_options(self, options):
        self._body_options = options[BODY] if BODY in options else {}
        self._canvas_options = options[CANVAS] if CANVAS in options else {}
        self._box_options = options[BOX] if BOX in options else {}
        self._vsb_options = options[VSB] if VSB in options else {}
        self._hsb_options = options[HSB] if HSB in options else {}


class _ScrollboxTest(Viewable):

    def __init__(self, root):
        self._root = root
        self._body = None

    def _on_build(self):
        self._body = tk.Frame(self._root)
        # Pane 1
        pane_1 = tk.Frame(self._root)
        pane_1.pack(side=tk.LEFT, padx=10,
                    pady=10, expand=1, fill=tk.BOTH)
        # Scrollbox 1
        scrollbox_1 = Scrollbox(pane_1, orient=VERTICAL)
        scrollbox_1.build_pack(pady=5, expand=1, fill=tk.BOTH)
        # Button 1
        command = (lambda self=self, box=scrollbox_1.box, side=tk.TOP:
                   self._on_click_add(box, side))
        button_1 = tk.Button(pane_1, text="Add",
                             command=command)
        button_1.pack(side=tk.BOTTOM)
        # Pane 2
        pane_2 = tk.Frame(self._root)
        pane_2.pack(side=tk.LEFT, padx=10,
                    pady=10, expand=1, fill=tk.BOTH)
        # Scrollbox 2
        scrollbox_2 = Scrollbox(pane_2, orient=HORIZONTAL)
        scrollbox_2.build_pack(pady=5, expand=1, fill=tk.BOTH)
        # Button 2
        command = (lambda self=self, box=scrollbox_2.box, side=tk.LEFT:
                   self._on_click_add(box, side))
        button_2 = tk.Button(pane_2, text="Add",
                             command=command)
        button_2.pack(side=tk.BOTTOM)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _on_click_add(self, frame, side=tk.TOP):
        label = tk.Label(frame, text="Hello Friend")
        label.pack(side=side)


if __name__ == "__main__":
    root = tk.Tk()
    scrollbox_test = _ScrollboxTest(root)
    scrollbox_test.build_pack(fill=tk.BOTH, expand=1)
    root.mainloop()
