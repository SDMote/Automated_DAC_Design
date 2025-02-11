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

Vdd vdd 0 1.2
Vss vss 0 0
Vd0 d0 0 dc 0 PULSE(0 1.2 0 2n 2n 100n 200n)
Vd1 d1 0 dc 0 PULSE(0 1.2 0 2n 2n 200n 400n)
Vd2 d2 0 dc 0 PULSE(0 1.2 0 2n 2n 400n 800n)

.control
save v(d0) v(d1) v(d2) v(vout)
tran 0.001 1000n
plot v(d0) v(d1) v(d2) v(vout)

setplot const
let i = 0
repeat 8
 alter Vd0 \{$&i / 1 % 2 * 1.2\}
 alter Vd1 \{$&i / 2 % 2 * 1.2\}
 alter Vd2 \{$&i / 4 % 2 * 1.2\}
 op
 wrdata /foss/designs/dac/python/rdac_dc.txt i vout
 set appendwrite
 let i = i + 1
end

.endc
"
}
