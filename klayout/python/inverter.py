# ============================================================================
# RDAC inverter layout 
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


# ============================================================================

from pdk import *
from utils import *
from params import *
import klayout.db as kl

RES_W = RHIa
M1_RES = RES_W
M1_WIDTH = dbu2um(M1_RES)


## Initialize layout
layout = kl.Layout()                            # create Layout (layout containing cell hierarchy, including cells and instances)
layout.dbu = pdk.DBU                            # set database unit
top_cell = layout.create_cell("inverter")       # create Cell in Layout object (layout module)


## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)


## Draw inverter
M1_W    = um2dbu(M1_WIDTH)
MOS_L   = um2dbu(MOS_LENGHT)
POLY_W  = um2dbu(POLY_WIDTH)
xnmos = um2dbu(NMOS_W/N_GATES)
xpmos = um2dbu(PMOS_W/N_GATES)
nmos_w_dummies  = dbu2um((N_GATES+4)*xnmos)
pmos_w_dummies  = dbu2um((N_GATES+4)*xpmos)
NMOS_W  = dbu2um(N_GATES*xnmos)
PMOS_W  = dbu2um(N_GATES*xpmos)

# Ties
yoffset = NWe + CNTc
xoffset = max(M1b+M1_W/2, GATd+POLY_W/2, (NWc+NWd)/2, (300+PSDb+PSDc1)/2) + CNTc
xstep = CNTa + CNTb
n = int((xnmos - CNTa - 2*CNTc)/xstep) + 1
paint_array(top_cell, layer_cnt, -xoffset, yoffset, -CNTa, CNTa, n, -xstep)
n = int((xpmos - CNTa - 2*CNTc)/xstep) + 1
paint_array(top_cell, layer_cnt, xoffset, yoffset, CNTa, CNTa, n, xstep)
xoffset = xoffset - CNTc
paint(top_cell, layer_m1, -xoffset, yoffset, -xoffset-xnmos-M1b-M1_W, yoffset+M1a)
paint(top_cell, layer_m1, xoffset, yoffset, xoffset+xpmos+M1b+M1_W, yoffset+M1a)
paint(top_cell, layer_psd, -xoffset+PSDc1, yoffset-CNTc-PSDc1, -xoffset-xnmos-PSDc1, yoffset+PSDa)
yoffset = yoffset + PSDc + CNTg1 + CNTa
paint(top_cell, layer_activ, -xoffset, NWe, -xoffset-xnmos, yoffset)
paint(top_cell, layer_nwell, xoffset-NWc, 0, xoffset+xpmos+NWc, yoffset)
paint(top_cell, layer_activ, xoffset, NWe, xoffset+xpmos, yoffset)

# MOS devices
pcell_nmos = layout.create_cell("nmos", "SG13_dev", { "l": MOS_LENGHT*1e-6, "w": nmos_w_dummies*1e-6, "ng": N_GATES+4 })
pcell_pmos = layout.create_cell("pmos", "SG13_dev", { "l": MOS_LENGHT*1e-6, "w": pmos_w_dummies*1e-6, "ng": N_GATES+4 })
nmos_instance = top_cell.insert(kl.CellInstArray(pcell_nmos, kl.Trans(1, 0, -xoffset, yoffset)))
pmos_instance = top_cell.insert(kl.CellInstArray(pcell_pmos, kl.Trans(1, 1, xoffset, yoffset)))

