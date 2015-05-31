import socket, sys
from struct import *
from sample_manager import SampleManager

class Sniffer: 
   
    def __init__(self):
        self.__ownmac = "b8:27:eb:7c:ca:88"

    def eth_addr(self, a):
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
        return b
 
    def doSniff(self):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
         
        i = 0
        while True:
            i = i + 1
            packet = s.recvfrom(65565)
            packet = packet[0]

            source_mac = packet[6:12];
            if self.eth_addr(source_mac) == self.__ownmac:
                continue             

            unique = ord(source_mac[5]) % 3;

            eth_length = 14
            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_protocol = socket.ntohs(eth[2])

            if eth_protocol == 8:
                ip_header = packet[eth_length:20+eth_length]
                 
                iph = unpack('!BBHHHBBH4s4s' , ip_header)
                
                version_ihl = iph[0]
                version = version_ihl >> 4
                ihl = version_ihl & 0xF
                iph_length = ihl * 4        
 
                ttl = iph[5]
                protocol = iph[6]
                s_addr = socket.inet_ntoa(iph[8]);
                d_addr = socket.inet_ntoa(iph[9]);

                if (protocol == 1): #ICMP
                    print "ICMP :D "+str(i)
                    SampleManager.playFromFile('bytes/icmp'+str(unique))

                elif (protocol == 17): #UDP
                    u = iph_length + eth_length
                    udp_header = packet[u:u+8] 
                    
                    udph = unpack('!HHHH' , udp_header)
                    source_port = udph[0]
                    dest_port = udph[1]                    
                    
                    if dest_port == 5353: #MDNS
                        SampleManager.playFromFile('bytes/mdns')

                    elif dest_port == 53: #DNS
                        SampleManager.playFromFile('bytes/dns')
                        print "DNS"

                    elif dest_port == 67 or dest_port == 68: #DHCP
                        SampleManager.playFromFile('bytes/dhcp')    

                    else:
                        print "Other UDP Packet"
                        print "src:"+str(source_port)+" dest:"+str(dest_port)

                # else: 
                    #print "iph: "+str(protocol)
                    #print iph
            
            elif eth_protocol == 1544:  #Guess: ARP
                SampleManager.playFromFile('bytes/arp')

            else:
                print "eth: "+str(eth_protocol)
                print eth


s = Sniffer()

s.doSniff()
