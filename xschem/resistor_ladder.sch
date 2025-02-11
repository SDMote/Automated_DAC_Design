v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -300 -460 -260 -460 {lab=d2}
N -200 -460 -160 -460 {lab=vout}
N -160 -460 -160 -420 {lab=vout}
N -160 -460 -80 -460 {lab=vout}
N -160 -320 -160 -280 {lab=#net1}
N -160 -180 -160 -40 {lab=#net2}
N -200 -180 -160 -180 {lab=#net2}
N -160 -220 -160 -180 {lab=#net2}
N -200 -320 -160 -320 {lab=#net1}
N -160 -360 -160 -320 {lab=#net1}
N -300 -320 -260 -320 {lab=d1}
N -300 -180 -260 -180 {lab=d0}
N -200 -40 -160 -40 {lab=#net2}
N -300 -40 -260 -40 {lab=vss}
C {iopin.sym} -80 -460 0 0 {name=p1 lab=vout}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -230 -460 3 0 {name=R1
w=0.5e-6
l=1.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -230 -320 3 0 {name=R2
w=0.5e-6
l=1.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -230 -180 3 0 {name=R3
w=0.5e-6
l=1.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -230 -40 3 0 {name=R4
w=0.5e-6
l=1.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -160 -390 0 0 {name=R5
w=0.5e-6
l=0.5e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -160 -250 0 0 {name=R6
w=0.5e-6
l=0.5e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {iopin.sym} -300 -180 2 0 {name=p3 lab=d0}
C {iopin.sym} -300 -320 2 0 {name=p10 lab=d1}
C {iopin.sym} -300 -460 2 0 {name=p11 lab=d2}
C {iopin.sym} -300 -40 2 0 {name=p9 lab=vss}
C {code_shown.sym} 20 -470 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ

Vdd vdd 0 1.2
Vss vss 0 0
Vd0 d0 0 PULSE(0 1.2 0 1p 1p 100n 200n)
Vd1 d1 0 PULSE(0 1.2 0 1p 1p 200n 400n )
Vd2 d2 0 PULSE(0 1.2 0 1p 1p 400n 800n)

.control
save v(d0) v(d1) v(d2) v(vout)
tran 0.001 1500n
plot v(d0) v(d1) v(d2) v(vout)
.endc
"
}
