import parglare as g


def merge_dicts(*dicts):
    d = {}

    for x in dicts:
        d.update(x)

    return d


def collect_flat(_, nodes):
    return nodes[0] + nodes[1:] if len(nodes) > 1 else nodes or []


grammar = g.Grammar.from_file('projx/grammar.pg')
parser  = g.Parser(grammar, actions={
    'collect_flat': collect_flat,
    'make_dict':  lambda context, nodes, **kwds: kwds,
    'key_value':  lambda context, nodes: {nodes[0].lower(): nodes[1]},
    'join_dicts': lambda context, nodes, **kwds: merge_dicts(*[node for node in nodes if isinstance(node, dict)], kwds),
})


def parse_query(query: str) -> dict:
    data = parser.parse(query)

    return {
        'extractor': {
            'networkx': {
                'type':      (data['type'] or 'subgraph').lower(),
                'traversal': data['traversal'],
            },
        },
        'transformers': data['transformers'],
        'loader': {
            'nx2nx': {},
        },
    }
