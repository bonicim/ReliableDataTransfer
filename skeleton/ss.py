import udt


class StopAndWait:
	"""
	Simple implementation of Stop and Wait Transport Protocol
	"""
	def __init__(self, local_port, remote_port, msg_handler):
		self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
		self.msg_handler = msg_handler

	def send(self, msg):
		"""
		Creates a transport layer segment based on msg and then sends
		the segment to the network layer
		:param msg: msg is a byte object
		:return:
		"""
		# TODO: impl protocol to send packet from application layer.
		# call self.network_layer.send() to send to network layer.
		# self.network_layer.send(msg)
		pass

	def make_checksum(self, data_type, seq_num):
		"""
		Creates a checksum based on data_type and seq_num
		:param data_type: a two byte object having a integer value of 1 or 2
		:param seq_num: a two byte object having an integer value of 0 or 1
		:return: Returns the ones complement of the sum of the two args
		"""
		# TODO: Implement
		pass

	def make_sndpkt(self, data_type, seq_num, checksum, payload):
		"""
		Creates a send packet based on arguments
		:param data_type:
		:param seq_num:
		:param checksum:
		:param payload:
		:return: byte object consisting of arguments
		"""
		# TODO: implement
		pass

	def isACK(self, rcvpkt, seq_num):
		"""
		Returns True if the packet is an ACK message; false otherwise
		:param rcvpkt: a byte object represented in transport layer segment format
		:param seq_num: a byte object representing the expected sequence number of 0 or 1
		:return: Boolean
		"""
		# TODO: implement
		pass

	def corrupt(self, rcvpkt):
		"""
		Returns true if rcvpkt is corrupt false other wise
		:param rcvpkt: a byte object represented in transport layer segment format
		:return: Boolean
		"""
		# TODO: implement
		pass

	def notcorrupt(self, rcvpkt):
		"""
		Returns true if rcvpkt is corrupt false other wise
		:param rcvpkt: a byte object represented in transport layer segment format
		:return: Boolean
		"""
		# TODO: implement
		pass

	def handle_arrival_msg(self):
		"""
		Receives msg from the network layer
		:return:
		"""
		msg = self.network_layer.recv()
		# TODO: impl protocol to handle arrived packet from network layer.
		# call self.msg_handler() to deliver to application layer.
		pass

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
