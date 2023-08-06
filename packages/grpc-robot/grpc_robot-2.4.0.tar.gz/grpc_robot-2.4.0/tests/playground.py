# from dmi_tools import DmiTools
from grpc_robot.tools.voltha_tools import VolthaTools

# records = [
#  {'message': b"\x08e\x12Y\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$96f716bd-9e72-5c39-9a79-58bb3821df19\x1a\x07cpu 0/1\x1a9\x08\x07\x10\x01\x18\t(\x012\x07percent:\x06\x08\xde\x96\x84\xfd\x05@\x88'J\x1bMETRIC_CPU_USAGE_PERCENTAGE",
#   'timestamp': 1604389726676,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xaf\x02\x12f\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$f14853c0-51e8-5f5a-8983-e8dc9c060f5d\x1a\x14storage-resource 0/1\x1a:\x08_\x10\x01\x18\t(\x012\x07percent:\x06\x08\xe3\x96\x84\xfd\x05@\x88'J\x1cMETRIC_DISK_USAGE_PERCENTAGE",
#   'timestamp': 1604389731109,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$81ba5a6b-b8b9-582e-9cea-a512ed6bd8ad\x1a\x10power-supply 0/1\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xe7\x96\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389735478,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$760d33cd-ad0d-541b-8014-272af0cfbff8\x1a\x10power-supply 0/2\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xe7\x96\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389735478,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$0f3a8a29-2b79-560a-a034-2255e0c85920\x1a\x13pluggable-fan 0/1/1\x1a+\x08\xc0%\x10\n\x18\t(\x012\x03rpm:\x06\x08\xeb\x96\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389739993,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$80d0e158-efc0-59ea-808d-e273d1c46099\x1a\x13pluggable-fan 0/1/2\x1a+\x08\xe5&\x10\n\x18\t(\x012\x03rpm:\x06\x08\xeb\x96\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389739993,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$15d3103a-36b2-5774-ae06-d2d59a2ab6e7\x1a\x13pluggable-fan 0/1/3\x1a+\x08\xc8$\x10\n\x18\t(\x012\x03rpm:\x06\x08\xeb\x96\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389739993,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xd8\x04\x12a\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$dc8c95f1-6b84-5e6d-b645-c76b02b7551b\x1a\x0ftemperature 0/1\x1aB\x085\x10\x08\x18\t(\x012\x0edegree Celsius:\x06\x08\xf0\x96\x84\xfd\x05@\x88'J\x1dMETRIC_INNER_SURROUNDING_TEMP",
#   'timestamp': 1604389744403,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08e\x12Y\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$96f716bd-9e72-5c39-9a79-58bb3821df19\x1a\x07cpu 0/1\x1a9\x08\x0f\x10\x01\x18\t(\x012\x07percent:\x06\x08\x9b\x97\x84\xfd\x05@\x88'J\x1bMETRIC_CPU_USAGE_PERCENTAGE",
#   'timestamp': 1604389787831,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xaf\x02\x12f\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$f14853c0-51e8-5f5a-8983-e8dc9c060f5d\x1a\x14storage-resource 0/1\x1a:\x08_\x10\x01\x18\t(\x012\x07percent:\x06\x08\xa0\x97\x84\xfd\x05@\x88'J\x1cMETRIC_DISK_USAGE_PERCENTAGE",
#   'timestamp': 1604389792190,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$81ba5a6b-b8b9-582e-9cea-a512ed6bd8ad\x1a\x10power-supply 0/1\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xa4\x97\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389796608,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$760d33cd-ad0d-541b-8014-272af0cfbff8\x1a\x10power-supply 0/2\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xa4\x97\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389796608,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$0f3a8a29-2b79-560a-a034-2255e0c85920\x1a\x13pluggable-fan 0/1/1\x1a+\x08\xc0%\x10\n\x18\t(\x012\x03rpm:\x06\x08\xa9\x97\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389801159,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$80d0e158-efc0-59ea-808d-e273d1c46099\x1a\x13pluggable-fan 0/1/2\x1a+\x08\xf4&\x10\n\x18\t(\x012\x03rpm:\x06\x08\xa9\x97\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389801159,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\x01\x12e\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$15d3103a-36b2-5774-ae06-d2d59a2ab6e7\x1a\x13pluggable-fan 0/1/3\x1a+\x08\xc8$\x10\n\x18\t(\x012\x03rpm:\x06\x08\xa9\x97\x84\xfd\x05@\x88'J\x10METRIC_FAN_SPEED",
#   'timestamp': 1604389801159,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xd8\x04\x12a\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$dc8c95f1-6b84-5e6d-b645-c76b02b7551b\x1a\x0ftemperature 0/1\x1aB\x085\x10\x08\x18\t(\x012\x0edegree Celsius:\x06\x08\xad\x97\x84\xfd\x05@\x88'J\x1dMETRIC_INNER_SURROUNDING_TEMP",
#   'timestamp': 1604389805353,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08e\x12Y\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$96f716bd-9e72-5c39-9a79-58bb3821df19\x1a\x07cpu 0/1\x1a9\x08\x0f\x10\x01\x18\t(\x012\x07percent:\x06\x08\xd8\x97\x84\xfd\x05@\x88'J\x1bMETRIC_CPU_USAGE_PERCENTAGE",
#   'timestamp': 1604389848403,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xaf\x02\x12f\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$f14853c0-51e8-5f5a-8983-e8dc9c060f5d\x1a\x14storage-resource 0/1\x1a:\x08_\x10\x01\x18\t(\x012\x07percent:\x06\x08\xdc\x97\x84\xfd\x05@\x88'J\x1cMETRIC_DISK_USAGE_PERCENTAGE",
#   'timestamp': 1604389852771,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$81ba5a6b-b8b9-582e-9cea-a512ed6bd8ad\x1a\x10power-supply 0/1\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xe1\x97\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389857207,
#   'topic': 'dm.metrics'},
#  {'message': b"\x08\xf6\x03\x12b\n&\n$4c411df2-22e6-58d2-b1bb-545a0263d18d\x12&\n$760d33cd-ad0d-541b-8014-272af0cfbff8\x1a\x10power-supply 0/2\x1a;\x082\x10\x01\x18\t(\x012\x07percent:\x06\x08\xe1\x97\x84\xfd\x05@\x88'J\x1dMETRIC_POWER_USAGE_PERCENTAGE",
#   'timestamp': 1604389857207,
#   'topic': 'dm.metrics'}]

