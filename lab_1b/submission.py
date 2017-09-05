from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32,STRING,BUFFER

class MyPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.student_qxf.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("counter1",UINT32),
		("counter2",UINT32),
		("name",STRING),
		("data",BUFFER)
	]


packet1 = MyPacket()
packet1.counter1 = 100
packet1.counter2 = 200
packet1.name = "qxf"
packet1.data = b"This may look like a string but it's actually a sequence of bytes."
packetBytes = packet1.__serialize__()

packet2 = PacketType.Deserialize(packetBytes)

if(packet1 == packet2):
	print("These two packets are the same!")
