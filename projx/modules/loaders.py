# -*- coding: utf-8 -*-
"""
Loader functions take 5 params: extractor function, stream function,
list of transformers (JSON), the loader JSON, and graph object. They handle
the particulars of extracting the necessary data from the stream, taking into
account the particularities of the source and loading/writing to the
destination.
"""
import time
import networkx as nx
from projx import nxprojx
from .nx_xtrct import _nx_lookup_attrs


def nx2nx_loader(extractor, stream, transformers, loader_json, graph):
    """
    Loader for NetworkX graph.

    :returns: networkx.Graph
    """
    extractor_json = extractor(graph)
    graph = extractor_json["graph"]
    node_type_attr = extractor_json["node_type_attr"]
    edge_type_attr = extractor_json["edge_type_attr"]
    transformers = list(transformers)
    if len(transformers) > 1:
        removals = set()
        projector = nxprojx.NXProjector(max(graph.nodes()))
        for trans in stream(transformers, extractor_json):
            record, trans_kwrd, trans, attrs = trans
            method = trans.get("method", {"none": []})
            method_kwrd = list(method.keys())[0]
            params = method.get(method_kwrd, {"args": []})["args"]
            src, target, to_del = _apply_nx2nx_transformer(trans, record)
            fn = projector.transformations[trans_kwrd]
            graph = fn(src, target, graph, attrs, node_type_attr,edge_type_attr,
                       method=method_kwrd, params=params)
            for i in to_del:
                removals.update([i])
        graph.remove_nodes_from(removals)
    elif len(transformers) == 1:
        graph = nx2nx_single_transform_loader(
            transformers[0],
            extractor_json["paths"],
            graph,
            node_type_attr,
            edge_type_attr
        )
    return graph


def nx2nx_single_transform_loader(transformer, paths, graph, node_type_attr,
                                  edge_type_attr):
    """
    Special transformer/loader for single transformations across nx graphs.

    :param graph: networkx.Graph
    :param paths: List of lists.
    :returns: networkx.Graph
    """
    removals = set()
    projector = nxprojx.NXProjector(max(graph.nodes()))
    trans_kwrd = list(transformer.keys())[0]
    trans = transformer[trans_kwrd]
    to_set = trans.get("set", [])
    method = trans.get("method", {"none": []})
    method_kwrd = list(method.keys())[0]
    params = method.get(method_kwrd, {"args": []})["args"]
    fn = projector.transformations[trans_kwrd]
    for record in paths:
        attrs = _nx_lookup_attrs(to_set, record, graph)
        src, target, to_del = _apply_nx2nx_transformer(trans, record)
        graph = fn(src, target, graph, attrs, node_type_attr, edge_type_attr,
                   method=method_kwrd, params=params)
        for i in to_del:
            removals.update([i])
    graph.remove_nodes_from(removals)
    return graph


def _apply_nx2nx_transformer(trans, record):
    pattern = trans["pattern"]
    source, target = _nx_get_source_target(pattern, record)
    delete_alias = trans.get("delete", {}).get("alias", [])
    to_delete = [record[alias] for alias in delete_alias]
    return source, target, to_delete


def _nx_get_source_target(pattern, record):
    """
    Uses Node alias system to perform a pattern match.

    :param node_alias: Dict.
    :param pattern: List.
    :returns: Int. Source and target list indices.
    """
    try:
        alias_seq = [p["node"]["alias"] for p in pattern[0::2]]
    except KeyError:
        raise Exception("Please define valid transformation pattern.")
    source = record[alias_seq[0]]
    target = record[alias_seq[-1]]
    return source, target
