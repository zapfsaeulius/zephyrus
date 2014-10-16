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

from math import sqrt, pi, cos, sin, radians, exp
from funcs import cot, cmp
from params import *

class Cat26213:
    def __init__(self, inp):
        beton = inp['var_beton']
        betonstahl = inp['var_betonstahl']
        ss_cat = inp['var_ss_cat']
        spannstahl = inp['var_spannstahl']
        lamelle = inp['var_lamelle']

        self.gamma_c = inp['var_gamma_c']
        self.gamma_s = inp['var_gamma_s']
        self.roh = inp['var_roh']
        self.ke = inp['var_ke']
        self.eta_t = inp['var_eta_t']
        self.epsilon_c1d = epsilon_c1d  # inp['var_\u03B5c1d']
        self.epsilon_c2d = epsilon_c2d  # inp['var_\u03B5c2d']
        self.kc = inp['var_kc']

        self.dmax = inp['var_dmax']
        self.alpha = inp['var_alpha']
        self.beta = inp['var_beta']
        self.delta = inp['var_delta']

        self.lc = inp['var_lc']

        self.es = es


        # Kriechen
        # (12)
        self.epsilon_c_el = 2 # ???
        # (13)
        self.phi_rh = 1 # ???
        self.beta_t0 = 0.8 # ???
        self.beta_t_t0 = 0.7 # ???
        # (14)
        self.sigma_c = 1 # ???

        # Schwinden
        # (15)
        self.epsilon_ca_t = 2 # ???
        # (16)
        self.beta_t_ts = 0.9 # ???
        self.epsilon_cd_8 = 0.8 # ???

        # Geometrische Imperfektionen
        self.l = 3 # ???
        self.m = 3 # ???

        # (23)
        self.fck_t = 1 # ???

        self.f_43322 = inp['var_f_43322']
        self.f_43323 = inp['var_f_43323']
        self.f_43324 = inp['var_f_43324']

        self.rho_l = 2200  # [kg/m3]
        self.es_bg = 205000 # [N/mm2]

        self.f_l = 0

        self.fck, self.fctm, self.beta_fc = values_concrete[beton]
        self.fsk, self.ks, self.epsilon_ud = values_reinforcing_steel[betonstahl]
        self.fpk, self.fp0_1k = values_prestressing_steel[ss_cat][spannstahl]

        if lamelle != '':
            self.flk, self.el = values_adhesive_reinforcement[lamelle]

        self.semi_rslts = []
        self.check_list = []

    def __str__(self):
        list_of_meths = [
            '(1) rd = {}'.format(self.rd()),
            '(2) fcd = {}'.format(self.fcd()),
            '(3) \u03C4cd = {}'.format(self.tau_cd()),
            '(4) fsd = {}'.format(self.fsd()),
            '(5) fpd = {}'.format(self.fpd()),
            '(6) fcm = {}'.format(self.fcm()),
            '(7) fctk0_05 = {}'.format(self.fctk0_05()),
            '(8) fctk0_95 = {}'.format(self.fctk0_95()),
            '(9) \u03B7ll = {}'.format(self.eta_l()),
            '(10) Ecm = {}'.format(self.ecm()),
            '(11) \u03B7lE = {}'.format(self.eta_le()),
            '(12) \u03B5cc(t) = {}'.format(self.epsilon_cc_t()),
            '(13) \u03C6(t,t0) = {}'.format(self.phi_t_t0()),
            '(14) \u03B2\u03c3c = {}'.format(self.beta_sigma_c()),
            '(15) \u03B5cs(t) = {}'.format(self.epsilon_cs_t()),
            '(16) \u03B5cd(t) = {}'.format(self.epsilon_cd_t()),
            '(17) \u03B1i = {}'.format(self.alpha_i()),
            '(18) \u03B1im = {}'.format(self.alpha_im()),
            '(26) \u03B7fc = {}'.format(self.eta_fc()),
        ]
        return '\n'.join(map(str, list_of_meths))

    def add(self, rslt, ff, f, unit):
        if ff not in self.check_list:
            if ff != 'f':
                self.check_list.append(ff)
            if ff.startswith('!'):
                ff = ' '
            self.semi_rslts.append(['{}'.format(ff), f, rslt, unit])

    def get_rslt(self):
        semi_rslts = self.semi_rslts[:]
        del self.semi_rslts[:]
        del self.check_list[:]
        return semi_rslts

    def a_cir(self, dm, s):
        term = dm**2*pi/4*1000/s
        return term

    def as_(self, dm, s):
        as_ = self.a_cir(dm,s)
        self.add(round(as_), '!as_', 'As_', 'mm2')
        return as_

    def asw(self, dm, s):
        asw = self.a_cir(dm, s)
        self.add(round(asw), '!asw', 'Asw', 'mm2')
        return asw