records = [
    {
        'message': b'\nL\n#Voltha.openolt..1613491472935896440\x10\x02\x18\x04 \x02*\x030.12\x0c\x08\x90\xda\xaf\x81\x06\x10\x97\xb2\xa2\xbe\x03:\x0c\x08'
                   b'\x90\xda\xaf\x81\x06\x10\x86\xd3\xa2\xbe\x03"\xc2\x02\x11@w,\xf2Ed\xb6C\x1a\xb6\x02\n\x93\x01\n\x08NNIStats\x119w,\xf2Ed\xb6C*$a3281'
                   b'32d-ad87-4edf-976e-ad1a364144012-\n\x05oltid\x12$a328132d-ad87-4edf-976e-ad1a364144012\x15\n\ndevicetype\x12\x07openolt2\x12\n\tport'
                   b'label\x12\x05nni-0\x12\x15\n\x0eTxMcastPackets\x15\x00\x80\xccD\x12\x15\n\x0eTxBcastPackets\x15\x00\x80\xccD\x12\x0e\n\x07RxBytes\x15'
                   b'\x00p\xaaH\x12\x10\n\tRxPackets\x15\x00p\xaaE\x12\x15\n\x0eRxMcastPackets\x15\x00\x80\xccD\x12\x15\n\x0eRxBcastPackets\x15\x00\x80\xcc'
                   b'D\x12\x0e\n\x07TxBytes\x15\x00p\xaaH\x12\x10\n\tTxPackets\x15\x00p\xaaE',
        'timestamp': -1,
        'topic': 'voltha.events'
    },
    {
        'message': b'\nJ\n#Voltha.openolt..1613491472935961326\x10\x02 \x02*\x030.12\x0c\x08\x90\xda\xaf\x81\x06\x10\xdf\xba\xa6\xbe\x03:\x0c\x08\x90\xda'
                   b'\xaf\x81\x06\x10\xb8\xcf\xa6\xbe\x03"\xc2\x02\x11?x,\xf2Ed\xb6C\x1a\xb6\x02\n\x93\x01\n\x08PONStats\x11=x,\xf2Ed\xb6C*$a328132d-ad87'
                   b'-4edf-976e-ad1a364144012-\n\x05oltid\x12$a328132d-ad87-4edf-976e-ad1a364144012\x15\n\ndevicetype\x12\x07openolt2\x12\n\tportlabel\x12'
                   b'\x05pon-0\x12\x0e\n\x07TxBytes\x15\x00\xd0\xa6H\x12\x10\n\tTxPackets\x15\x00\xd0\xa6E\x12\x15\n\x0eTxMcastPackets\x15\x00 \xc8D\x12'
                   b'\x15\n\x0eTxBcastPackets\x15\x00 \xc8D\x12\x0e\n\x07RxBytes\x15\x00\xd0\xa6H\x12\x10\n\tRxPackets\x15\x00\xd0\xa6E\x12\x15\n\x0eRxMc'
                   b'astPackets\x15\x00 \xc8D\x12\x15\n\x0eRxBcastPackets\x15\x00 \xc8D',
        'timestamp': -1,
        'topic': 'voltha.events'
    }
]

for record in records:
    print(VolthaTools.events_decode_event(record.get('message'), return_defaults=True))
