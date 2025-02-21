# ============================================================================
# New View project
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

NMOS_W      = 2.0
PMOS_W      = 5.0
N_GATES     = 4
M1_WIDTH    = 0.16
MOS_LENGHT  = 0.13
POLY_WIDTH  = 0.2

# ============================================================================

import pya
from pdk import *
from utils import *
  
## Initialize layout

if (0):
  app = pya.Application.instance()                # get Application
  app.set_config("grid-micron", str(pdk.GRID))
  window = app.main_window()                      # get MainWindow
  if window.current_view() is None:
    print("No open LayoutView. Creating view...")
    tech = "sg13g2"
    window.create_layout(tech, 0)                 # create LayoutView (and CellView)
  layout_view = window.current_view()             # get LayoutView (tab panel in the main window)
  cell_view = layout_view.active_cellview()       # get CellView (specific layout loaded into a view)
  layout = cell_view.layout()                     # create Layout (layout containing cell hierarchy, including cells and instances)
  layout.dbu = pdk.DBU                            # set database unit
  if cell_view.cell is None:
      print("No current Cell. Creating cell...")
      layout.create_cell("TOP")                   # create Cell in Layout object
      cell_view.set_cell_name("TOP")              # set Cell of CellView object
  top_cell = cell_view.cell                       # get Cell (layout module)
else:
  layout = pya.Layout()                           # create Layout (layout containing cell hierarchy, including cells and instances)
  layout.dbu = pdk.DBU                            # set database unit
  top_cell = layout.create_cell("TOP")            # create Cell in Layout object (layout module)

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)


## Draw inverter
xnmos = um2dbu(NMOS_W/N_GATES)
xpmos = um2dbu(PMOS_W/N_GATES)
NMOS_W  = dbu2um(N_GATES*xnmos)
PMOS_W  = dbu2um(N_GATES*xpmos)
M1_W    = um2dbu(M1_WIDTH)
MOS_L   = um2dbu(MOS_LENGHT)
POLY_W  = um2dbu(POLY_WIDTH)
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
pcell_nmos = layout.create_cell("nmos", "SG13_dev", { "l": MOS_LENGHT*1e-6, "w": NMOS_W*1e-6, "ng": N_GATES })
pcell_pmos = layout.create_cell("pmos", "SG13_dev", { "l": MOS_LENGHT*1e-6, "w": PMOS_W*1e-6, "ng": N_GATES })
nmos_instance = top_cell.insert(pya.CellInstArray(pcell_nmos, pya.Trans(1, 0, -xoffset, yoffset)))
nmos_instance2 = top_cell.insert(pya.CellInstArray(pcell_pmos, pya.Trans(1, 1, xoffset, yoffset)))
# Vin and Vout
yoffset = yoffset + 340
ystep = 380 + MOS_L
paint_array(top_cell, layer_poly, -xoffset, yoffset, 2*xoffset, MOS_L, 1, 0, N_GATES, ystep)
paint(top_cell, layer_poly, -POLY_W/2, yoffset, POLY_W/2, yoffset + (N_GATES-1)*ystep)
yoffset = yoffset + 110 + MOS_L
paint(top_cell, layer_poly, -CNTa/2-CNTd, yoffset-M1b-CNTa-M1c1-CNTd, CNTa/2+CNTd, yoffset-M1b-M1c1+CNTd)
paint(top_cell, layer_m1, -M1_W/2, 0, M1_W/2, yoffset-M1b)
paint(top_cell, layer_cnt, -CNTa/2, yoffset-M1b-M1c1-CNTa, CNTa/2, yoffset-M1b-M1c1)
port(top_cell, layer_m1, "vin", -M1_W/2, 0, M1_W/2, M1_W)
ystep = 760 + 2*MOS_L
paint_array(top_cell, layer_m1, -xoffset, yoffset, 2*xoffset, M1a, 1, 0, (N_GATES+1)//2, ystep)
paint(top_cell, layer_m1,-M1_W/2, yoffset, M1_W/2, 5000)
port(top_cell, layer_m1, "vout", -M1_W/2, 5000-M1_W, M1_W/2, 5000)
# Vss and Vdd
xoffset = -xoffset - xnmos
yoffset = PSDc + CNTg1 + CNTa + CNTc + NWe + 70
paint_array(top_cell, layer_m1, xoffset, yoffset, -M1b-M1_W, M1a, 1, 0, N_GATES//2+1, ystep)
paint(top_cell, layer_m1, xoffset-M1b, 0, xoffset-M1b-M1_W, yoffset + ((N_GATES+1)//2)*ystep)
port(top_cell, layer_m1, "vss", xoffset-M1b, 0, xoffset-M1b-M1_W, M1_W)
xoffset = -xoffset + xpmos - xnmos
paint_array(top_cell, layer_m1, xoffset, yoffset, M1b+M1_W, M1a, 1, 0, N_GATES//2+1, ystep)
paint(top_cell, layer_m1, xoffset+M1b, 0, xoffset+M1b+M1_W, yoffset + ((N_GATES+1)//2)*ystep)
port(top_cell, layer_m1, "vdd", xoffset+M1b, 0, xoffset+M1b+M1_W, M1_W)

## Draw 2R
#pcell_rhigh = layout.create_cell("rhigh", "SG13_dev", {})


## Save GDS
print("Writing GDS")
layout.write("../klayout/rdac_bit.gds")