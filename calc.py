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

from cat_262 import Cat26213
from cat_rect import Rect, RectL
from params import val_proof

from collections import OrderedDict
from copy import deepcopy

class Calc():
    def __init__(self, inp):
        self.proof = inp['var_proof']

        self.dmax = inp['var_dmax']
        self.alpha = inp['var_alpha']
        self.beta = inp['var_beta']
        self.kc = inp['var_kc']
        self.dm = inp['var_dm_inf']
        self.s = inp['var_s_inf']
        self.dmw = inp['var_dmw']
        self.sw = inp['var_sw']
        self.ew = inp['var_ew']
        self.al = inp['var_bl']*inp['var_tl']
        self.h = inp['var_h']
        self.b = inp['var_b']

        self.d_inf = inp['var_d_inf']
        self.check_d_6 = inp['var_delta_dv']

        self.lamelle = inp['var_lamelle']

        self.bw = self.b

        self.ved = inp['var_ved']
        self.med = inp['var_med']
        self.md = self.med

        self.rslts = []

        getattr(self, val_proof[self.proof])(inp)

    def get_results(self):
        results = self.rslts[:]
        return results

    def check(self, inp):
        check = Cat26213(inp)
        print(check)
        self.rslts.append(check.get_rslt())

    def rectl(self, inp):
        rectl = RectL(inp)

        if self.b > 0 and self.d_inf > 0 and self.lamelle != '':
            x = float(rectl.x())

            dcd = rectl._dcd(x)
            self.rslts.append(rectl.get_rslt())
            zsd = rectl.zsd(x)
            self.rslts.append(rectl.get_rslt())
            zld = rectl._zld(x)
            self.rslts.append(rectl.get_rslt())
            sigma_l = rectl._sigma_l(x)
            self.rslts.append(rectl.get_rslt())
            mrd = rectl.mrd(x)
            self.rslts.append(rectl.get_rslt())
            xds = rectl.xds(x)
            self.rslts.append(rectl.get_rslt())
            xdl = rectl.xdl(x)
            self.rslts.append(rectl.get_rslt())
            epsilon_s = rectl.epsilon_s(x)
            self.rslts.append(rectl.get_rslt())
            epsilon_l = rectl._epsilon_l(x)
            self.rslts.append(rectl.get_rslt())

    def rect(self, inp):
        rect = Rect(inp)

        if self.d_inf != 0 and self.b != 0:
            rect.mrd()
            self.rslts.append(rect.get_rslt())
        if self.b != 0 and self.h != 0:
            mrd_ = rect.mrd_()
            self.rslts.append(rect.get_rslt())
        if self.b != 0 and self.d_inf != 0:
            xd = rect.xd()
            self.rslts.append(rect.get_rslt())
            epsilon_s = rect.epsilon_s()
            self.rslts.append(rect.get_rslt())
        if self.b != 0 and self.d_inf != 0 and self.h:
            as_min = rect.as_min()
            self.rslts.append(rect.get_rslt())
        if self.b != 0 and self.d_inf != 0:
            mrd_max = rect.mrd_max035()
            self.rslts.append(rect.get_rslt())
            mrd_max = rect.mrd_max050()
            self.rslts.append(rect.get_rslt())

    def cat_4332(self, inp):
        cat = Cat26213(inp)
        rect = Rect(inp)

        if self.check_d_6 >= self.d_inf/6:
            dv = self.d_inf-self.check_d_6
        else:
            dv = self.d_inf

        if self.d_inf > 0:
            vrd = cat.vrd(1, 1, self.d_inf, self.dmax, dv)
            self.rslts.append(cat.get_rslt())

        if self.b > 0 and self.d_inf > 0 and self.med > 0:
            mrd = rect.mrd()
            self.rslts.append(rect.get_rslt())

            vrd_mm = cat.vrd(self.med, mrd*1e-6, self.d_inf, self.dmax, dv)
            self.rslts.append(cat.get_rslt())

    def cat_4333(self, inp):
        # d, b, ved, dm, s, alpha, kc
        cat = Cat26213(inp)
        rect = Rect(inp)
        if self.d_inf != 0 and self.b != 0 and self.ved == 0:

            asw = rect.asw(self.dmw, self.ew)
            self.rslts.append(rect.get_rslt())
            z = rect.z()
            self.rslts.append(rect.get_rslt())
            print(rect.get_rslt())

            vrd_s = cat.vrd_s(asw, self.sw, z)
            self.rslts.append(cat.get_rslt())
            if self.beta != 90:
                vrd_s = cat.vrd_sb(asw, self.sw, z)
                self.rslts.append(cat.get_rslt())
        if self.d_inf != 0 and self.b != 0 and self.ved != 0:

            z = rect.z()
##            self.rslts.append(rect.get_rslt())

            vrd_s_asw = cat.vrd_s_asw(self.ved, self.s, z)
            self.rslts.append(cat.get_rslt())
        if self.d_inf != 0 and self.b != 0:

            z = rect.z()
##            self.rslts.append(rect.get_rslt())

            vrd_c = cat.vrd_c(self.bw, z, self.kc)
            self.rslts.append(cat.get_rslt())
            if self.beta != 90:
                vrd_c = cat.vrd_cb(self.bw, z, self.kc)
                self.rslts.append(cat.get_rslt())
        if self.ved != 0:
            ftvd_as = cat.ftvd_as(self.ved)
            self.rslts.append(cat.get_rslt())
        if self.d_inf != 0 and self.b != 0 and self.ved != 0:
            roh_w_asw = cat.roh_w_asw(self.s, self.bw)
            self.rslts.append(cat.get_rslt())

def main():
    pass

if __name__ == '__main__':
    main()
