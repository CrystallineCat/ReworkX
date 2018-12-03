import parglare as g


action = g.get_collector()


@action
def make_keyword(_, nodes):
    return nodes[0].lower()


@action
def make_flat_list(_, nodes):
    return nodes[0] + nodes[1:] if len(nodes) > 1 else nodes or []


@action
def make_dict(_, nodes, **kwds):
    return kwds


@action
def make_pair_dict(_, nodes):
    return {nodes[0].lower(): nodes[1]}


@action
def make_pair_dict_from_merged_dicts(_, nodes, **kwds):
    for x in nodes[-1]:
        kwds.update(x)

    return {nodes[0].lower(): kwds}


grammar = g.Grammar.from_file('projx/grammar.pg')
parser  = g.Parser(grammar, actions=action.all)


def parse_query(query: str) -> dict:
    data = parser.parse(query)

    return {
        'extractor': {
            'networkx': {
                'type':      data['type'] or 'subgraph',
                'traversal': data['traversal'],
            },
        },
        'transformers': data['transformers'],
        'loader': {
            'nx2nx': {},
        },
    }
