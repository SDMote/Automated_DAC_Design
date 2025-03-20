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


M1_W    = um2dbu(M1_WIDTH)
MOS_L   = MOS_LENGHT
POLY_W  = POLY_WIDTH
RES_WIDTH = dbu2um(RES_W)

# ============================================================================
# Draw common part

## Initialize layout
layout = kl.Layout()                            # create Layout (layout containing cell hierarchy, including cells and instances)
layout.dbu = pdk.DBU                            # set database unit
top_cell = layout.create_cell("r2r_bit_0")      # create Cell in Layout object (layout module)

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)

## Draw
match N_RES:
    case 1:
        pass
        segment_lenght = RES_LENGHT
        R_SEG_L  = dbu2um(segment_lenght)
        yoffset = -130 + EXTBc + SALc
        xoffset = -segment_lenght - RHId - CNTa/2
        ystep = RES_W + 2*SALc + SALb
        pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
        r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(1, 1, xoffset, yoffset), kl.Vector(0,ystep), kl.Vector(), 3, 1))
        xoffset = xoffset - RHId - CNTa/2
        xstep = segment_lenght + 2*RHId + CNTa
        paint(top_cell, layer_m1, -M1_W/2, 0, M1_W/2, yoffset+RES_W)
        port(top_cell, layer_m1, "n2", -M1_W/2, 0, M1_W/2, SALc)
        paint(top_cell, layer_m1, xoffset-M1_RES/2, yoffset, xoffset+M1_RES/2, yoffset+RES_W+ystep)
        yoffset = yoffset + ystep
        paint(top_cell, layer_m1, xoffset+xstep-M1_RES/2, yoffset, xoffset+xstep+M1_RES/2, yoffset+RES_W+ystep)
        yoffset = yoffset + ystep
        temp = CNTa/2 + CNTd + PSDc + PSDb/2
        # paint(top_cell, layer_m1, xoffset-temp-M1_W, yoffset, xoffset+M1_RES/2, yoffset+RES_W)
        # pin_n0 = port(top_cell, layer_m1, "n0", xoffset-temp, yoffset, xoffset-temp+M1_W/2, yoffset+RES_W)
        paint(top_cell, layer_m1, xoffset+xstep-M1_W/2, yoffset, xoffset+xstep+temp, yoffset+RES_W)
        port(top_cell, layer_m1, "n1", xoffset+xstep+temp-PSDb/2, yoffset, xoffset+xstep+temp, yoffset+RES_W)
    case 2:
        segment_lenght = RES_LENGHT/2
        R_SEG_L  = dbu2um(segment_lenght)
        xstep = RES_W + 2*SALc + SALb
        xoffset = -RES_W/2
        yoffset = -130 + RHId + CNTa + CNTd + PSDc + PSDb
        paint(top_cell, layer_m1, -M1_W/2, 0, M1_W/2, yoffset-RHId-CNTa/2+RES_W/2)
        port(top_cell, layer_m1, "n2", -M1_W/2, 0, M1_W/2, PSDc)
        ystep = segment_lenght + 2*(RHId + CNTa + CNTd + PSDc) + PSDb
        pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
        r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(0, 0, xoffset, yoffset), kl.Vector(xstep,0), kl.Vector(0,ystep), 3, 2))
        yoffset = yoffset-RHId-CNTa/2
        paint(top_cell, layer_m1, xoffset+xstep, yoffset-M1_RES/2, xoffset+2*xstep+RES_W, yoffset+M1_RES/2)
        temp = yoffset + ystep
        yoffset = yoffset + segment_lenght + 2*RHId + CNTa
        paint(top_cell, layer_m1, xoffset, yoffset-M1_RES/2, xoffset+xstep+RES_W, yoffset+M1_RES/2)
        paint(top_cell, layer_m1, xoffset+2*xstep, yoffset-M1_RES/2, xoffset+2*xstep+RES_W, temp+M1_RES/2)
        paint(top_cell, layer_m1, xoffset, temp-M1_RES/2, xoffset+xstep+RES_W, temp+M1_RES/2)
        yoffset = yoffset + ystep
        temp = SALc + SALb/2
        # paint(top_cell, layer_m1, xoffset-temp-M1_W, yoffset-M1_RES/2, xoffset+RES_W, yoffset+M1_RES/2)
        # pin_n0 = port(top_cell, layer_m1, "n0", xoffset-temp, yoffset-M1_RES/2, xoffset-PSDc, yoffset+M1_RES/2)
        paint(top_cell, layer_m1, xoffset+xstep, yoffset-M1_RES/2, xoffset+2*xstep+temp+RES_W, yoffset+M1_RES/2)
        port(top_cell, layer_m1, "n1", xoffset+2*xstep+RES_W+PSDc, yoffset-M1_RES/2, xoffset+2*xstep+temp+RES_W, yoffset+M1_RES/2)
    case _:
        pass
