v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -300 -80 -300 -60 {lab=n1}
N -140 -80 -140 -60 {lab=n2}
N -140 -220 -140 -200 {lab=n0}
N -300 -220 -140 -220 {lab=n0}
N -300 -220 -300 -140 {lab=n0}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -300 -110 0 0 {name=R1
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {iopin.sym} -220 -220 3 0 {name=p11 lab=n0}
C {iopin.sym} -300 -60 1 0 {name=p1 lab=n1}
C {code_shown.sym} 20 -270 0 0 {name=s1 only_toplevel=false value="
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ

Vn0 n0 0 1.2
Vn1 n1 0 0
Vn2 n2 0 0

.control
save v(n0) v(n3) @vn1[i] @vn2[i]
dc Vn0 0.001 1.2 0.001
plot 2*v(n0)/@vn1[i] v(n0)/@vn2[i]
.endc
"
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -140 -170 0 0 {name=R2
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/rhigh.sym} -140 -110 0 0 {name=R3
w=0.5e-6
l=10.0e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {iopin.sym} -140 -140 2 0 {name=p2 lab=n3}
C {iopin.sym} -140 -60 1 0 {name=p3 lab=n2}
