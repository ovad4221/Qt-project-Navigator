import json

rect_side = 60
foot_graph = {0: [[1, 2], [6, 5]], 1: [[0, 2], [2, 2], [7, 2]], 2: [[1, 2], [3, 3]],
              3: [[2, 3], [7, 4], [4, 2]], 4: [[3, 2], [5, 1]], 5: [[6, 3], [4, 1]],
              6: [[0, 5], [7, 2], [5, 3]], 7: [[1, 2], [6, 2], [3, 4]]}
foot_max_of_len = 13
cycle_graph = {0: [[7, 3], [3, 5]], 2: [[6, 9]], 3: [[0, 5], [6, 5], [5, 3]],
               5: [[3, 3], [7, 4]], 6: [[3, 5], [2, 9]], 7: [[0, 3], [5, 4]]}
cycle_max_of_len = 23
coordinates = {0: (50, 50), 1: (250, 50), 2: (460, 50), 3: (400, 240),
               4: (480, 400),
               5: (330, 460), 6: (70, 400), 7: (190, 220)}
dict_of_names = {0: 'Жил дом №1', 1: 'Жил дом №2', 2: 'Жил дом №3',
                 3: 'Магазин', 4: 'Больница', 5: 'Аптека',
                 6: 'Музей данного поселения', 7: 'Школа'}
# writing to json
with open('graphs.json', 'w', encoding='utf-8') as file:
    file.write(
        json.dumps(
            [rect_side, foot_graph, foot_max_of_len, cycle_graph, cycle_max_of_len, coordinates,
             dict_of_names]))
