import os
import sys
import networkx as nx
import string
import random
import matplotlib.pyplot as plt

# Globals: Question type
TYPE = 0    # Which type of question should be generated?
            # 0: Random
            # 1: Edges of complete graph
            # 2: Number of cycles
            # 3: Simple paths of length n from u
            # 4: Simple paths between two vertices
            # 5: All paths of length n
            # 6: Find cycles
            # 7: Number of edges in complete graph with n vertices

# Globals: Graph generation
NUM_NODES_LOWER = 5     # Smallest number of nodes generated
NUM_NODES_UPPER = 6     # Largest number of nodes generated

# Globals: Number of edges in complete graph with n vertices
RANDOM_VERTICES_LOWER = 5   # Smallest number of vertices to computer number of edges for
RANDOM_VERTICES_UPPER = 10  # Largest number of vertices to computer number of edges for

# Globals: Images
COUNT = 1
GENERATE_IMAGES = False
QUESTION_LIST_COUNT = 1

CURRENT = 1

def config(type=None, num_nodes_lower=None, num_nodes_upper=None, question_list_count=None,
           random_vertices_lower=None, random_vertices_upper=None, generate_images=None):
    global TYPE, NUM_NODES_LOWER, NUM_NODES_UPPER, RANDOM_VERTICES_LOWER, \
            RANDOM_VERTICES_UPPER, GENERATE_IMAGES, QUESTION_LIST_COUNT

    if type != None: TYPE = type
    if num_nodes_lower != None: NUM_NODES_LOWER = num_nodes_lower
    if num_nodes_upper != None: NUM_NODES_UPPER = num_nodes_upper
    if random_vertices_lower != None: RANDOM_VERTICES_LOWER = random_vertices_lower
    if random_vertices_upper != None: RANDOM_VERTICES_UPPER = random_vertices_upper
    if generate_images != None: GENERATE_IMAGES = generate_images
    if question_list_count != None: QUESTION_LIST_COUNT = question_list_count

def generate_random_graph():
    global NUM_NODES_LOWER, NUM_NODES_UPPER, COUNT, GENERATE_IMAGES

    n = random.randint(NUM_NODES_LOWER, NUM_NODES_UPPER)

    letters = string.ascii_uppercase[:n]

    G = nx.Graph()
    G.add_nodes_from(letters)

    for i, node1 in enumerate(letters):
        for node2 in letters[i+1:]:
            if random.random() < 0.5:
                G.add_edge(node1, node2)

    if GENERATE_IMAGES:
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        sys.path.append(os.path.abspath('../../../'))
        dir = f'./data/images_{QUESTION_LIST_COUNT}/image_{COUNT}.png'
        plt.savefig(dir)
        plt.close()
        COUNT += 1
                
    return G

# List edges of complete graph
def generate_question_1():
    def question():
        global NUM_NODES_LOWER, NUM_NODES_UPPER

        n = random.randint(NUM_NODES_LOWER, NUM_NODES_UPPER)
        G = nx.complete_graph(n)

        return G.nodes, G

    def answer(G):  
        return G.edges
    
    nodes, G = question()
    print("Question:")
    print(f"List all edges of a complete graph with 5 vertices by using V = {nodes}.")
    print("Answer:")
    print(answer(G))

