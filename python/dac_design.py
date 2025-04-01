# ============================================================================
# Functions for automated design of DAC
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
import pdk
import user
from utils import read_data
from dac_spice import dac, dac_tb, dac_tb_tran
from rdac_design import design_r2r_rdac


def design_dac(N, type, max_nl, target_R_th, options, Wpoly):
    match type:
        case 0:     # R2R-ladder RDAC
            spice_params, BIT_WIDTH = design_r2r_rdac(N, options['IDEAL_WIDTH'], options['RES_NUMBER'], max_nl, target_R_th, Wpoly)
        case 1:     # Binary-weighted RDAC
            spice_params = {'Wn':500, 'Wp':1000, 'Ng':2, 'Lr':1000}
        case _:
            print("Error")
    layout_params = spice_params.copy()
    layout_params['Wpoly'] = Wpoly
    if type == 0:
        layout_params['Wbit'] = BIT_WIDTH
    return spice_params, layout_params


def simulate_dac(N, type, params, c_load):
    Q = 2**N # number of codes
    match type:
        case 0:     # R2R-ladder RDAC
            LSB = pdk.LOW_VOLTAGE/Q
        case 1:     # Binary-weighted RDAC
            LSB = pdk.LOW_VOLTAGE/(Q-1)
        case _:
            print("Error")
    dac(N, type, params)
    dac_tb(N)
    subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
    subprocess.run("ngspice -b sim/dac_tb.spice -o sim/dac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
    data_dc = read_data("sim/dac_dc.txt")
    digital_input = np.arange(Q)
    transfer_function = np.flip(data_dc[1][0:Q])
    tfunction_ref = digital_input * LSB
    inl = (transfer_function - tfunction_ref)/LSB
    dnl = (transfer_function[1:] - transfer_function[:Q-1] - LSB)/LSB

    dac_tb_tran(N, c_load, type)
    subprocess.run("ngspice -b sim/dac_tb_tran.spice -o sim/dac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
    data = read_data("sim/dac_tran.txt")
    rise_time = data[1][0]
    # R_th = rise_time / (2.2 * c_load * 1e-12)
    print(' Simulate => INL:', max(abs(inl)), ' DNL:', max(abs(dnl)), " Worst transition time:", rise_time)
    return inl, dnl, rise_time


def write_layout_params(N=4, type=0, Wn=0.3, Wp=0.3, Ng=1, Lr=pdk.RES_MIN_L, Nr=1, Wbit=3850, Wpoly=pdk.MOS_MIN_L):
    """Generates python file with parameters for layout generation.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    """
    fp = open("../klayout/python/params.py", "w")
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
    fp.write("N_RES       = "+str(Nr)+"\n")
    fp.write("HALF_WIDTH  = "+str(Wbit//2)+"\n")
    fp.write("\n")
    return


def layout_dac(N, type, params):
    write_layout_params(N, type, **params)   # set layout generator parameters to match simulated circuit
    match type:
        case 0:
            subprocess.run("klayout -zz -r ../klayout/python/rdac.py -j ../klayout/", shell=True, check=True) # call layout generation with klayout
        case 1:
            pass
        case _:
            print("Error")

    print("\nVerification:")
    # Run DRC
    print(" Running DRC")
    subprocess.run("klayout -zz -r "+user.KLAYOUT_DRC+" -rd in_gds=\"../klayout/dac.gds\" -rd report_file=\"../klayout/drc/sg13g2_maximal.lyrdb\" >../klayout/drc/drc.log", shell=True, check=True)
    # Extract spice netlist from GDS
    subprocess.run("magic -rcfile "+user.MAGICRC_PATH+" -noconsole -nowrapper ../magic/extract_dac.tcl > sim/temp.txt", shell=True, check=True)
    # Perform LVS
    print(" Running LVS")
    subprocess.run("netgen -batch lvs \"../magic/dac.spice dac\" \"sim/dac.spice dac\" "+user.NETGEN_SETUP+" ../netgen/comp.out > sim/temp.txt", shell=True, check=True)
    return