v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 220 -180 260 -180 {lab=#net1}
N 220 -320 260 -320 {lab=#net2}
N 220 -860 260 -860 {lab=#net3}
N 220 -420 260 -420 {lab=#net4}
N 220 -560 260 -560 {lab=#net5}
N 220 -660 260 -660 {lab=#net6}
N 220 -760 260 -760 {lab=#net7}
N 60 -420 80 -420 {lab=d1}
N 80 -420 80 -320 {lab=d1}
N 60 -180 80 -180 {lab=d0}
N 80 -860 80 -560 {lab=d2}
N 60 -860 80 -860 {lab=d2}
N 320 -180 400 -180 {lab=vout}
N 320 -320 360 -320 {lab=vout}
N 360 -420 360 -320 {lab=vout}
N 320 -420 360 -420 {lab=vout}
N 360 -420 400 -420 {lab=vout}
N 360 -860 400 -860 {lab=vout}
N 360 -660 360 -560 {lab=vout}
N 320 -860 360 -860 {lab=vout}
N 320 -560 360 -560 {lab=vout}
N 320 -660 360 -660 {lab=vout}
N 360 -760 360 -660 {lab=vout}
N 320 -760 360 -760 {lab=vout}
N 360 -860 360 -760 {lab=vout}
N 400 -420 400 -180 {lab=vout}
N 400 -860 400 -420 {lab=vout}
N 400 -860 440 -860 {lab=vout}
C {iopin.sym} 440 -860 0 0 {name=p1 lab=vout}
C {inverter.sym} 140 -180 0 0 {name=x1}
C {iopin.sym} 60 -180 2 0 {name=p11 lab=d0}
C {lab_pin.sym} 140 -220 2 0 {name=p5 sig_type=std_logic lab=vdd}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -180 3 0 {name=R1
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {inverter.sym} 140 -320 0 0 {name=x2}
C {iopin.sym} 60 -420 2 0 {name=p4 lab=d1}
C {lab_pin.sym} 140 -280 2 0 {name=p6 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -320 3 0 {name=R2
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {inverter.sym} 140 -860 0 0 {name=x7}
C {iopin.sym} 140 -900 0 0 {name=p7 lab=vdd}
C {iopin.sym} 60 -860 2 0 {name=p8 lab=d2}
C {lab_pin.sym} 140 -820 2 0 {name=p9 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -860 3 0 {name=R3
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {iopin.sym} 140 -140 0 0 {name=p2 lab=vss}
C {lab_pin.sym} 140 -360 2 0 {name=p3 sig_type=std_logic lab=vdd}
C {inverter.sym} 140 -420 0 0 {name=x3}
C {lab_pin.sym} 140 -380 2 0 {name=p10 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -420 3 0 {name=R4
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {lab_pin.sym} 140 -460 2 0 {name=p12 sig_type=std_logic lab=vdd}
C {inverter.sym} 140 -560 0 0 {name=x4}
C {lab_pin.sym} 140 -520 2 0 {name=p13 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -560 3 0 {name=R5
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {lab_pin.sym} 140 -600 2 0 {name=p14 sig_type=std_logic lab=vdd}
C {inverter.sym} 140 -660 0 0 {name=x5}
C {lab_pin.sym} 140 -620 2 0 {name=p15 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -660 3 0 {name=R6
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {lab_pin.sym} 140 -700 2 0 {name=p16 sig_type=std_logic lab=vdd}
C {inverter.sym} 140 -760 0 0 {name=x6}
C {lab_pin.sym} 140 -720 2 0 {name=p17 sig_type=std_logic lab=vss}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 290 -760 3 0 {name=R7
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {lab_pin.sym} 140 -800 2 0 {name=p18 sig_type=std_logic lab=vdd}
