import projx as px


def test_examples() -> None:
    for test in ('project', 'transfer', 'combine', 'multi_transform'):
        graph  = px.load_graph(f'examples/{test}/graph.yaml')
        expect = px.load_graph(f'examples/{test}/result.yaml')
        query  = px.load_query(f'examples/{test}/query.rework')
        etl    = px.load_etl  (f'examples/{test}/etl.yaml')

        parsed = px.parse_query(query)

        assert parsed == etl

        result = px.execute_etl(etl, graph)

        assert px.content_of(result)['nodes'] == px.content_of(expect)['nodes']
        assert px.content_of(result)['edges'] == px.content_of(expect)['edges']
