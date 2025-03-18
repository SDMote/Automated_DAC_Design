v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -200 -240 -200 -160 {lab=vin}
C {rdac.sym} -140 -220 0 0 {name=x1}
C {iopin.sym} -80 -220 0 0 {name=p1 lab=vout}
C {iopin.sym} -140 -160 1 0 {name=p2 lab=vss}
C {iopin.sym} -200 -160 2 0 {name=p7 lab=vin}
C {iopin.sym} -140 -280 3 0 {name=p8 lab=vdd}
C {code_shown.sym} 20 -470 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ

C1 vout 0 50p
R1 vin2 vout2 15000
C2 vout2 0 50p

Vdd vdd 0 1.2
Vss vss 0 0
Vin vin 0 PULSE(1.2 0 1u 1p 1p 10u 20u)
Vin2 vin2 0 PULSE(0 1.05 1u 1p 1p 10u 20u)

.control
save v(vin) v(vout) v(vout2)
let C=\{Cload\}
tran 0.001 10u
meas tran t1 find time when v(vout)=0.105 TD=0 RISE=1
meas tran t2 find time when v(vout)=0.945 TD=0 RISE=1
plot v(vin) v(vout) v(vout2)
print t2 - t1
print (t2-t1)/(2.2*50e-12)

.endc
"
}
