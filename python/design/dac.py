# ============================================================================
# Functions for automated design of DAC
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
import pdk
from utils import read_data
from spice.dac import dac, dac_tb, dac_tb_tran
from design.rdac import design_r2r_rdac, design_weighted_rdac


def help():
    file = open("help.txt", 'r')
    file_content = file.read()
    print(file_content)
    return


def design_dac(N, type, max_nl, target_R_th, options, Wpoly):
    match type:
        case 0:     # R2R-ladder RDAC
            spice_params, BIT_WIDTH = design_r2r_rdac(N, options['IDEAL_WIDTH'], options['RES_NUMBER'], max_nl, target_R_th, Wpoly)
        case 1:     # Binary-weighted RDAC
            spice_params = design_weighted_rdac()
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

