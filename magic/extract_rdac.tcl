# ============================================================================
# Extract spice netlist from GDS
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

cd ../magic
gds read ../klayout/rdac_bit.gds
load TOP
extract
ext2spice lvs
ext2spice
exit