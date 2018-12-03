import projx as px


def test_execute_etl() -> None:

    def try_to_transform(source: str, etl: str, target: str) -> None:
        graph = px.load_graph(f'examples/{source}.graph.yaml')
        expect = px.load_graph(f'examples/{target}.graph.yaml')
        via = px.load_etl(f'examples/{etl}.etl.yaml')
        result = px.execute_etl(via, graph)

        assert px.content_of(result)['nodes'] == px.content_of(expect)['nodes']
        assert px.content_of(result)['edges'] == px.content_of(expect)['edges']

    try_to_transform('example', 'project',         'projected')
    try_to_transform('example', 'transfer',        'transferred')
    try_to_transform('example', 'combine',         'combined')
    try_to_transform('example', 'multi_transform', 'multi_transformed')


def test_parse_query() -> None:

    def try_to_parse(etl: str, query: str) -> None:
        expect = px.load_etl(f'examples/{etl}.etl.yaml')
        result = px.parse_query(query)

        assert result == expect

    try_to_parse('project', '''
        MATCH   (p1:Person)-(wild)-(p2:Person)
        PROJECT (p1)-(p2)
        METHOD JACCARD Institution, City
        SET     name = wild.label
        DELETE  wild
    ''')
