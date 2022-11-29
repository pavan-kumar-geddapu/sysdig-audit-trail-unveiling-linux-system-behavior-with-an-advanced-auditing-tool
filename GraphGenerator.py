import csv

import jgrapht


class Backtrack:

    def __init__(self, parsedLogFile):
        self.data = []
        self.simplifiedTime = {}
        self.createTuples(parsedLogFile)

        self.processVertices = []
        self.fileVertices = []
        self.createVerticesForGraph()

        self.edges = []
        self.edgeAttrs = {}
        self.createEdgesForGraph()

        self.vertexIdDict = {}

    def createGraph(self):
        """
        create graph using jgrapht.
        """
        graph = jgrapht.create_graph(directed=True, weighted=True, allowing_self_loops=False, allowing_multiple_edges=True, any_hashable=True)

        graph.add_vertices_from(self.processVertices)
        graph.add_vertices_from(self.fileVertices)
        id = 0
        for v in graph.vertices:
            graph.vertex_attrs[v]['label'] = v
            if v in self.processVertices:
                graph.vertex_attrs[v]['shape'] = "rectangle"
            self.vertexIdDict[v] = id
            id += 1

        for edge in self.edges:
            e = graph.add_edge(edge[0], edge[1])
            edgeAttr = str(self.simplifiedTime[self.edgeAttrs[edge][0]]) + "," + str(self.simplifiedTime[self.edgeAttrs[edge][1]])
            graph.edge_attrs[e]['label'] = edgeAttr

        graphDotString = jgrapht.io.exporters.generate_dot(graph, export_vertex_id_cb=self.exportVertexIdCb)

        with open("initialGraph.dot", "w") as file:
            file.write(graphDotString)
            file.close()

    def formatData(self, row):
        """
        format read data from csv file.
        """
        resultRow = []
        for cell in row:
            if len(cell) == 0:
                resultRow.append(None)
            else:
                resultRow.append(cell)
        return resultRow

    def readDataFromFile(self, filePath):
        """
        read parsed data from csv file.
        """
        results = []
        with open(filePath, "r") as f:
            csvFile = csv.reader(f)
            for row in csvFile:
                results.append(self.formatData(row))
        return results

    def createSimplifiedTime(self, times):
        """
        simplify nano sec time to start with 0 and get increment.
        """
        times.sort()
        idx = 0
        self.simplifiedTime[times[0]] = idx
        for i in range(1, len(times)):
            if times[i] != times[i - 1]:
                idx += 1
            self.simplifiedTime[times[i]] = idx

    def createTuples(self, filePath):
        """
        create <subject, operation, object> tuples from data.
        """
        results = self.readDataFromFile(filePath)
        times = []
        for row in results[1:]:
            if row[4]:
                self.data.append(((row[0], row[1]), (row[2], row[3], row[10]), (row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[9])))
                times.append(row[10])
        self.createSimplifiedTime(times)

    def exportVertexIdCb(self, v):
        """
        export_vertex_id_cb function.
        """
        if v in self.vertexIdDict:
            return self.vertexIdDict[v]

    def createVerticesForGraph(self):
        """
        create Vertices for graph.
        """
        for row in self.data:
            process = str(row[0][0]) + " " + str(row[0][1])
            file = row[2][2]
            if process not in self.processVertices:
                self.processVertices.append(process)
            if file not in self.fileVertices:
                self.fileVertices.append(file)

    def getMaxTime(self, t1, t2):
        """
        get max of two times in nano sec.
        """
        t1s, t1n = list(map(int, t1.split(".")))
        t2s, t2n = list(map(int, t2.split(".")))
        if t1s > t2s or (t1s == t2s and t1n > t2n):
            return t1
        return t2

    def getMinTime(self, t1, t2):
        """
        get min of two times in nano sec.
        """
        t1s, t1n = list(map(int, t1.split(".")))
        t2s, t2n = list(map(int, t2.split(".")))
        if t1s > t2s or (t1s == t2s and t1n > t2n):
            return t2
        return t1

    def createEdgesForGraph(self):
        """
        create edges for graph.
        """
        for row in self.data:
            process = str(row[0][0]) + " " + str(row[0][1])
            file = row[2][2]
            direction = row[1][1]
            operation = row[1][0]
            time = row[1][2]

            key = None
            if direction == ">":
                key = (process, file)
            else:
                key = (file, process)

            if key in self.edges:
                value = self.edgeAttrs[key]
                minTime = self.getMinTime(value[0], time)
                maxTime = self.getMaxTime(value[1], time)
                self.edgeAttrs[key] = (minTime, maxTime)
            else:
                self.edges.append(key)
                self.edgeAttrs[key] = (time, time)

if __name__ == "__main__":
    """
    Graph Generator execution starts here.
    """
    backtrack = Backtrack("parsedData.csv")
    backtrack.createGraph()