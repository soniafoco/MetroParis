from database.DAO import DAO
from model.model import Model

myModel = Model()

myModel.buildGraph()

print(f"The graph has {myModel.getNumNodes()} nodes")
print(f"The graph has {myModel.getNumEdges()} edges")

myLinee = DAO.getAllLinee()
print(myLinee)