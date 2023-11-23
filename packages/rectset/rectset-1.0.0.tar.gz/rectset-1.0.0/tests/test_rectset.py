#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Created: 11/2023
# Author: Carmelo Mordini <cmordini@phys.ethz.ch>


import numpy as np
from rectset import rectangle_electrode as rect
from rectset import pseudopotential as ps


def test_rectangle_electrode():
    # Square electrode of 20 x 20 um
    # Potential and derivatives along one line at 50 um above the trap plane

    x1, y1 = -10e-6, -10e-6
    x2, y2 = 10e-6, 10e-6

    x = np.linspace(-100, 100) * 1e-6
    y = 0
    z = 50e-6

    pot = rect.rect_el_potential(x, y, z, x1, x2, y1, y2)  # ndarray, shape (50,)
    grad = rect.rect_el_gradient(x, y, z, x1, x2, y1, y2)  # ndarray, shape (50, 3)
    hess = rect.rect_el_hessian(x, y, z, x1, x2, y1, y2)  # ndarray, shape (50, 3, 3)

    assert pot.shape == (50,)
    assert grad.shape == (50, 3)
    assert hess.shape == (50, 3, 3)


def test_pseudopotential():
    # Infinite pair of RF electrodes, large 100 um and separated by 40 um
    # Pseudopotential and derivatives experienced by a 40Ca+ ion with
    # RF voltage amplitude = 50 V
    # RF voltage frequency = 30 MHz

    a = 40e-6
    w = 100e-6
    rf_v = 50  # volt
    rf_freq_mhz = 30  # megahertz
    ion_unit_charge = 1  # elementary charges
    ion_mass_amu = 40  # amu

    K = (rf_v**2 * ion_unit_charge) / (
        ion_mass_amu * rf_freq_mhz**2
    )  # trap and ion scaling factor

    x = np.linspace(-100, 100) * 1e-6
    y = 0
    z = 50e-6

    pspot = K * ps.pseudo_potential(x, y, z, a, w)  # ndarray, shape (50,)
    psgrad = K * ps.pseudo_gradient(x, y, z, a, w)  # ndarray, shape (50, 3)
    pshess = K * ps.pseudo_hessian(x, y, z, a, w)  # ndarray, shape (50, 3, 3)

    assert pspot.shape == (50,)
    assert psgrad.shape == (50, 3)
    assert pshess.shape == (50, 3, 3)
