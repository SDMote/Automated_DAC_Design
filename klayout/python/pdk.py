# ============================================================================
# PDK constants: IHP sg13g2
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

GRID = 0.005
DBU = 0.001


# ============================================================================
# Devices rules

# Rhigh
RHIa = RHIa_MIN_GAT_WIDTH   = 500
RHId = RHId_SPACE_TO_CONT   = 200
RHIf = RHIf_MIN_SALB_LENGHT = 960 # 500

# ============================================================================
# DRC rules

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

# SalBlock
SALb = SALb_MIN_SPACING         = 420
SALc = SALc_MIN_OVER_ACT_GAT    = 200

# EXTBlock
EXTBa = EXTBa_MIN_WIDTH     = 310
EXTBb = EXTBb_MIN_SPACING   = 310
EXTBc = EXTBc_MIN_TO_PSD    = 310

