import parglare as g


action = g.get_collector()


@action
def join_dicts(_, dicts, **kwds):
    for x in dicts[1]:
        kwds.update(x)

    return kwds


@action
def collect_flat(_, nodes):
    return nodes[0] + nodes[1:] if len(nodes) > 1 else nodes or []


@action
def key_value(_, nodes):
    return {nodes[0].lower(): nodes[1]}


@action
def make_dict(_, nodes, **kwds):
    return kwds


grammar = g.Grammar.from_file('projx/grammar.pg')
parser  = g.Parser(grammar, actions=action.all)


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
