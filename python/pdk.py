# ============================================================================
# PDK constants: IHP sg13g2
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import user

LOW_VOLTAGE = 1.2
HIGH_VOLTAGE = 3.3


## DRC
MOS_MIN_W = 0.15
MOS_MIN_L = 0.13
LVNMOS_MIN_W = MOS_MIN_W
LVPMOS_MIN_W = MOS_MIN_W
LVNMOS_MIN_L = MOS_MIN_L
LVPMOS_MIN_L = MOS_MIN_L

HVNMOS_MIN_W = 0.15
HVPMOS_MIN_W = 0.15
HVNMOS_MIN_L = 0.45
HVPMOS_MIN_L = 0.40

LVNMOS_THR = 0.5
LVPMOS_THR = -0.47
HVNMOS_THR = 0.7
HVPMOS_THR = -0.65

RES_MIN_W = 0.5
RES_MIN_L = 0.5


## Models
LIB_MOS_TT = ".lib "+user.PDKPATH+"/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt\n"
LIB_RES_T = ".lib "+user.PDKPATH+"/libs.tech/ngspice/models/cornerRES.lib res_typ\n"