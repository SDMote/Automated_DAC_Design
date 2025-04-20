# ============================================================================
# Functions for layout generation of DAC
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import subprocess
import pdk
from user import *
from layout.rdac import layout_rdac


def write_layout_params(N=4, type=0, Wn=300, Wp=300, Ng=1, Lr=pdk.RES_MIN_L, Nr=1, Wbit=3850, Wpoly=pdk.MOS_MIN_L):
    """Generates python file with parameters for layout generation.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    """
    fp = open(PROJECT_ROOT + "/python/layout/params.py", "w")
    fp.write("# ============================================================================\n")
    fp.write("# DAC layout parameters\n")
    fp.write("#\n")
    fp.write("# ============================================================================\n")
    fp.write("\n")
    fp.write("RESOLUTION  = "+str(N)+"\n")
    fp.write("TYPE        = "+str(type)+"\n")
    fp.write("NMOS_W      = "+str(Wn)+"\n")
    fp.write("PMOS_W      = "+str(Wp)+"\n")
    fp.write("N_GATES     = "+str(Ng)+"\n")
    fp.write("MOS_LENGHT  = "+str(pdk.MOS_MIN_L)+"\n")
    fp.write("POLY_WIDTH  = "+str(Wpoly)+"\n")
    fp.write("RES_LENGHT  = "+str(Lr)+"\n")
    if type == 0:
        fp.write("N_RES       = "+str(Nr)+"\n")
        fp.write("HALF_WIDTH  = "+str(Wbit//2)+"\n")
    fp.write("\n")
    return


def layout_dac(N, type, params, drc=0):
    write_layout_params(N, type, **params)   # set layout generator parameters to match simulated circuit
    if type == 0:
        layout_rdac(N, **params) # call layout generation with klayout
    elif type == 1:
        pass
    else:
        print("Error")

    print("\nVerification:")
    if drc == 1:    # only run if the complete KLayout tool is installed
        # Run DRC
        print(" Running DRC")
        subprocess.run("klayout -zz -r "+KLAYOUT_DRC+" -rd in_gds=\"../klayout/dac.gds\" -rd report_file=\"../klayout/drc/sg13g2_maximal.lyrdb\" >../klayout/drc/drc.log", shell=True, check=True)
    # Extract spice netlist from GDS
    subprocess.run("magic -rcfile "+MAGICRC_PATH+" -noconsole -nowrapper ../magic/extract_dac.tcl > sim/temp.txt", shell=True, check=True)
    # Perform LVS
    print(" Running LVS")
    subprocess.run("netgen -batch lvs \"../magic/dac.spice dac\" \"sim/dac.spice dac\" "+NETGEN_SETUP+" ../netgen/comp.out > sim/temp.txt", shell=True, check=True)
    return