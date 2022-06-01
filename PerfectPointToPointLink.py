import json
from threading import Thread, Lock
from FairLossPointToPointLink import FairLossPointToPointLink as FLL

class PerfectPointToPointLink:
	"""
	Module 2.3: Interface and properties of perfect point-to-point links
	Uses: FairLossPointToPointLink

	Events
	------
	Send(q, m):
		Requests to send message m to process q.
	Deliver(p, m):
		Delivers message m sent by process p.

	Properties
	----------
	PL1: Reliable delivery:
		If a correct process p sends a message m to a correct
		process q, then q eventually delivers m.
	PL2: No duplication:
		No message is delivered by a process more than once.
	PL3: No creation:
		If some process q delivers a message m with sender p, then m
		was previously sent to q by process p.
	"""

	def __init__(self, address, on_delivery = print):
		self.handle_delivery = on_delivery

		self.link = FLL(address, self.receive)

		self.pending = set()
		self.delivered = set()
		self.signature = str(address)

		self.execution = Lock()
		self.id_counter = 0

	def Send(self, q, m):
		# Requests to send message m to process q.
		with self.execution:
			message = json.dumps({
				'id': self.get_uid(),
				'message': m
			})
			self.pending.add((q, message))

		# Keep sending until delivery is confirmed.
		t = Thread(target=self.send_until_confirmed, args=(q, message))
		self.threads.append(t)
		t.start()

	def Deliver(self, p, m):
		# Delivers message m sent by process p.
		with self.execution:
			self.handle_delivery(p, m)

	def send_until_confirmed(self, q, message):
		# Keep sending until confirmed.
		self.execution.acquire()
		while((q, message) in self.pending):
			self.execution.release()
			self.execution.acquire()

			self.link.Send(q, message)

	def receive(self, p, message):
		# Receives a message and interprets it.
		message = json.loads(message)

		if(self.signature in message['id']):
			# Message is a confirmation.
			with self.execution:
				pending -= {(p, message)}

		else:
			# Deliver if not delivered.
			if(not message in self.delivered):
				self.Deliver(p, message['message'])
				self.delivered.add((p, message))

			# Send confirmation.
			self.link.Send(p, message)

	def get_uid(self):
		self.id_counter += 1
		return self.signature + str(self.id_counter)