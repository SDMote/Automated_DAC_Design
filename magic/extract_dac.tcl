# ============================================================================
# Extract spice netlist from GDS
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

cd ../magic
gds read ../klayout/dac.gds
load dac
extract
ext2spice lvs
ext2spice
exit