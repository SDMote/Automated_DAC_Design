# R2R-ladder DAC

The R2R-ladder DAC, as shown in the figure, is made of inverters (one for each resolution bit) that are connected to a ladder of resistors, 
which have a unit resistance (R) or twice the unit resistance (2R). It can be shown that, by supperposition, each bit $i$ of an **ideal** N-bit 
R2R DAC produces $v_i=V_{REF}\cdot\frac{2^i}{2^N}$ in the output.

![R2R Circuit](https://raw.githubusercontent.com/SDMote/Automated_DAC_Design/main/background/resistor_ladder_dac.png)

However, to produce the desired output perfectly, the R-2R ratio in the ladder must be precise, making this circuit very sensitive to parasitic 
resistances, particularly the on-resistances of the inverter transistors.
Then, the main design parameters for the circuit are the sizing of the unit resistor and the transistors in the inverter, that is, width and 
lenght for 3 devices: NMOS, PMOS and resistor.

In general, we need the on-resistances of the transistors to be negligible compared to the unit resistance R. Resistor width and transistor 
lenght are fixed for convenience. Then, increasing the resistor lenght is an easy solution but it comes at the expense of reducing the circuit speed. 
It will also be necessary to increase the transistors width to reduce their on-resistances. Increasing the area of the pysical implementation 
with both of this actions will increase the parasitic resistance of the routing between devices.


## Nonlinearity estimation

Under the assumption that the on-resistances of the transistors are constant over input codes and bits, the voltage output of the DAC can be 
calculated recursively taking the on-resistances into consideration, as shown in the following figure. This allows to estimate the nonlinearity 
of the circuit much faster than with simulation.

![Output calculation](https://raw.githubusercontent.com/SDMote/Automated_DAC_Design/main/background/r2r_dac.png)

Simulation of the top-level circuit showed that the transistors on-resistance behaves constant over input codes and bits if they are sufficiently 
small compared to the unit resistance. This is usually true in the relevant solution space. Moreover, under the same conditions, it can be observed 
that the value of the on-resistances varies very little when changing the resolution of the DAC. This was leveraged in the circuit design step, 
where on-resistance estimation is always done by simulating a 2-bit DAC and top-level performance is estimated analyticaly as explained above. 
Since the spice simulation time increases exponentially with the number of bits, this method reduces computation time significantly. 
The results show that the presented R2R-ladder DAC design loop can effectively reach the target performance without simulating the top-level circuit.