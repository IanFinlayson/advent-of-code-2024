import heapq
import sys

def getInput():
    if len(sys.argv) < 2:
        print("Please pass file name")
        sys.exit(1)
    grid = []
    with open(sys.argv[1]) as file:
        for line in file:
            grid.append([let for let in line[:-1]])
    return grid

def p(grid):
    for row in grid:
        for thing in row:
            print(thing, end="")
        print()

# we build a graph where the nodes are identified by (row, col, dir) tuples
# the graph is a dict mapping the nodes to a list of edges
# each edge is a (row, col, dir, cost) tuple
def buildGraph(grid):
    graph = dict()

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "#":
                continue

            # make empty lists for ease of adding
            graph[(row, col, "<")] = []
            graph[(row, col, ">")] = []
            graph[(row, col, "^")] = []
            graph[(row, col, "v")] = []

            # we put in the edges from this cell to neighboring ones, in the appropriate dir w/ cost 1
            if grid[row - 1][col] != "#":
                graph[(row, col, "^")].append((row - 1, col, "^", 1))
            if grid[row + 1][col] != "#":
                graph[(row, col, "v")].append((row + 1, col, "v", 1))
            if grid[row][col - 1] != "#":
                graph[(row, col, "<")].append((row, col - 1, "<", 1))
            if grid[row][col + 1] != "#":
                graph[(row, col, ">")].append((row, col + 1, ">", 1))

            # next we put in the edges from here to here w/ rotation costs
            # you can always rotate 90 degrees either right or left
            graph[(row, col, "^")].append((row, col, "<", 1000))
            graph[(row, col, "^")].append((row, col, ">", 1000))

            graph[(row, col, "<")].append((row, col, "v", 1000))
            graph[(row, col, "<")].append((row, col, "^", 1000))
            
            graph[(row, col, ">")].append((row, col, "^", 1000))
            graph[(row, col, ">")].append((row, col, "v", 1000))

            graph[(row, col, "v")].append((row, col, ">", 1000))
            graph[(row, col, "v")].append((row, col, "<", 1000))

    return graph


# find the start/end
def findSym(grid, sym):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == sym:
                return row, col
    # should not happen
    return None

# do the search thingy
def dijkstra(graph, start, end):
    # the tentative costs are a dict of (row, col, dir) keys and int values
    # if there is no path found, there is no entry
    tentative = dict()
    tentative[(start[0], start[1], ">")] = 0

    # we also store the paths we use to get to each cell that gave us the tentative cost
    paths = dict()
    paths[(start[0], start[1], ">")] = [[(start[0], start[1])]]

    # we make a heap of (row, col, dir) to explore from
    nodes = []
    heapq.heappush(nodes, (0, start[0], start[1], ">"))

    while len(nodes) > 0:
        tent, nrow, ncol, ndir = heapq.heappop(nodes)
        #print("\nConsidering", nrow, ncol, ndir)

        # see where we can go from 
        possibles = graph[(nrow, ncol, ndir)]
        for (drow, dcol, ddir, cost) in possibles:
            distance = tentative[(nrow, ncol, ndir)] + cost

            if (drow, dcol, ddir) not in tentative or distance < tentative[(drow, dcol, ddir)]:
                #print("Found path of", cost, "to", drow, dcol, ddir)
                tentative[(drow, dcol, ddir)] = distance
                # add this cell to all paths to n{row,coldir}
                nexts = []
                for p in paths[(nrow, ncol, ndir)]:
                    nexts.append(p + [(drow, dcol)])
                paths[(drow, dcol, ddir)] = nexts
                heapq.heappush(nodes, (distance, drow, dcol, ddir))

            # for part 2, if the path is EQUAL in cost we need to bifurcate
            elif (drow, dcol, ddir) in tentative and distance == tentative[(drow, dcol, ddir)]:
                for firstpart in paths[(nrow, ncol, ndir)]:
                    # if this new (equal cost) way not already in path list, add it
                    if firstpart + [(drow, dcol)] not in paths[(drow, dcol, ddir)]:
                        paths[(drow, dcol, ddir)].append(firstpart + [(drow, dcol)])

    # find the cost to the end node with the smallest cost
    options = []
    for dir in "<>^v":
        options.append((tentative[(end[0], end[1], dir)], paths[(end[0], end[1], dir)]))

    mini = 0
    for i in range(len(options[1:])):
        if options[i][0] < options[mini][0]:
            mini = i
    return options[mini]

# add paths to grid
def addPaths(grid, paths):
    for path in paths:
        for (r, c) in path:
            grid[r][c] = "O"

def countSeats(grid):
    seats = 0
    for row in grid:
        for thing in row:
            if thing == "O":
                seats += 1
    return seats


grid = getInput()
graph = buildGraph(grid)
score, paths = dijkstra(graph, findSym(grid, "S"), findSym(grid, "E"))
addPaths(grid, paths)
print(countSeats(grid))






