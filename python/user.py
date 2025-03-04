# ============================================================================
# User constants
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

PDK = "ihp-sg13g2"
PDK_ROOT = "/foss/pdks"
PROJECT_ROOT = "/foss/designs/Automated_DAC_Design"

# ============================================================================


PDKPATH = PDK_ROOT + "/" + PDK
MAGICRC_PATH = PDKPATH + "/libs.tech/magic/ihp-sg13g2.magicrc"
NETGEN_SETUP = PDKPATH + "/libs.tech/netgen/ihp-sg13g2_setup.tcl"
KLAYOUT_DRC = PDKPATH + "/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc"

SIM_PATH = PROJECT_ROOT + "/python/sim"