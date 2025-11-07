from typing import List, Tuple, Dict, Union
import matplotlib.pyplot as plt
import networkx as nx


def find_parent(parent: Dict[Union[int, str], Union[int, str]], vertex: Union[int, str]) -> Union[int, str]:
    """Find the root parent of a vertex."""
    while parent[vertex] != vertex:
        parent[vertex] = parent[parent[vertex]]
        vertex = parent[vertex]
    return vertex


def union(parent: Dict[Union[int, str], Union[int, str]], rank: Dict[Union[int, str], int], vertex1: Union[int, str], vertex2: Union[int, str]) -> None:
    """Merge two sets."""
    root1 = find_parent(parent, vertex1)
    root2 = find_parent(parent, vertex2)

    if rank[root1] < rank[root2]:
        parent[root1] = root2
    elif rank[root1] > rank[root2]:
        parent[root2] = root1
    else:
        parent[root2] = root1
        rank[root1] += 1


def kruskal_mst(edges: List[Tuple[Union[int, str], Union[int, str], float]],
                vertices: List[Union[int, str]]) -> Tuple[List[Tuple[Union[int, str], Union[int, str], float]], float]:
    """
    Find Minimum Spanning Tree using Kruskal's Algorithm.

    Args:
        edges: List of tuples (vertex1, vertex2, weight)
        vertices: List of all vertices in the graph

    Returns:
        (mst_edges, total_weight)
    """
    # We first need to sort all the edges by weight so as to have a sorted weight list
    sorted_edges = sorted(edges, key=lambda edge: edge[2])

    # We first need to declare a union-find structure to monitor inherent families and numbers of members in the family
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    # Build MST
    mst_edges = []
    total_weight = 0

    for u, v, weight in sorted_edges:
        # For both vertices, we need to find their root parents
        # Before we add two vertices, we need to check if they belong to the same family
        # This way we avoid cycles, because adding an edge between two vertices in the same family creates a cycle
        if find_parent(parent, u) != find_parent(parent, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            # Union check is to merge the two families
            union(parent, rank, u, v)

            # MST complete when we have (n-1) edges
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, total_weight


def visualize_mst(edges: List[Tuple[Union[int, str], Union[int, str], float]],
                  mst_edges: List[Tuple[Union[int, str], Union[int, str], float]],
                  vertices: List[Union[int, str]],
                  title: str = "Minimum Spanning Tree",
                  weight_label: str = "Weight"):

    try:
        # Create graph
        G = nx.Graph()
        G.add_nodes_from(vertices)

        # Add all edges
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)

        # Create MST edge set for highlighting
        mst_edge_set = set()
        for u, v, w in mst_edges:
            mst_edge_set.add((min(u, v), max(u, v)))

        # Layout
        pos = nx.spring_layout(G, seed=42, k=2)

        # Create figure
        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                               node_size=800, alpha=0.9)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

        # Separate MST edges from other edges
        mst_edge_list = []
        other_edge_list = []

        for u, v in G.edges():
            edge_tuple = (min(u, v), max(u, v))
            if edge_tuple in mst_edge_set:
                mst_edge_list.append((u, v))
            else:
                other_edge_list.append((u, v))

        # Draw non-MST edges in gray
        nx.draw_networkx_edges(G, pos, edgelist=other_edge_list,
                               edge_color='gray', width=2, alpha=0.3, style='dashed')

        # Draw MST edges in red
        nx.draw_networkx_edges(G, pos, edgelist=mst_edge_list,
                               edge_color='red', width=4, alpha=0.8)

        # Draw edge labels
        edge_labels = {(u, v): f"{w} {weight_label}" for u, v, w in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)

        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"  [Visualization error: {e}]\n")


def first_example():
    print("=" * 50)
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    edges = [
        ('A', 'B', 4),
        ('A', 'H', 8),
        ('B', 'C', 8),
        ('B', 'H', 11),
        ('C', 'D', 7),
        ('C', 'I', 2),
        ('C', 'F', 4),
        ('D', 'E', 9),
        ('D', 'F', 14),
        ('E', 'F', 10),
        ('F', 'G', 2),
        ('G', 'H', 1),
        ('G', 'I', 6),
        ('H', 'I', 7),
    ]

    print("\nVertices:", ', '.join(vertices))
    print("\nEdges:")
    for u, v, w in edges:
        print(f"  ({u}, {v}) - weight: {w}")

    # Run Kruskal's algorithm
    mst_edges, total_weight = kruskal_mst(edges, vertices)

    # Visualize
    visualize_mst(edges, mst_edges, vertices,
                  "First Example: Graph 1", "")

    return mst_edges, total_weight


def second_example():
    print("=" * 50)

    vertices = ['A', 'B', 'C', 'D', 'E', 'F']

    # Edges representing roads between cities with distances in km
    edges = [
        ('A', 'B', 12),
        ('A', 'C', 8),
        ('A', 'D', 15),
        ('B', 'C', 10),
        ('B', 'E', 20),
        ('C', 'D', 7),
        ('C', 'E', 14),
        ('D', 'F', 9),
        ('E', 'F', 11),
    ]

    print("\nCities (Vertices):", ', '.join(vertices))
    print("\nRoads (Edges) with distances:")
    for u, v, w in edges:
        print(f"  City {u} ↔ City {v}: {w} km")

    # Run Kruskal's algorithm
    mst_edges, total_weight = kruskal_mst(edges, vertices)

    # Visualize
    visualize_mst(edges, mst_edges, vertices,
                  "Second Example:City Network MST (Minimum Road Distance)", "km")

    return mst_edges, total_weight


def third_example():
    print("=" * 50)

    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    # Edges representing task dependencies with time in hours
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 5),
        ('A', 'D', 4),
        ('B', 'C', 2),
        ('B', 'E', 6),
        ('C', 'D', 3),
        ('C', 'E', 4),
        ('C', 'F', 5),
        ('D', 'F', 7),
        ('E', 'F', 2),
        ('E', 'G', 8),
        ('F', 'G', 3),
    ]

    print("\nTasks (Vertices):", ', '.join(vertices))
    print("\nTask Connections (Edges) with durations:")
    for u, v, w in edges:
        print(f"  Task {u} ↔ Task {v}: {w} hours")

    # Run Kruskal's algorithm
    mst_edges, total_weight = kruskal_mst(edges, vertices)

    # Visualize
    visualize_mst(edges, mst_edges, vertices,
                  "Third Example: Task Network MST (Minimum Time)", "hours")

    return mst_edges, total_weight


def main():
    print("=" * 50)
    print("Kruskal's Minimum Spanning Tree Algorithm - Minimal Version")
    print("=" * 50)
    
    while True:
        print("\nChoose an example to run:")
        print("  1. First Example (Graph with alphabet vertices)")
        print("  2. Second Example (City network - distances in km)")
        print("  3. Third Example (Task network - durations in hours)")
        print("  4. Exit")

        choice = input("\nYour choice (1-4): ").strip()

        if choice == '1':
            first_example()
        elif choice == '2':
            second_example()
        elif choice == '3':
            third_example()
        elif choice == '4':
            print("\nExiting. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")
        
        # Ask if user wants to continue
        continue_choice = input("\nWant to run another example? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\nExiting. Goodbye!")
            break


if __name__ == "__main__":
    main()
