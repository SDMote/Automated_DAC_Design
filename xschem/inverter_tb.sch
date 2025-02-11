v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {inverter.sym} -160 -140 0 0 {name=x1}
C {iopin.sym} -80 -140 0 0 {name=p1 lab=vout}
C {code_shown.sym} 20 -270 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt

Vdd vdd 0 1.2
Vss vss 0 0
Vin vin 0 0.7

.control
save v(vin) v(vout)
dc Vin 0 1.5 0.01
plot v(vin) v(vout)
.endc
"
}
C {iopin.sym} -160 -100 1 0 {name=p2 lab=vss}
C {iopin.sym} -220 -140 2 0 {name=p3 lab=vin}
C {iopin.sym} -160 -180 3 0 {name=p4 lab=vdd}
