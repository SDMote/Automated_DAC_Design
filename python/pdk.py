# ============================================================================
# PDK constants: IHP sg13g2
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

LOW_VOLTAGE = 1.2
HIGH_VOLTAGE = 3.3

MIN_MOS_W = 0.15
MIN_MOS_L = 0.13
MIN_LV_NMOS_W = MIN_MOS_W
MIN_LV_PMOS_W = MIN_MOS_W
MIN_LV_NMOS_L = MIN_MOS_L
MIN_LV_PMOS_L = MIN_MOS_L

MIN_HV_NMOS_W = 0.15
MIN_HV_PMOS_W = 0.15
MIN_HV_NMOS_L = 0.45
MIN_HV_PMOS_L = 0.40

MIN_RES_W = 0.5
MIN_RES_L = 0.5


LIB_MOS_TT = ".lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt\n"
LIB_RES_T = ".lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ\n"