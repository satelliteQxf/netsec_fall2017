from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32,STRING,BUFFER
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
	packet1 = Request()
	packet1.ID = 1
	packet1Bytes = packet1.__serialize__()
	packet1a = Request.Deserialize(packet1Bytes)
	assert packet1 == packet1a
	assert packet1.ID == packet1a.ID

	packet2 = Verify()
	packet2.ID = 2
	packet2.key = random.randint(1,100)
	packet2Bytes = packet2.__serialize__()
	packet2a = Verify.Deserialize(packet2Bytes)
	assert packet2 == packet2a

	packet3 = Confirm()
	packet3.Client_ID = 1
	packet3.Server_ID = 2
	packet3.key = packet2.key
	packet3Bytes = packet3.__serialize__()
	packet3a = Confirm.Deserialize(packet3Bytes)
	assert packet3 == packet3a

if __name__=="__main__":
	BasicUnitTest()


