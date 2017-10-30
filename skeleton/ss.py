import udt
import config
import socket
import select
import threading
import _thread
import struct


class StopAndWait:
	"""
	Simple implementation of Stop and Wait Transport Protocol
	"""
	def __init__(self, local_port, remote_port, msg_handler):
		self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
		self.msg_handler = msg_handler
		self.seq_num = 0
		self.lock = threading.RLock()  # to ensure thread-safe global var of seq_num
		self.header_format = "!hhh"
		# self.init_sck(local_port)

	def init_sck(self, local_port):
		# TODO: Verify if this is needed
		srv_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		srv_sck.bind(('localhost', local_port))
		srv_sck.listen(10)
		while True:
			read_sockets, write_sockets, err_sockets = select.select([srv_sck], [], [])
			for sock in read_sockets:
				if sock == srv_sck:
					client_socket, addr = sock.accept()
					read_sockets.append(client_socket)
				else:
					_thread.start_new_thread(self.handle_arrival_msg(), (sock,))

	def send(self, msg):
		"""
		Creates a transport layer segment based on msg and then sends
		the segment to the network layer
		:param msg: msg is a byte object
		:return:
		"""
		with self.lock:
			# Step 1: Prepare the Stop and Wait Header packet
			data_type = config.MSG_TYPE_DATA
			checksum = 0
			header = struct.pack(self.header_format, data_type, self.seq_num, checksum)
			checksum = self.make_checksum(header + msg)
			snd_pkt = self.make_sndpkt(data_type, self.seq_num, checksum, msg)

			# Step 2: Send the header packet over the network
			self.network_layer.send(snd_pkt)

			# Step 3: After sending, then call receive to get ack messages
			self.handle_arrival_msg_sender(snd_pkt)

	def make_checksum(self, data):
		"""
		Creates a checksum based on data_type and seq_num
		:param data: a byte object containing information
		:return: Returns the ones complement of the sum of the two args
		"""
		checksum = 0
		checksum += sum(data)
		return ~checksum

	def make_sndpkt(self, data_type, seq_num, checksum, payload):
		"""
		Creates a send packet based on arguments
		:param data_type: integer in range 1 or 2
		:param seq_num: integer in range 0 or 1
		:param checksum: integer
		:param payload: a byte object representation of the message
		:return: byte object concatenation of args and payload
		"""
		header = struct.pack(self.header_format, data_type, seq_num, checksum)
		return header + payload

	def isACK(self, rcvpkt):
		"""
		Returns True if the packet is an ACK message; false otherwise
		:param rcvpkt: a byte object represented in transport layer segment format
		:return: Boolean
		"""
		with self.lock:
			return struct.unpack("!hhh", rcvpkt)[1] == self.seq_num

	def corrupt(self, rcvpkt):
		"""
		Returns true if rcvpkt is corrupt false other wise
		:param rcvpkt: a byte object represented in transport layer segment format
		:return: Boolean
		"""
		return (sum(rcvpkt) & 1) == sum(rcvpkt)

	def handle_arrival_msg_sender(self, snd_pkt):
		"""
		Receives msg from the network layer
		Only meant for receiver
		Must make one for sender
		:return: Boolean
		"""
		packet = self.network_layer.recv()
		if self.corrupt(packet) or not self.isACK(packet):
			self.network_layer.send(snd_pkt)
			self.handle_arrival_msg_sender(snd_pkt)
		else:
			with self.lock:
				if self.seq_num == 0:
					self.seq_num == 1
				else:
					self.seq_num == 0
			return True

	def handle_arrival_msg(self):
		msg = self.network_layer.recv()
		
		# check for corruption
		# check for expected seq_num
		# build the sndpkt
		# send to the sender
		# pass msg to the app layer
		self.msg_handler(msg)

	def has_seq_0(self, rcvpkt):
		"""
		Returns True if sequence number in rcvpkt is 0
		:param rcvpkt: byte object representation of Transport Layer segment
		:return: Boolean
		"""
		pass

	def has_seq_1(self, rcvpkt):
		"""
		Returns True if sequence number in rcvpkt is 1
		:param rcvpkt: byte object representation of Transport Layer segment
		:return: Boolean
		"""
		pass

	def make_ackpkt(self, data_type, seq_num, checksum):
		"""
		Creates an acknowledgement transport packet
		:param data_type: a two byte object with values of 1 or 2
		:param seq_num: a two byte object with values of 0 or 1
		:param checksum: a two byte object that is the one's complement of the sum of data_type
		and seq_num
		:return: byte object representation of all the arguments
		"""
		pass

	def shutdown(self):
		# TODO: cleanup anything else you may have when implementing this
		"""
		# Cleanup resources.
		:return:
		"""
		self.network_layer.shutdown()
