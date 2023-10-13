# Homework 4: UDP Client Pinger

Toby Werthan

10/13/2023

ENCE 3321

## Table of Contents
1. [Introduction](#introduction)
2. [main()](#main)
    1. [Description](#mainDesc)
    2. [Flow Chart](#mainChart)
    3. [Code](#mainCode)
3. [socket_create()](#create)
    1. [Description](#createDesc)
    2. [Flow Chart](#createChart)
    3. [Code](#createCode)
4. [ping_client()](ping#)
    1. [Description](#pingDesc)
    2. [Flow Chart](#pingChart)
    3. [Code](#pingCode)
5. [ping_statistics()](#stats)
    1. [Description](#statsDesc)
    2. [Flow Chart](#statsChart)
    3. [Code](#statsCode)
6. [Conclusion](#conclusion)

*Note: If images are hard to view, please click on them. A new tab will open, displaying the full-size image.*
<div align="left">
<h2>Introduction</h2>  <a name="introduction"></a>
<dl><dd>
    <p>
       The purpose of this lab was to incorporate the simple electrostatic discharge protection circuit seen in Figure 1 with the padframe constructed in Lab 2. The circuit consists of two diodes that regulate the voltage through the output node. Integrating ESD protection in the padframe will help prevent the internal logic from being damaged. The final integrated circuit consists of a pad cell that has ESD protection, a padframe consisting of pad cells with ESD protection, and finally an NMOS transistor connected to the ESD-protected padframe. 
    </p>
</dd><dl>

<h2>main()</h2> <a name="main"></a>

<dl><dd><h3>Description</h3> <a name="mainDesc"></a></dd></dl> 

<dl><dd><dl><dd>
    <p>    
        The schematic for the pad cell with ESD protection (Figure 2) is similar to Figure 1. The voltage source is connected to a pActive-nWell diode, while ground is connected to a pWell-nActive diode. The connection pin to the pad cell is connected between both diodes. 
    </p>
</dd></dl></dd></dl>

<dl><dd><h3>Flowchart</h3> <a name="mainChart"></a></dd></dl> 

<dl><dd><dl><dd><p>
<p align="center">
  <img width="325" height="500" src="https://github.com/tobywerthan/ENCE_3501_VLSI_2023/assets/55803740/0ae45432-c1fe-41d4-857e-ba36e2a3f9ca">
</p>
<p align="center">Figure 4 (Layout of the pad cell with ESD protection created in Electric VLSI)</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="mainCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    
</p></dd></dl></dd></dl>

<h2>socket_create()</h2> <a name="create"></a>

<dl><dd><h3>Description</h3> <a name="createDesc"></a></dd></dl> 

<dl><dd><dl><dd>
    <p>    
        The schematic for the pad cell with ESD protection (Figure 2) is similar to Figure 1. The voltage source is connected to a pActive-nWell diode, while ground is connected to a pWell-nActive diode. The connection pin to the pad cell is connected between both diodes. 
    </p>
</dd></dl></dd></dl>

<dl><dd><h3>Flowchart</h3> <a name="createChart"></a></dd></dl> 

<dl><dd><dl><dd><p>
<p align="center">
  <img width="325" height="500" src="https://github.com/tobywerthan/ENCE_3501_VLSI_2023/assets/55803740/0ae45432-c1fe-41d4-857e-ba36e2a3f9ca">
</p>
<p align="center">Figure 4 (Layout of the pad cell with ESD protection created in Electric VLSI)</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="createCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    
</p></dd></dl></dd></dl>

<h2>ping_client()</h2> <a name="ping"></a>

<dl><dd><h3>Description</h3> <a name="pingDesc"></a></dd></dl> 

<dl><dd><dl><dd>
    <p>    
        The schematic for the pad cell with ESD protection (Figure 2) is similar to Figure 1. The voltage source is connected to a pActive-nWell diode, while ground is connected to a pWell-nActive diode. The connection pin to the pad cell is connected between both diodes. 
    </p>
</dd></dl></dd></dl>

<dl><dd><h3>Flowchart</h3> <a name="pingChart"></a></dd></dl> 

<dl><dd><dl><dd><p>
<p align="center">
  <img width="325" height="500" src="https://github.com/tobywerthan/ENCE_3501_VLSI_2023/assets/55803740/0ae45432-c1fe-41d4-857e-ba36e2a3f9ca">
</p>
<p align="center">Figure 4 (Layout of the pad cell with ESD protection created in Electric VLSI)</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="pingCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    
</p></dd></dl></dd></dl>

<h2>ping_statistics()</h2> <a name="stats"></a>

<dl><dd><h3>Description</h3> <a name="statsDesc"></a></dd></dl> 

<dl><dd><dl><dd>
    <p>    
        The schematic for the pad cell with ESD protection (Figure 2) is similar to Figure 1. The voltage source is connected to a pActive-nWell diode, while ground is connected to a pWell-nActive diode. The connection pin to the pad cell is connected between both diodes. 
    </p>
</dd></dl></dd></dl>

<dl><dd><h3>Flowchart</h3> <a name="statsChart"></a></dd></dl> 

<dl><dd><dl><dd><p>
<p align="center">
  <img width="325" height="500" src="https://github.com/tobywerthan/ENCE_3501_VLSI_2023/assets/55803740/0ae45432-c1fe-41d4-857e-ba36e2a3f9ca">
</p>
<p align="center">Figure 4 (Layout of the pad cell with ESD protection created in Electric VLSI)</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="statsCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    
</p></dd></dl></dd></dl>

<h2>Conclusion</h3>  <a name="conclusion"></a>
    Connecting each pad cell to this simple ESD protection circuit provides some defense against ESD for the internals of the IC. This design can be used in further projects for more complex circuits, and padframes can be created from this library that incorporate more complex ESD protection as well. Lab 4 dives further into the use of transistors for the design of pullup and pulldown networks for logic gates, specifically, the inverter. 
</div>
