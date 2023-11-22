import contextlib
import os


@contextlib.contextmanager
def chdir(target: str):
    """Context-managed chdir, original implementation by GitHub @Akuli"""
    current = os.getcwd()
    try:
        os.chdir(target)
        yield
    finally:
        os.chdir(current)


local = os.path.abspath(os.path.dirname(__file__))


def loadt():
    from tkinter import _default_root  # 获取默认窗口
    from tkinter import TclError

    itcl = os.path.join(local, "itcl4.2.3")
    itk = os.path.join(local, "itk4.1.0")
    iwidgets = os.path.join(local, "iwidgets4.0.1")
    from os import environ
    environ["ITCL_LIBRARY"] = itcl
    environ["ITK_LIBRARY"] = itk
    with chdir(itcl):
        _default_root.tk.eval("set dir [file dirname [info script]]")
        _default_root.tk.eval("source pkgIndex.tcl")
        _default_root.tk.eval("package require itcl 4.2.3")
    with chdir(itk):
        _default_root.tk.eval("set dir [file dirname [info script]]")
        _default_root.tk.eval("source pkgIndex.tcl")
        _default_root.tk.eval("package require itk 4.1.0")
    with chdir(iwidgets):
        _default_root.tk.eval("set dir [file dirname [info script]]")
        _default_root.tk.eval("source pkgIndex.tcl")
        _default_root.tk.eval("package require Iwidgets 4.0.1")

def load():
    from tkinter import _default_root  # 获取默认窗口
    from tkinter import TclError

    tcl = _default_root
    try:
        tcl.tk.eval("package require Itcl 4.2.3")
        tcl.tk.eval("package require Itk 4.1.0")
        tcl.tk.eval("package require Iwidgets 4.0.1")
    except AttributeError:
        raise AttributeError("未初始化Tk")
    except TclError:
        from sys import executable
        raise TclError(f"未安装库，请运行{executable} -m tkinteri命令")


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    load()
    root.mainloop()
