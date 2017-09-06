from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32,STRING,BUFFER,ListFieldType,PacketFields,ComplexFieldType
import random
'''
protocol:
1. The client sneds a request to the server to start a conversation:
* client sends Request(ID) to server

2. The server responds by sending a key and the id of server:
* server sends verify(ID,key) to client

3. The client sends a confirm text to start the conversation:
* client sends confirm(ID,SERVER_ID,KEY) to client

The key here is to make sure this conversation is made by this specific client and server.
'''

class Request(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.student_qxf.request"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("ID",UINT32),
	]

class Verify(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.student_qxf.verify"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("ID",UINT32),
		("key",UINT32)
	]

class Confirm(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.student_qxf.confirm"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("Client_ID",UINT32),
		("Server_ID",UINT32),
		("key",UINT32)
	]

def BasicUnitTest():

	#test packet 1
	packet1 = Request()
	packet1.ID = 1
	packet1Bytes = packet1.__serialize__()
	packet1a = Request.Deserialize(packet1Bytes)
	assert packet1 == packet1a
	assert packet1.ID == packet1a.ID

	#test packet 2
	packet2 = Verify()
	packet2.ID = 2
	packet2.key = random.randint(1,100)
	packet2Bytes = packet2.__serialize__()
	packet2a = Verify.Deserialize(packet2Bytes)
	assert packet2 == packet2a

	#test packet 3
	packet3 = Confirm()
	packet3.Client_ID = 1
	packet3.Server_ID = 2
	packet3.key = packet2.key
	packet3Bytes = packet3.__serialize__()
	packet3a = Confirm.Deserialize(packet3Bytes)
	assert packet3 == packet3a

	#now try something new
	#Deserializer()
	deserializer = PacketType.Deserializer()
	deserializer.update(packet1Bytes)
	for packet in deserializer.nextPackets():
		if packet == packet1:
			print("I got the same packet from Deserializer()!\n")

	#now try to send three packets in a byte buffer
	Bytes = packet1Bytes + packet2Bytes + packet3Bytes
	deserializer = PacketType.Deserializer()
	print("Starting with {} bytes of data".format(len(Bytes)))
	while(len(Bytes) > 0):
		chunk,Bytes = Bytes[:10],Bytes[10:]
		deserializer.update(chunk)
		print("Another 10 bytes loaded into deserializer. Left={}".format(len(Bytes)))
		for packet in deserializer.nextPackets():
			if packet == packet1:
				print("I got packet1!")
			elif packet == packet2:
				print("I got packet2!")
			elif packet == packet3:
				print("I got packet3!\n")


	#now try negative value with UINT32
	packet4 = Request()
	print ("try to initialize UINT32 with -1!")
	try:
		packet4.ID = -1
	except ValueError as e:
		print(e)
		print("\n")

	#now try list type
	class TestPacket(PacketType):
		DEFINITION_IDENTIFIER = "lab1b.student_qxf.testPacket"
		DEFINITION_VERSION = "1.0"		
		FIELDS = [
			("testlist",ListFieldType(UINT32))
		]

	packet5 = TestPacket()
	packet5.testlist = [1,2,3,4,5]
	print("the list has been appended with 1,2,3,4,5")
	packet5Bytes = packet5.__serialize__()
	packet5a = TestPacket.Deserialize(packet5Bytes)
	for i in range(0,packet5a.testlist.__len__()):
		print(packet5a.testlist.__getitem__(i),end="\t")

	print("\n\n")

	#now try subtype
	class TestSubPacket(PacketType):
		DEFINITION_IDENTIFIER = "lab1b.student_qxf.testSubPacket"
		DEFINITION_VERSION = "1.0"			

		class SubFields(PacketFields):
			FIELDS = [
				("subfield1",UINT32),
				("subfield2",UINT32)
			]

		FIELDS = [
			("testWords",STRING),
			("sub1",ComplexFieldType(SubFields)),
			("sub2",ComplexFieldType(SubFields))
		]
	packet6 = TestSubPacket()
	packet6.testWords = "Hello"
	packet6.sub1 = TestSubPacket.SubFields()
	packet6.sub2 = TestSubPacket.SubFields()
	packet6.sub1.subfield1 = 1
	packet6.sub1.subfield2 = 2
	packet6.sub2.subfield1 = 3
	packet6.sub2.subfield2 = 4
	packet6Bytes = packet6.__serialize__()
	packet6a = TestSubPacket.Deserialize(packet6Bytes)
	assert packet6.sub1.subfield1 != packet6a.sub2.subfield1
	assert packet6.sub1.subfield1 == packet6a.sub1.subfield1
	print (packet6a.sub2.subfield2)

if __name__=="__main__":
	BasicUnitTest()

