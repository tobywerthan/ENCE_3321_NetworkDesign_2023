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
       The purpose of this homework was to create a UDP client in Python that acts as a pinger. The client is meant to interact with the provided server through UDP sockets. The client sends a message (utf-8 encoded) to the server and receives one back depending on if simulated packet loss is enabled. The round trip time of each packet, as well as the total RTT of 10 transmitted packets, is calculated. Each packet's RTT is displayed if the message from the server is received. Once all packets have been transmitted, the pinger statistics are displayed including total RTT, packet loss, and packets transmitted. This program uses the packages: time, sys, and socket. 
    </p>
</dd><dl>

<h2>main()</h2> <a name="main"></a>

<dl><dd><h3>Description</h3> <a name="mainDesc"></a></dd></dl> 

<dl><dd><dl><dd>
    <p>    
        The main program consists of three sub-functions: socket_create(), ping_client(), and ping_statistics(). Each program has dedicated tasks related to the communication between client and server as well as calculations and displaying data. 
    </p>
</dd></dl></dd></dl>

<dl><dd><h3>Flowchart</h3> <a name="mainChart"></a></dd></dl> 

<dl><dd><dl><dd><p>
<p align="center">
  <img width="250" height="600" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/5d87614f-569c-4796-9e3a-a76e2b391555">
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
        The function socket_create() handles the definition of host, port, timeout, and the creation of a UDP socket. The function starts by declaring global variables necessary throughout the program. Then the host, port, and timeout are all assigned values. The function then implements a try-except block that catches any errors in the creation of the UDP socket. The socket's timeout is also set within the try-except block. A future iteration might have two separate try-except blocks, one for the creation of the socket and the other for setting the timeout. This will help differentiate between error messages. 
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
        The function ping_client() makes use of the socket created in socket_create() to communicate with the server. First, the necessary global variables are declared, and variables are initialized. The sequence number (each iteration of the ping) is set to zero. Likewise, the total RTT, packets lost, and input count are all initialized at zero. The client input is initialized to an empty string. 
        A while loop checks the client input, and will continue looping if the string does not equal, "RND" or "NO RND". Within the loop, if the input count is greater than zero (the client has yet to input any commands since program execution) an error message is displayed with the unrecognized command. The list of valid commands is also displayed. The client input is then recorded and the input count increments. Once the while loop completes (the client enters a valid command), the entered command is displayed. 
        Another while loop then checks if the sequence number is less than ten. If so, the sequence number is incremented. The message to be sent to the server is then set to the client input. A try-except block then wraps the entire individual ping to the server. The current time is then recorded, and another try-except block is used to send the encoded message to the server. If an error occurs when sending the message, the error is printed. The data from the server is then received and another timestamp is recorded. The RTT for the individual ping is calculated using the two recorded timestamps. That value is then used to add to the total RTT. The amount of bytes received from the server is then recorded. The number of bytes, address, sequence number, and packet RTT are all displayed proceeding with a delay of one second. In the event that the client selects "RND" mode, the server will occasionally not send back messages. Because the timeout is set to one second, the exception is hit, and "Request timed out is displayed". This exception also increments packets lost. 
        Once the sequence number reaches 10, the while loop is exited, and the socket is closed. 
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
        The function ping_statistics() calculates and displays the ping statistics. First, the global variables are defined, and the title of the ping statistics section is displayed. The packet loss is then calculated by taking the total number of packets lost divided by ten and multiplied by 100. The total number of packets received is calculated by subtracting the total number of packets lost from ten. Lastly, the total number of packets transmitted, packets received, packet loss, and total RTT are displayed. 
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

<dl><dd>
    <p>
        The output of the program can be seen in both Figures 9 and 10. The client successfully pings the server and listens for an acknowledgment. Future iterations of this program might include handling when the request to the server does timeout. Instead of moving on with the next packet, the client should send the same one until it receives a successful acknowledgment. The full code is also included in Figure 11. 
    </p>
    <p align="center">
        <img width="750" height="300" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/931e1e12-d1dc-4940-851f-42b84a76c35b">
    </p>
    <p align="center">Figure 9 (Running the UDP client with no packet loss)</p>
    <p align="center">
        <img width="750" height="300" src="https://github.com/tobywerthan/ENCE_3321_NetworkDesign_2023/assets/55803740/3499f12d-fc5a-4c3f-89d3-53d198625695">
    </p>
    <p align="center">Figure 10 (Running the UDP client with packet loss)</p>
        
        import sys, time
        from time import sleep
        import socket
        
        
        # Socket create
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
        
        
        # Ping client
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
        
        
        # Run ping statistics
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
        
        
        # **************************************
        if __name__ == "__main__":
            socket_create()
            ping_client()
            ping_statistics(ptime, time)
<p align="center">Figure 11 (Full code for the UDP client))</p>
</dd><dl>
    
</div>
