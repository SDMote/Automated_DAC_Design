v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 200 -500 240 -500 {lab=#net1}
N 300 -500 340 -500 {lab=vout}
N 340 -500 340 -460 {lab=vout}
N 340 -500 420 -500 {lab=vout}
N 340 -360 340 -320 {lab=#net2}
N 340 -220 340 -80 {lab=#net3}
N 300 -80 340 -80 {lab=#net3}
N 300 -220 340 -220 {lab=#net3}
N 340 -260 340 -220 {lab=#net3}
N 300 -360 340 -360 {lab=#net2}
N 340 -400 340 -360 {lab=#net2}
N 200 -360 240 -360 {lab=#net4}
N 200 -220 240 -220 {lab=#net5}
N 200 -80 240 -80 {lab=vss}
C {iopin.sym} 420 -500 0 0 {name=p1 lab=vout}
C {inverter.sym} 120 -220 0 0 {name=x1}
C {inverter.sym} 120 -360 0 0 {name=x2}
C {inverter.sym} 120 -500 0 0 {name=x3}
C {iopin.sym} 120 -540 0 0 {name=p2 lab=vdd}
C {iopin.sym} 60 -220 2 0 {name=p3 lab=d0}
C {iopin.sym} 200 -80 2 0 {name=p9 lab=vss}
C {iopin.sym} 60 -360 2 0 {name=p10 lab=d1}
C {iopin.sym} 60 -500 2 0 {name=p11 lab=d2}
C {lab_pin.sym} 120 -180 2 0 {name=p12 sig_type=std_logic lab=vss}
C {lab_pin.sym} 120 -320 2 0 {name=p4 sig_type=std_logic lab=vss}
C {lab_pin.sym} 120 -460 2 0 {name=p5 sig_type=std_logic lab=vss}
C {lab_pin.sym} 120 -400 2 0 {name=p6 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 120 -260 2 0 {name=p7 sig_type=std_logic lab=vdd}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 270 -500 3 0 {name=R1
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 270 -360 3 0 {name=R2
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 270 -220 3 0 {name=R3
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 270 -80 3 0 {name=R4
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 340 -430 0 0 {name=R5
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} 340 -290 0 0 {name=R6
w=0.5e-6
l=5.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
