v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 160 -160 160 -150 {lab=vout}
N 160 -240 160 -230 {lab=vdd}
N 160 -80 160 -60 {lab=vss}
N 160 -120 180 -120 {lab=vss}
N 180 -120 180 -80 {lab=vss}
N 160 -80 180 -80 {lab=vss}
N 160 -90 160 -80 {lab=vss}
N 160 -200 180 -200 {lab=vdd}
N 180 -240 180 -200 {lab=vdd}
N 160 -240 180 -240 {lab=vdd}
N 160 -260 160 -240 {lab=vdd}
N 160 -160 240 -160 {lab=vout}
N 160 -170 160 -160 {lab=vout}
N 100 -200 120 -200 {lab=vin}
N 100 -160 100 -120 {lab=vin}
N 100 -120 120 -120 {lab=vin}
N 80 -160 100 -160 {lab=vin}
N 100 -200 100 -160 {lab=vin}
C {iopin.sym} 240 -160 0 0 {name=p1 lab=vout}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/sg13_lv_nmos.sym} 140 -120 0 0 {name=M1
l=0.13u
w=1.5u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/sg13_lv_pmos.sym} 140 -200 0 0 {name=M2
l=0.13u
w=3.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 160 -60 1 0 {name=p2 lab=vss}
C {iopin.sym} 80 -160 2 0 {name=p3 lab=vin}
C {iopin.sym} 160 -260 3 0 {name=p4 lab=vdd}
