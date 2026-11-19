"""Emergency phone network: what happens when one wireless link breaks?

A small static network of phones is built, a route is found, one link is broken and a new
route is found. Delivery probability along a route is p**hops (every link must succeed).
Note: the route search is a plain shortest-path search (BFS). It does NOT simulate AODV, DSR or OLSR.
"""
import math
import random

import matplotlib.pyplot as plt

NUMBER_OF_NODES = 15
RADIO_RANGE = 95            # metres
SPEED = 5                   # m/s, only used by the selection rule (phones are static here)
LINK_SUCCESS = 0.95         # probability that one link delivers a packet
DISCONNECT_LINK = (3, 4)


def choose(n_phones, speed):
    """Selection rule of the paper (Table IV): returns the suggested protocol."""
    if n_phones >= 70:
        return "OLSR"          # large crowd
    if speed >= 10:
        return "AODV"          # fast movement
    return "OLSR"              # small group, walking pace


def route_delivery(p_link, hops):
    """Probability that a packet crosses all hops."""
    return p_link ** hops


def create_nodes():
    """Eight phones in a chain from phone 0 to phone 7, the others at random places."""
    random.seed(10)
    nodes = {}
    for i in range(8):
        nodes[i] = (40 + i * 70, 180 + (i % 2) * 15)
    for i in range(8, NUMBER_OF_NODES):
        nodes[i] = (random.randint(30, 570), random.randint(50, 350))
    return nodes


def build_network(nodes):
    """Two phones are linked if they are within radio range."""
    links = {n: [] for n in nodes}
    for i in nodes:
        for j in nodes:
            if i != j and math.dist(nodes[i], nodes[j]) <= RADIO_RANGE:
                links[i].append(j)
    return links


def disconnect_link(links, a, b):
    if b in links[a]:
        links[a].remove(b)
    if a in links[b]:
        links[b].remove(a)


def find_path(links, source, destination):
    """Shortest path in hops (breadth-first search)."""
    queue = [[source]]
    visited = {source}
    while queue:
        path = queue.pop(0)
        if path[-1] == destination:
            return path
        for nb in links[path[-1]]:
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None


def probability(path):
    return 0 if path is None else route_delivery(LINK_SUCCESS, len(path) - 1)


def draw_network(nodes, links, new_path):
    plt.figure(figsize=(11, 7))
    for a in links:
        for b in links[a]:
            if a < b:
                plt.plot([nodes[a][0], nodes[b][0]], [nodes[a][1], nodes[b][1]],
                         color="lightgray", linewidth=1)
    a, b = DISCONNECT_LINK
    plt.plot([nodes[a][0], nodes[b][0]], [nodes[a][1], nodes[b][1]],
             color="black", linestyle="--", linewidth=2, label="Disconnected link")
    if new_path:
        for u, v in zip(new_path, new_path[1:]):
            plt.plot([nodes[u][0], nodes[v][0]], [nodes[u][1], nodes[v][1]],
                     color="red", linewidth=3)
    for n, (x, y) in nodes.items():
        color = "green" if n == 0 else "red" if n == 7 else \
                "orange" if new_path and n in new_path else "skyblue"
        plt.scatter(x, y, color=color, s=180, zorder=3)
        plt.text(x, y + 12, str(n), ha="center")
    plt.title("Phone network after a link failure")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.savefig("link_failure.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    nodes = create_nodes()
    links = build_network(nodes)
    print("Number of phones:", NUMBER_OF_NODES, " speed:", SPEED, "m/s")
    print("Recommended protocol:", choose(NUMBER_OF_NODES, SPEED))

    before = find_path(links, 0, 7)
    disconnect_link(links, *DISCONNECT_LINK)
    after = find_path(links, 0, 7)

    print("Route before failure:", before, "hops:", len(before) - 1,
          "delivery:", round(probability(before) * 100, 2), "%")
    print("Disconnected link:", DISCONNECT_LINK)
    if after:
        print("Route after failure: ", after, "hops:", len(after) - 1,
              "delivery:", round(probability(after) * 100, 2), "%")
        print("Change:", round((probability(after) - probability(before)) * 100, 2),
              "percentage points")
    else:
        print("No alternative route is available.")
    draw_network(nodes, links, after)
