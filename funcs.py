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

from math import pi, cos, sin, radians

def cot(x):
    return cos(x)/sin(x)

def cmp(x, y):
    if x <= y:
        return x
    else:
        return y


def f_delta(delta):
    factor = 1/(sin(radians(delta))**4+cos(radians(delta))**4)
    return factor











