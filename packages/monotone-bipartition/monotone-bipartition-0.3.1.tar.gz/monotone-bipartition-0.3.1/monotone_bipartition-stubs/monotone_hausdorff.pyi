from lazytree.lazytree import LazyTree
from monotone_bipartition.rectangles import (
    Interval,
    Rec,
)
from numpy import float64
from typing import (
    Dict,
    Set,
    Tuple,
    Union,
)


def best_worst_case(
    approx1: Set[LazyTree],
    approx2: Set[LazyTree],
    adj_mat: Dict[Tuple[LazyTree, LazyTree], Interval]
) -> Tuple[LazyTree, LazyTree]: ...


def dinf(
    a: Union[Tuple[int, float], Tuple[int, float64], Tuple[float64, int], Tuple[float, float], Tuple[float64, float64]],
    b: Union[Tuple[int, float64], Tuple[float, int], Tuple[float64, int], Tuple[float, float], Tuple[float64, float64]]
) -> float64: ...


def node_dist(
    n1: LazyTree,
    n2: LazyTree
) -> Interval: ...


def rec_dist(
    r1: Rec,
    r2: Rec
) -> Interval: ...


def worst_case(
    node1: LazyTree,
    approx2: Set[LazyTree],
    adj_mat: Dict[Tuple[LazyTree, LazyTree], Interval]
) -> Tuple[Tuple[LazyTree, LazyTree], Interval]: ...
