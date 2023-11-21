#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 08:08:26 2022

@author: danielpipa
"""

import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph.widgets.RawImageWidget import RawImageGLWidget
from tqdm import tqdm
from scipy.ndimage import correlate
import math

dtype = 'float32'  # float32 is the fastest

Dx = .1e-3
Dz = Dx
Dt = 8e-9  # ok

# PML
# R, Np = 1e-5, 10
# R, Np = 1e-5, 20
# # R, Np = 1e-2, 30
# Lp = Np * Dx

Lx = 50e-3  # Block width
Lz = 50e-3  # Block height
Lt = 8e-6  # Simulation time

Nx = round(Lx / Dx)
Nz = round(Lz / Dz)
Nt = round(Lt / Dt)

c_scalar = 5490
# c = 1480

xsource = Nx//2
zsource = Nz//2

xscan = Nx//4
zscan = Nz//3

# show = True
show = False
if show:
    sfmt = pg.QtGui.QSurfaceFormat()
    sfmt.setSwapInterval(0)
    pg.QtGui.QSurfaceFormat.setDefaultFormat(sfmt)
    # app = pg.QtGui.QApplication([])
    app = pg.QtWidgets.QApplication([])
    riw = RawImageGLWidget(scaled=True)
    riw.show()

# Source signal
t = np.linspace(0, Lt - Dt, Nt, dtype=dtype)
f0 = 1e6  # Transducer central frequency
bwp = .8  # Bandwidth in percentage
bw = bwp * f0
t0 = 1 / f0
alpha = -(np.pi * bw / 2) ** 2 / np.log(np.sqrt(2) / 2)
s = -np.exp(-alpha * (t - t0) ** 2) * np.sin(2 * np.pi * f0 * (t - t0))
# s = -2*(t-t0)*f0*4*np.exp(-(t-t0)**2*f0**2*10)
# s = np.diff(s, append=0)
s /= np.max(np.abs(s))
s_int = np.cumsum(s)
# plt.plot(t, s, t, s_int)

#%%

def coeff1storder(N):
    "10.1111/j.1365-246X.2009.04305.x"
    c = np.zeros(N)
    for n in range(1, N + 1):
        m = np.arange(1, N + 1)
        m = m[m != n]
        p = np.prod(np.abs((2 * m - 1) ** 2 / ((2 * n - 1) ** 2 - (2 * m - 1) ** 2)))
        c[n - 1] = (((-1) ** (n + 1)) / (2 * n - 1)) * p

    c = c[None]
    return np.hstack((-np.flip(c), c))


def coeff2ndOrder(N):
    deriv_order = 2
    deriv_n_coef = 2 * np.floor((deriv_order + 1) / 2).astype('int') - 1 + N
    p = np.round((deriv_n_coef - 1) / 2).astype('int')
    A = np.arange(-p, p + 1) ** np.arange(0, 2 * p + 1)[None].T
    b = np.zeros(2 * p + 1)
    b[deriv_order] = math.factorial(deriv_order)
    h = np.zeros((deriv_n_coef, deriv_n_coef))
    h[deriv_n_coef // 2, :] = np.linalg.solve(A, b)
    h += h.T
    return h


accuracy = 8
border = 2*accuracy

c = np.zeros((Nz, Nz))
c[border:-border, border:-border] = c_scalar
# c[border:Nz//3, :] = c_scalar/2

c1stOrd = coeff1storder(accuracy//2)
c2ndOrd = coeff2ndOrder(accuracy)

px = np.zeros((Nz, Nx), dtype=dtype)
px_1 = np.zeros((Nz, Nx), dtype=dtype)
pz = np.zeros((Nz, Nx), dtype=dtype)
pz_1 = np.zeros((Nz, Nx), dtype=dtype)
# Ax = np.zeros((Nz, Nx), dtype=dtype)
# Ax_1 = np.zeros((Nz, Nx), dtype=dtype)
# Az = np.zeros((Nz, Nx), dtype=dtype)
# Az_1 = np.zeros((Nz, Nx), dtype=dtype)
Ax = np.zeros((Nz, Nx+1), dtype=dtype)
Ax_1 = np.zeros((Nz, Nx+1), dtype=dtype)
Az = np.zeros((Nz+1, Nx), dtype=dtype)
Az_1 = np.zeros((Nz+1, Nx), dtype=dtype)

# px = np.zeros((Nz-2, Nx-2), dtype=dtype)
# px_1 = np.zeros((Nz-2, Nx-2), dtype=dtype)
# pz = np.zeros((Nz-2, Nx-2), dtype=dtype)
# pz_1 = np.zeros((Nz-2, Nx-2), dtype=dtype)
# Ax = np.zeros((Nz-2, Nx-2), dtype=dtype)
# Ax_1 = np.zeros((Nz-2, Nx-2), dtype=dtype)
# Az = np.zeros((Nz-2, Nx-2), dtype=dtype)
# Az_1 = np.zeros((Nz-2, Nx-2), dtype=dtype)


p = np.zeros((Nz, Nx), dtype=dtype)
p_1 = np.zeros((Nz, Nx), dtype=dtype)
p_2 = np.zeros((Nz, Nx), dtype=dtype)

Ascan = np.zeros((Nt, 2))

for k in tqdm(range(1, Nt)):
    px_1, pz_1, Ax_1, Az_1 = px, pz, Ax, Az

    # px = px_1 - c[1:-1, 1:-1] ** 2 * (Dt / Dx) * correlate(Ax_1, c1stOrd, mode='constant')
    # pz = pz_1 - c[1:-1, 1:-1] ** 2 * (Dt / Dx) * correlate(Az_1, c1stOrd.T, mode='constant')
    px = px_1 - c ** 2 * (Dt / Dx) * correlate(Ax_1, c1stOrd, mode='constant')[:, 1:]
    pz = pz_1 - c ** 2 * (Dt / Dx) * correlate(Az_1, c1stOrd.T, mode='constant')[1:, :]
    # px = px_1 - c ** 2 * (Dt / Dx) * correlate(Ax_1, c1stOrd, mode='reflect')[:, 1:]
    # pz = pz_1 - c ** 2 * (Dt / Dx) * correlate(Az_1, c1stOrd.T, mode='reflect')[1:, :]
    # px[Nz//2-1, Nx//2-1] += s_int[k]/2
    # pz[Nz//2-1, Nx//2-1] += s_int[k]/2
    px[zsource, xsource] += s_int[k]/2
    pz[zsource, xsource] += s_int[k]/2
    # Dirichlet boundary conditions
    # px[0, :] = 0
    # px[-1, :] = 0
    # px[:, 0] = 0
    # px[:, -1] = 0
    # pz[0, :] = 0
    # pz[-1, :] = 0
    # pz[:, 0] = 0
    # pz[:, -1] = 0
    # px[0, :] = px[1, :]
    # px[-1, :] = px[-2, :]
    # px[:, 0] = px[:, 1]
    # px[:, -1] = px[:, -2]
    # pz[0, :] = pz[1, :]
    # pz[-1, :] = pz[-2, :]
    # pz[:, 0] = pz[:, 1]
    # pz[:, -1] = pz[:, -2]


    Ax[:, :-1] = Ax_1[:, :-1] - (Dt / Dx) * correlate(px + pz, c1stOrd, mode='constant')
    Az[:-1, :] = Az_1[:-1, :] - (Dt / Dx) * correlate(px + pz, c1stOrd.T, mode='constant')
    # Ax[:, :-1] = Ax_1[:, :-1] - (Dt / Dx) * correlate(px + pz, c1stOrd, mode='reflect')
    # Az[:-1, :] = Az_1[:-1, :] - (Dt / Dx) * correlate(px + pz, c1stOrd.T, mode='reflect')
    # Ax[:accuracy, :] = 0
    # Ax[-accuracy:, :] = 0
    # Ax[:, :accuracy] = 0
    # Ax[:, -accuracy:] = 0
    # Az[:accuracy, :] = 0
    # Az[-accuracy:, :] = 0
    # Az[:, :accuracy] = 0
    # Az[:, -accuracy:] = 0
    # Ascan[k, 0] = px[Nz//2 - 1, Nx//2 - 1].copy()+pz[Nz//2 - 1, Nx//2 - 1].copy()
    Ascan[k, 0] = px[zscan, xscan] + pz[zscan, xscan]


    p_1, p_2 = p, p_1
    p = 2*p_1 - p_2 + (Dt*c/Dx)**2 * correlate(p_1, c2ndOrd, mode='constant')
    # p = 2 * p_1 - p_2 + (Dt * c / Dx) ** 2 * correlate(p_1, c2ndOrd, mode='reflect')
    p[zsource, xsource] += s[k]
    # p[0, :] = 0
    # p[-1, :] = 0
    # p[:, 0] = 0
    # p[:, -1] = 0
    Ascan[k, 1] = p[zscan, xscan]

    if show:
        level = 1e-3
        # riw.setImage(np.vstack((p.T, (px + pz).T)), levels=[-level, level])
        #riw.setImage(p.T - (px + pz).T, levels=[-level, level])
        riw.setImage(np.vstack((p.T, (px + pz).T, p.T - (px + pz).T)), levels=[-level, level])
        app.processEvents()  ## force complete redraw for every plot
        plt.pause(1e-12)

#app.quit()

# tmp = p[Nz//2, :]
# plt.plot(tmp/np.max(tmp))
# tmp = px[Nz//2, :]+pz[Nz//2, :]
# plt.plot(tmp/np.max(tmp))

#%%
plt.plot(Ascan)
plt.legend(('P-V', 'P only'))
