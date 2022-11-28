import csv


def parseFile(filePath):
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


def extractFields(filePath):
    """
    extract required fields from parsed log file.
    """
    parsedOutput = parseFile(filePath)
    protocolTypes = {"tcp", "udp", "icmp", "raw"}
    results = []

    for entry in parsedOutput:
        pid = None
        processName = None
        operationName = None
        eventDirection = None
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
            if len(entry["eventDir"]) > 0 and entry["eventDir"] != "<NA>":
                eventDirection = entry["eventDir"]
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
            result = [pid, processName, operationName, eventDirection, fileName, sourceIp, sourcePort, destinationIp, destinationPort, protocol]
            results.append(result)

    return results


def writeFile(filePath, fields, data):
    """
    write parsed data to file.
    """
    with open(filePath, "w", newline = "") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(data)


if __name__ == "__main__":
    """
    log parser execution starts here.
    """
    data = extractFields("sysdig.txt")
    fields = ["pid", "processName", "operationName", "eventDirection", "fileName", "sourceIp", "sourcePort", "destinationIp", "destinationPort", "protocol"]
    writeFile("parsedData.csv", fields, data)