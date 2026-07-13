import numpy as np

try:
    from scipy.spatial import KDTree
except ImportError:
    KDTree = None

from core import shapefile


def getNeighborsAreaContiguity(AREAS):
    """Generate Queen and Rook contiguity neighbor dictionaries."""
    segment2areas = {}
    point2areas = {}
    Wqueen = {}
    Wrook = {}

    for idx in range(len(AREAS)):
        Wqueen[idx] = []
        Wrook[idx] = []

    for area_id, area in enumerate(AREAS):
        for ring in area:
            for point_id, point in enumerate(ring[:-1]):
                p1 = tuple(round(coord, 3) for coord in point)
                p2 = tuple(round(coord, 3) for coord in ring[point_id + 1])
                segment = tuple(sorted([p1, p2], key=lambda x: x[0] ** 2 + x[1] ** 2))

                if segment in segment2areas:
                    segment2areas[segment].append(area_id)
                    for area1 in segment2areas[segment]:
                        for area2 in segment2areas[segment]:
                            if area2 != area1 and area2 not in Wrook[area1]:
                                Wrook[area1].append(area2)
                                Wrook[area2].append(area1)
                else:
                    segment2areas[segment] = [area_id]

                if p1 in point2areas:
                    point2areas[p1].append(area_id)
                    for area1 in point2areas[p1]:
                        for area2 in point2areas[p1]:
                            if area2 != area1 and area2 not in Wqueen[area1]:
                                Wqueen[area1].append(area2)
                                Wqueen[area2].append(area1)
                else:
                    point2areas[p1] = [area_id]

    return Wqueen, Wrook


def kNearestNeighbors(centroids, k):
    if KDTree is None:
        raise ImportError("scipy is required for kNearestNeighbors")
    tree = KDTree(centroids)
    neighbors = {}
    for i, centroid in enumerate(centroids):
        _, indices = tree.query(centroid, k=k + 1)
        neighbors[i] = indices[1:].tolist()
    return neighbors


def extractCentroidsFromShapefile(shapefile_path):
    sf = shapefile.Reader(shapefile_path)
    centroids = []
    for shape in sf.shapes():
        centroids.append(tuple(np.mean(shape.points, axis=0)))
    return centroids
