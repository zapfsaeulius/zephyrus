# -*- coding: utf-8 -*-

from tkinter import ttk
from tkinter import Toplevel, StringVar, DoubleVar
from tkinter import W, E

padding = {'padx': 2, 'pady': 1}


def label(parent, row, column, sticky, f):
    l = ttk.Label(parent, text=f)
    l.grid(row=row, column=column, sticky=sticky)
    return l


def frame(parent, row, column, sticky):
    f = ttk.Frame(parent)
    f.grid(row=row, column=column, sticky=sticky)
    return f


def labelframe(parent, row, column, title):
    lf = ttk.LabelFrame(parent, text=title)
    lf.grid(row=row, column=column, sticky=(W, E))
    return lf


def lf_param(parent, row, column, title):
    lf = ttk.LabelFrame(parent, text=title)
    lf.grid(row=row, column=column, sticky=(W, E))
    lf.columnconfigure(2, weight=1)
    return lf


def grid_pad(parent, x, y):
    for child in parent.winfo_children():
        child.grid_configure(padx=x, pady=y)


def pack_pad(parent, x, y):
    for child in parent.winfo_children():
        child.pack_configure(padx=x, pady=y)


def tab(parent, text):
    f = ttk.Frame(parent, padding=4)
    f.columnconfigure(1, weight=1)
    parent.add(f, text=text)
    return f


def treeview(parent, headings, settings, height):
    columns = ['#0'] + headings[1:]
    t = ttk.Treeview(parent, height=height)
    t['columns'] = headings[1:]
    for column, heading, setting in zip(columns, headings, settings):
        t.column(column, width=setting[0], anchor=setting[1])
        t.heading(column, text=heading)
    t.pack(side='top', fill='both', expand=1)
    return t


def var(self, prefix, name, preset):
    if isinstance(preset, str):
        setattr(self, prefix + name, StringVar())
    else:
        setattr(self, prefix + name, DoubleVar())
    v = getattr(self, prefix + name)
    v.set(preset)
    return v


def e_input(self, parent, row, column, symbol, name, preset, command):
    f = ttk.Frame(parent)
    f.grid(row=row, column=column, sticky=E, **padding)
    ttk.Label(f, text=symbol).pack(side='left')
    v = var(self, 'var_', name, preset)
    e = ttk.Entry(f, textvariable=v, width=5)
    e.pack(side='left')
    e.bind("<FocusOut>", command)
    e.bind("<Return>", command)
    return f


def cbb_input(self, parent, row, column, width, symbol, name, preset, values, command):
    f = ttk.Frame(parent)
    f.grid(row=row, column=column, sticky=E)
    ttk.Label(f, text=symbol).pack(side='left', **padding)
    v = var(self, 'var_', name, preset)
    cb = ttk.Combobox(f, textvariable=v, values=values, width=width)
    cb.pack(side='left')
    cb.bind('<<ComboboxSelected>>', command)
    return f


def e_param(self, parent, row, column, description, symbol, name, preset):
    ttk.Label(parent, text=description).grid(row=row, column=1, sticky=W)
    ttk.Label(parent, text=symbol).grid(row=row, column=2, sticky=E)
    v = var(self, 'var_', name, preset)
    e = ttk.Entry(parent, textvariable=v, width=7)
    e.grid(row=row, column=3, sticky=W)


def cbb_param(self, parent, row, description, symbol, name, preset, values):
    ttk.Label(parent, text=description).grid(row=row, column=1, sticky=W)
    ttk.Label(parent, text=symbol).grid(row=row, column=2, sticky=E)
    v = var(self, 'var_', name, preset)
    cb = ttk.Combobox(parent, textvariable=v, values=values, width=0)
    cb.grid(row=row, column=3, sticky=(W, E))


def cb_param(self, parent, row, description, name, preset, command):
    v = var(self, 'var_', name, preset)
    cb = ttk.Checkbutton(parent, text=description, variable=v, command=command)
    cb.grid(row=row, column=1, sticky=W)


def e_general(self, parent, row, column, width, description, name, preset):
    ttk.Label(parent, text=description).grid(row=row, column=(column*2)-1, sticky=E)
    v = var(self, 'var_', name, preset)
    e = ttk.Entry(parent, textvariable=v, width=width)
    e.grid(row=row, column=column*2, sticky=(W, E), **padding)
    if width is None:
        e.grid(columnspan=3)


def toplevel(parent, title):
    t = Toplevel(parent, borderwidth=8)
    t.title(title)
    x = parent.winfo_rootx()
    y = parent.winfo_rooty()
    t.geometry('+{}+{}'.format(x+4, y+4))
    return t


def button(parent, text, command):
    b = ttk.Button(parent, text=text, command=command)
    b.pack(side='right', **padding)