import projx
import yaml
import networkx as nx


def listed(view):
    return list(map(list, sorted(view(data=True))))


def content_of(graph):
    return {
        'nodes': listed(graph.nodes),
        'edges': listed(graph.edges),
    }


def graph_from(content):
    graph = nx.Graph()
    graph.add_nodes_from(content['nodes'])
    graph.add_edges_from(content['edges'])
    return graph


def test_project_etl():
    with open('examples/example.yaml') as file:
        graph = graph_from(yaml.load(file))

    #with open('examples/example.graph.yaml', 'w') as file:
    #    reference = yaml.dump(content_of(graph), file, default_flow_style=True, indent=4)

    result = projx.execute_etl(projx.project_etl, graph)

    with open('examples/example_projected.yaml') as file:
        reference = yaml.load(file)

    assert content_of(result) == reference
