# TkinterI 
Tkinter扩展组件库

--- 

## 特点

- 支持跨平台使用
- 暂时有2个组件（完全实现总共52+组件）

## 安装
```python
pip install tkinteri
python -m tkinteri
```

## 简介
本组件库基于
[`Incr Widgets`](https://wiki.tcl-lang.org/page/incr+Widgets)，
通过`Tcl`提供的接口使用
[`Incr Widgets`](https://wiki.tcl-lang.org/page/incr+Widgets)
进行开发。

## ButtonBox 按钮盒
### 示例
```python
from tkinter import Tk
from tkinteri import IButtonbox

root = Tk()

bb = IButtonbox()

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
```