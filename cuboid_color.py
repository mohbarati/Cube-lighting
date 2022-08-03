import pygame
from pygame.locals import *
from math import sin, cos

sc = pygame.display.set_mode((800, 800))
# Vertices of the cube
points = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
]
# Faces of the cube
faces = [
    (0, 1, 2, 3),
    (5, 4, 7, 6),
    (4, 0, 3, 7),
    (1, 5, 6, 2),
    (4, 5, 1, 0),
    (3, 2, 6, 7),
]
# Color values for the cube
red = 211
green = 211
blue = 211
# Center of the screen
xs, ys = 400, 400


def product(RM, vertices):
    """Calculate the matrix product

    Args:
        RM (list): general rotation matrix
        vertices (list): list of vertices to be rotated

    Returns:
        list: rotated points
    """
    mult = [
        [sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in vertices]
        for row_a in RM
    ]
    return list(zip(*mult))


def rot_matrix(alpha, beta, gamma):
    """General rotation matrix

    Args:
        alpha (float): Angle of rotation around x-axis
        beta (float): Angle of rotation around y-axis
        gamma (float): Angle of rotation around z-axis

    Returns:
        list: Matrix of general rotation
    """
    R = [
        (cos(beta) * cos(gamma), -sin(gamma) * cos(beta), sin(beta)),
        (
            sin(alpha) * sin(beta) * cos(gamma) + sin(gamma) * cos(alpha),
            -sin(alpha) * sin(beta) * sin(gamma) + cos(alpha) * cos(gamma),
            -sin(alpha) * cos(beta),
        ),
        (
            sin(alpha) * sin(gamma) - sin(beta) * cos(alpha) * cos(gamma),
            sin(alpha) * cos(gamma) + sin(beta) * sin(gamma) * cos(alpha),
            cos(alpha) * cos(beta),
        ),
    ]

    return R


def cube(points, phi, theta):
    """draws a set of polygons as faces of the cube in 3D

    Args:
        points (list): vertices of the cube
    """
    lx, ly, lz = light(phi, theta)  # light ray vector
    z_avg_sorted = {}  # to store faces with their average z value (for face culling)
    for a, b, c, d in faces:
        avg_z = (points[a][2] + points[b][2] + points[c][2] + points[d][2]) / 4
        z_avg_sorted[avg_z] = (a, b, c, d)
    for avg_z, (a, b, c, d) in sorted(z_avg_sorted.items(), reverse=True):
        # coordinates of the points for each face of the cube:
        x1, y1, z1 = points[a]
        x2, y2, z2 = points[b]
        x3, y3, z3 = points[c]
        x4, y4, z4 = points[d]
        # normal to the surface:
        i = (x1 + x3) / 2
        j = (y1 + y3) / 2
        k = (z1 + z3) / 2
        # the component of light ray in the direction of the surface:
        dp = i * lx + j * ly + k * lz
        # moving the cube back and finding scale factor for depth creation:
        z1 += 7
        z2 += 7
        z3 += 7
        z4 += 7
        # Drawing the cube and shading the faces
        if dp >= 0:

            pygame.draw.polygon(
                sc,
                (dp * red, dp * green, dp * blue),
                [
                    ((x1 * 100) * 10 / z1 + xs, (y1 * 100) * 10 / z1 + ys),
                    ((x2 * 100) * 10 / z2 + xs, (y2 * 100) * 10 / z2 + ys),
                    ((x3 * 100) * 10 / z3 + xs, (y3 * 100) * 10 / z3 + ys),
                    ((x4 * 100) * 10 / z4 + xs, (y4 * 100) * 10 / z4 + ys),
                ],
            )
        # ???????????????? why?
        else:

            dp = abs(dp) / 20
            pygame.draw.polygon(
                sc,
                (0, 0, 0),
                [
                    ((x1 * 100) * 10 / z1 + xs, (y1 * 100) * 10 / z1 + ys),
                    ((x2 * 100) * 10 / z2 + xs, (y2 * 100) * 10 / z2 + ys),
                    ((x3 * 100) * 10 / z3 + xs, (y3 * 100) * 10 / z3 + ys),
                    ((x4 * 100) * 10 / z4 + xs, (y4 * 100) * 10 / z4 + ys),
                ],
            )


def light(phi, theta):
    """Finds the three components of light ray in the
    spherical coordinate system with rho = 1. This will
    ensure normality

    Args:
        phi (float): angle (w/r to z axis) in radian
        theta (float): angle (w/r to x axis) in radian

    Returns:
        tuple: a tuple of 3 components lx,ly, and lz
    """
    return cos(phi) * cos(theta), cos(phi) * sin(theta), sin(phi)


# ------------------
"""setting initial values"""
phi, theta = -2, 3  # initial direction of light source
change_phi, change_theta = 0, 0
alpha, beta, gamma = 0, -1, 1
change_alpha, change_beta, change_gamma = 0, 0, 0
"""Starting the pygame loop"""
cont = True
while cont:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Use arrow keys to move the light source
            if event.key == pygame.K_UP:
                change_theta = -0.001
            if event.key == pygame.K_DOWN:
                change_theta = 0.001
            if event.key == pygame.K_RIGHT:
                change_phi = -0.001
            if event.key == pygame.K_LEFT:
                change_phi = 0.001
            # --------------------------
            # Use (q,w) for rotation around x-axis
            # Use (a,s) for rotation around y-axis
            # Use (z,x) for rotation around z-axis
            if event.key == pygame.K_q:
                change_alpha = 0.001
            if event.key == pygame.K_w:
                change_alpha = -0.001
            if event.key == pygame.K_a:
                change_beta = 0.001
            if event.key == pygame.K_s:
                change_beta = -0.001
            if event.key == pygame.K_z:
                change_gamma = 0.001
            if event.key == pygame.K_x:
                change_gamma = -0.001
        if event.type == KEYUP:
            if event.key == pygame.K_UP:
                change_theta = 0
            if event.key == pygame.K_DOWN:
                change_theta = 0
            if event.key == pygame.K_RIGHT:
                change_phi = 0
            if event.key == pygame.K_LEFT:
                change_phi = 0
            if event.key == pygame.K_ESCAPE:
                cont = False
            # --------------------------
            if event.key == pygame.K_q:
                change_alpha = 0
            if event.key == pygame.K_w:
                change_alpha = 0
            if event.key == pygame.K_a:
                change_beta = 0
            if event.key == pygame.K_s:
                change_beta = 0
            if event.key == pygame.K_z:
                change_gamma = 0
            if event.key == pygame.K_x:
                change_gamma = 0
        if event.type == QUIT:
            cont = False
            pygame.quit()
    # Increments in angles are added to the corresponding variables
    phi += change_phi
    theta += change_theta
    alpha += change_alpha
    beta += change_beta
    gamma += change_gamma

    sc.fill((5, 5, 5))  # clear the screen before each new change
    pts = product(rot_matrix(alpha, beta, gamma), points)  # New points after rotation
    cube(pts, phi, theta)  # Drawing the new cube
    pygame.display.set_caption(
        "Control -   q,w : X Rotation    a,s : Y Rotation    z,x : Z Rotation       arrwos: Light source rotation"
    )
    pygame.display.update()
