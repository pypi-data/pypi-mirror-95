from monotone_bipartition.rectangles import (
    Interval,
    Rec,
)
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
    Union,
    Sequence,
)



def from_threshold(
    func: Callable,
    dim: int,
    *,
    memoize_nodes: bool = ...,
    find_intersect: bool = ...,
    bounding_box: Optional[Rec] = ...
) -> BiPartition: ...


class BiPartition:
    def approx(self, tol: float = ...) -> List[Rec]: ...
    @property
    def dim(self) -> int: ...
    def dist(
        self,
        other: BiPartition,
        tol: float = ...
    ) -> Interval: ...
    def label(self, point: Tuple[float, float]) -> bool: ...
