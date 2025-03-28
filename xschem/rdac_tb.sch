v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {rdac_ladder.sym} -160 -120 0 0 {name=x1}
C {iopin.sym} -80 -120 0 0 {name=p1 lab=vout}
C {iopin.sym} -160 -60 1 0 {name=p2 lab=vss}
C {iopin.sym} -240 -140 2 0 {name=p5 lab=d0}
C {iopin.sym} -240 -120 2 0 {name=p6 lab=d1}
C {iopin.sym} -240 -100 2 0 {name=p7 lab=d2}
C {iopin.sym} -160 -180 3 0 {name=p8 lab=vdd}
C {code_shown.sym} 20 -470 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ
.include "../adc_model.spice"

x2 vin d0 d1 d2 adc

Vdd vdd 0 1.2
Vss vss 0 0
Vin vin 0 dc 0 SIN(0.6 0.55 50000)
*Vin vin 0 dc 0 PULSE(0.05 1.15 1u 10u 10u 1u 22u)

.control
save v(vin) v(d0) v(d1) v(d2) v(vout) v(vout2)

*tran 0.001 25u
*plot v(vin) v(d0) v(d1) v(d2) v(vout)
*plot v(vin) v(vout) v(vout2)

save @n.x2.x1.xm1.nsg13_lv_nmos[ids] @n.x2.x1.xm2.nsg13_lv_pmos[ids] @n.x2.x2.xm1.nsg13_lv_nmos[ids] @n.x2.x2.xm2.nsg13_lv_pmos[ids] @n.x2.x5.xm1.nsg13_lv_nmos[ids] @n.x2.x5.xm2.nsg13_lv_pmos[ids]
save @n.x2.x1.xm1.nsg13_lv_nmos[vds] @n.x2.x1.xm2.nsg13_lv_pmos[vds] @n.x2.x2.xm1.nsg13_lv_nmos[vds] @n.x2.x2.xm2.nsg13_lv_pmos[vds] @n.x2.x5.xm1.nsg13_lv_nmos[vds] @n.x2.x5.xm2.nsg13_lv_pmos[vds]
*setplot const
dc Vin 0.075 1.2 0.15
plot v(vout) v(vout2)
plot @n.x2.x1.xm1.nsg13_lv_nmos[vds]/@n.x2.x1.xm1.nsg13_lv_nmos[ids] @n.x2.x2.xm1.nsg13_lv_nmos[vds]/@n.x2.x2.xm1.nsg13_lv_nmos[ids] @n.x2.x5.xm1.nsg13_lv_nmos[vds]/@n.x2.x5.xm1.nsg13_lv_nmos[ids]
plot @n.x2.x1.xm2.nsg13_lv_pmos[vds]/@n.x2.x1.xm2.nsg13_lv_pmos[ids] @n.x2.x2.xm2.nsg13_lv_pmos[vds]/@n.x2.x2.xm2.nsg13_lv_pmos[ids] @n.x2.x5.xm2.nsg13_lv_pmos[vds]/@n.x2.x5.xm2.nsg13_lv_pmos[ids]

.endc
"
}
C {iopin.sym} -80 -360 0 0 {name=p3 lab=vout2}
C {iopin.sym} -160 -300 1 0 {name=p4 lab=vss}
C {iopin.sym} -240 -380 2 0 {name=p9 lab=d0}
C {iopin.sym} -240 -360 2 0 {name=p10 lab=d1}
C {iopin.sym} -240 -340 2 0 {name=p11 lab=d2}
C {iopin.sym} -160 -420 3 0 {name=p12 lab=vdd}
C {rdac_weighted.sym} -160 -360 0 0 {name=x2}
