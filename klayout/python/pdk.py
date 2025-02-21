# ============================================================================
# PDK constants: IHP sg13g2
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

GRID = 0.005
DBU = 0.001



# ============================================================================
# DRC rules

#GatPoly
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
CNTa = CNT_WIDTH            = 160
CNTb = CNTb_MIN_SPACE       = 180
CNTc = CNTc_MIN_ACT_OVER    = 70
CNTd = CNTd_MIN_GAT_OVER    = 70
CNTg1 = CNTg1_MIN_TO_PSD    = 90

# Metal1
M1a = M1a_MIN_WIDTH         = 160
M1b = M1b_MIN_SPACE         = 180
M1c1 = M1c1_MIN_ENDCAP_CNT  = 50


