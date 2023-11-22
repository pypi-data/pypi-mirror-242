from tkinter import Widget


class Calendar(Widget):
    def __init__(self, master=None, **kwargs):
        """
The buttonbox command creates a manager widget for controlling buttons.
The button box also supports the display and invocation of a default button.
The button box can be configured either horizontally or vertically.

`calendar` 命令为所选内容创建日历小组件 `日期`，一次显示一个月。按钮存在于 `顶部更改月份`，实际上翻动日历的页面。
如 `翻开一页`，修改了该月的日期。
`选择` 日期在视觉上标记该日期。
可以监控所选值 通过 `-command` 选项或仅使用 `get` 命令检索。

`backwardimage`: Specifies an image to be displayed on the backwards calendar button. This image must have been created previously with the image create command. If none is specified, a default is provided. 指定要在后向日历上显示的图像 按钮。此映像必须是之前使用 image create 命令。如果未指定任何值，则默认 提供。
`buttonforeground`: Specifies the foreground color of the forward and backward buttons in any of the forms acceptable to Tk_GetColor. The default color is blue. 指定前进和后退按钮的前景色 以Tk_GetColor可接受的任何形式。默认 颜色为蓝色。
`command`: Specifies a Tcl script to executed upon selection of a date in the calendar. 指定在 日历。
`currentDateFont`: Specifies the font used for the current date text in any of the forms acceptable to Tk_GetFont. 指定用于任何表单中的当前日期文本的字体 Tk_GetFont可接受。
`datefont`: Specifies the font used for the days of the month text in any of the forms acceptable to Tk_GetFont. 指定用于任何表单中的当前日期文本的字体 Tk_GetFont可接受。
`dayfont`: Specifies the font used for the days of the week text in any of the forms acceptable to Tk_GetFont.指定任何窗体中星期几文本使用的字体 Tk_GetFont可接受。
`days`: Specifies a list of values to be used for the days of the week text to displayed above the days of the month. The default value is ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']. 指定要用于星期几的值列表 文本显示在月份中的几天上方。默认值 是 ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']}。
`forewardimage`: Specifies an image to be displayed on the forewards calendar button. This image must have been created previously with the image create command. If none is specified, a default is provided.指定要在 forewards 日历上显示的图像 按钮。此映像必须是之前使用 image create 命令。如果未指定任何值，则默认 提供。
`height`: Specifies a desired window height that the calendar widget should request from its geometry manager. The value may be specified in any of the forms acceptable to Tk_GetPixels. The default height is 165 pixels. 指定日历小组件应的所需窗口高度 来自其几何管理器的请求。该值可以在任何 Tk_GetPixels可接受的形式。默认高度 为 165 像素。
`outline`: Specifies the outline color used to surround the days of the month text in any of the forms acceptable to Tk_GetColor. The default is the same color as the background. 指定用于将 中的日期文本包围起来的轮廓颜色 Tk_GetColor可接受的任何形式。默认值为 与背景颜色相同。
`selectcolor`: Specifies the color of the ring displayed that distinguishes the currently selected date in any of the forms acceptable to Tk_GetColor. The default is red. 指定显示的环的颜色，用于区分 当前选择的日期以Tk_GetColor可接受的任何形式。默认值为红色。
`selectthickness`: Specifies the thickness of the ring displayed that distinguishes the currently selected date. The default is 3 pixels. 指定显示的用于区分的环的厚度 当前选定的日期。默认值为 3 像素。
`startday`: Specifies the starting day for the week: sunday, monday, tuesday, wednesday, thursday, friday, or saturday. The default is sunday. 指定一周的开始日期：星期日、星期一、星期二、星期三、星期四、星期五或星期六。默认值为 Sunday。
`titlefont`: Specifies the font used for the title text which consists of the month and year. The font may be given in any of the forms acceptable to Tk_GetFont. 指定用于标题文本的字体，该文本由 月和年。字体可以以任何形式给出 Tk_GetFont可接受。
`weekdaybackground`: Specifies the background color for the weekdays which allows it to be visually distinguished from the weekend. The color may be given in any of the forms acceptable to Tk_GetColor. The default is the same as the background. 指定工作日的背景色，使其能够 在视觉上与周末区分开来。颜色可以给出 以Tk_GetColor可接受的任何形式。默认值为 与背景相同。
`weekendbackground`: Specifies the background color for the weekends which allows it to be visually distinguished from the weekdays. The color may be given in any of the forms acceptable to Tk_GetColor. The default is the same as the background. 指定日历小组件应的所需窗口宽度 来自其几何管理器的请求。该值可以在任何 Tk_GetPixels可接受的形式。默认宽度 为 200 像素。
`width`: Specifies a desired window width that the calendar widget should request from its geometry manager. The value may be specified in any of the forms acceptable to Tk_GetPixels. The default width is 200 pixels. 指定日历小组件应的所需窗口宽度 来自其几何管理器的请求。该值可以在任何 Tk_GetPixels可接受的形式。默认宽度 为 200 像素。

        :param master:
        :param cnf:
        :param kw:
        """
        from tkinteri.core import load
        load()

        super().__init__(master, "iwidgets::Calendar")
        self.configure(**kwargs)

    def configure(self, **kwargs):
        ks = []
        for k in kwargs:
            ks.append(f"-{k}")
            if k == "command":
                ks.append([self.register(kwargs[k])])  # 注册函数
            else:
                ks.append(kwargs[k])
        return self.tk.call(self._w, "configure", *ks)

    def get(self, format=None):
        """
        Returns the currently selected date in a format of string or as an integer clock value using the -string and -clicks format options respectively.
        The default is by string.
        Reference the clock command for more information on obtaining dates and their formats.

        以 字符串或作为整数时钟值，分别使用 `-string` 和 `-clicks` 格式选项。
        默认值为 `-string` 。
        参考 clock 命令以获取有关获取日期及其 格式。

        :return:
        """
        return self.tk.call(self._w, "get", format)

    def select(self, date):
        """
        Changes the currently selected date to the value specified which must be in the form of a date string, an integer clock value or as the keyword "now".
        Reference the clock command for more information on obtaining dates and their formats.
        Note that selecting a date does not change the month being shown to that of the date given.
        This chore is left to the show command.

        将当前选定的日期更改为指定的值，该值 必须采用日期字符串、整数时钟值或 关键字“now”。
        参考时钟 命令以获取有关获取日期及其格式的详细信息。
        请注意，选择日期不会更改 显示为给定日期的月份。
        这个苦差事就剩下了 添加到 `show` 命令。

        :return:
        """
        return self.tk.call(self._w, "select", date)

    def show(self, date):
        """
        Changes the currently displayed date to be that of the date argument which must be in the form of a date string, an integer clock value or as the keyword "now".
        Reference the clock command for more information on obtaining dates and their formats.

        将当前显示的日期更改为日期的日期 参数，必须采用日期字符串的形式，一个 整数时钟值或 AS 关键字“now”。
        参考时钟 命令以获取有关获取日期及其格式的详细信息。

        :return:
        """
        return self.tk.call(self._w, "show", date)


def test():
    from tkinter import Tk
    root = Tk()

    def selectCmd():
        print("strings", c.get())
        print("clicks", c.get("-clicks"))

    c = Calendar(
        command=lambda: selectCmd(),
        weekendbackground="mistyrose", weekdaybackground="ghostwhite",
        outline="black", startday="wednesday",
        days=["三", "四", "五", "六", "天", "一", "二"]
    )
    c.pack()

    root.mainloop()

    """
proc selectCmd {date} {
    puts $date
}

calendar .c -command {selectCmd %d} -weekendbackground mistyrose \\
    -weekdaybackground ghostwhite -outline black \\
    -startday wednesday -days {We Th Fr Sa Su Mo Tu}
pack .c 
    """


if __name__ == '__main__':
    test()
