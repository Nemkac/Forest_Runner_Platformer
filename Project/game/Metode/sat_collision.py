import matplotlib.pyplot as plt
import numpy as np

def get_edges(vertices):
    edges = []
    for i in range(len(vertices)):
        curr = vertices[i]
        next = vertices[(i + 1) % len(vertices)]
        edge = next - curr
        edges.append(edge)
    return edges

def get_normals(edges):
    normals = []
    for edge in edges:
        normal = np.array([-edge[1], edge[0]])
        normals.append(normal)
    return normals

def project(vertices, axis):
    min_dot = np.inf
    max_dot = -np.inf
    for vertex in vertices:
        dot = np.dot(vertex, axis)
        if dot < min_dot:
            min_dot = dot
        if dot > max_dot:
            max_dot = dot
    return min_dot, max_dot

def is_separating_axis(vertices1, vertices2, axis):
    min1, max1 = project(vertices1, axis)
    min2, max2 = project(vertices2, axis)
    if max1 < min2 or max2 < min1:
        return True
    return False

def check_collision(vertices1, vertices2):
    edges1 = get_edges(vertices1)
    edges2 = get_edges(vertices2)
    normals1 = get_normals(edges1)
    normals2 = get_normals(edges2)
    for axis in normals1 + normals2:
        if is_separating_axis(vertices1, vertices2, axis):
            return False
    return True

def visualize_collision(vertices1, vertices2, title):
    fig, ax = plt.subplots()
    poly1 = plt.Polygon(vertices1, color='r', alpha=0.5)
    poly2 = plt.Polygon(vertices2, color='b', alpha=0.5)
    ax.add_patch(poly1)
    ax.add_patch(poly2)
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plt.title(title)
    plt.show()

vertices1 = np.array([[-1, 0], [-1, 1], [0, 1], [0, 0]])
vertices2 = np.array([[0.5, 0.5], [0.5, 1.5], [1.5, 1.5], [1.5, 0.5]])
collision = check_collision(vertices1, vertices2)
if collision:
    title = "Collision detected"
else:
    title = "No collision detected"
visualize_collision(vertices1, vertices2, title)


    # def horizontal_movement_collision(self):
    #    player = self.player.sprite
    #    player.rect.x += player.direction.x * player.speed

    #    p_topleft = player.player_cordinates_topleft()
    #    p_topright = player.player_cordinates_topright()
    #    p_bottomleft = player.player_cordinates_bottomleft()
    #    p_bottomright  = player.player_cordinates_bottomright()
    #    p_vertice = np.array([[p_bottomleft],[p_topleft],[p_topright],[p_bottomright]])
    #    #p_vertice = np.array([[-1, 0], [-1, 1], [0, 1], [0, 0]])

    #    for sprite in self.tiles.sprites():
    #         t_topleft = sprite.rect.topleft
    #         t_topright = sprite.rect.topright
    #         t_bottomleft = sprite.rect.bottomleft
    #         t_bottomright = sprite.rect.bottomright
    #         t_vertice = np.array([[t_bottomleft],[t_topleft],[t_topright],[t_bottomright]])
    #         #t_vertice = np.array([[0.5, 0.5], [0.5, 1.5], [1.5, 1.5], [1.5, 0.5]])

    #         if player.direction.x < 0:
    #            collision = self.check_collision(p_vertice, t_vertice)
    #            if collision:
    #                player.direction.x = 0
    #                print("Kolizija")
    #         elif player.direction.x > 0:
    #             collision = self.check_collision(p_vertice, t_vertice)
    #             if collision:
    #                 player.directio.x = 0
    #                 print("Kolizija")

                   

    # def vertical_movement_collision(self):
    #    player = self.player.sprite
    #    player.apply_gravity()

       
    #    p_topleft = player.player_cordinates_topleft()
    #    p_topright = player.player_cordinates_topright()
    #    p_bottomleft = player.player_cordinates_bottomleft()
    #    p_bottomright  = player.player_cordinates_bottomright()
    #    p_vertice = np.array([[p_bottomleft],[p_topleft],[p_topright],[p_bottomright]])
    #    for sprite in self.tiles.sprites():
    #         t_topleft = sprite.rect.topleft
    #         t_topright = sprite.rect.topright
    #         t_bottomleft = sprite.rect.bottomleft
    #         t_bottomright = sprite.rect.bottomright
    #         t_vertice = np.array([[t_bottomleft],[t_topleft],[t_topright],[t_bottomright]])
    #         if player.direction.y < 0:
    #            collision = self.check_collision(p_vertice, t_vertice)
    #            if collision:
    #                player.direction.x = 0
    #                print("Kolizija")
    #         elif player.direction.x > 0:
    #             collision = self.check_collision(p_vertice, t_vertice)
    #             if collision:
    #                 player.directio.x = 0
    #                 print("Kolizija")