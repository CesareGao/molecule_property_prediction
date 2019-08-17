# build graph with Pagerank algorithm by using pregel and graphframes

#---------------------
# These are the lines needed to get Python to work with Spark
#---------------------
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("Graph")
sc = SparkContext(conf=conf)

sc.setLogLevel("WARN")

# Import Spark SQL for DataFrames (for use in GraphFrames)
from pyspark.sql import SQLContext
sqlCtx = SQLContext(sc)

from pyspark.sql import functions as F
from graphframes import *    # for graphframes
from graphframes.lib import Pregel

# load the data
import pandas as pd
import numpy as np
import os

edges = pd.read_csv(r"../data/edges.csv")[['molecule_name','atom_index_0','atom_index_1','type','distance']]
edges["atom_index_0"] = edges['molecule_name'] +edges['atom_index_0'].astype(str)
edges["atom_index_1"] = edges['molecule_name'] +edges['atom_index_1'].astype(str)
edges.drop('molecule_name', axis=1, inplace=True)
nodes = pd.read_csv("../data/nodes.csv")[['molecule_name','atom_index',"atom"]]
nodes["atom_index"] = nodes['molecule_name'] +nodes['atom_index'].astype(str)
nodes.drop('molecule_name', axis=1, inplace=True)
edges = edges.values.tolist()
nodes = nodes.values.tolist()



# note that 3 has no in-links
edges = sqlCtx.createDataFrame(edges, ["src", "dst","type","dist"])
edges.cache()
edges.show()

vertices = sqlCtx.createDataFrame(nodes, ["id","ele"])
vertices.cache()
vertices.show()
numVertices = vertices.count()

# This is pagerrank so we need know the outdegree so just add it to the graph
# vertices = GraphFrame(vertices, edges).outDegrees
# vertices.cache()
# vertices.show()

graph = GraphFrame(vertices, edges)
alpha = 0.15

# The pregel functions

# Initial value to give the rank col
def initialValue():
    return F.lit(1.0 / numVertices) # should be changed to one column of nodes property.

# How to update the rank col with the new message
def updatedValue():
    return F.coalesce(Pregel.msg(), F.lit(0.0)) * F.lit(1.0 - alpha) + F.lit(alpha / numVertices)

# Sending messages along the edges in the direction of the edge
def sendDst():
    return Pregel.src("rank") / Pregel.edge("dist")

# Similar to sendDst but goes reverse along the edges
# Not needed for pagerank
def sendSrc():
   return Pregel.dst("rank") / Pregel.edge("dist")

# Called when we want to aggregrate the incoming messages
def agg():
    return F.sum(Pregel.msg())

# The pregel setup calling the above functions to do most of the work
ranks = graph.pregel.setMaxIter(2).setCheckpointInterval(0).withVertexColumn("rank", initialValue(), updatedValue()).sendMsgToDst(sendDst()).aggMsgs(agg()).run()

ranks.show()


#---------------------
sc.stop()
