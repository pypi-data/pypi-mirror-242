from tkinter import Widget


class ButtonBox(Widget):
    def __init__(self, master=None, **kwargs):
        """
The buttonbox command creates a manager widget for controlling buttons.
The button box also supports the display and invocation of a default button.
The button box can be configured either horizontally or vertically.

buttonbox 命令创建一个用于控制的管理器小部件 按钮。
按钮框还支持显示和调用 默认按钮。按钮盒可以水平配置 或垂直。


`orient`: Orientation of the button box: horizontal or vertical. The default is horizontal. 按钮框的方向：水平或垂直。默认 是水平的。


`padx`: Specifies a non-negative padding distance to leave between the button group and the outer edge of the button box in the x direction. The value may be given in any of the forms acceptable to Tk_GetPixels. The default is 5 pixels. 按钮框的方向：水平或垂直。默认 是水平的。


`pady`: Specifies a non-negative padding distance to leave between the button group and the outer edge of the button box in the y direction. The value may be given in any of the forms acceptable to Tk_GetPixels. The default is 5 pixels. 指定按钮组和按钮组之间要留出的非负填充距离 按钮框在 Y 方向上的外边缘。该值可以给出 以Tk_GetPixels可接受的任何形式。默认值为 5 像素。

        :param master:
        :param cnf:
        :param kw:
        """
        from tkinteri.core import load
        load()

        super().__init__(master, "iwidgets::Buttonbox")
        self.configure(**kwargs)

        self._t = 0

    def add(self, tag=None, **kwargs):
        """
        Add a button distinguished by tag to the end of the button box.
        If additional arguments are present they specify options to be applied to the button.
        See PushButton for information on the options available.

        在按钮框的末尾添加一个按标记区分的按钮。
        如果存在其他参数，则指定要应用的选项 到按钮。
        有关选项的信息，请参阅 PushButton 可用。
        :param tag: 标记标签
        :param kwargs: 选项
        :return:
        """
        if tag is None:
            self._t += 1
            tag = self._w + "." + str(self._t)
        ks = []
        for k in kwargs:
            ks.append(f"-{k}")
            if k == "command":
                ks.append([self.register(kwargs[k])])  # 注册函数
            else:
                ks.append(kwargs[k])
        self.tk.call(self._w, "add", tag, *ks)
        return tag

    def buttonconfigure(self, index, **kwargs):
        """
        This command is similar to the configure command, except that it applies to the options for an individual button, whereas configure applies to the options for the button box as a whole.
        Options may have any of the values accepted by the PushButton command.
        If options are specified, options are modified as indicated in the command and the command returns an empty string.
        If no options are specified, returns a list describing the current options for entry index (see Tk_ConfigureInfo for information on the format of this list).

        此命令类似于 configure 命令，不同之处在于 它适用于单个按钮的选项， 而配置适用于整个按钮框的选项。
        选项可以具有 PushButton 命令接受的任何值。
        如果指定了选项，则修改选项 如命令中所示，命令返回一个空字符串。
         如果未指定任何选项，则返回一个列表，描述 条目索引的当前选项（请参阅Tk_ConfigureInfo 有关此列表格式的信息）。
        :param index:
        :param kwargs:
        :return:
        """
        ks = []
        for k in kwargs:
            ks.append(f"-{k}")
            if k == "command":
                ks.append([self.register(kwargs[k])])  # 注册函数
            else:
                ks.append(kwargs[k])
        return self.tk.call(self._w, "buttonconfigure", index, *ks)

    def configure(self, **kwargs):
        ks = []
        for k in kwargs:
            ks.append(f"-{k}")
            if k == "command":
                ks.append([self.register(kwargs[k])])  # 注册函数
            else:
                ks.append(kwargs[k])
        return self.tk.call(self._w, "configure", *ks)

    def default(self, index):
        """
        Sets the default button to the button given by index.
        This causes the default ring to appear arround the specified button.

        将默认按钮设置为索引指定的按钮。
        这会导致在指定按钮周围显示默认环。

        :param index:
        :return:
        """
        self.tk.call(self._w, "default", index)

    def delete(self, index):
        """
        Deletes the button given by index from the button box.

        从按钮框中删除索引给出的按钮。

        :param index:
        :return:
        """
        self.tk.call(self._w, "delete", index)

    def hide(self, index):
        """
        Hides the button denoted by index. This doesn't remove the button `permanently`, just inhibits its display.

        隐藏由索引表示的按钮。这不会删除按钮 永久地，只是抑制其显示。

        :param index:
        :return:
        """
        self.tk.call(self._w, "hide", index)

    def index(self, index):
        """
        Returns the numerical index corresponding to `index`.

        返回与 `index` 对应的数字索引。

        :param index:
        :return:
        """
        return self.tk.call(self._w, "index", index)

    def insert(self, index, tag=None, **kwargs):
        """
        Same as the add command except that it inserts the new button just before the one given by index, instead of appending to the end of the button box.
        The option and value arguments have the same interpretation as for the add widget command.

        与 `add` 命令相同，只是它插入了新的 按钮，而不是附加 到按钮框的末尾。
        `option` 和 `value` 参数的解释与 `add` 小部件的解释相同 命令。
        :param tag: 标记标签
        :param index: 索引位置
        :param kwargs: 选项
        :return:
        """
        if tag is None:
            self._t += 1
            tag = self._w + "." + str(self._t)
        ks = []
        for k in kwargs:
            ks.append(f"-{k}")
            if k == "command":
                ks.append([self.register(kwargs[k])])  # 注册函数
            else:
                ks.append(kwargs[k])
        self.tk.call(self._w, "insert", index, tag, *ks)
        return tag

    def invoke(self, index=None):
        """
        Invoke the command associated with a button.
        If no arguments are given then the current default button is invoked, otherwise the argument is expected to be a button index.

        调用与按钮关联的命令。如果没有参数 则调用当前的默认按钮，否则参数 预计是按钮索引。

        :return:
        """

        self.tk.call(self._w, "invoke", index)

    def show(self, index):
        """
        Display a previously hidden button denoted by index.

        显示以前隐藏的按钮，由索引表示。

        :param index:
        :return:
        """
        self.tk.call(self._w, "show", index)


def test():
    from tkinter import Tk
    root = Tk()

    bb = ButtonBox()

    bb.add("OK", text="OK", command=lambda: print("OK"))
    bb.add("Apply", text="Apply", command=lambda: print("Apply"))
    bb.add("Cancel", text="Cancel", command=lambda: print("Cancel"))

    bb.default("OK")

    bb.pack(fill="both", expand="yes")

    bb2 = ButtonBox(orient="vertical")

    bb2.add("First", text="First", command=lambda: print("First"))
    bb2.add("Second", text="Second", command=lambda: print("Second"))
    bb2.add("Third", text="Third", command=lambda: print("Third"))

    bb2.insert(2, "Fourth", text="Fourth", command=lambda: print("Fourth"))

    bb2.default("First")

    bb2.invoke()
    bb2.invoke("Second")

    print("Button-Third`s Index", bb2.index("Third"))

    bb2.pack(fill="both", expand="yes")

    root.mainloop()

    """
iwidgets::buttonbox .bb 

.bb add OK -text OK -command "puts OK" 
.bb add Apply -text Apply -command "puts Apply"
.bb add Cancel -text Cancel -command "puts Cancel"
.bb default OK

pack .bb -expand yes -fill both
    """


if __name__ == '__main__':
    test()
