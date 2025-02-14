v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {rdac.sym} -140 -120 0 0 {name=x1}
C {iopin.sym} -80 -120 0 0 {name=p1 lab=vout}
C {iopin.sym} -140 -60 1 0 {name=p2 lab=vss}
C {iopin.sym} -200 -140 2 0 {name=p5 lab=d0}
C {iopin.sym} -200 -120 2 0 {name=p6 lab=d1}
C {iopin.sym} -200 -100 2 0 {name=p7 lab=d2}
C {iopin.sym} -140 -180 3 0 {name=p8 lab=vdd}
C {code_shown.sym} 20 -370 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ
.include "../adc_model.spice"

x2 vin d0 d1 d2 adc

Vdd vdd 0 1.2
Vss vss 0 0
Vin vin 0 dc 0 SIN(0.6 0.6 1000000)

.control
save v(vin) v(d0) v(d1) v(d2) v(vout)

tran 0.001 2u
plot v(vin) v(d0) v(d1) v(d2) v(vout)

*setplot const
*dc Vin 0.075 1.2 0.15
*plot v(vout)

.endc
"
}
