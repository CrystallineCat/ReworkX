import yaml
import networkx as nx


def content_of(graph: nx.Graph) -> dict:
    def listed(view):
        return list(sorted(view(data=True)))

    return {
        'nodes': listed(graph.nodes),
        'edges': listed(graph.to_directed().edges),   # Undirected source/target order isn't stable.
    }


def graph_from(content: dict) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(content['nodes'])
    graph.add_edges_from(content['edges'])
    return graph


def dump_etl(etl: dict, filename: str) -> None:
    with open(filename, 'w') as file:
        yaml.dump(etl, file, indent=4)


def dump_graph(graph: nx.Graph, filename: str) -> None:

    def tuple_representer(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

    try:
        yaml.add_representer(tuple, tuple_representer)

        with open(filename, 'w') as file:
            yaml.dump(content_of(graph), file, default_flow_style=False, indent=4)

    finally:
        yaml.add_representer(tuple, yaml.Dumper.represent_tuple)



def load_query(filename: str) -> str:
    with open(filename) as file:
        return '\n'.join(file.readlines())


def load_etl(filename: str) -> dict:
    with open(filename) as file:
        return yaml.load(file)


def load_graph(filename: str) -> nx.Graph:
    with open(filename) as file:
        return graph_from(yaml.load(file))
