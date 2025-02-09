import sys

def getInput():
    if len(sys.argv) < 2:
        print("Please pass file name")
        sys.exit(1)
    grid = []
    with open(sys.argv[1]) as file:
        for line in file:
            row = [let for let in line]
            grid.append(row[:-1])
    return grid


def floodID(crop, grid, regions, row, col, id):
    # if out of bounds
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return

    # if we've been here before
    if regions[row][col] != -1:
        return

    # if it's not the crop we're looking for
    if grid[row][col] != crop:
        return

    # mark it and recurse out
    regions[row][col] = id
    floodID(crop, grid, regions, row - 1, col, id)
    floodID(crop, grid, regions, row + 1, col, id)
    floodID(crop, grid, regions, row, col - 1, id)
    floodID(crop, grid, regions, row, col + 1, id)

# replaces letters with region ids, 0+
def findRegions(grid):
    regions = [[-1 for i in range(len(grid[0]))] for j in range(len(grid))]
    symbols = []
    nextrow, nextcol = 0, 0
    nextid = 0
    done = False

    while not done:
        # flood fill nextrow, nextcol
        floodID(grid[nextrow][nextcol], grid, regions, nextrow, nextcol, nextid)
        symbols.append(grid[nextrow][nextcol])

        # get next stuff
        isNext = False
        for row in range(0, len(grid)):
            if isNext:
                break
            for col in range(0, len(grid[0])):
                if isNext:
                    break
                if regions[row][col] == -1:
                    nextrow = row
                    nextcol = col
                    isNext = True
            
        # check if done
        if not isNext:
            done = True
        else:
            nextid += 1
    return regions, nextid + 1, symbols

# returns -1 for out-of-bounds to simplify checks
def r(regions, row, col):
    if row < 0 or row >= len(regions) or col < 0 or col >= len(regions[0]):
        return -1
    return regions[row][col]


# we count the top horizontal edges of the region
def topEdges(regions, id):
    # we scan through looking for the places where edges start, and then when they end
    # when they end we increment a counter
    onEdge = False
    edges = 0
    for row in range(0, len(regions)):
        for col in range(len(regions[0])):
            # if this one is different to one above it, we have the start of a top edge
            if regions[row][col] == id and not onEdge and r(regions, row - 1, col) != id:
                onEdge = True

            # if we're still on the edge, keep going
            elif onEdge and regions[row][col] == id and r(regions, row - 1, col) != id:
                pass

            # if we finish an edge
            elif onEdge and (regions[row][col] != id or r(regions, row - 1, col) == id):
                onEdge = False
                edges += 1

        # if still on edge, finish it
        if onEdge:
            onEdge = False
            edges += 1
    return edges


def numSides(regions, id):
    # get the top edges
    tops = topEdges(regions, id)

    # now flip the whole grid around and find top edges again (which are really bottoms now)
    newGrid = [[0 for i in range(len(regions[0]))] for j in range(len(regions))]
    for row in range(len(regions)):
        for col in range(len(regions[0])):
            newGrid[row][col] = regions[len(grid) - 1 - row][col]
    bottoms = topEdges(newGrid, id)

    # now double this for vertical edges (which must be equal in number)
    return (tops + bottoms) * 2


def part2(regions, num, symbols):
    # area is same, but now we get sides instead of perim
    area = [0 for i in range(num)]
    sides = [numSides(regions, i) for i in range(num)]

    for row in range(len(regions)):
        for col in range(len(regions[0])):
            # area is just 1
            area[regions[row][col]] += 1

    # cost is the sum of the products of likewise elements
    cost = 0
    for i in range(num):
        print("Region", i, "has", sides[i], "sides")
        cost += area[i] * sides[i]
    return cost


grid = getInput()
regions, num, symbols = findRegions(grid)
print("There are", num, "regions")
cost = part2(regions, num, symbols)
print(cost)

