# projx - Graph transformations in Python

**pre-alpha**

**projx** provides a simple and extensible API for interacting with graphs in Python. Its core functionality is built around making graph transformations using the [NetworkX](https://networkx.github.io/) module and a DSL based on [Neo4j's](http://neo4j.com/) [Cypher](http://neo4j.com/docs/stable/cypher-query-lang.html) query language. It also provides an extensible ETL pipeline that uses JSON configuration (roughly modeled after [orientdb-etl](https://github.com/orientechnologies/orientdb-etl/wiki)) to translate graph data between various persistent and in-memory representations.

**[Demo Notebook with NetworkX DSL](http://nbviewer.ipython.org/github/CrystallineCat/projx/blob/master/projx_neo4j_demo.ipynb)**

Thanks to [@versae](https://github.com/versae) for inspiring this project and [@davebshow](https://github.com/davebshow) for the original implementation.

## Post-fork changes

* Ported everything needed for Demo Notebook to Python 3.6 and NetworkX 2.2

## To port

* [Demo Notebook with Neo4j2NetworkX](http://nbviewer.ipython.org/github/davebshow/projx/blob/master/projx_neo4j_demo.ipynb)
* [Demo Notebook: Loading the Flickr group graph to Neo4j](http://nbviewer.ipython.org/github/davebshow/projx/blob/master/flicker_graph.ipynb)
