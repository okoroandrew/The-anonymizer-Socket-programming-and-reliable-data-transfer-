# The anonymizer: Socket-programming and reliable data transfer.
Anonymizer is a client-server application that anonymizes user-specified keyword from a text file. The server and client commuicate via a socket using TCP (a reliable transport layer protocol) and UDP with stop-and-wait protocol (to ensure reliability of the UDP protocol).

A socket is an Application Programming Interface (API), it is the interface between the application layer and the transport layer within a host. A program running on a host (client) sends a message into the client socket which is carried by the underlying transport layer (TCP or UDP) protocol to the server socket from where it is received into the end host(server).

## TCP VS UDP
TCP on the one hand is a connection-oriented transportation layer protocol that guarantees message delivery and in the correct order, whereas on the other hand UDP is not connection oriented, and does not guarantee message delivery, but could be faster than the TCP. The application developer does not have control over these protocols other than choosing which of them is best suited to the intended communication between the end hosts.  

## PARTS
This project has 3 parts:
1. TCP programming for both server and client 
2. Stop and wait reliability over UDP for both server and client. 
3. Wireshark trace collection and analysis. 

## OBSERVATIONS
1. The overall delay in TCP is always higher than the corresponding delay in UDP. This could be caused by a lot of fields used in the TCP header to ensure reliability. For example, the acknowledgment segment is present in the TCP header but absent for the UDP header. Also, TCP is connection-oriented, time taken to establish this connection contributes to the overall delay. 

2. The throughput for UDP is always greater than the corresponding throughput in TCP. This is because UDP allows continuous packet stream compared to TCP that does not allow continues packet stream to ensure reliable transfer, flow control, and congestion control. 

## CONCLUSION
In conclusion UDP is faster than TCP, it ensures that data is sent to the destination as fast as possible, however it does not guarantee that the packet will be delivered and in order. TCP guarantees that the data will be delivered, this it does by using the acknowledgment segment in the header to acknowledge packets received
