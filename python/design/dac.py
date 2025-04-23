# ============================================================================
# Functions for automated design of DAC
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
import pdk
from specs import *
from utils import read_data
from spice.dac import dac, dac_tb, dac_tb_tran
from design.rdac import design_r2r_rdac, design_weighted_rdac


def help():
    """Prints content of help.txt"""
    file = open("help.txt", 'r')
    file_content = file.read()
    print(file_content)
    return


def load_specs():
    """Builds dictionary with user input specifications from spec.py file.
    return: input_specs dictionary.
    """
    # TODO: check valid specs
    POLY_W = 300    # Not the gate width/lenght but the width of the inverter input. Not yet leveraged in the design flow
    # Set topology-dependant specifications in the options dictionary
    if TOPOLOGY == 0:   # R2R-ladder RDAC
        print("R2R-ladder RDAC with", RESOLUTION, "bits of resolution")
        RES_NUMBER = 2  # number of resistance instances that make the unit resistor R, changing the layout
        options = {'ideal_width':IDEAL_WIDTH, 'res_number':RES_NUMBER}
    # elif TOPOLOGY == 1:     # Binary-weighted RDAC
    #     print("Binary-weighted RDAC with", RESOLUTION, "bits of resolution")
    #     options = {}
    # elif TOPOLOGY == 2:     # Series RDAC
    #     print("Series-resistor RDAC with", RESOLUTION, "bits of resolution")
    #     options = {}
    # elif TOPOLOGY == 3:     # Capacitive DAC
    #     print("Capacitive DAC with", RESOLUTION, "bits of resolution")
    else:
        print("Error")

    # topology-independent specs from specs.py
    input_specs = {'resolution':RESOLUTION, 'topology':TOPOLOGY, 'max_nl':MAX_NL, 'max_time':MAX_TIME, 'c_load':C_LOAD, 'poly_w':POLY_W, 'options':options}
    print("Target max NL:", MAX_NL, "\tTarget max transition time:", MAX_TIME, "us, with load of", C_LOAD, "pF")
    return input_specs


def design_dac(resolution, topology, max_nl, max_time, c_load, poly_w, options):
    """General DAC design function.
    resolution: number of bits.
    topology: type of DAC circuit.
    max_nl: target worst nonlinearity (INL or DNL).
    max_time: target maximum transition time (speed).
    c_load: load capacitance (for speed).
    poly_w: inverter input width.
    options: topology-dependent specifications.
    return: a dictionary with circuit sizing and one with layout parameters.
    """
    target_R_th = max_time * 1e-6 / (2.2 * c_load * 1e-12)     # 10%-90%, rise_time = 2.2*tau = 2.2*R_th*C_load
    if topology == 0:        # R2R-ladder RDAC
        spice_params, bit_width = design_r2r_rdac(resolution, options['ideal_width'], options['res_number'], max_nl, target_R_th, poly_w)
        layout_params = spice_params.copy()
        layout_params['Wpoly'] = poly_w
        layout_params['Wbit'] = bit_width
    # elif topology == 1:      # Binary-weighted RDAC
    #     spice_params = design_weighted_rdac()
    else:
        print("Error")
    return spice_params, layout_params


def simulate_dac(N, type, params, c_load):
    """General DAC simulation function.
    resolution: number of bits.
    topology: type of DAC circuit.
    params: dictionary with circuit sizing.
    c_load: load capacitance for output transition time simulation (speed).
    return: nonlinearities and worst output transition time.
    """
    Q = 2**N # number of codes
    if type == 0:     # R2R-ladder RDAC
        LSB = pdk.LOW_VOLTAGE/Q
    elif type == 1:     # Binary-weighted RDAC
        LSB = pdk.LOW_VOLTAGE/(Q-1)
    else:
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

