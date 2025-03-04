# ============================================================================
# RDAC bit_i layout 
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

# subprocess.run("klayout -zz -r ../klayout/python/inverter.py -j ../klayout/", shell=True, check=True) 
# subprocess.run("klayout -zz -r ../klayout/python/r2r_ladder.py -j ../klayout/", shell=True, check=True)

## Initialize layout
layout = kl.Layout()                            # create Layout (layout containing cell hierarchy, including cells and instances)
layout.dbu = pdk.DBU                            # set database unit
layout.read("../klayout/inverter.gds")          # load inverter GDS
inverter_cell = layout.cell("inverter")
layout.read("../klayout/r2r_bit_i.gds")               # load R-2R GDS
r2r_cell = layout.cell("r2r_bit_i")
top_cell = layout.create_cell("rdac_bit")       # create Cell in Layout object (layout module)


## Instantiate 
inverter_instance = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(0, 0, 0, 0)))
r2r_instance = top_cell.insert(kl.CellInstArray(r2r_cell, kl.Trans(0, 0, 0, inverter_instance.bbox().top-RES_W/2)))


## Save GDS
print("Writing RDAC Bit GDS")
layout.write("../klayout/rdac_bit.gds")