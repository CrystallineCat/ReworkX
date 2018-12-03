import parglare as g


def parse_query(query: str) -> dict:
    def merge_dicts(*dicts):
        d = {}

        for x in dicts:
            d.update(x)

        return d

    prsd = g.Parser(g.Grammar.from_file('projx/grammar.pg'), actions={
        'make_dict':  lambda context, nodes, **kwds: kwds,
        'pass_lower': lambda context, nodes: (nodes[0] or '').lower(),
        'key_value':  lambda context, nodes: {nodes[0].lower(): nodes[1]},
        'join_dicts': lambda context, nodes: merge_dicts(*nodes),
    }).parse(query)

    etl = {
        'extractor': {
            'networkx': {
                'type': prsd['type'] or 'subgraph',
                'traversal': prsd['traversal'],
            }
        },
        'transformers': prsd['transformers'],
        'loader': {
            'nx2nx': {},
        }
    }
    
    return etl
