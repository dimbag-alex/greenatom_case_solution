"""Рабочее решение без бд и api"""

import networkx as nx

#  граф
waste_graph = nx.Graph()

organizations = {
    1: {"name": "ОО1", "waste": {"пластик": 10, "стекло": 50, "биоотходы": 50}},
    2: {"name": "ОО2", "waste": {"пластик": 60, "стекло": 20, "биоотходы": 50}},
}

# хранилища
storages = {
    1: {"name": "МНО1", "capacity": {"стекло": 300, "пластик": 100, "биоотходы": 0}, "filled": {}},
    2: {"name": "МНО2", "capacity": {"пластик": 50, "стекло": 0, "биоотходы": 150}, "filled": {}},
    3: {"name": "МНО3", "capacity": {"пластик": 10, "стекло": 0, "биоотходы": 250}, "filled": {}},
    5: {"name": "МНО5", "capacity": {"стекло": 220, "пластик": 0, "биоотходы": 25}, "filled": {}},
    6: {"name": "МНО6", "capacity": {"стекло": 100, "пластик": 0, "биоотходы": 150}, "filled": {}},
    7: {"name": "МНО7", "capacity": {"пластик": 100, "стекло": 0, "биоотходы": 250}, "filled": {}},
    8: {"name": "МНО8", "capacity": {"стекло": 35, "пластик": 25, "биоотходы": 52}, "filled": {}},
    9: {"name": "МНО9", "capacity": {"пластик": 250, "стекло": 0, "биоотходы": 20}, "filled": {}},
}

# организации в графе
for org_id, org_data in organizations.items():
    waste_graph.add_node(f"ОО{org_id}", **org_data)

# хранилища в графе
for storage_id, storage_data in storages.items():
    waste_graph.add_node(f"МНО{storage_id}", **storage_data)

# связи между организациями и хранилищами
waste_graph.add_edge("ОО1", "МНО1", distance=100)
waste_graph.add_edge("ОО1", "МНО2", distance=50)
waste_graph.add_edge("ОО1", "МНО3", distance=600)
waste_graph.add_edge("ОО2", "МНО3", distance=50)

# связи между хранилищами
waste_graph.add_edge("МНО1", "МНО8", distance=500)
waste_graph.add_edge("МНО8", "МНО9", distance=10)
waste_graph.add_edge("МНО2", "МНО5", distance=50)
waste_graph.add_edge("МНО3", "МНО7", distance=50)
waste_graph.add_edge("МНО3", "МНО6", distance=600)


def find_nearest_storage(graph, org_node, waste_type, waste_volume):
    """
    Ищет ближайшее хранилище, которое может принять указанный тип отходов.
    """
    shortest_path = nx.single_source_dijkstra_path_length(graph, org_node, weight="distance")
    sorted_paths = sorted(shortest_path.items(), key=lambda x: x[1])  # сортируем по расстоянию

    for target_node, _ in sorted_paths:
        if not target_node.startswith("МНО"):
            continue

        storage = graph.nodes[target_node]
        capacity = storage["capacity"].get(waste_type, 0)
        filled = storage["filled"].get(waste_type, 0)
        available = capacity - filled

        if available >= waste_volume:
            return target_node, waste_volume

        if available > 0:
            return target_node, available

    return None, 0 # если нет доступного


def distribute_waste(graph):
    """
    Распределяет отходы от организаций к ближайшим хранилищам.
    Уменьшает объем отходов в организациях на каждом шаге.
    """
    steps = []
    for org_node in [node for node in graph.nodes if node.startswith("ОО")]:
        org_data = graph.nodes[org_node]
        for waste_type, waste_volume in list(org_data["waste"].items()):
            while waste_volume > 0:
                nearest_storage, accepted_volume = find_nearest_storage(graph, org_node, waste_type, waste_volume)
                if not nearest_storage:
                    break

                # обновляем данные хранилища
                storage = graph.nodes[nearest_storage]
                storage["filled"][waste_type] = storage["filled"].get(waste_type, 0) + accepted_volume

                # уменьшаем объём отходов в организации
                waste_volume -= accepted_volume
                org_data["waste"][waste_type] -= accepted_volume

                # если весь тип отходов вывезен, удаляем его из списка
                if org_data["waste"][waste_type] == 0:
                    del org_data["waste"][waste_type]

                steps.append({
                    "from": org_node,
                    "to": nearest_storage,
                    "waste_type": waste_type,
                    "volume": accepted_volume
                })

    return steps


print("до вывоза отходов")
for node, data in waste_graph.nodes(data=True):
    print(node, data)

distribution_steps_updated = distribute_waste(waste_graph)
remaining_waste_in_organizations = {node: data["waste"] for node, data in waste_graph.nodes(data=True) if node.startswith("ОО")}
for step in distribution_steps_updated:
    print(step)


print("после вывоза отходов")
for node, data in waste_graph.nodes(data=True):
    print(node, data)
