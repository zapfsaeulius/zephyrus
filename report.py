# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#
# Name:        Zephyrus aka ZapfGenius
# Purpose:     Tool for Analysis and Design of Conrete Structures
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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from collections import OrderedDict
from datetime import datetime

import os

content_data = {'asdf': [{'var_dmw': 10, 'var_f_43322': 0, 'var_betonstahl': 'B500B', 'var_sw': 150, 'var_lamelle': 'CFK', 'var_med': 0.0, 'var_ved': 0.0, 'var_element': '', 'var_f_43324': 1.0, 'var_nl': 1, 'var_kc': 0.55, 'var_f_43323': 1.0, 'var_b': 1000, 'var_h': 250, 'var_ew': 150, 'var_cfk': '', 'var_dv': 0, 'var_d': 110, 'var_dm': 10, 'var_proof': 'Querschnitt', 'var_beton': 'C25/30', 'var_alpha': 45, 'var_c': 30, 'var_delta': 45, 'var_beta': 90, 'var_s': 150, 'var_al': 0}, [[['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 'z', 103, 'mm'], ['( )', 'MRd', 23.5, 'kNm']], [['( )', 't*', 0.05, 'm'], ['(99)', 'kt*', 1.0, '-'], ['(98)', 'fctd*', 2.5, 'N/mm2'], ['( )', 'Mrd', 9.5, 'kNm']], [['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 'x/d', 0.15, '-']], [['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 's', 17.32, '']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['( )', 't*', 0.05, 'm'], ['(99)', 'kt*', 1.0, '-'], ['(98)', 'fctd*', 2.5, 'N/mm2'], ['( )', 'As,min', 203.8, 'mm2']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'MRd_max,035', 50.6, 'kNm']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'MRd_max,050', 66.8, 'kNm']]]],
        'fdsa': [{'var_dmw': 10, 'var_f_43322': 0, 'var_betonstahl': 'B500B', 'var_sw': 150, 'var_lamelle': 'CFK', 'var_med': 0.0, 'var_ved': 0.0, 'var_element': '', 'var_f_43324': 1.0, 'var_nl': 1, 'var_kc': 0.55, 'var_f_43323': 1.0, 'var_b': 250, 'var_h': 500, 'var_ew': 150, 'var_cfk': '', 'var_dv': 0, 'var_d': 110, 'var_dm': 10, 'var_proof': 'Querschnitt', 'var_beton': 'C25/30', 'var_alpha': 45, 'var_c': 30, 'var_delta': 45, 'var_beta': 90, 'var_s': 150, 'var_al': 0}, [[['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 'z', 103, 'mm'], ['( )', 'MRd', 23.5, 'kNm']], [['( )', 't*', 0.05, 'm'], ['(99)', 'kt*', 1.0, '-'], ['(98)', 'fctd*', 2.5, 'N/mm2'], ['( )', 'Mrd', 9.5, 'kNm']], [['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 'x/d', 0.15, '-']], [['( )', 'As_', 524, 'mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'x', 16, 'mm'], ['( )', 's', 17.32, '']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['(4)', 'fsd*', 435, 'N/mm2'], ['( )', 't*', 0.05, 'm'], ['(99)', 'kt*', 1.0, '-'], ['(98)', 'fctd*', 2.5, 'N/mm2'], ['( )', 'As,min', 203.8, 'mm2']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'MRd_max,035', 50.6, 'kNm']], [['(25)', 'fc*', 1.0, '-'], ['(2)', 'fcd*', 16.5, 'N/mm2'], ['( )', 'MRd_max,050', 66.8, 'kNm']]]],
}

project_data = {
    'project': '02403, Neubau EFH Wiederkehr/Jenni, 6204 Sempach',
    'info': 'L1: Decke Ueber UG',
    'company': 'Studer Partner AG, Bauingenieure, 6206 Neuenkirch',
    'signature': 'mr',
    'version': 'Zephyrus v.3.1-beta',
    'path': 'Z:\\Zephyrus\\02403, Wiederkehr.z1s'
}

order = [
    'var_beton',
    'var_betonstahl',
    'var_dm',
    'var_s',
    'var_b',
    'var_h',
    'var_c',
    'var_d',
    'var_dv',
    'var_med',
]

included = [
    'var_beton',
    'var_betonstahl',
    'var_dm',
    'var_s',
    'var_h',
    'var_c',
    'var_b',
    'var_d',
]

customized = {
    'Querschnitt': [
        ''
    ],
    'Querschnitt - Lamelle': [
        ''
    ],
    '4.3.3 Querkraft ohne QB': [
        'var_dv', 'var_med'
        ],
    '4.3.3 Querkraft mit QB': [
        ''
        ]
}

sizes = {
    'var_beton': 'Beton',
    'var_betonstahl': 'Betonstahl',
    'var_dm': '\u2205',
}

units = {
    'var_dm': 'mm',
    'var_b': 'mm',
    'var_c': 'mm',
    'var_d': 'mm',
    'var_h': 'mm',
    'var_s': 'mm',
}

class Report():
    def __init__(self, project_data, content_data, report):
        self.c = canvas.Canvas('results.pdf', pagesize=A4)
        self.width, self.height = A4
        self.report = report

        self.pd = project_data
        self.cd = content_data
        self.page = 1
        self.detailed = 0

        self.print_content()

        self.c.save()
        os.startfile('results.pdf')

    def print_content(self):
        w, h = self.width, self.height-72

        self.set_frame()
        self.set_project_data()

        for name, content in self.cd.items():
            h = self.title_component(h, name)

            vals, rslts = list(content)
            h = self.title_analysis(h, vals['var_proof'])
            h = self.title_inputs_results(h)

            hi = h
            sorted_vals = OrderedDict((k, vals[k]) for k in order)
            for k, v in sorted_vals.items():
                if k in included or k in customized[vals['var_proof']]:
                    hi = self.inputs(hi, k, v)


            rh = h-300
            rw = 150
            vb = vals['var_b']
            vh = vals['var_h']
            vc = vals['var_c']
            f = 60/max(vb, vh, vc)
            print(vb*f, vh*f, f)
            self.c.setLineWidth(0.8)
            self.c.rect(rw, rh, vb*f, vh*f, fill=0)
            self.c.line(rw+vc*f, rh+vc*f, rw+vb*f-vc*f, rh+vc*f)
            self.c.setFont('Helvetica', 8)
            self.c.drawString(rw, rh+vh*f+12, vals['var_beton'])
            self.c.drawString(rw, rh+vh*f+4, vals['var_betonstahl'])
            self.c.setFont('Helvetica', 7)
            self.c.drawString((rw+(vb*f)/2-4), rh+vc*f+2, 'As')


            hr = h
            for rslt in rslts:
                hr = self.results(hr, rslt)
                if hr < 108:
                    w, hr = self.create_new_page()
                    hi = hr

            h = min(hi, hr)
            self.finish_line(h)

            if h < 108:
                w, h = self.create_new_page()

    def set_frame(self):
        w, h = self.width, self.height
        self.c.setLineWidth(0.8)
        self.c.rect(60, 30, w-80, h-50, fill=0)
        self.c.setLineWidth(0.4)
        self.c.line(60, h-51, w-20, h-51)
        self.c.setLineWidth(0.8)
        self.c.line(60, h-69, w-20, h-69)
        self.c.line(w-120, h-69, w-120, h-20)

    def set_project_data(self):
        w, h = self.width, self.height
        self.c.setFont('Helvetica', 9)
        self.c.drawString(70, h-33, self.pd['project'])
        self.c.drawString(70, h-45, self.pd['info'])
        self.c.drawString(70, h-63, self.pd['company'])
        self.c.drawRightString(w-130, h-63, self.pd['signature'])

        self.c.drawString(w-110, h-33, 'Page {}'.format(self.page))
        self.c.drawString(w-110, h-45, datetime.now().strftime('%d.%m.%y, %H:%M'))
        self.c.setFont('Helvetica', 8)
        self.c.drawString(w-110, h-63, self.pd['version'])

        self.c.setFont('Helvetica', 8)
        self.c.drawString(60, 20, self.pd['path'])

    def title_component(self, h, name):
        self.c.setFont('Helvetica', 9)
        h -= 36
        self.c.drawRightString(125, h, 'Component:')
        self.c.drawString(130, h, name)
        return h

    def title_analysis(self, h, name):
        self.c.setFont('Helvetica', 9)
        h -= 12
        self.c.drawRightString(125, h, 'Analysis:')
        self.c.drawString(130, h, name)
        return h

    def title_inputs_results(self, h):
        self.c.setFont('Helvetica', 9)
        h -= 12
        self.c.drawRightString(125, h, 'Inputs:')
        self.c.drawRightString(300, h, 'Results:')

        self.c.setLineWidth(0.8)
        self.c.setStrokeColorRGB(0.2, 0.5, 0.3)
        h -= 5
        self.c.line(90, h, 240, h)
        self.c.line(260, h, 510, h)

        return h

    def inputs(self, h, k, v):
        self.c.setFont('Helvetica', 8)
        h -= 10
        self.c.drawRightString(150, h, sizes.get(k, k.split('_')[1]))
        self.c.drawRightString(200, h, str(v))
        self.c.drawString(210, h, units.get(k, '-'))
        return h

    def results(self, h, rslt):
        self.c.setFont('Helvetica', 8)
        h -= 12
        self.c.drawString(300, h, rslt[-1][0])
        self.c.drawRightString(400, h, rslt[-1][1])
        self.c.drawRightString(450, h, str(rslt[-1][2]))
        self.c.drawString(475, h, rslt[-1][3])

        if self.report == 1:
            for semi_rslt in rslt[:-1]:
                self.c.setFont('Helvetica', 6)
                h -= 10
                self.c.drawString(320, h, semi_rslt[0])
                self.c.drawRightString(400, h, semi_rslt[1])
                self.c.drawRightString(450, h, str(semi_rslt[2]))
                self.c.drawString(475, h, semi_rslt[3])

        return h

    def finish_line(self, h):
        self.c.setLineWidth(0.8)
        self.c.setStrokeColorRGB(0.2,0.5,0.3)
        h -= 5
        self.c.line(90, h, 240, h)
        self.c.line(260, h, 510, h)

    def create_new_page(self):
        self.c.showPage()
        self.page += 1
        self.set_frame()
        self.set_project_data()
        return self.width, self.height-72

def main():
    Report(project_data, content_data, 0)

if __name__ == '__main__':
    main()
