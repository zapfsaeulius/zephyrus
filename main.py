# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
#
# Name:        Zephyrus aka ZapfGenius
# info:     Tool for Analysis and Design of Conrete Structures
#
# Author:      Mathieu Reiner <dutu8ure@gmail.com>
#
# Created:     04.04.2014
# Copyright:   (c) Mathieu Reiner 2014
# Licence:     This file is part of Zephyrus.
#
#    Zephyrus is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 of the License.
#
#    Zephyrus is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR info.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from copy import deepcopy
import pickle

from calc import Calc
from params import *
from report import Report

import gui
import l10n

def _(msg):
    return l10n.trans[lang].get(msg, msg)


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=8)

        parent.iconbitmap(default='icons/test.ico')
        parent.title('{} v.{}'.format(title, version))
        parent.bind("<Return>", lambda event: self.calc())

        self.parent = parent

        self.pack(fill=BOTH, expand=1)

        self.initUI()

        self.store = {}
        self.project_components = {}


    def initUI(self):
        self.centerWindow()
        self.menu_bar()

        self.notebook()

        self.main_right()


        self.disable_widgets()
        self.enable_widgets()

    def centerWindow(self):
        w = 640
        h = 420
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def menu_bar(self):
        self.parent.option_add('*tearOff', False)
        path = 'icons/'

        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)

        def add_menu(menu_bar, label):
            menu = Menu(menu_bar)
            menu_bar.add_cascade(menu=menu, label=label)
            return menu

        menu_file = add_menu(menu_bar, 'File')
        menu_tools = add_menu(menu_bar, 'Tools')
        menu_project = add_menu(menu_bar, 'Project')

        submenu_print = Menu(menu_file)

        # adding menu items

        def add_menu_item(menu, label, path, name, command):
            if name:
                image = PhotoImage(file=path+name+'.gif')
            else:
                image = ''
            menu.add_command(label=label, image=image, compound='left', command=command)

        # menu_file

        add_menu_item(menu_file, _('open'), path, 'open_c', self.open_file)
        menu_file.add_command(label=_('close'), command=self.destroy)
        menu_file.add_separator()
        add_menu_item(menu_file, _('save'), path, 'save_c', self.save_file)
        add_menu_item(menu_file, _('save_as'), path, '', self.save_file_as)
        menu_file.add_separator()
        add_menu_item(menu_file, _('print_to_pdf'), path, 'print_c', self.print_to_pdf)

        menu_file.add_cascade(label='Print Setup', menu=submenu_print)

        self.m_report = IntVar()
        submenu_print.add_checkbutton(label='Full Report',
                                      variable=self.m_report)

        menu_file.add_separator()

        menu_file.add_command(label=_('exit'), command='', state=DISABLED)

        # menu_project

        menu_project.add_command(label='Project Data...',
                                 command=self.project_data)

    def open_file(self):
        filename = filedialog.askopenfilename(
            defaultextension='.z1s',
            filetypes=[('Zephyrus', '.z1s')]
        )
        if filename:
            f = open(filename, 'rb')
            self.project_data = pickle.load(f)
            self.project_components = pickle.load(f)
            f.close()
            self.project_data['path'] = filename

            self.update_notes()

    def save(self, filename):
        f = open(filename, 'wb')
        pickle.dump(self.project_data, f)
        pickle.dump(self.project_components, f)
        f.close()
        self.project_data['path'] = filename

    def save_file(self):
        filename = self.project_data['path']
        if filename != 'None':
            self.save(filename)
        else:
            self.save_file_as()

    def save_file_as(self):
        filename = filedialog.asksaveasfilename(
            defaultextension='.z1s',
            filetypes=[('Zephyrus', '.z1s')]
        )
        if filename:
            self.save(filename)

    def print_to_pdf(self):
        Report(project_data, self.project_components, self.m_report.get())

    def project_data(self):
        t = gui.toplevel(self, _('project_data'))

        f_data = gui.lf_param(t, 1, 1, '')

        gui.e_general(self, f_data, 1, 1, None, _('project_name'), 'project', 'None')
        gui.e_general(self, f_data, 2, 1, None, _('further_info'), 'info', 'None')
        gui.e_general(self, f_data, 3, 1, 56, _('engineer'), 'engineer', project_data['engineer'])
        gui.e_general(self, f_data, 3, 2, 7, _('signature'), 'signature', 'mr')

        def ok():
            project_data['project'] = self.var_project.get()
            project_data['info'] = self.var_info.get()
            project_data['engineer'] = self.var_engineer.get()
            project_data['signature'] = self.var_signature.get()
            t.destroy()

        def cancel():
            t.destroy()

        f2 = gui.frame(t, 2, 1, E)

        gui.button(f2, 'Cancel', cancel)
        gui.button(f2, 'OK', ok)

    def tap_parameters(self):
        self.lf_basic = self.p_basic()
        self.lf_4332 = self.p_4332()
        self.lf_4333 = self.p_4333()

    def p_basic(self):
        lf = gui.lf_param(self.t2, 1, 1, _('basic'))
        lf.columnconfigure(2, weight=1)
        gui.e_param(self, lf, 1, 2, _('gamma_c'), '\u0263c', 'gamma_c', gamma_c)
        gui.e_param(self, lf, 2, 2, _('gamma_s'), '\u0263s', 'gamma_s', gamma_s)
        gui.e_param(self, lf, 3, 2, '', '\u03C1', 'roh', roh)
        gui.cb_param(self, lf, 3, _('lc'), 'lc', 0, '')
        gui.e_param(self, lf, 4, 2, _('ke'), 'kE', 'ke', ke)
        gui.cbb_param(self, lf, 5, _('eta_t'), '\u03B7t', 'eta_t', eta_t, eta_t_set)
        gui.cbb_param(self, lf, 6, _('kc'), 'kc', 'kc', kc, kc_set)
        gui.cb_param(self, lf, 17, _('i'), 'ap', 0, '')

        return lf

    def p_4332(self):
        lf = gui.lf_param(self.t2, 2, 1, _('4332'))
        gui.cbb_param(self, lf, 1, _('dmax'), 'Dmax', 'dmax', dmax, dmax_set)
        gui.cb_param(self, lf, 14, _('43322'), 'f_43322', 0, '')
        gui.cb_param(self, lf, 15, _('43323'), 'f_43323', 0, '')
        gui.e_param(self, lf, 16, 2, _('delta'), '\u03B4', 'delta', 0)
        gui.cb_param(self, lf, 16, _('43324'), 'f_43324', 0, '')

        return lf

    def p_4333(self):
        lf = gui.lf_param(self.t2, 3, 1, _('4333'))
        gui.cbb_param(self, lf, 12, _('alpha'), '\u03B1', 'alpha', alpha, alpha_set)
        gui.e_param(self, lf, 13, 2, _('beta'), '\u03B2', 'beta', beta)

        return lf

    def tab_check_view(self):
        headings = ['ff', 'f', 'values', '[]']
        settings = [(125, 'w'), (50, 'center'), (50, 'center'), (75, 'center')]

        self.check_view = gui.treeview(self.t3, headings, settings, 0)

    def notebook(self):

        def on_button(event):
            if event.widget.identify(event.x, event.y) == 'label':
                index = event.widget.index('@%d, %d' % (event.x, event.y))
                tab = event.widget.tab(index, 'text')
                if tab == _('checkview'):
                    self.check_invoke()

        n = ttk.Notebook(self)
        n.pack(side='left', fill='y')
        n.bind("<Button-1>", on_button)

        self.t1 = gui.tab(n, _('inputs'))
        self.t2 = gui.tab(n, _('parameters'))
        self.t3 = gui.tab(n, _('checkview'))

        self.tab_inputs()
        self.tap_parameters()
        self.tab_check_view()

        for item in [self.t1, self.t2]:
            gui.grid_pad(item, 0, 2)

    def tab_inputs(self):
        self.construction_materials()
        self.reinforcement()
        self.geometry()
        self.actions()

    def construction_materials(self):
        lf = gui.labelframe(self.t1, 1, 1, _('construction_materials'))

        val = list(values_concrete)
        gui.cbb_input(self, lf, 1, 1, 7, _('concrete')+': ', 'beton', 'C 25/30', val, '')

        val = list(values_reinforcing_steel)
        gui.cbb_input(self, lf, 2, 1, 7, _('reinforcing_steel')+': ', 'betonstahl', 'B500B', val, '')

        #
        val = list(values_prestressing_steel)
        cmd = lambda event: self.update_spannstahl()
        self.f_pss = gui.cbb_input(self, lf, 3, 1, 7, 'prestressing_steel: ', 'ss_cat', 'Litzen', val, cmd)
        self.f_pss_add = gui.cbb_input(self, lf, 3, 2, 14, '', 'spannstahl', 'Y1860S7-12,9', '', '')

        #
        val = list(values_adhesive_reinforcement)
        cmd = lambda event: self.update_type()
        self.f_ar = gui.cbb_input(self, lf, 4, 1, 7, 'Adhesive reinf: ', 'lamelle', '', val, cmd)

    def reinforcement(self):
        lf = gui.labelframe(self.t1, 2, 1, _('reinforcement'))

        self.l_as_sup = gui.label(lf, 1, 1, E, 'As_sup:')
        self.f_as_sup = gui.frame(lf, 1, 2, W)
        cmd = lambda event: self.update_d_inf()
        gui.cbb_input(self, self.f_as_sup, 1, 1, 3, '\u2300', 'dm_sup', 10, val_dm, cmd)
        gui.cbb_input(self, self.f_as_sup, 1, 2, 4, '-', 's_sup', 150, val_s, '')

        # As_inf
        self.l_as_inf = gui.label(lf, 3, 1, E, 'As_inf:')
        self.f_as_inf = gui.frame(lf, 3, 2, W)
        gui.cbb_input(self, self.f_as_inf, 1, 1, 3, '\u2300', 'dm_inf', 10, val_dm, lambda event: self.update_d_inf())
        gui.cbb_input(self, self.f_as_inf, 1, 2, 4, '-', 's_inf', 150, val_s, '')

        # Asw
        self.l_asw = gui.label(lf, 2, 1, E, 'Asw:')
        self.f_asw = gui.frame(lf, 2, 2, W)
        gui.cbb_input(self, self.f_asw, 1, 1, 3, '\u2300', 'dmw', 10, val_dm, '')
        self.f_sw = gui.cbb_input(self, self.f_asw, 1, 2, 4, '-', 'sw', 150, val_s, '')
        self.f_ew = gui.cbb_input(self, self.f_asw, 1, 3, 4, 'e', 'ew', 150, val_s, '')

        # Al
        self.l_al = gui.label(lf, 4, 1, E, 'Al_inf:')
        self.f_al = gui.frame(lf, 4, 2, E)
        gui.e_input(self, self.f_al, 1, 1, 'tl ', 'tl', 0, '')
        gui.e_input(self, self.f_al, 1, 2, 'bl ', 'bl', 0, '')
        gui.cbb_input(self, self.f_al, 1, 3, 4, 'e', 'el', 1000, val_s, '')

    def geometry(self):
        lf = gui.labelframe(self.t1, 3, 1, _('geometry'))
        self.f_h = gui.e_input(self, lf, 2, 1, 'h ', 'h', 0, lambda event: self.update_d_inf())
        self.f_c_inf = gui.e_input(self, lf, 2, 2, 'c_inf ', 'c_inf', 30, lambda event: self.update_d_inf())
        self.f_b = gui.e_input(self, lf, 1, 1, 'b ', 'b', 1000, '')
        self.f_d_inf = gui.e_input(self, lf, 4, 2, 'd_inf ', 'd_inf', 0, '')
        self.f_delta_dv = gui.e_input(self, lf, 4, 3, 'check d/6 ', 'delta_dv', 0, '')

    def actions(self):
        lf = gui.labelframe(self.t1, 4, 1, _('actions'))
        self.f_ned = gui.e_input(self, lf, 1, 1, 'Nd ', 'ned', 0, '')
        self.f_ved = gui.e_input(self, lf, 1, 2, 'Vd ', 'ved', 0, '')
        self.f_med = gui.e_input(self, lf, 1, 3, 'Md ', 'med', 0, '')

    def update_d_inf(self):
        if self.var_h.get() > 0:
            d = self.var_h.get() - self.var_c_inf.get() - self.var_dm_inf.get()
            self.var_d_inf.set(int(d))

    def main_right(self):
        self.f_r = ttk.Frame(self)
        self.f_r.pack(side='left', fill='y')
        self.frame7()
        self.frame_results()
        self.frame9()

    def frame7(self):
        self.f7 = ttk.Frame(self.f_r)
        self.f7.pack(side='top', fill='x')
        self.f7.columnconfigure(1, weight=1)

        ttk.Label(self.f7, text='Analysing: ').grid(row=1, column=1, sticky=W)
        val = list(val_proof)[1:]
        self.var_proof = StringVar()
        self.var_proof.set(_('cross_section'))
        proof = ttk.Combobox(self.f7, textvariable=self.var_proof, values=val)
        proof.grid(row=2, column=1, sticky=(W, E))
        proof.bind('<<ComboboxSelected>>', lambda event: self.calc())

        self.i_list = PhotoImage(file='icons/list_2.gif')
        calc = ttk.Button(self.f7, width=10, text='calc', command=self.calc, padding=0)
        calc.grid(row=2, column=2)

    def frame_results(self):
        headings = ['ff', 'f', 'values', '[]']
        settings = [(75, 'w'), (75, 'w'), (75, 'e'), (75, 'w')]

        self.tree = gui.treeview(self.f_r, headings, settings, 0)

    def frame9(self):
        self.f9 = ttk.Frame(self.f_r)
        self.f9.pack(side='top', fill='x')
        self.f9.columnconfigure(1, weight=1)

        ttk.Label(self.f9, text='Components: ').grid(row=3, column=1, sticky=W)
        self.var_element = StringVar()
        element = ttk.Combobox(self.f9, textvariable=self.var_element)
        element.grid(row=2, column=1, sticky=(W, E))
        element.bind('<<ComboboxSelected>>', lambda event: self.restore_notes())
        self.element = element

        self.img_del = PhotoImage(file="icons/del.gif")
        button = ttk.Button(self.f9, width=4, text='del', padding=0, command=self.del_note)
        button.grid(row=2, column=3)

        self.img_add = PhotoImage(file="icons/add.gif")
        button = ttk.Button(self.f9, width=4, text='add', padding=0, command=self.add_note)
        button.grid(row=2, column=2)

    def calc(self):
        self.disable_widgets()
        self.enable_widgets()

        values = self.get_variables_from_gui()
        results = Calc(values).get_results()

        self.add_to_tree(results)
        self.store = [values, results]

    def add_to_tree(self, results):
        self.tree.delete(*self.tree.get_children())
        results_dc = deepcopy(results)
        for result in results_dc:
            main_result = result.pop()
            id = self.tree.insert('', 'end', text=main_result.pop(0), values=(main_result))
            for semi_result in result:
                self.tree.insert(id, 'end', text=semi_result.pop(0), values=semi_result)

    def check_invoke(self):
        values = self.get_variables_from_gui()
        values['var_proof'] = 'check'
        results = Calc(values).get_results()
        self.add_to_checkview(results)

    def add_to_checkview(self, results):  # alternative to 'add_to_tree'
        self.check_view.delete(*self.check_view.get_children())

        cats = [
            (2, 5, 'Tragsicherheit'),
            (6, 9, 'Festigkeit'),
            (10, 11, 'Verformungen'),
            (12, 14, 'Kriechen'),
            (15, 16, 'Schwinden'),
            (19, 26, 'Bemessungswerte')
        ]

        for cat in cats:
            f, t, content = cat

            id = self.check_view.insert('', 'end', text=content, values='')
            rslts = results[0]
            rslts.sort(key=lambda x: int(x[0]))
            print('test = {}'.format(rslts))
            for rslt in rslts[f - 1:t]:
                print(cat, rslt)
                self.check_view.insert(id, 'end', text='({})'.format(rslt[0]), values=(rslt[1:]))

            if content in ('Tragsicherheit', 'Festigkeit', 'Bemessungswerte'):
                self.check_view.item(id, open=TRUE)

    def get_variables_from_gui(self):
        var = {}
        for k, v in self.__dict__.items():
            if k.startswith('var'):
                var[k] = v.get()
        return var

    def disable_widgets(self):
        widgets = [
            self.f_pss, self.f_pss_add,
            self.l_asw, self.f_asw,
            self.f_ar,
            self.l_as_sup, self.f_as_sup,
            self.l_al, self.f_al,
            self.f_delta_dv,
            self.f_ned, self.f_ved, self.f_med,
            self.lf_4332,
            self.lf_4333,
        ]

        for item in widgets:
            item.grid_remove()

    def enable_widgets(self):
        widget = {
            _('cross_section'): [

            ],
            'Querschnitt - Lamelle': [
                self.f_pss, self.f_pss_add,
                self.l_as_sup, self.f_as_sup,
                self.l_al, self.f_al,
                self.f_ned, self.f_ved, self.f_med
            ],
            _('4332'): [
                self.lf_4332,
                self.f_delta_dv, self.f_med
            ],
            _('4333'): [
                self.lf_4333,
                self.l_asw, self.f_asw,
            ]
        }
        for item in widget[self.var_proof.get()]:
            item.grid()

    def add_note(self):
        print('add_note')
        name = self.var_element.get()
        print(name)
        if name != '':
            self.project_components[name] = self.store
            print(self.project_components)
            self.update_notes()

    def del_note(self):
        print('del_note')
        name = self.var_element.get()
        if name != '':
            del self.project_components[name]
            print(self.project_components)
            self.update_notes()

    def update_notes(self):
        names = list(self.project_components.keys())
        print(names)
        self.val_element = ['test3', 'test4']
        self.element['values'] = names

    def restore_notes(self):
        print('restore_notes')
        name = self.var_element.get()
        print(name)
        if name != '':
            vals, rslts = list(self.project_components[name])
            print('vals = {} \nrslts = {}'.format(vals, rslts))

            for k, v in vals.items():
                print(k, v)
                if k not in ['var_element']:
                    try:
                        func = getattr(self, k)
                        func.set(v)
                    except:
                        pass

            self.add_to_tree(list(rslts))


def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
