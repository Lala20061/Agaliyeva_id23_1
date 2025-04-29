from itertools import permutations
import math
from collections import defaultdict
from fastapi import APIRouter
from app.schemas.tsp import Graph, PathResult
from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.post("/shortest-path/", response_model=PathResult)
def shortest_path(graph: Graph):
    nodes = graph.graph.nodes
    raw_edges = graph.graph.edges

    distance = defaultdict(dict)
    for edge in raw_edges:
        if len(edge) == 2:
            u, v = edge
            w = 1
        elif len(edge) == 3:
            u, v, w = edge
        else:
            raise HTTPException(status_code=400, detail=f"Неверный формат ребра: {edge}")

        distance[u][v] = w
        distance[v][u] = w

    start = nodes[0]
    min_path = []
    min_distance = math.inf

    for perm in permutations(nodes[1:]):
        path = [start] + list(perm) + [start]
        total = 0
        valid = True

        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            if v in distance[u]:
                total += distance[u][v]
            else:
                valid = False
                break

        if valid and total < min_distance:
            min_distance = total
            min_path = path

    if not min_path:
        raise HTTPException(status_code=400, detail="Нет здесь")

    return {"path": min_path, "total_distance": min_distance}
