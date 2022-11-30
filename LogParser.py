import csv


class LogParser:
    def parseFile(self, filePath):
        """
        parse and extract data from sysdig log file.
        """
        results = []
        with open(filePath, "r") as file:
            rows = file.read().split("\n")
            for row in rows:
                if len(row) > 0:
                    columns = row[1:-1].split("] [")
                    entry = {}
                    for column in columns:
                        key, value = column.split("=", 1)
                        entry[key] = value
                    results.append(entry)
        return results


    def extractFields(self, filePath):
        """
        extract required fields from parsed log file.
        """
        parsedOutput = self.parseFile(filePath)
        protocolTypes = {"tcp", "udp", "icmp", "raw"}
        outOperationTypes = {"read", "readv", "fcntl", "execve", "pipe", "sendmsg"}
        inOperationTypes = {"write", "writev", "accept", "clone", "rename", "recvmsg"}
        results = []

        for entry in parsedOutput:
            pid = None
            processName = None
            operationName = None
            eventDirection = None
            timeNanoSec = None
            fileName = None
            protocol = None
            sourceIp = None
            sourcePort = None
            destinationIp = None
            destinationPort = None

            try:
                if len(entry["procPid"]) > 0 and entry["procPid"] != "<NA>":
                    pid = entry["procPid"]
                if len(entry["procName"]) > 0 and entry["procName"] != "<NA>":
                    processName = entry["procName"]
                if len(entry["eventType"]) > 0 and entry["eventType"] != "<NA>":
                    operationName = entry["eventType"]
                    if operationName in inOperationTypes:
                        eventDirection = "<"
                    else:
                        eventDirection = ">"
                if len(entry["timeNanoSec"]) > 0 and entry["timeNanoSec"] != "<NA>":
                    timeNanoSec = entry["timeNanoSec"]
                if len(entry["fdL4Proto"]) > 0 and entry["fdL4Proto"] != "<NA>":
                    protocol = entry["fdL4Proto"]
                if len(entry["fdName"]) > 0 and entry["fdName"] != "<NA>":
                    fileName = entry["fdName"]
                if protocol in protocolTypes and fileName:
                    if "->" in fileName:
                        source, destination = fileName.split("->")
                        sourceIp, sourcePort = source.split(":")
                        destinationIp, destinationPort = destination.split(":")
                    else:
                        sourceIp, sourcePort = fileName.split(":")
                    fileName = None

            except:
                print("exception in parsing event: {}".format(entry))

            else:
                if fileName:
                    result = [pid, processName, operationName, eventDirection, fileName, sourceIp, sourcePort, destinationIp, destinationPort, protocol, timeNanoSec]
                    results.append(result)
        return results


    def writeFile(self, filePath, fields, data):
        """
        write parsed data to file.
        to write files into csv, we are storing fields as list instead of tuples.
        """
        with open(filePath, "w", newline = "") as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(data)


if __name__ == "__main__":
    """
    log parser execution starts here.
    """
    logParser = LogParser()
    data = logParser.extractFields("sysdig.txt")
    fields = ["pid", "processName", "operationName", "eventDirection", "fileName", "sourceIp", "sourcePort", "destinationIp", "destinationPort", "protocol", "timeNanoSec"]
    logParser.writeFile("parsedData.csv", fields, data)