##  eta \u03B7

    # Grenzzustaende der Tragsicherheit

    def rd(self):
        """(1)"""
        self.add(None, '1', 'Rd', None)

    def fcd(self):
        """(2)"""
        print(self.eta_fc, self.eta_t, self.fck, self.gamma_c)
        term = self.eta_fc()*self.eta_t*self.fck/self.gamma_c
        term = round(term*2)/2
        self.add(term, '2', 'fcd', 'N/mm2')
        return term

    def tau_cd(self):
        """(3)"""
        term = 0.3*self.eta_t*sqrt(self.fck)/self.gamma_c
        term = round(term*2, 1)/2
        self.add(term, '3', '\u03C4cd', 'N/mm2')
        return term

    def fsd(self):
        """(4)"""
        term = self.fsk/self.gamma_s
        term = round(term)
        self.add(term, '4', 'fsd', 'N/mm2')
        return term

    def fpd(self):
        """(5)"""
        term = self.fp0_1k/self.gamma_s
        term = round(term)
        self.add(term, '5', 'fpd', 'N/mm2')
        return term

    # Beton; Festigkeit

    def fcm(self):
        """(6)"""
        term = self.fck+8
        self.add(term, '6', 'fcm', 'N/mm2')
        return term

    def fctk0_05(self):
        """(7)"""
        term = 0.7*self.fctm
        self.add(round(term, 2), '7', 'fctk0_05', 'N/mm2')
        return term

    def fctk0_95(self):
        """(8)"""
        term = 1.3*self.fctm
        self.add(round(term, 2), '8', 'fctk0_95', 'N/mm2')
        return term

    def eta_l(self):
        """(9)"""
        term = 0.4 + 0.6*self.roh/2200
        self.add(round(term, 2), '9', '\u03B7l', '-')
        return term

    # Beton; Elastische Verformungen

    def ecm(self):
        """(10)"""
        term = self.ke*self.fcm()**(1/3)
        self.add(round(term), '10', 'Ecm', 'N/mm2')
        return term

    def eta_le(self):
        """(11)"""
        term = (self.roh/2200)**2
        self.add(round(term), '11', '\u03B7lE', '-')
        return term

    # Beton; Kriechen

    def epsilon_cc_t(self):
        """(12)"""
        term = self.phi_t_t0()*self.epsilon_c_el
        self.add(round(term, 2), '12', '\u03B5cc(t)', '?')
        return term

    def phi_t_t0(self):
        """(13)"""
        term = self.phi_rh*self.beta_fc*self.beta_t0*self.beta_t_t0
        self.add(round(term, 2), '13', '\u03C6(t,t0)', '?')
        return term

    def beta_sigma_c(self):
        """(14)"""
        term = exp(1.5*(self.sigma_c/(self.fck-0.45)))
        self.add(round(term, 2), '14', '\u03B2\u03c3c', '?')
        return term

    # Beton; Schwinden

    def epsilon_cs_t(self):
        """(15)"""
        term = self.epsilon_cd_t() + self.epsilon_ca_t
        self.add(round(term, 3), '15', '\u03B5cs(t)', '?')
        return term

    def epsilon_cd_t(self):
        """(16)"""
        term = self.beta_t_ts*self.epsilon_cd_8
        self.add(round(term, 2), '16', '\u03B5cd(t)', '?')
        return term

    # Geometrische Imperfektionen

    def alpha_i(self):
        """(17)"""
        term = 0.01/sqrt(self.l)

        if term >= 1/200:
            term = 1/200
        elif term <= 1/300:
            term = 1/300
        else:
            term

        self.add(round(term), '17', '\u03B1i', '?')
        return term

    def alpha_im(self):
        """(18)"""
        term = self.alpha_i()*sqrt(0.5*(1.0+1.0/self.m))
        self.add(round(term, 2), '18', '\u03B1im', '?')
        return term

    # Tragwerksgeometrie

    def beff(self):
        """(19)"""
        term = self.beff_i + self.bw
        term = self.b if term >= self.b else term
        self.add(round(term, 2), '19', 'beff', 'm')
        return term

    def beff_i(self):
        """(20)"""
        pass



    # Bemessungswerte

    def eta_fc(self):
        """(26)"""
        term = (30/self.fck)**(1/3)
        term = 1.0 if term >= 1.0 else term
        self.add(round(term, 3), '26', '\u03B7fc', '-')
        return term

    # 4.3 Nachweis der Tragsicherheit

    # 4.3.3 Querkraft

    def vrd(self, md, mrd, d, dmax, dv):
        """ (35) """
        term = self.kd(md, mrd, d, dmax)*self.tau_cd()*dv
        if md == 1 or mrd == 1:
            self.add(round(term, 1), '35', 'vRd', 'N/mm')
        else:
            self.add(round(term, 1), '35', 'vRd_md/mRd', 'N/mm')
        return term

    def kd(self, md, mrd, d, dmax):
        """ (36) """
        term = 1/(1+self.epsilon_v(md, mrd)*d*self.kg(dmax))
        self.add(round(term, 2), '36', 'kd', '-')
        return term

    def kg(self, dmax):
        """ (37 """
        if self.lc == 1 or self.fck > 70:
            dmax = 0  # Dmax in mm
            self.add(dmax, 'f', 'Dmax', 'mm')

        term = 48/(16+dmax)
        self.add(round(term, 2), '37', 'kg', '-')
        return term

    def epsilon_v(self, md, mrd):
        """" (38, 39) """
        factor = 1

        if self.f_43323 == 1:
            coefficient = 1.5
            factor *= coefficient
            self.add(coefficient, 'f', '4.3.3.2.3', '-')

        if self.f_43324 == 1:
            delta = radians(self.delta)
            coefficient = 1/(sin(delta)**4+cos(delta)**4)
            factor *= coefficient
            self.add(round(coefficient, 2), 'f', '4.3.3.2.4', '-')

        if self.f_43322 == 0:
            term = (self.fsd()/self.es)*(md/mrd)*factor
            self.add(round(term, 4), '38', '\u03B5v', '-')
        else:
            term = 1.5*self.fsd()/self.es*factor
            self.add(round(term, 4), '39', '\u03B5v', '-')

        return term

    # (40) *
    def alpha(self, alpha):
        return radians(alpha)

    # (43) *
    def vrd_s(self, asw, s, z):
        alpha = radians(self.alpha)
        vrd_s = asw/s*z*self.fsd()*cot(alpha)
        self.add(round(vrd_s*1e-3, 1), '43', 'VRd,s*', 'kN')
        return vrd_s

    def vrd_s_asw(self, vrd_s, s, z, alpha):
        vrd_s_asw = vrd_s*1e3*s/(z*self.fsd()*cot(self.alpha(alpha)))
        self.add(round(vrd_s_asw), '43_', 'VRd,s_asw*', 'mm2')
        return vrd_s_asw

    # (44) *
    def vrd_sb(self, asw, s, z):
        alpha, beta = radians(self.alpha), radians(self.beta)
        vrd_s = asw/s*z*self.fsd()*(cot(alpha)+cot(beta))*sin(beta)
        self.add(round(vrd_s*1e-3, 1), '44', 'VRd,s_\u03B2*', 'kN')
        return vrd_s

    # (45)
    def vrd_c(self, bw, z, kc):
        alpha = radians(self.alpha)
        vrd_c = bw*z*kc*self.fcd()*sin(alpha)*cos(alpha)
        self.add(round(vrd_c*1e-3, 1), '45', 'VRd,c*', 'kN')
        return vrd_c

    # (46)
    def vrd_cb(self, bw, z, kc, alpha, beta):
        alpha, beta = radians(alpha), radians(beta)
        vrd_c = bw*z*kc*self.fcd()*(cos(alpha)+cot(beta)*sin(alpha))*sin(alpha)
        self.add(round(vrd_c*1e-3, 1), '46', 'VRd,c_\u03B2*', 'kN')
        return vrd_c

    # (50)*
    def ftvd(self, vd, alpha):
        ftvd = vd*1e3*cot(self.alpha(alpha))
        self.add(round(ftvd*1e-3, 1), '50', 'FtVd*', 'kN')
        return ftvd

    def ftvd_as(self, vd, alpha):
        ftvd_as = self.ftvd(vd, alpha)/self.fsd()/2
        self.add(round(ftvd_as, 1), '50_', 'FtVd_as*', 'mm2')
        return ftvd_as

    # (110) *
    def roh_w(self):
        roh_w = 0.001*sqrt(self.fck/30)*500/self.fsk
        self.add(round(roh_w, 4), '110', '\u03C1w*', 'mm2')
        return roh_w

    def roh_w_asw(self, s, bw):
        roh_w_asw = self.roh_w()*s*bw
        self.add(round(roh_w_asw, 1), '110_', '\u03C1w_asw*', 'mm2')
        return roh_w_asw



    # (56)
    def ke(self, mxd, myd, vd, ax, ay, dv):
        ke = 1/(1+self.eu(mxd, myd, vd)/self.b_circle(ax, ay, dv))
        self.add(round(ke, 1), '56', 'ke*', '-')
        return ke

    def eu(self, mxd, myd, vd):
        eu = sqrt(mxd**2+myd**2)/vd*1e3
        self.add(round(eu, 1), '!', 'ke*', 'mm')
        return eu

    def b_circle(self, ax, ay, dv):
        bc = sqrt(4/pi*((ax+dv)*(ay+dv)-dv**2*(1-pi/4)))
        self.add(round(bc, 1), '!', 'bc*', '-')
        return bc

    def mrd_circle(self, roh, d):
        mrdc = roh*d**2*self.fsd()*(1-(roh*self.fsd())/(2*self.fcd()))
        self.add(round(mrdc*1e-6, 1), '!', 'bc*', 'kNm')
        return mrdc*1e-3

    def bs(self, lx, ly):
        bs = 1.5*sqrt(self.rs(lx)*self.rs(ly))
        self.add(round(bs, 1), '!', 'bs*', 'mm')
        return bs

    def rs(self, l):
        rs = 0.22*l
        self.add(round(rs, 1), '!', 'rs*', 'mm')
        return rs

    def msd_(self, vd, eu_, bs):
        msd_ = vd*(1/8+abs(eu_)/(2*bs))
        return msd_

    def eu_(self, md, vd):
        eu_ = md/vd*1e3
        self.add(round(eu_, 1), '!', 'eu_*', 'mm')
        return eu_

    def u0(self, ax, ay, dv0, ke):
        ax = cmp(ax, 3*dv0)
        ay = cmp(ay, 3*dv0)
        u0 = 2*(ax+ay)+dv0*pi
        return ke*u0

    def u1(self, a_korb, dv1, ke_u1):
        u1 = 4*a_korb+dv1*pi
        return ke_u1*u1

    def as_bg0(self, ax, ay, dv0, roh_w_bg):
        as_bg0 = (2*(ax+ay)+2*(0.25+0.75/2)*dv0*pi)*0.75*dv0*roh_w_bg
        return as_bg0




    # (57)
    def vrd_c0(self, kr, dv, u):
        vrd_c0 = kr*self.tau_cd()*dv*u
        self.add(round(vrd_c0, 1), '57', 'VRd,c*', 'N/mm')
        return vrd_c0

    # (58)
    def kr(self, psi, d, kg):
        kr = 1/(0.45+.18*psi*d*kg)
        kr = cmp(kr, 2)
        self.add(round(kr, 1), '58', 'kr*', '-')
        return kr

    # (59)
    def psi(self, rs, d, msd, mrd):
        psi = 1.5*(rs/d)*(self.fsd()/self.es)*(msd/mrd)**(3/2)
        self.add(round(psi, 1), '59', '\u03C8*', '-')
        return psi

    # (67)
    def vrd_cs0(self, kr, dv0, u0, ke, sigma_sd, as_bg0):
        vrd_cs0 = kr*self.tau_cd()*dv0*u0+ke*sigma_sd*as_bg0
        self.add(round(vrd_cs0, 1), '67', 'VRd,cs0*', 'kN')
        return vrd_cs0

    # (68)
    def sigma_sd(self, psi, d, dm_sw):
        print(self.es_bg, psi, self.fbd(), self.fsd(), d, dm_sw)
        sigma_sd = (self.es_bg*0.0107)/6*(1+(2.1/self.fsd())*(d/dm_sw))
        print(sigma_sd)
        sigma_sd = cmp(sigma_sd, self.fsd())

        self.add(round(sigma_sd, 1), '68', 's_sd*', 'N/mm2')
        return sigma_sd

    # (69)
    def vrd_cc0(self, ksys, kr, dv0, u0):
        vrd_cc0 = ksys*kr*self.tau_cd()*dv0*u0
        limit = 3.5*self.tau_cd()*dv0*u0
        vrd_cc0 = cmp(vrd_cc0, limit)
        self.add(round(vrd_cc0, 1), '69', 'VRd,cc0*', 'kN')
        return vrd_cc0



    # 4.4 Nachweis der Gebrauchstauglichkeit

    def t(self, h):
        t = h/3*1e-3
        self.add(round(t, 3), '!', 't*', 'm')
        return t

    # (98)
    def fctd(self, h):
        fctd = self.kt(h)*self.fctm
        self.add(round(fctd, 1), '98', 'fctd*', 'N/mm2')
        return fctd

    # (99)
    def kt(self, h):
        kt = 1/(1+0.5*self.t(h))
        self.add(round(kt, 1), '99', 'kt*', '-')
        return kt

    # (103)
    def fbd(self):
        fbd = 1.4*self.fctm/self.gamma_c
        self.add(round(fbd, 1), '103', 'fbd*', 'N/mm2')
        return fbd

def main():
    test = Cat26213(test_dict)
    print(test)
    for rslt in test.get_rslt():
        print(rslt)


if __name__ == '__main__':
    main()
