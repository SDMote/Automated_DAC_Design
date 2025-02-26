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
top_cell = layout.create_cell("r2r")            # create Cell in Layout object (layout module)


## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)


## Draw R-2R
M1_W    = um2dbu(M1_WIDTH)
MOS_L   = um2dbu(MOS_LENGHT)
POLY_W  = um2dbu(POLY_WIDTH)
RES_WIDTH = dbu2um(RES_W)
if RES_LAYOUT:
  segment_lenght = um2dbu(RES_LENGHT)
  R_SEG_L  = dbu2um(segment_lenght)
  yoffset = RES_W/2 - 130 + EXTBc + SALc
  xoffset = -segment_lenght - RHId - CNTa/2 #x0 - segment_lenght/2
  ystep = RES_W + 2*SALc + SALb
  pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
  r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(1, 1, xoffset, yoffset), kl.Vector(0,ystep), kl.Vector(), 3, 1))
  xoffset = xoffset - RHId - CNTa/2
  xstep = segment_lenght + 2*RHId + CNTa
  paint(top_cell, layer_m1, -M1_W/2, -M1_W/2, M1_W/2, yoffset+RES_W)
  port(top_cell, layer_m1, "n2", -M1_W/2, -M1_W/2, M1_W/2, M1_W/2)
#   paint(top_cell, layer_m1, xoffset+xstep-M1_RES/2, y0-PSDc-CNTc+M1b, xoffset+xstep+M1_RES/2, yoffset+RES_W)
  paint(top_cell, layer_m1, xoffset-M1_RES/2, yoffset, xoffset+M1_RES/2, yoffset+RES_W+ystep)
  yoffset = yoffset + ystep
  paint(top_cell, layer_m1, xoffset+xstep-M1_RES/2, yoffset, xoffset+xstep+M1_RES/2, yoffset+RES_W+ystep)
  yoffset = yoffset + ystep
  paint(top_cell, layer_m1, xoffset-M1_RES/2-500, yoffset, xoffset+M1_RES/2, yoffset+RES_W)
  port(top_cell, layer_m1, "n1", xoffset-M1_RES/2-500, yoffset, xoffset+M1_RES/2-500, yoffset+RES_W)
  paint(top_cell, layer_m1, xoffset+xstep-M1_RES/2, yoffset, xoffset+xstep+M1_RES/2+500, yoffset+RES_W)
  port(top_cell, layer_m1, "n0", xoffset+xstep-M1_RES/2+500, yoffset, xoffset+xstep+M1_RES/2+500, yoffset+RES_W)
else:
  segment_lenght = um2dbu(RES_LENGHT/2)
  R_SEG_L  = dbu2um(segment_lenght)
  xstep = RES_W + 2*SALc + SALb
  xoffset = -RES_W/2 # x0 - xstep - RES_W/2
  yoffset = RES_W/2 - 130 + RHId + CNTa + CNTd + PSDc + PSDb #, M1_W - PSDc - CNTc + 2*M1b + M1_RES/2 + CNTa/2)
  paint(top_cell, layer_m1, -M1_W/2, -M1_W/2, M1_W/2, yoffset-RHId-CNTa/2+RES_W/2)
  port(top_cell, layer_m1, "n2", -M1_W/2, -M1_W/2, M1_W/2, M1_W/2)
  ystep = segment_lenght + 2*(RHId + CNTa + CNTd + PSDc) + PSDb
  pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
  r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(0, 0, xoffset, yoffset), kl.Vector(xstep,0), kl.Vector(0,ystep), 3, 2))
  #paint(top_cell, layer_m1, xoffset, 0, xoffset+M1_RES, yoffset-RHId+M1c1)
  yoffset = yoffset-RHId-CNTa/2
  paint(top_cell, layer_m1, xoffset+xstep, yoffset-M1_RES/2, xoffset+2*xstep+RES_W, yoffset+M1_RES/2)
  temp = yoffset + ystep #CNTa + 2*(CNTd + PSDc) + PSDb
  yoffset = yoffset + segment_lenght + 2*RHId + CNTa
  paint(top_cell, layer_m1, xoffset, yoffset-M1_RES/2, xoffset+xstep+RES_W, yoffset+M1_RES/2)
  paint(top_cell, layer_m1, xoffset+2*xstep, yoffset-M1_RES/2, xoffset+2*xstep+RES_W, temp+M1_RES/2)
  paint(top_cell, layer_m1, xoffset, temp-M1_RES/2, xoffset+xstep+RES_W, temp+M1_RES/2)
  yoffset = yoffset + ystep
  paint(top_cell, layer_m1, xoffset+xstep, yoffset-M1_RES/2, xoffset+2*xstep+RES_W+500, yoffset+M1_RES/2)
  port(top_cell, layer_m1, "n1", xoffset+2*xstep+500, yoffset-M1_RES/2, xoffset+2*xstep+RES_W+500, yoffset+M1_RES/2)
  paint(top_cell, layer_m1, xoffset-500, yoffset-M1_RES/2, xoffset+RES_W, yoffset+M1_RES/2)
  port(top_cell, layer_m1, "n0", xoffset-500, yoffset-M1_RES/2, xoffset-500+RES_W, yoffset+M1_RES/2)

# else:
#   segment_lenght = um2dbu(RES_LENGHT/3)
#   R_SEG_L  = dbu2um(segment_lenght)
#   yoffset = y0 + EXTBc + SALc
#   ystep = RES_W + 2*SALc + SALb
#   pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", { "w": RES_WIDTH*1e-6, "l":R_SEG_L*1e-6 })
#   r_instance = top_cell.insert(kl.CellInstArray(pcell_rhigh, kl.Trans(1, 1, x0-segment_lenght/2, yoffset), kl.Vector(0,ystep), kl.Vector(), 9, 1))


## Save GDS
print("Writing R-2R GDS")
layout.write("../klayout/r2r.gds")