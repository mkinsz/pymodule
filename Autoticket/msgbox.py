#!/usr/bin/python
# -*- coding:utf-8 -*-

import tkinter
import tkinter.messagebox

window=tkinter.Tk()
# window.title('menu')
# window.geometry('400x400')
window.withdraw()

ok = tkinter.messagebox.askokcancel('提示','人生苦短')
print(ok)
# def hit() :
#     tkinter.messagebox.askquestion(title='hi', message='Are you sure to cancel it?')

# b=tkinter.Button(window,text='there will be a msgbox',command=hit).pack()


# tkinter.mainloop()