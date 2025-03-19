# ============================================================================
# PDK constants: IHP sg13g2
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import user

GRID = 0.005
DBU = 0.001

LOW_VOLTAGE = 1.2
HIGH_VOLTAGE = 3.3

# Model paths
LIB_MOS_TT = ".lib "+user.PDKPATH+"/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt\n"
LIB_RES_T = ".lib "+user.PDKPATH+"/libs.tech/ngspice/models/cornerRES.lib res_typ\n"


# ============================================================================
# Device layout rules

# Mosfets
MOS_MIN_W = 150
MOS_MIN_L = 130
LVNMOS_MIN_W = MOS_MIN_W
LVPMOS_MIN_W = MOS_MIN_W
LVNMOS_MIN_L = MOS_MIN_L
LVPMOS_MIN_L = MOS_MIN_L

HVNMOS_MIN_W = 150
HVPMOS_MIN_W = 150
HVNMOS_MIN_L = 450
HVPMOS_MIN_L = 400

# Rhigh
RHIa = RHIa_MIN_GAT_WIDTH   = 500
RHId = RHId_SPACE_TO_CONT   = 200
RHIf = RHIf_MIN_SALB_LENGHT = 960 # 500
RES_MIN_W = 500
RES_MIN_L = 500


# ============================================================================
# Other device constants

LVNMOS_THR = 0.5
LVPMOS_THR = -0.47
HVNMOS_THR = 0.7
HVPMOS_THR = -0.65


# ============================================================================
# DRC

#GatPoly
GATa = GATa_MIN_WIDTH       = 130
GATb = GATb_MIN_SPACING     = 180
GATc = GATc_MIN_OVER_ACT    = 180
GATd = GATd_MIN_TO_ACT      = 70

# NWell
NWc = NWc_MIN_OVER_PACT     = 310
NWd = NWd_MIN_TO_NACT       = 310
NWe = NWe_MIN_OVER_NACT     = 240  # for NWell tie

# pSD
PSDa = PSDa_MIN_WIDTH       = 310
PSDb = PSDb_MIN_SPACING     = 310
PSDc = PSDc_MIN_OVER_PACT   = 180
PSDc1 = PSDc1_MIN_OVER_ACT  = 30

# Cnt
CNTa = CNTa_MIN_WIDTH       = 160
CNTb = CNTb_MIN_SPACING     = 180
CNTc = CNTc_MIN_ACT_OVER    = 70
CNTd = CNTd_MIN_GAT_OVER    = 70
CNTg1 = CNTg1_MIN_TO_PSD    = 90
CNTf = CNTf_MIN_TO_GAT      = 110

# Metal1
M1a = M1a_MIN_WIDTH         = 160
M1b = M1b_MIN_SPACING       = 180
M1c1 = M1c1_MIN_ENDCAP_CNT  = 50

# Metal2-5
MNa = MNa_MIN_WIDTH         = 200
MNb = MNb_MIN_SPACING       = 210

# SalBlock
SALb = SALb_MIN_SPACING         = 420
SALc = SALc_MIN_OVER_ACT_GAT    = 200

# EXTBlock
EXTBa = EXTBa_MIN_WIDTH     = 310
EXTBb = EXTBb_MIN_SPACING   = 310
EXTBc = EXTBc_MIN_TO_PSD    = 310

