# ============================================================================
# RDAC layout 
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


# ============================================================================

from pdk import *
from utils import *
from params import *
import klayout.db as kl
import subprocess

RES_W = RHIa
M1_RES = RES_W
M1_WIDTH = dbu2um(M1_RES)


# subprocess.run("klayout -zz -r ../klayout/python/inverter.py -j ../klayout/", shell=True, check=True) 
subprocess.run("klayout -zz -r ../klayout/python/r2r.py -j ../klayout/", shell=True, check=True)
## Initialize layout
layout = kl.Layout()                            # create Layout (layout containing cell hierarchy, including cells and instances)
layout.dbu = pdk.DBU                            # set database unit
layout.read("../klayout/inverter.gds")          # load inverter GDS
layout.read("../klayout/r2r.gds")               # load R-2R GDS
inverter_cell = layout.cell("inverter")
r2r_cell = layout.cell("r2r")
r_cell = layout.cell("rhigh")
top_cell = layout.create_cell("TOP")            # create Cell in Layout object (layout module)

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)


## Intantiate bits
#bit_layout = kl.Layout()
#bit_layout.read("../klayout/rdac_bit.gds")
#bit_cell = layout.create_cell(bit_layout.cell("rdac_bit"))
#bit_cell = layout.create_cell(bit_layout.cell("nmos"))
# bit0_instance = top_cell.insert(kl.CellInstArray(bit_cell, kl.Trans(0, 0, 0, 0)))
ystep = r2r_cell.bbox().right - r2r_cell.bbox().left
inverters_instance_1 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(0, 0, 0, 0), kl.Vector(2*ystep,0), kl.Vector(), 3, 1))
inverters_instance_2 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(2, 1, ystep, 0), kl.Vector(2*ystep,0), kl.Vector(), 3, 1))
ladder_instance = top_cell.insert(kl.CellInstArray(r2r_cell, kl.Trans(0, 0, 0, inverter_cell.bbox().top-RES_W/2), kl.Vector(ystep,0), kl.Vector(), 6, 1))
# inv = top_cell.insert(kl.CellInstArray(r_cell, kl.Trans(0, 0, 0, 20000)))



## Save GDS
print("Writing RDAC GDS")
layout.write("../klayout/rdac.gds")