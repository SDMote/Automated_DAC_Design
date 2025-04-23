# ============================================================================
# RDAC layout 
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


# ============================================================================

from user import *
import sys
sys.path.append(PDKPATH + "/libs.tech/klayout/python/")
sys.path.append(PDKPATH + "/libs.tech/klayout/python/pycell4klayout-api/source/python/")
import sg13g2_pycell_lib
import klayout.db as kl

from pdk import *
from layout.utils import *
from layout.inverter import layout_inverter
from layout.r2r_ladder import layout_r2r_rdac

def layout_rdac(N, Wn, Wp, Ng, Lr, Nr, Wbit, Wpoly):
    MOS_LENGHT = MOS_MIN_L
    RES_W = RHIa
    M1_W = RES_W
    M1_WIDTH = dbu2um(M1_W)
    
    layout_inverter(Wn, Wp, Ng, MOS_LENGHT, Wbit//2, Wpoly)
    layout_r2r_rdac(Lr, Nr)

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
    layout.read(LAYOUT_PATH + "/inverter.gds")          # load inverter GDS
    layout.read(LAYOUT_PATH + "/r2r_bit_i.gds")         # load R-2R GDS
    layout.read(LAYOUT_PATH + "/r2r_bit_0.gds")         # load 2R-2R GDS
    inverter_cell = layout.cell("inverter")
    r2r_bit_i_cell = layout.cell("r2r_bit_i")
    r2r_bit_0_cell = layout.cell("r2r_bit_0")
    r_cell = layout.cell("rhigh")
    top_cell = layout.create_cell("dac")            # create Cell in Layout object (layout module)


    ## Draw R2R-RDAC
    # Intantiate bits
    xstep = r2r_bit_i_cell.bbox().right - r2r_bit_i_cell.bbox().left
    inverters_instance_1 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(0, 0, 0, 0), kl.Vector(2*xstep,0), kl.Vector(), (N+1)//2, 1))
    inverters_instance_2 = top_cell.insert(kl.CellInstArray(inverter_cell, kl.Trans(2, 1, xstep, 0), kl.Vector(2*xstep,0), kl.Vector(), N//2, 1))
    paint_array(top_cell, layer_m1, -M1_W/2, inverter_cell.bbox().top-M1_W, M1_W, 2*M1_W, N, xstep)
    yoffset = inverter_cell.bbox().top
    r0_instance = top_cell.insert(kl.CellInstArray(r2r_bit_0_cell, kl.Trans(0, 0, 0, yoffset)))
    ladder_instance = top_cell.insert(kl.CellInstArray(r2r_bit_i_cell, kl.Trans(0, 0, xstep, yoffset), kl.Vector(xstep,0), kl.Vector(), N-1, 1))
    yoffset = yoffset + r2r_bit_i_cell.bbox().top - PSDc - CNTd - CNTa/2 - M1_W/2
    paint_array(top_cell, layer_m1, r2r_bit_i_cell.bbox().right-M1_W, yoffset, 2*M1_W, M1_W, N, xstep)
    xoffset = (N-1)*xstep + r2r_bit_i_cell.bbox().right
    port(top_cell, layer_m1, "vout", xoffset, yoffset, xoffset+M1_W, yoffset+M1_W)
    for i in range(N):
        port(top_cell, layer_m1, "d"+str(i), i*xstep-M1_W/2, 0, i*xstep+M1_W/2, M1_W)
    # Vdd and Vss
    yoffset = M1_W
    temp = 3*V1a + 2*V1b + 2*MNc
    paint_array(top_cell, layer_via1, (-xstep-V1a)/2, yoffset+MNc, V1a, V1a, 1+N//2, 2*xstep, 3, V1a+V1b)
    paint_array(top_cell, layer_m1, (-xstep-V1a)/2, yoffset, V1a, temp, 1+N//2, 2*xstep)
    paint(top_cell, layer_m2, (-xstep-M1_W)/2, yoffset, (N-0.5)*xstep+1.5*M1_W, yoffset+temp)
    port(top_cell, layer_m2, "vss", (N-0.5)*xstep+0.5*M1_W, yoffset, (N-0.5)*xstep+1.5*M1_W, yoffset+temp)
    yoffset = yoffset + MNb + temp
    paint_array(top_cell, layer_via1, (xstep-V1a)/2, yoffset+MNc, V1a, V1a, (N+1)//2, 2*xstep, 3, V1a+V1b)
    paint_array(top_cell, layer_m1, (xstep-V1a)/2, yoffset, V1a, temp, (N+1)//2, 2*xstep)
    paint(top_cell, layer_m2, (-xstep-M1_W)/2, yoffset, (N-0.5)*xstep+1.5*M1_W, yoffset+temp)
    port(top_cell, layer_m2, "vdd", (N-0.5)*xstep+0.5*M1_W, yoffset, (N-0.5)*xstep+1.5*M1_W, yoffset+temp)
        
    if Nr == 1:
        pass
    elif Nr == 2:
        yoffset = inverter_cell.bbox().top
        paint(top_cell, layer_m1, (-xstep-M1_W)/2, yoffset-M1_W, (-xstep+M1_W)/2, yoffset+M1_W)
        # yoffset = yoffset + r2r_bit_i_cell.bbox().top - PSDc - CNTd - CNTa/2
        # xoffset = (RESOLUTION-1)*xstep + r2r_bit_i_cell.bbox().right
        # paint(top_cell, layer_m1, xoffset-M1_W, yoffset-M1_W/2, xoffset+M1_W, yoffset+M1_W/2)
        # port(top_cell, layer_m1, "vout", xoffset, yoffset-M1_W/2, xoffset+M1_W, yoffset+M1_W/2)
    else:
        print("ERROR: Invalid number of resistors")
    #yoffset = inverter_cell.bbox().top + r2r_bit_i_cell.bbox().top - (r_cell.bbox().right-r_cell.bbox().left)/2
    #port(top_cell, layer_m1, "vout", (RESOLUTION-1)*xstep-M1_W/2, yoffset-M1_W/2, (RESOLUTION-1)*xstep+M1_W/2, yoffset+M1_W/2)
    # Vss and Vdd

    ## Save GDS
    print(" Writing RDAC GDS")
    layout.write(LAYOUT_PATH + "/dac.gds")
    return