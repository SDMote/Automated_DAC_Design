# ============================================================================
# Extract spice netlist from GDS
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

cd ../magic
gds read ../klayout/rdac.gds
load rdac
extract
ext2spice lvs
ext2spice
exit