# Vin and Vout
ystep = 2*CNTf + CNTa + MOS_L
yoffset = yoffset + 2*ystep + CNTc + CNTa + CNTf
paint_array(top_cell, layer_poly, -xoffset, yoffset, 2*xoffset, MOS_L, 1, 0, N_GATES, ystep)
paint(top_cell, layer_poly, -POLY_W/2, yoffset, POLY_W/2, yoffset + (N_GATES-1)*ystep)
yoffset = yoffset + CNTf + MOS_L
paint(top_cell, layer_poly, -CNTa/2-CNTd, yoffset-M1b-CNTa-M1c1-CNTd, CNTa/2+CNTd, yoffset-M1b-M1c1+CNTd)
paint(top_cell, layer_m1, -M1_W/2, 0, M1_W/2, yoffset-M1b)
paint(top_cell, layer_cnt, -CNTa/2, yoffset-M1b-M1c1-CNTa, CNTa/2, yoffset-M1b-M1c1)
port(top_cell, layer_m1, "vin", -M1_W/2, 0, M1_W/2, M1_W)
paint_array(top_cell, layer_m1, -xoffset, yoffset, 2*xoffset, M1a, 1, 0, (N_GATES+1)//2, 2*ystep)
temp = pmos_instance.bbox().top - M1_W# - 130 - PSDc - CNTc + M1b
paint(top_cell, layer_m1,-M1_W/2, yoffset, M1_W/2, temp+M1_W)
port(top_cell, layer_m1, "vout", -M1_W/2, temp, M1_W/2, temp+M1_W)

# Vss and Vdd (and dummies)
xoffset = -xoffset - xnmos
yoffset = PSDc + CNTg1 + CNTa + 2*CNTc + NWe
paint_array(top_cell, layer_m1, xoffset, yoffset, -M1b-M1_W, M1a, 1, 0, 2, ystep)
temp = yoffset + 2*ystep
paint_array(top_cell, layer_m1, xoffset, temp, -M1b-M1_W, M1a, 1, 0, N_GATES//2+1, 2*ystep)
temp = temp + (N_GATES+1)*ystep
paint_array(top_cell, layer_m1, xoffset, temp, -M1b-M1_W, M1a, 1, 0, 2, ystep)
temp = temp + ystep + M1a
paint(top_cell, layer_m1, xoffset-M1b, 0, xoffset-M1b-M1_W, temp)
port(top_cell, layer_m1, "vss", xoffset-M1b, 0, xoffset-M1b-M1_W, M1_W)
xoffset = -xoffset + xpmos - xnmos
paint(top_cell, layer_m1, xoffset+M1b, 0, xoffset+M1b+M1_W, temp)
port(top_cell, layer_m1, "vdd", xoffset+M1b, 0, xoffset+M1b+M1_W, M1_W)
temp = temp - ystep - M1a
paint_array(top_cell, layer_m1, xoffset, yoffset, M1b+M1_W, M1a, 1, 0, 2, ystep)
paint_array(top_cell, layer_m1, xoffset, temp, M1b+M1_W, M1a, 1, 0, 2, ystep)
temp = yoffset + 2*ystep
paint_array(top_cell, layer_m1, xoffset, temp, M1b+M1_W, M1a, 1, 0, N_GATES//2+1, 2*ystep)
# dummies
yoffset = yoffset + CNTa + CNTf
xoffset = xoffset + M1b - CNTd
paint(top_cell, layer_poly, xoffset+CNTa+2*CNTd, yoffset, xoffset, yoffset+ystep+GATa)
paint(top_cell, layer_cnt, xoffset+CNTa+CNTd, yoffset+GATa+CNTf, xoffset+CNTd, yoffset+ystep-CNTf)
temp = yoffset + (N_GATES+2)*ystep
paint(top_cell, layer_poly, xoffset+CNTa+2*CNTd, temp, xoffset, temp+ystep+GATa)
paint(top_cell, layer_cnt, xoffset+CNTa+CNTd, temp+GATa+CNTf, xoffset+CNTd, temp+ystep-CNTf)
xoffset = -xoffset + xpmos - xnmos
paint(top_cell, layer_poly, xoffset-CNTa-2*CNTd, yoffset, xoffset, yoffset+ystep+GATa)
paint(top_cell, layer_cnt, xoffset-CNTa-CNTd, yoffset+GATa+CNTf, xoffset-CNTd, yoffset+ystep-CNTf)
paint(top_cell, layer_poly, xoffset-CNTa-2*CNTd, temp, xoffset, temp+ystep+GATa)
paint(top_cell, layer_cnt, xoffset-CNTa-CNTd, temp+GATa+CNTf, xoffset-CNTd, temp+ystep-CNTf)


## Save GDS
print("Writing inverter GDS")
layout.write("../klayout/inverter.gds")