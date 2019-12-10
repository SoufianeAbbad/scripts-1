#!/usr/bin/env python3
import struct
import socket
from ctypes import * 

class IP(Structure):
	'''
	This class parse IP header
	'''
	# list of ip protocols

	# structre of ip header
	# total size of ip header is 20 bytes
	_fields_ = [
			("ihl", c_ubyte, 4),	# Internet Header Length represent the number of 32bits words.
			("version", c_ubyte, 4),	# ip version number ( 4 for ipv4 ) , size = 4 bits
			("tos", c_ubyte),
			("len", c_ushort),	# Total Size of ip packet not only the header (20 bytes < len < 65535), size = 2 bytes
			("id", c_ushort),	
			('offset', c_ushort),
			('ttl', c_ubyte),	# Time To Live in seconds , size = 1 byte
			('protocol_num', c_ubyte),	# Protocol Number , (1 : icmp, 6:tcp, 17:udp ...) , size = 1 byte
			('sum', c_ushort),	# Header CheckSum, size = 2 bytes
			("src", c_uint),	# Source Address , size = 4 bytes
			("dst", c_uint)	# Destination Address , size = 4 bytes
	]
	def __new__(self, socket_buffer=None):
		# create ctypes buffer from socket buffer
		return self.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer=None):
		# human readable ip
		self.src_address = socket.inet_ntoa(struct.pack('<L', self.src))
		self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))

		# get type of protocol
		if self.protocol_num == 1:
			self.protocol = 'ICMP'
		elif self.protocol_num == 6:
			self.protocol = 'TCP'
		elif self.protocol_num == 17:
			self.protocol = 'UDP'
		else :
			self.protocol = self.protocol_num

def sniffer():
	'''
	create raw socket , sniff packets , close socket
	'''

	# create socket
	socket_protocol = socket.IPPROTO_ICMP
	sniff = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

	sniff.bind(('0.0.0.0', 0))
	# include ip header in the capture
	sniff.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	# capture packet 
	try :
		while True:
			raw_buffer, addr = sniff.recvfrom(65565)

			# parse packet header
			# size of header is 20 bytes
			header = IP(raw_buffer[0:20])
			print("procotol : {}, src : {} -> dst : {}".format(header.protocol, header.src_address, header.dst_address))
	except KeyboardInterrupt:
		sniff.close()

if __name__ == '__main__':
	print("packet sniffer")
	sniffer()