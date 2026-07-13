def getSpaceTimeAreaContiguity(AREAS):
    """Return Queen and Rook contiguity dictionaries for polygon areas.

    Space-Time FlowLISA uses these area-level contiguity relationships to
    build origin-destination-time flow neighborhoods.
    """
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