# Find number of cycles
def generate_question_2():
    global COUNT, GENERATE_IMAGES

    def question():
        G = generate_random_graph()
        return G.nodes, G.edges, G

    def answer(G):
        def find_new_cycles(G, path, cycles):
            start_node = path[0]
            for neighbor in G.neighbors(start_node):
                if neighbor == path[-1]:
                    if len(path) > 2:
                        p = rotate_to_smallest(path)
                        inv = invert(p)
                        if isNew(p, cycles) and isNew(inv, cycles):
                            cycles.append(p)
                    continue
                if visited(neighbor, path):
                    continue
                sub = [neighbor]
                sub.extend(path)
                find_new_cycles(G, sub, cycles)

        def invert(path):
            return rotate_to_smallest(path[::-1])

        def rotate_to_smallest(path):
            n = path.index(min(path))
            return path[n:] + path[:n]

        def isNew(path, cycles):
            return not any(path == cycle for cycle in cycles)

        def visited(node, path):
            return node in path
        
        cycles = []
        nodes = list(G.nodes())
        for node in nodes:
            find_new_cycles(G, [node], cycles)

        result = []
        for cycle in cycles:
            if len(cycle) >= 3:
                path = [str(node) for node in cycle]
                s = "".join(path)
                result.append(s)

        for i in range(len(result)):
            result[i] += result[i][0]

        return len(result)

    nodes, edges, G = question()
    print("Question:")
    print(f"Find the number of different cycles contained in the graph with vertices {nodes} and edges {edges}.")
    if GENERATE_IMAGES:
        print(f'Graph saved to data/images_{QUESTION_LIST_COUNT}/image_{COUNT - 1}.png')
    print("Answer:")
    num_cycles = answer(G)
    if num_cycles == 1:
        print(f"There is 1 cycle in the graph.")
    else:
        print(f"There are {num_cycles} cycles in the graph.")


# Find all simple paths of length n from node u
def generate_question_3():
    global COUNT, GENERATE_IMAGES

    def question():
        G = generate_random_graph()

        random_node = random.choice(list(G.nodes()))
        random_num = random.randint(2, len(G.nodes()) - 1)

        return random_node, random_num, G.nodes, G.edges, G
    
    def answer(G, u, n):
        if n == 0:
            return [u]
        
        paths = []
        for neighbor in G.neighbors(u):
            for path in answer(G, neighbor, n - 1):
                if u not in path:
                    paths.append(u + ''.join(path))

        return paths

    u, n, nodes, edges, G = question()
    print("Question:")
    print(f"List all simple paths of length {n} starting from vertex {u} in the graph with vertices {nodes} and edges {edges}.")
    if GENERATE_IMAGES:
        print(f'Graph saved to data/images_{QUESTION_LIST_COUNT}/image_{COUNT - 1}.png')
    print("Answer:")
    paths = answer(G, u, n)
    if len(paths) == 0:
        print("No paths exist.")
    elif len(paths) == 1:
        print(f"There is 1 path. The path is {paths}.")
    else:
        print(f"There are {len(paths)} paths. The paths are {paths}.")

# Find all simple paths between two vertices
def generate_question_4():
    global COUNT, GENERATE_IMAGES

    def question():
        G = generate_random_graph()

        a = random.choice(list(G.nodes()))
        b = random.choice(list(G.nodes()))
        while (b == a):
            b = random.choice(list(G.nodes()))

        return a, b, G.nodes, G.edges, G
    
    def answer(G, a, b):
        paths = list(nx.all_simple_paths(G, a, b))
        paths = [''.join(sublist) for sublist in paths]

        return paths

    a, b, nodes, edges, G = question()
    print("Question:")
    print(f"Identify all of the simple paths from vertex {a} to vertex {b} in the graph with vertices {nodes} and edges {edges}.")
    if GENERATE_IMAGES:
        print(f'Graph saved to data/images_{QUESTION_LIST_COUNT}/image_{COUNT - 1}.png')
    print("Answer:")
    paths = answer(G, a, b)
    if len(paths) == 0:
        print("No paths exist.")
    elif len(paths) == 1:
        print(f"There is 1 path. The path is {paths}.")
    else:
        print(f"There are {len(paths)} paths. The paths are {paths}.")


