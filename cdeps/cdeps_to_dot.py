import argparse
import glob
import os
import re

import pprint

import networkx as nx
from networkx.drawing.nx_pydot import write_dot


ap = argparse.ArgumentParser()
ap.add_argument("path", help="Folder to search for c/cpp files")


class Include:
    def __init__(self, path: str, islocal: bool):
        self.path = path
        self.islocal = islocal

    def filename(self):
        return os.path.split(self.path)[1]

    def __str__(self):
        return "#include " + self.path + " " + ("local" if self.islocal else "gloabl")

    def __repr__(self):
        return self.__str__()


def parse_include(text: str) -> Include:
    _, path, *__ = text.split()
    islocal = path.startswith('"')
    return Include(path, islocal)


def extract_includes_from_file(path: str) -> list:
    results = []
    with open(path) as f:
        for line in f.readlines():
            if line.strip().lower().startswith("#include"):
                results.append(parse_include(line))
    return results


def extract_includes_from_paths(paths: list):
    return {path: extract_includes_from_file(path) for path in paths}


def include_dict_to_graph(path_to_include: dict) -> nx.DiGraph:
    g = nx.DiGraph()
    for f, targets in path_to_include.items():
        for t in targets:
            if not t.islocal:
                continue

            if "cairoint" in t.path:
                continue

            if "-xlib-" in t.path:
                continue

            if "-quartz-" in t.path:
                continue

            if "gl-" in t.path:
                continue

            if "cairo-error-private" in t.path:
                continue

            g.add_edge(f, t.path)
    return g

if __name__ == "__main__":
    path = ap.parse_args().path
    includes = extract_includes_from_paths(glob.glob(path))
    pprint.pprint(includes)
    g = include_dict_to_graph(includes)
    write_dot(g, "out.dot")