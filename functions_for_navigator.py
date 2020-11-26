def min_way_func(graph, max_of_len, a, b, first=-1, len_of_hod_way=0, level_recursion=0):
    # {home: [next_home, len_of_wey]...}
    # m_w_f return [p1, p2, p3, ..., pn, len_of_wey]
    len_of_wey = len_of_hod_way
    list_of_obj = []
    lvl_norm = level_recursion
    min_wey = [len_of_wey]
    list_of_ways = []
    if a != b and a not in graph:
        return -1
    if a == b:
        return min_wey
    for next_point in graph[a]:
        if next_point[0] != first:
            list_of_obj.append(next_point[0])
            len_of_wey += next_point[1]
            if len_of_wey > max_of_len:
                return -1
            wey_2 = min_way_func(graph, max_of_len, next_point[0], b, first=a,
                                 len_of_hod_way=len_of_wey,
                                 level_recursion=level_recursion + 1)
            if wey_2 == -1:
                list_of_obj = []
                len_of_wey = len_of_hod_way
                continue
            list_of_obj.extend(wey_2)
            if level_recursion == lvl_norm:
                list_of_ways.append(list_of_obj.copy())
                # попытка удалить все, что не надо
                list_of_obj = []
                len_of_wey = len_of_hod_way
            else:
                return list_of_obj
    try:
        return sorted(list_of_ways, key=lambda x: x[-1])[0]
    except IndexError:
        return -1


class StartPointError(Exception):
    pass


class EndPointError(Exception):
    pass


class WeyError(Exception):
    pass
