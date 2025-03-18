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
M1_W = RES_W
M1_WIDTH = dbu2um(M1_W)


subprocess.run("klayout -zz -r ../klayout/python/inverter.py -j ../klayout/", shell=True, check=True) 
subprocess.run("klayout -zz -r ../klayout/python/r2r_ladder.py -j ../klayout/", shell=True, check=True)
## Initialize layout
layout = kl.Layout()                            # create Layout (layout containing cell hierarchy, including cells and instances)
layout.dbu = pdk.DBU                            # set database unit
layout.read("../klayout/inverter.gds")          # load inverter GDS
layout.read("../klayout/r2r_bit_i.gds")         # load R-2R GDS
layout.read("../klayout/r2r_bit_0.gds")         # load 2R-2R GDS
inverter_cell = layout.cell("inverter")
r2r_bit_i_cell = layout.cell("r2r_bit_i")
r2r_bit_0_cell = layout.cell("r2r_bit_0")
r_cell = layout.cell("rhigh")
top_cell = layout.create_cell("rdac")            # create Cell in Layout object (layout module)

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_psd   = layout.layer(14, 0)


## Draw RDAC
# Intantiate bits
xstep = r2r_bit_i_cell.bbox().right - r2r_bit_i_cell.bbox().left - 2*M1_W
inverters_instance_1 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(0, 0, 0, 0), kl.Vector(2*xstep,0), kl.Vector(), (RESOLUTION+1)//2, 1))
inverters_instance_2 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(2, 1, xstep, 0), kl.Vector(2*xstep,0), kl.Vector(), RESOLUTION//2, 1))
r0_instance = top_cell.insert(kl.CellInstArray(r2r_bit_0_cell, kl.Trans(0, 0, 0, inverter_cell.bbox().top)))
ladder_instance = top_cell.insert(kl.CellInstArray(r2r_bit_i_cell, kl.Trans(0, 0, xstep, inverter_cell.bbox().top), kl.Vector(xstep,0), kl.Vector(), RESOLUTION-1, 1))
for i in range(RESOLUTION):
    port(top_cell, layer_m1, "d"+str(i), i*xstep-M1_W/2, 0, i*xstep+M1_W/2, M1_W)
    
match N_RES:
    case 1:
        pass
    case 2:
        pass
    case _:
        print("ERROR: Invalid number of resistors")
#yoffset = inverter_cell.bbox().top + r2r_bit_i_cell.bbox().top - (r_cell.bbox().right-r_cell.bbox().left)/2
#port(top_cell, layer_m1, "vout", (RESOLUTION-1)*xstep-M1_W/2, yoffset-M1_W/2, (RESOLUTION-1)*xstep+M1_W/2, yoffset+M1_W/2)
# Vss and Vdd





## Save GDS
print("Writing RDAC GDS")
layout.write("../klayout/rdac.gds")