# ============================================================================
# Common functions for automated design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import subprocess
from utils import read_data
from spice import resistor_tb


def measure_resistance(Lr, Nr=1):
    resistor_tb(Lr, Nr)
    subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
    data_op_res = read_data("sim/resistor_op.txt")
    return  data_op_res[0][0]/data_op_res[1][0]