# else:
#   segment_lenght = um2dbu(RES_LENGHT/3)
#   R_SEG_L  = dbu2um(segment_lenght)
#   yoffset = y0 + EXTBc + SALc
#   ystep = RES_W + 2*SALc + SALb
#   pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
#   r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(1, 1, x0-segment_lenght/2, yoffset), kl.Vector(0,ystep), kl.Vector(), 9, 1))
r_instance.flatten()

## Save temp GDS
layout.write("../klayout/r2r_bit_0.gds")


# ============================================================================
# Draw resistors for Bit i

top_cell.name = "r2r_bit_i"
match N_RES:
    case 1:
        paint(top_cell, layer_m1, xoffset-temp, yoffset, xoffset+M1_RES/2, yoffset+RES_W)
        pin_n0 = port(top_cell, layer_m1, "n0", xoffset-temp, yoffset, xoffset-temp+PSDb/2, yoffset+RES_W)
    case 2:
        paint(top_cell, layer_m1, xoffset-temp, yoffset-M1_RES/2, xoffset+RES_W, yoffset+M1_RES/2)
        pin_n0 = port(top_cell, layer_m1, "n0", xoffset-temp, yoffset-M1_RES/2, xoffset-PSDc, yoffset+M1_RES/2)
    case _:
        pass

print(" Writing R-2R GDS")
layout.write("../klayout/r2r_bit_i.gds")


# ============================================================================
# Draw resistors for Bit 0

## Initialize new layout
layout = kl.Layout()                            # create new Layout
layout.dbu = pdk.DBU                            # set database unit
layout.read("../klayout/r2r_bit_0.gds")         # load common part
top_cell = layout.cell("r2r_bit_0")

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)

## Draw
match N_RES:
    case 1:
        temp = xoffset
        yoffset = yoffset + RES_W/2 - RHId - CNTa/2
        xoffset = xoffset - CNTa/2 - CNTd - PSDc - EXTBa - EXTBb - RES_W
        pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
        r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(0, 1, xoffset, yoffset)))
        yoffset = yoffset + RHId + CNTa/2
        paint(top_cell, layer_m1, xoffset, yoffset-M1_W/2, temp+M1_W/2, yoffset+M1_W/2)
        yoffset = yoffset - xstep
        temp = yoffset - CNTa/2 - CNTd - PSDc
        paint(top_cell, layer_m1, xoffset, temp-M1_W, xoffset+M1_W, yoffset+M1_W/2)
        port(top_cell, layer_m1, "n0", xoffset, yoffset-M1_W, xoffset+M1_W, temp)
    case 2:
        yoffset = -130 + RHId + CNTa + CNTd + PSDc + PSDb
        xoffset = xoffset-xstep
        pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
        r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(0, 0, xoffset, yoffset), kl.Vector(0, ystep), kl.Vector(), 2, 1))
        paint(top_cell, layer_m1, xoffset-temp-M1_W/2, yoffset-RHId-CNTa/2-M1_W/2, xoffset+M1_W, yoffset-RHId-CNTa/2+M1_W/2)
        port(top_cell, layer_m1, "n0", xoffset-temp, yoffset-RHId-CNTa/2-M1_W/2, xoffset-PSDc, yoffset-RHId-CNTa/2+M1_W/2)
        temp = yoffset + ystep - RHId - CNTa/2
        yoffset = yoffset + segment_lenght + RHId + CNTa/2
        paint(top_cell, layer_m1, xoffset, yoffset-M1_W/2, xoffset+M1_W, temp+M1_W/2)
        yoffset = yoffset + ystep
        paint(top_cell, layer_m1, xoffset, yoffset-M1_W/2, xoffset+xstep+M1_W, yoffset+M1_W/2)
    case _:
        pass
r_instance.flatten()

# try to delete/edit ports from the previous cell
# layer_number = layout.layer_infos()[layer_m1].layer
# pin_layer = layout.layer(layer_number, 2)
# text_layer = layout.layer(layer_number, 25)
# print(top_cell.shapes(text_layer)[0].)
  
## Save GDS
print(" Writing 2R-2R GDS")
layout.write("../klayout/r2r_bit_0.gds")