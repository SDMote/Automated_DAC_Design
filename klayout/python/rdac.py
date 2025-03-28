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

## Layers
layer_poly  = layout.layer(5, 0)
layer_activ = layout.layer(1, 0)
layer_nwell = layout.layer(31, 0)
layer_cnt   = layout.layer(6, 0)
layer_m1    = layout.layer(8, 0)
layer_via1  = layout.layer(19, 0)
layer_m2    = layout.layer(10, 0)
layer_psd   = layout.layer(14, 0)

## Load cells
layout.read("../klayout/inverter.gds")          # load inverter GDS
layout.read("../klayout/r2r_bit_i.gds")         # load R-2R GDS
layout.read("../klayout/r2r_bit_0.gds")         # load 2R-2R GDS
inverter_cell = layout.cell("inverter")
r2r_bit_i_cell = layout.cell("r2r_bit_i")
r2r_bit_0_cell = layout.cell("r2r_bit_0")
r_cell = layout.cell("rhigh")
top_cell = layout.create_cell("dac")            # create Cell in Layout object (layout module)



## Draw R2R-RDAC
# Intantiate bits
xstep = r2r_bit_i_cell.bbox().right - r2r_bit_i_cell.bbox().left
inverters_instance_1 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(0, 0, 0, 0), kl.Vector(2*xstep,0), kl.Vector(), (RESOLUTION+1)//2, 1))
inverters_instance_2 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(2, 1, xstep, 0), kl.Vector(2*xstep,0), kl.Vector(), RESOLUTION//2, 1))
paint_array(top_cell, layer_m1, -M1_W/2, inverter_cell.bbox().top-M1_W, M1_W, 2*M1_W, RESOLUTION, xstep)
yoffset = inverter_cell.bbox().top
r0_instance = top_cell.insert(kl.CellInstArray(r2r_bit_0_cell, kl.Trans(0, 0, 0, yoffset)))
ladder_instance = top_cell.insert(kl.CellInstArray(r2r_bit_i_cell, kl.Trans(0, 0, xstep, yoffset), kl.Vector(xstep,0), kl.Vector(), RESOLUTION-1, 1))
yoffset = yoffset + r2r_bit_i_cell.bbox().top - PSDc - CNTd - CNTa/2 - M1_W/2
paint_array(top_cell, layer_m1, r2r_bit_i_cell.bbox().right-M1_W, yoffset, 2*M1_W, M1_W, RESOLUTION, xstep)
xoffset = (RESOLUTION-1)*xstep + r2r_bit_i_cell.bbox().right
port(top_cell, layer_m1, "vout", xoffset, yoffset, xoffset+M1_W, yoffset+M1_W)
for i in range(RESOLUTION):
    port(top_cell, layer_m1, "d"+str(i), i*xstep-M1_W/2, 0, i*xstep+M1_W/2, M1_W)
# Vdd and Vss
yoffset = M1_W
temp = 3*V1a + 2*V1b + 2*MNc
paint_array(top_cell, layer_via1, (-xstep-V1a)/2, yoffset+MNc, V1a, V1a, 1+RESOLUTION//2, 2*xstep, 3, V1a+V1b)
paint_array(top_cell, layer_m1, (-xstep-V1a)/2, yoffset, V1a, temp, 1+RESOLUTION//2, 2*xstep)
paint(top_cell, layer_m2, (-xstep-M1_W)/2, yoffset, (RESOLUTION-0.5)*xstep+1.5*M1_W, yoffset+temp)
port(top_cell, layer_m2, "vss", (RESOLUTION-0.5)*xstep+0.5*M1_W, yoffset, (RESOLUTION-0.5)*xstep+1.5*M1_W, yoffset+temp)
yoffset = yoffset + MNb + temp
paint_array(top_cell, layer_via1, (xstep-V1a)/2, yoffset+MNc, V1a, V1a, (RESOLUTION+1)//2, 2*xstep, 3, V1a+V1b)
paint_array(top_cell, layer_m1, (xstep-V1a)/2, yoffset, V1a, temp, (RESOLUTION+1)//2, 2*xstep)
paint(top_cell, layer_m2, (-xstep-M1_W)/2, yoffset, (RESOLUTION-0.5)*xstep+1.5*M1_W, yoffset+temp)
port(top_cell, layer_m2, "vdd", (RESOLUTION-0.5)*xstep+0.5*M1_W, yoffset, (RESOLUTION-0.5)*xstep+1.5*M1_W, yoffset+temp)
    
match N_RES:
    case 1:
        pass
    case 2:
        yoffset = inverter_cell.bbox().top
        paint(top_cell, layer_m1, (-xstep-M1_W)/2, yoffset-M1_W, (-xstep+M1_W)/2, yoffset+M1_W)
        # yoffset = yoffset + r2r_bit_i_cell.bbox().top - PSDc - CNTd - CNTa/2
        # xoffset = (RESOLUTION-1)*xstep + r2r_bit_i_cell.bbox().right
        # paint(top_cell, layer_m1, xoffset-M1_W, yoffset-M1_W/2, xoffset+M1_W, yoffset+M1_W/2)
        # port(top_cell, layer_m1, "vout", xoffset, yoffset-M1_W/2, xoffset+M1_W, yoffset+M1_W/2)

    case _:
        print("ERROR: Invalid number of resistors")
#yoffset = inverter_cell.bbox().top + r2r_bit_i_cell.bbox().top - (r_cell.bbox().right-r_cell.bbox().left)/2
#port(top_cell, layer_m1, "vout", (RESOLUTION-1)*xstep-M1_W/2, yoffset-M1_W/2, (RESOLUTION-1)*xstep+M1_W/2, yoffset+M1_W/2)
# Vss and Vdd





## Save GDS
print(" Writing RDAC GDS")
layout.write("../klayout/dac.gds")