import csv
import jgrapht

class GraphGenerator:
    """
    Class for graph generation.
    """
    def __init__(self):
        self._vertexIdDict = {}

    def createGraph(self, data):
        """
        create graph using jgrapht.
        """
        graph = jgrapht.create_graph(directed=True, weighted=True, allowing_self_loops=False, allowing_multiple_edges=True, any_hashable=True)
        processVertices, fileVertices = self.getVerticesForGraph(data)
        edges, edgeAttrs = self.getEdgesForGraph(data)

        graph.add_vertices_from(processVertices)
        graph.add_vertices_from(fileVertices)

        for i in range(len(edges)):
            e = graph.add_edge(edges[i][0], edges[i][1])
            # graph.edge_attrs[e]['label'] = edgeAttrs[i]


        id = 0
        for v in graph.vertices:
            graph.vertex_attrs[v]['label'] = v
            if v in processVertices:
                graph.vertex_attrs[v]['shape'] = "rectangle"
            self._vertexIdDict[v] = id
            id += 1

        graphDotString = jgrapht.io.exporters.generate_dot(graph, export_vertex_id_cb=self.exportVertexIdCb)

        with open("initialGraph.dot", "w") as file:
            file.write(graphDotString)
            file.close()
    def exportVertexIdCb(self, v):
        """
        export_vertex_id_cb function.
        """
        if v in self._vertexIdDict:
            return self._vertexIdDict[v]
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

    def createTuples(self, data):
        """
        create <subject, operation, object> tuples from data.
        """
        results = []
        for row in data[1:]:
            if row[4]:
                results.append(((row[0], row[1]), (row[2], row[3], row[10]), (row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[9])))
        return results

    def getVerticesForGraph(self, data):
        """
        create Vertices for graph.
        """
        processVertices = []
        fileVertices = []
        for row in data:
            process = str(row[0][0]) + " " + str(row[0][1])
            file = row[2][2]
            if process not in processVertices:
                processVertices.append(process)
            if file not in fileVertices:
                fileVertices.append(file)
        return processVertices, fileVertices

    def getEdgesForGraph(self, data):
        """
        create edges for graph.
        """
        edges = []
        edgeAttrs = []
        for row in data:
            process = str(row[0][0]) + " " + str(row[0][1])
            file = row[2][2]
            direction = row[1][1]
            if direction == ">":
                edges.append((process, file))
            else:
                edges.append((file, process))
            edgeAttrs.append(row[1][0])
        return edges, edgeAttrs



if __name__ == "__main__":
    """
    Graph Generator execution starts here.
    """
    graphGenerator = GraphGenerator()
    data = graphGenerator.readDataFromFile("parsedData.csv")
    tuples = graphGenerator.createTuples(data)
    graphGenerator.createGraph(tuples)