# Find all paths of length n
def generate_question_5():
    global COUNT, GENERATE_IMAGES

    def question():
        G = generate_random_graph()
        random_num = random.randint(2, len(G.nodes()) - 1)
        return random_num, G.nodes, G.edges, G
    
    def answer(G, n):
        paths = []
        for source in G.nodes():
            for target in G.nodes():
                if source != target:
                    for path in nx.all_simple_paths(G, source=source, target=target, cutoff=n):
                        if len(path) == n + 1:
                            path_str = ''.join(path)
                            paths.append(path_str)

        return paths

    n, nodes, edges, G = question()
    print("Question:")
    print(f"How many paths of length {n} are there in the graph with vertices {nodes} and edges {edges}.")
    if GENERATE_IMAGES:
        print(f'Graph saved to data/images_{QUESTION_LIST_COUNT}/image_{COUNT - 1}.png')
    print("Answer:")
    paths = answer(G, n)
    if len(paths) == 0:
        print("No paths exist.")
    elif len(paths) == 1:
        print(f"There is 1 path. The path is {paths}.")
    else:
        print(f"There are {len(paths)} paths. The paths are {paths}.")

# Find cycles
def generate_question_6():
    global COUNT, GENERATE_IMAGES

    def question():
        G = generate_random_graph()
        return G.nodes, G.edges, G

    def answer(G):
        def find_new_cycles(G, path, cycles):
            start_node = path[0]
            for neighbor in G.neighbors(start_node):
                if neighbor == path[-1]:
                    if len(path) > 2:
                        p = rotate_to_smallest(path)
                        inv = invert(p)
                        if isNew(p, cycles) and isNew(inv, cycles):
                            cycles.append(p)
                    continue
                if visited(neighbor, path):
                    continue
                sub = [neighbor]
                sub.extend(path)
                find_new_cycles(G, sub, cycles)

        def invert(path):
            return rotate_to_smallest(path[::-1])

        def rotate_to_smallest(path):
            n = path.index(min(path))
            return path[n:] + path[:n]

        def isNew(path, cycles):
            return not any(path == cycle for cycle in cycles)

        def visited(node, path):
            return node in path
        
        cycles = []
        nodes = list(G.nodes())
        for node in nodes:
            find_new_cycles(G, [node], cycles)

        result = []
        for cycle in cycles:
            if len(cycle) >= 3:
                path = [str(node) for node in cycle]
                s = "".join(path)
                result.append(s)

        for i in range(len(result)):
            result[i] += result[i][0]

        return result

    nodes, edges, G = question()
    print("Question:")
    print(f"Identify all cycles contained in the graph with vertices {nodes} and edges {edges}.")
    if GENERATE_IMAGES:
        print(f'Graph saved to data/images_{QUESTION_LIST_COUNT}/image_{COUNT - 1}.png')
    print("Answer:")
    cycles = answer(G)
    if len(cycles) == 0:
        print(f"There are no cycles.")
    else:
        print(f"By inspection, the cycles are {cycles}.")

# Number of edges in complete graph with n vertices
def generate_question_7():
    def question():
        global RANDOM_VERTICES_LOWER, RANDOM_VERTICES_UPPER

        return random.randint(RANDOM_VERTICES_LOWER, RANDOM_VERTICES_UPPER)
        
    def answer(n):
        return n * (n - 1) // 2

    n = question()
    print("Question:")
    print(f"How many edges are there in a complete graph with {n} vertices?")
    print("Answer:")
    print(f"There are {answer(n)} edges.")

def main():
    global TYPE, GENERATE_IMAGES, QUESTION_LIST_COUNT, CURRENT

    if GENERATE_IMAGES:
        sys.path.append(os.path.abspath('../../../'))
        dir = f'./data/images_{QUESTION_LIST_COUNT}'
        if not os.path.exists(dir):
            os.mkdir(dir)

    if TYPE == 0:
        eval(f'generate_question_{CURRENT}()')
        if CURRENT == 7:
            CURRENT = 1
        else:
            CURRENT += 1
    else:
        eval(f'generate_question_{TYPE}()')

if __name__ == "__main__":
    main()