v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -100 -180 -100 -170 {lab=S}
N -100 -140 -80 -140 {lab=S}
N -100 -180 -80 -180 {lab=S}
N -100 -200 -100 -180 {lab=S}
N -80 -180 -80 -140 {lab=S}
C {iopin.sym} -100 -200 3 0 {name=p2 lab=S}
C {iopin.sym} -140 -140 2 0 {name=p1 lab=G}
C {iopin.sym} -100 -110 1 0 {name=p3 lab=D}
C {code_shown.sym} 20 -330 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt

Vd D 0 0
Vs S 0 1.2
Vg G 0 0

.control
save v(d) v(s) @n.xm1.nsg13_lv_pmos[ids]
dc Vd 1.19 0 -0.01
let R=(v(d)-v(s))/@n.xm1.nsg13_lv_pmos[ids]
let R0=R[0]
let R1=1.1*R0
meas dc v1 FIND v(d) WHEN R=R1
let k= 1.2/(v1 - 1.2) - 1
print k
plot @n.xm1.nsg13_lv_pmos[ids]
plot (v(d)-v(s))/@n.xm1.nsg13_lv_pmos[ids]
.endc
"
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/sg13_lv_pmos.sym} -120 -140 0 0 {name=M1
l=0.13u
w=3.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
