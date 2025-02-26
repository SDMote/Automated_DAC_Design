# ============================================================================
# Drawing utility functions
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import pdk
import pya

def um2dbu(u: float):
  d = 5*round(u/pdk.GRID)
  return d

def dbu2um(d: int):
  u = pdk.DBU*d
  return u

def dbu(d):
  d = 5*round(d/5)
  return d

def paint(cell: pya.Cell, layer: pya.LayerInfo, x1, y1, x2, y2):
  cell.shapes(layer).insert(pya.Box(x1, y1, x2, y2))

def paint_array(cell: pya.Cell, layer, xoffset, yoffset, xsize, ysize, n=1, xstep=0, m=1, ystep=0):
  for i in range(n):
    for j in range(m):
      cell.shapes(layer).insert(pya.Box(xoffset+i*xstep, yoffset+j*ystep, xoffset+i*xstep+xsize, yoffset+j*ystep+ysize))
  
def port(cell: pya.Cell, layer, text: str, x1, y1, x2, y2):
  layout = cell.layout()
  layer_number = layout.layer_infos()[layer].layer
  pin_layer = layout.layer(layer_number, 2)
  text_layer = layout.layer(layer_number, 25)
  cell.shapes(pin_layer).insert(pya.Box(x1, y1, x2, y2))
  cell.shapes(text_layer).insert(pya.Text(text, (x1+x2)/2, (y1+y2)/2))

