import math
import pygame
from AlgoRRT import RRTGraph
from AlgoRRT import RRTMap


def main():
    # to quickly run testcases you can change dimensions to change the red rectangles size, obsnum changes number of red rectangles
    # start and goal node positions are the following below can also be modified.
    dimensions = (1080, 1080)
    start = (30, 30)
    goal = (800, 800)
    obsdim = 80
    obsnum = 90
    iteration = 0
    total_nodes = 0
    shortest_path_distance = float('inf')
    shortest_path = []
    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)
    obstacles = graph.createObstacles()
    map.renderMap(obstacles)
    pass_through_obstacle = pygame.Rect((500, 500), (80, 80))
    pygame.draw.rect(map.map, (173, 216, 230), pass_through_obstacle)
    pygame.display.update()
    running = True
    while running:
        num_nodes = int(input("Please enter the number of iterations you want: "))
        for _ in range(num_nodes):
            if iteration % 10 == 0:
                X, Y, Parent = graph.bias(goal)
                pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
                pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                                 map.edgeThickness)
            else:
                X, Y, Parent = graph.expand()
                pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
                pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                                 map.edgeThickness)

            if iteration % 5 == 0:
                pygame.display.update()
            total_nodes = len(X)
            if graph.pathToGoal():
                map.renderPath(graph.getPathCoords())
                pathCoords = graph.getPathCoords()
                path_distance = 0
                checked = False
                for i in range(len(pathCoords) - 1):
                    current_node = pathCoords[i]
                    next_node = pathCoords[i + 1]
                    distance = math.sqrt((next_node[0] - current_node[0]) ** 2 + (next_node[1] - current_node[1]) ** 2)
                    path_distance += distance
                    if checked==False:
                        segment = pygame.Rect(current_node[0], current_node[1], next_node[0] - current_node[0],
                                          next_node[1] - current_node[1])
                        if segment.colliderect(pass_through_obstacle):
                            path_distance += 100
                            checked= True

                if path_distance < shortest_path_distance:  # Compare with current shortest path
                    shortest_path_distance = path_distance
                    shortest_path = pathCoords

                    out_text = "New best path found: Path Distance: {:.2f}    Iterations: {}    Total Nodes: {}".format(path_distance, iteration, total_nodes)
                    print("\n" + out_text + "\n")
                pygame.display.update()
            iteration += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == '__main__':
    result = False
    while not result:
        try:
            main()
            result = True
        except:
            result = False