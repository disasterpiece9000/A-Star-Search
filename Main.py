import random
from tkinter import messagebox, Canvas, Tk


def main():
    master = Tk()

    # Create empty 15x15 maze
    maze = [[0 for _ in range(25)] for _ in range(25)]

    # Color all maze cells white
    for x in range(len(maze)):
        for y in range(len(maze)):
            Canvas(master, width=25, height=25, bg="white").grid(row=x, column=y)

    # Get a random number of random obstacles
    num_obstacles = random.randint(50, 75)
    for _ in range(num_obstacles):
        
        obstacle_type = random.randint(0, 2)
        obstacleX = random.randint(0, len(maze) - 1)
        obstacleY = random.randint(0, len(maze) - 1)

        # Horizontal line
        if obstacle_type == 0:
            length = int(random.randint(1, len(maze) - obstacleY) / 2)
            for y in range(length):
                maze[obstacleX][obstacleY + y] = 1
                Canvas(master, width=25, height=25, bg="black").grid(row=obstacleX, column=obstacleY + y)

        # Vertical line
        elif obstacle_type == 1:
            length = int(random.randint(1, len(maze) - obstacleX) / 2)
            for x in range(length):
                maze[obstacleX + x][obstacleY] = 1
                Canvas(master, width=25, height=25, bg="black").grid(row=obstacleX + x, column=obstacleY)

        # Box
        elif obstacle_type == 2:
            width = int(random.randint(1, len(maze) - obstacleY) / 2)
            height = int(random.randint(1, len(maze) - obstacleX) / 2)
            for x in range(height):
                for y in range(width):
                    maze[obstacleX + x][obstacleY + y] = 1
                    Canvas(master, width=25, height=25, bg="black").grid(row=obstacleX + x, column=obstacleY + y)

    # Create random start and end points
    startX = random.randint(0, len(maze) - 1)
    startY = random.randint(0, len(maze) - 1)
    endX = random.randint(0, len(maze) - 1)
    endY = random.randint(0, len(maze) - 1)

    # Make sure start and end points are different and are not an obstacle
    while (startX == endX and startY == startY) or \
            (maze[startX][startY] == 1) or \
            (maze[endX][endY] == 1):
        startX = random.randint(0, len(maze) - 1)
        startY = random.randint(0, len(maze) - 1)
        endX = random.randint(0, len(maze) - 1)
        endY = random.randint(0, len(maze) - 1)

    # Draw a triangle to represent the robot
    robot_canvas = Canvas(master)
    robot_canvas.config(width=25, height=25)
    robot_canvas.create_line(0, 25, 12.5, 0, fill="black")
    robot_canvas.create_line(25, 25, 12.5, 0, fill="black")
    robot_canvas.create_line(0, 25, 25, 25, fill="black")
    robot_canvas.grid(row=startX, column=startY)
    # Color the end Node red
    Canvas(master, width=25, height=25, bg="red").grid(row=endX, column=endY)

    path = get_path(maze, startX, startY, endX, endY)

    if path is None:
        master.after(250, messagebox.showinfo("Error", "No path was found"))
        
    else:
        old_node = path[0]
        for index, node in enumerate(path):
            new_node = node
            print("Move " + str(index + 1) + ": " + str(node.posX) + ", " + str(node.posY))
            master.after(ms=500, func=update_path(master, old_node, new_node))
            old_node = new_node

        master.after(250, messagebox.showinfo("Done!", "A valid path has been found\n"
                                                       "Number of moves: " + str(len(path) - 1)))

    master.mainloop()


def update_path(master, old_node, new_node):
    Canvas(master, width=25, height=25, bg="green").grid(row=old_node.posX, column=old_node.posY)
    Canvas(master, width=25, height=25, bg="blue").grid(row=new_node.posX, column=new_node.posY)

    robot_canvas = Canvas(master)
    robot_canvas.config(width=25, height=25, bg="white")
    robot_canvas.create_line(0, 25, 12.5, 0, fill="black")
    robot_canvas.create_line(25, 25, 12.5, 0, fill="black")
    robot_canvas.create_line(0, 25, 25, 25, fill="black")
    robot_canvas.grid(row=new_node.posX, column=new_node.posY)

    master.update()


def get_path(maze, startX, startY, endX, endY):
    start_node = Node(startX, startY, None)
    end_node = Node(endX, endY, None)

    node_list = []  # List of nodes able to travel to
    closed_list = []  # List of nodes unable to travel to or already visited
    node_list.append(start_node)

    # Loop until no Nodes are left
    while len(node_list) > 0:
        current_index = 0
        current_node = node_list[current_index]

        # Search node_list for the Node with the lowest F
        for index, enum_node in enumerate(node_list):
            if enum_node.f < current_node.f:
                current_node = enum_node
                current_index = index

        node_list.pop(current_index)
        closed_list.append(current_node)

        # End has been reached
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]  # Reverse list and return

        # Find neighboring Nodes
        neighbors = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_posX = current_node.posX + new_pos[0]
            node_posY = current_node.posY + new_pos[1]

            # Skip if Node is not in range of the maze or if Node is an obstacle
            if node_posX > (len(maze) - 1) \
                    or \
                    node_posX < 0 \
                    or \
                    node_posY > (len(maze[len(maze)-1]) - 1) \
                    or \
                    node_posY < 0\
                    or \
                    maze[node_posX][node_posY] == 1:
                continue

            new_node = Node(node_posX, node_posY, current_node)
            neighbors.append(new_node)

        # Find the next Node to travel to
        for neighbor in neighbors:
            # Skip if neighbor is already in closed list
            if neighbor in closed_list:
                continue

            # Calculate f, g, and h
            neighbor.g = current_node.g + 1
            # Using Pythagorean's Theorem
            neighbor.h = ((neighbor.posX - end_node.posX) ** 2) + \
                         ((neighbor.posY - end_node.posY) ** 2)
            neighbor.f = neighbor.g + neighbor.h

            # Skip if the neighbor is already in open list and has been visited before
            skip_node = False
            for open_node in node_list:
                if neighbor == open_node and neighbor.g > open_node.g:
                    skip_node = True
                    break
            if skip_node:
                continue

            # Add the neighbor to node_list
            node_list.append(neighbor)


class Node:
    def __init__(self, posX, posY, parent):
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return other.posX == self.posX and other.posY == self.posY


main()
