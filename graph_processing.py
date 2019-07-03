# Pagerank using pregel and graphframes

# This example is from:
# useful for pregel:
# https://graphframes.github.io/graphframes/docs/_site/api/python/graphframes.html

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

# note that 3 has no in-links
edges = sqlCtx.createDataFrame([[0, 1], [1, 2], [2, 4], [2, 0], [3, 4], [4, 0],[4, 2]], ["src", "dst"])
edges.cache()
edges.show()

vertices = sqlCtx.createDataFrame([[0], [1], [2], [3], [4]], ["id"])
vertices.show()
numVertices = vertices.count()

# This is pagerrank so we need know the outdegree so just add it to the graph
vertices = GraphFrame(vertices, edges).outDegrees
vertices.cache()
vertices.show()

graph = GraphFrame(vertices, edges)
alpha = 0.15

# The pregel functions

# Initial value to give the rank col
def initialValue():
    return F.lit(1.0 / numVertices)

# How to update the rank col with the new message
def updatedValue():
    return F.coalesce(Pregel.msg(), F.lit(0.0)) * F.lit(1.0 - alpha) + F.lit(alpha / numVertices)

# Sending messages along the edges in the direction of the edge
def sendDst():
    return Pregel.src("rank") / Pregel.src("outDegree")

# Similar to sendDst but goes reverse along the edges
# Not needed for pagerank
#def sendSrc():
#    return ???

# Called when we want to aggregrate the incoming messages
def agg():
    return F.sum(Pregel.msg())

# The pregel setup calling the above functions to do most of the work
ranks = graph.pregel.setMaxIter(5).setCheckpointInterval(0).withVertexColumn("rank", initialValue(), updatedValue()).sendMsgToDst(sendDst()).aggMsgs(agg()).run()


# This was the original example - all in one without functions
#ranks = graph.pregel.setMaxIter(5).setCheckpointInterval(0).withVertexColumn("rank", F.lit(1.0 / numVertices), F.coalesce(Pregel.msg(), F.lit(0.0)) * F.lit(1.0 - alpha) + F.lit(alpha / numVertices)).sendMsgToDst(Pregel.src("rank") / Pregel.src("outDegree")).aggMsgs(F.sum(Pregel.msg())).run()

ranks.show()


#---------------------
sc.stop()
