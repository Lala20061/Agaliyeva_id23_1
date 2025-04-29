from pydantic import BaseModel
from typing import List

class GraphData(BaseModel):
    nodes: List[int]
    edges: List[List[int]]  # [[from, to, weight], ...]

class Graph(BaseModel):
    graph: GraphData

class PathResult(BaseModel):
    path: List[int]
    total_distance: float
