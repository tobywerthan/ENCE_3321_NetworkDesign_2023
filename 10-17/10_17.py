import networkx as nx
import matplotlib.pyplot as plt


def example_1():
    graph = nx.Graph()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 5)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)

    nx.draw_networkx(graph)

    plt.axis("off")
    plt.show()

    # Whether the graph is Eulerian circuit
    print("Circuit: " + str(nx.is_eulerian(graph)))

    # Whether the graph is Eulerian path
    print("Path: " + str(nx.has_eulerian_path(graph)))

    print("--------------------------------------------------------------------------")
    for element in nx.eulerian_path(graph, source=1):
        print(element)


def example_2():
    graph = nx.Graph()

    # Graph nodes
    graph.add_nodes_from(["s", "a", "b", "c", "g"])

    # Add edges
    graph.add_edge("s", "a")
    graph.add_edge("s", "b")
    graph.add_edge("b", "c")
    graph.add_edge("a", "c")
    graph.add_edge("c", "g")
    graph.add_edge("a", "b")
    graph.add_edge("a", "g")

    # Labels
    graph.add_edge("s", "a", weight=1)
    graph.add_edge("s", "b", weight=4)
    graph.add_edge("b", "c", weight=2)
    graph.add_edge("a", "c", weight=5)
    graph.add_edge("c", "g", weight=3)
    graph.add_edge("a", "b", weight=2)
    graph.add_edge("a", "g", weight=12)

    fixed_positions = {
        "s": (0, 4),
        "a": (4, 6),
        "b": (4, 2),
        "c": (8, 4),
        "g": (12, 4),
    }
    edge_labs = dict([((u, v), d["weight"]) for u, v, d in graph.edges(data=True)])

    nx.draw_networkx(graph, fixed_positions)
    nx.draw_networkx_edge_labels(graph, fixed_positions, edge_labels=edge_labs)
    nx.draw_networkx_nodes(graph, fixed_positions, node_color="red")

    plt.title("Simple Weighted Graph")
    plt.axis("off")

    plt.show()

    # Shortest Path (not weighted)
    print("Shortest Path: " + str(nx.shortest_path(graph, "s", "g")))

    # Dijkstra Path
    print("Dijkstra Path: " + str(nx.dijkstra_path(graph, "s", "g")))

    # Dijkstra Path
    print("A* Search: " + str(nx.astar_path(graph, "s", "g", heuristic=None)))


if __name__ == "__main__":
    # example_1()
    example_2()
