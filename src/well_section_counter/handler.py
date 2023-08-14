# обработчик получаемого с фронат в бек
data = {'filterColumn': {'type': 'Фильтровая колонна', 'diameter': '3', 'depth': {'from': '3', 'to': '3'
        }, 'intervals': [
            {'from': '3', 'to': '3'
            },
            {'from': '4', 'to': '4'
            }
        ]
    }, 'horizons': [
        {'depositType': ['пески мелкие'
            ], 'interlayers': ['супеси'
            ], 'inclusions': ['глыбы'
            ], 'name': '7', 'depth': {'from': '7', 'to': '7'
            }
        },
        {'depositType': ['глины'
            ], 'interlayers': ['глины'
            ], 'inclusions': ['галька'
            ], 'name': '8', 'depth': {'from': '8', 'to': '8'
            }
        }
    ], 'well': {'project_name': 'name', 'depth': 'depth_well'
    }, 'casingString': [
        {'diameter': '1', 'depth': {'from': '1', 'to': '1'
            }
        },
        {'diameter': '2', 'depth': {'from': '2', 'to': '2'
            }
        }
    ]
}

def handler_front(data):
    result_data = {}
    columns = {}
    if data['casingString']:
        for i in range(len(data['casingString'])):
            columns[i + 1] = {}
            columns[i + 1]['id'] = i + 1
            columns[i + 1]['D'] = int(data['casingString'][i]['diameter'])
            columns[i + 1]['from'] = float(data['casingString'][i]['depth']['from'])
            columns[i + 1]['till'] = float(data['casingString'][i]['depth']['to'])
            columns[i + 1]['till'] = float(data['casingString'][i]['depth']['to'])
            columns[i + 1]['type'] = 'обсадная'
    if data['filterColumn']:
            i += 1
            columns[i + 1] = {}
            columns[i + 1]['id'] = i + 1
            columns[i + 1]['D'] = int(data['filterColumn']['diameter'])
            columns[i + 1]['from'] = float(data['filterColumn']['depth']['from'])
            columns[i + 1]['till'] = float(data['filterColumn']['depth']['to'])
            columns[i + 1]['till'] = float(data['filterColumn']['depth']['to'])
            # определяем тип фильтровой колонны
            if data['filterColumn']['type'] == 'Фильтровая колонна':
                columns[i + 1]['type'] = 'фильтровая'
                if data['filterColumn']['intervals']:
                    for j in range(len(data['filterColumn']['intervals'])):
                        columns[i + 1]['filter'] = {}
                        columns[i + 1]['filter'][j + 1] = {}
                        columns[i + 1]['filter'][j + 1]['id'] = j + 1
                        columns[i + 1]['filter'][j + 1]['from'] = data['filterColumn']['intervals'][j]['from']
                        columns[i + 1]['filter'][j + 1]['till'] = data['filterColumn']['intervals'][j]['to']        
            else:
                columns[i + 1]['type'] = 'О.С.'

            
                
    print(columns)

handler_front(data)