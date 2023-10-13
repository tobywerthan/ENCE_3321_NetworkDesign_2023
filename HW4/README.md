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
  <img width="300" height="600" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/5d87614f-569c-4796-9e3a-a76e2b391555">
</p>
<p align="center">Figure 1 (Flowchart of main())</p>

</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="mainCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    if __name__ == "__main__":
        socket_create()
        ping_client()
        ping_statistics(ptime, time)
<p align="center">Figure 2 (Snippet of the code from main())</p>
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
  <img width="325" height="700" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/04bbc010-37b5-4516-bc7c-ca61b8a1234a">

</p>
<p align="center">Figure 3 (Flowchart of socket_create())</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="createCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    def socket_create():
        # Global variables
        global host
        global port
        global s
        global addr
    
        # Assign host and port and define timeout
        host = "localhost"
        port = 1001
        timeout = 1
    
        # Try except for socket creation
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(timeout)
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
<p align="center">Figure 4 (Snippet of the code from socket_create())</p>
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
  <img width="600" height="1150" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/5dbcc58b-e46f-41ab-8aa8-6090000919bd">
</p>
<p align="center">Figure 5 (Flowchart of ping_client())</p>

</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="pingCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    def ping_client():
        # Global variables
        global s, host, port, RTT, ptime, addr, time, packet_lost
    
        # Sequence number of the ping message
        ptime = 0
    
        # Set round trip time, number of packets lost, client input, and number of client inputs to empty or zero
        RTT = 0
        packet_lost = 0
        client_input = ""
        input_count = 0
    
        # Get the input message from the client
        while not (client_input == "RND" or client_input == "NO RND"):
            if input_count > 0:
                print("ping> Unrecognized Command: {}".format(client_input))
                print("      Valid Commands: RND, NO RND")
            client_input = input("ping> ").strip()
            input_count += 1
        print("")
        print("Pinging server in mode: {}".format(client_input))
        print("")
    
        # Ping for 10 times
        while ptime < 10:
            ptime += 1
            # Format the message to be sent
            message = client_input
    
            try:
                # Sent time
                RTTb = time.time()
    
                # Send the UDP packet with the ping message
                try:
                    s.sendto(message.encode("utf-8"), (host, port))
                except socket.error as msg:
                    print(str(msg))
    
                # Receive the server response
                data, addr = s.recvfrom(2048)
    
                # Received time
                RTTa = time.time()
    
                # Compute RTT
                RTT_packet = RTTa - RTTb
                RTT = (RTT_packet) + RTT
    
                # Display packet time
                dataCount = len(data)
                print(
                    "{} bytes from {}: seq={} time={} ms".format(
                        dataCount, addr[0], ptime, RTT_packet * 1000
                    )
                )
    
                # Delay for readability
                sleep(1)
    
            except:
                # Server does not response
                # Assume the packet is lost
                print("Request timed out.")
                packet_lost += 1
                continue
    
        # Close socket
        s.close()
<p align="center">Figure 6 (Snippet of the code from ping_client())</p>
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
  <img width="325" height="600" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/e9ae46e1-4275-450a-b67c-1db80d31343d">
</p>
<p align="center">Figure 7 (Flowchart of ping_statistics())</p>
</p></dd></dl></dd></dl>

<dl><dd><h3>Code</h3> <a name="statsCode"></a></dd></dl> 

<dl><dd><dl><dd><p>

    def ping_statistics(ptime, time):
    # Global variables
    global s, host, port, RTT, addr

    print("")
    print("--- IP ping statistics ---")

    # Print statistics
    packet_loss = ((packet_lost) / 10) * 100
    packet_recieved = 10 - packet_lost
    print(
        "{} packets transmitted, {} recieved, {}% packet loss, time {} ms".format(
            ptime, packet_recieved, packet_loss, RTT * 1000
        )
    )
<p align="center">Figure 8 (Snippet of the code from ping_statistics())</p>
</p></dd></dl></dd></dl>

<h2>Conclusion</h3>  <a name="conclusion"></a>
    Connecting each pad cell to this simple ESD protection circuit provides some defense against ESD for the internals of the IC. This design can be used in further projects for more complex circuits, and padframes can be created from this library that incorporate more complex ESD protection as well. Lab 4 dives further into the use of transistors for the design of pullup and pulldown networks for logic gates, specifically, the inverter. 
</div>
