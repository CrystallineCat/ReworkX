"""
ETL does initial validation on config JSON and provides the extractor function,
stream function, list of transformers (JSON), the loader JSON, and graph object
for the loader pipeline.
"""
from .modules import loaders, nx_xtrct, edgelist_xtrct


class ETL(object):

    def __init__(self, etl):
        """
        A helper class that parses the ETL JSON, and initializes the
        required extractor, transformers, and loader. Also store key
        variables used in transformation/loading.

        :param etl: ETL JSON.
        """

        self.extractor_json = etl["extractor"]
        self.extractor_name = list(self.extractor_json.keys())[0]

        self.transformers = etl.get("transformers", [])
        
        self.loader_json = etl["loader"]
        self.loader_name = list(self.loader_json.keys())[0]

        self.extractor = {
            'networkx': lambda graph: nx_xtrct      .nx_extractor      (self.extractor_json[self.extractor_name], graph),
            'edgelist': lambda graph: edgelist_xtrct.edgelist_extractor(self.extractor_json[self.extractor_name], graph),
        }[self.extractor_name]
        
        self.stream = {
            'networkx': nx_xtrct      .nx_stream,
            'edgelist': edgelist_xtrct.edgelist_stream,
        }[self.extractor_name]
        
        self.loader = {
            'nx2nx': lambda extractor, stream, transformers, graph: loaders.nx2nx_loader(extractor, stream, transformers, self.loader_json[self.loader_name], graph),
        }[self.loader_name]
