class Subject:
    def __init__(self, pid, processName):
        self.pid = pid
        self.processName = processName

class Operation:
    def __init__(self, operationName, eventDirection):
        self.operationName = operationName
        self.eventDirection = eventDirection

class Object:
    def __init__(self, pid, processName, fileName, sourceIp, sourcePort, destinationIp, destinationPort, protocol):
        self.pid = pid
        self.processName = processName
        self.fileName = fileName
        self.sourceIp = sourceIp
        self.sourcePort = sourcePort
        self.destinationIp = destinationIp
        self.destinationPort = destinationPort
        self.protocol = protocol

class SysdigNode:
    def __init__(self, subject, operation, object):
        self.subject = subject
        self.operation = operation
        self.object = object

def printSysdigNode(sysdigNode):
    if sysdigNode.object.protocol:
        print(sysdigNode.subject.pid, sysdigNode.subject.processName, sysdigNode.operation.operationName, sysdigNode.operation.eventDirection, \
              sysdigNode.object.fileName, sysdigNode.object.sourceIp, sysdigNode.object.sourcePort, \
                sysdigNode.object.destinationIp, sysdigNode.object.destinationPort, sysdigNode.object.protocol)