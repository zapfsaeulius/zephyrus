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
#    along with Zephyrus.  If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------

from cat_262 import Cat26213
from params import epsilon_c2d, test_dict
from math import sqrt
from sympy.solvers import solve
from sympy import Symbol

class RectL(Cat26213):
    
    def __init__(self, inp):
        Cat26213.__init__(self, inp)
        
        self.dm = inp['var_dm']
        self.s = inp['var_s']
        self.tl = inp['var_tl']
        self.bl = inp['var_bl']
        self.b = inp['var_b']
        self.h = inp['var_h']
        self.ds = inp['var_d']
        self.dl = self.h+self.tl/2
        
        self.lmtl = 0

    def __str__(self):
        x = self.x()
        list_of_meths = [
            'x = {}'.format(x),
            'zs = {}'.format(self.zs()),
            'zl = {}'.format(self.zl()),
            'mrd = {}'.format(self.mrd(x)),
            '_dcd = {}'.format(self._dcd(x)),
            '_epsilon_s = {}'.format(self.epsilon_s(x)),
            'zsd = {}'.format(self.zsd(x)),
            '_epsilon_l = {}'.format(self._epsilon_l(x)),
            '_sigma_l = {}'.format(self._sigma_l(x)),
            '_zld = {}'.format(self._zld(x)),
            'Eh = {}'.format(round(self._dcd(x)+self.zsd(x)+self._zld(x)), 3)
        ]
        return '\n'.join(map(str, list_of_meths))

    def _dcd(self, x):
        term = -self.b*0.85*x*self.fcd()
        if isinstance(x, float):
            self.add(round(term*1e-3, 1), '!_dcd', 'Dc*', 'kN')
        return term

    def epsilon_s(self, x):
        term = epsilon_c2d/x*(self.ds-x)
        self.add(round(term*1e3, 2), '!es', '\u03B5s*', '\u2030')
        return term

    def zsd(self, x):
        term = self.as_(self.dm, self.s)*self.fsd()
        self.add(round(term*1e-3, 1), '!_zsd', 'Zs*', 'kN')
        return term

    def _epsilon_l(self, x):
        term = epsilon_c2d/x*(self.dl-x)
        if isinstance(x, float):
            self.add(round(term*1e3, 2), '!_el', '\u03B5l*', '\u2030')
        return term

    def _sigma_l(self, x):
        if self.lmtl == 0:
            term = self._epsilon_l(x)*self.el
        else:
            term = 2800
        if isinstance(x, float):
            self.add(round(term, 1), '!_sl', '\u03C3l*', 'N/mm2')
        return term

    def _zld(self, x):
        al = self.tl*self.bl
        term = al*self._sigma_l(x)
        if isinstance(x, float):
            self.add(round(term*1e-3, 1), '!_zld', 'Zl*', 'kN')
        return term

    def x(self):
        while True:
            x = Symbol('x')
            term = max(solve(self._dcd(x)+self.zsd(x)+self._zld(x), x))

            if self._sigma_l(term) > self.flk:
                self.lmtl = 1
            else:
                break

        self.add(round(term), '!x', 'x*', 'mm')
        return term

    def zs(self):
        term = self.ds-0.425*self.x()
        self.add(round(term), '!zs', 'zs*', 'mm')
        return term

    def zl(self):
        term = self.dl-0.425*self.x()
        self.add(round(term), '!zl', 'zl*', 'mm')
        return term

    def mrd(self, x):
        term = self.zsd(x)*self.zs()+self._zld(x)*self.zl()
        self.add(round(term*1e-6, 1), '!mrd', 'MRd*', 'kNm')
        return term

    def xds(self, x):
        term = x/self.ds
        self.add(round(term, 2), '!xds', 'x/ds*', '-')
        return term

    def xdl(self, x):
        term = x/self.dl
        self.add(round(term, 2), '!xdl', 'x/dl*', '-')
        return term


class Rect(Cat26213):
    def __init__(self, inp):
        Cat26213.__init__(self, inp)

        self.dm = inp['var_dm_inf']
        self.s = inp['var_s_inf']
        self.b = inp['var_b']
        self.h = inp['var_h']
        self.d = inp['var_d_inf']

    def __str__(self):
        list_of_meths = [
            'x = {}'.format(self.x()),
            'z = {}'.format(self.z()),
            'mrd = {}'.format(self.mrd()),
            'mrd_ = {}'.format(self.mrd_()),
            'xd = {}'.format(self.xd()),
            'epsilon_s = {}'.format(self.epsilon_s()),
            'mrd_max,035 = {}'.format(self.mrd_max035()),
            'mrd_max,050 = {}'.format(self.mrd_max050()),
            'as_min = {}'.format(self.as_min())
        ]
        return '\n'.join(map(str, list_of_meths))

    def x(self):
        x = self.as_(self.dm, self.s)*self.fsd()/(0.85*self.b*self.fcd())
        self.add(round(x), '!1', 'x', 'mm')
        return x

    def z(self):
        z = self.d-0.425*self.x()
        self.add(round(z), '!2', 'z', 'mm')
        return z

    def mrd(self):
        mrd = self.as_(self.dm, self.s)*self.fsd()*self.z()
        self.add(round(mrd*1e-6, 1), '!3', 'MRd', 'kNm')
        return mrd

    def mrd_(self):
        mrd_ = self.fctd(self.h)*self.b*self.h**2/6
        self.add(round(mrd_*1e-6, 1), '!4', 'Mrd', 'kNm')
        return mrd_

    def xd(self):
        xd = self.x()/self.d
        self.add(round(xd, 2), '!5', 'x/d', '-')
        return xd

    def epsilon_s(self):
        epsilon_s = epsilon_c2d/self.x()*(self.d-self.x())
        self.add(round(epsilon_s*1e3, 2), '!6', '\u03B5s', '\u2030')
        return epsilon_s

    def mrd_max035(self):
        x = 0.35
        mrd_max = x*self.d*0.85*self.b*self.fcd()*(self.d-(x*self.d*0.85)/2)
        self.add(round(mrd_max*1e-6, 1), '!7', 'MRd_max,035', 'kNm')
        return mrd_max

    def mrd_max050(self):
        x = 0.5
        mrd_max = x*self.d*0.85*self.b*self.fcd()*(self.d-(x*self.d*0.85)/2)
        self.add(round(mrd_max*1e-6, 1), '!8', 'MRd_max,050', 'kNm')
        return mrd_max

    def as_min(self):
        fcd = self.fcd()
        as_min = self.b*fcd/self.fsd()*(self.d-sqrt(
            (3*self.d**2*fcd-self.fctd(self.h)*self.h**2)/(3*fcd)))
        self.add(round(as_min, 1), '!9', 'As,min', 'mm2')
        return as_min


def main():
    test = RectL(test_dict)
    print(test)

if __name__ == '__main__':
    main()
