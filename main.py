import pygame
from pygame.locals import *
from math import *
from PIL import Image

pygame.display.set_caption("Raycaster")
window = pygame.display.set_mode((960, 540))
display = pygame.Surface((480, 270)).convert()
display.set_colorkey((255, 0, 255))
clock = pygame.time.Clock()

player_position = pygame.Vector2(1.5, 1.5)
player_direction = radians(0)

fov = 90
world_display = pygame.Surface((fov, 270))

wall_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 2, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

wall_1 = Image.open('textures/wall_1.png', 'r')
wall_1 = list(wall_1.getdata())
door_1 = Image.open('textures/door_1.png', 'r')
door_1 = list(door_1.getdata())
textures = []
textures.extend(wall_1)
textures.extend(door_1)

if __name__ == "__main__":
    running = True
else:
    running = False

def move_player(move_speed, turn_speed):
    global player_direction

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[K_d]:
        player_direction += radians(turn_speed)
        if player_direction > pi * 2:
            player_direction -= pi * 2
    if keys_pressed[K_a]:
        player_direction -= radians(turn_speed)
        if player_direction < 0:
            player_direction += pi * 2
    if keys_pressed[K_w]:
        player_position.x += cos(player_direction) * move_speed
        if colliding(player_position) > 0:
            player_position.x -= cos(player_direction) * move_speed
        player_position.y += sin(player_direction) * move_speed
        if colliding(player_position) > 0:
            player_position.y -= sin(player_direction) * move_speed
    if keys_pressed[K_s]:
        player_position.x -= cos(player_direction) * move_speed
        if colliding(player_position) > 0:
            player_position.x += cos(player_direction) * move_speed
        player_position.y -= sin(player_direction) * move_speed
        if colliding(player_position) > 0:
            player_position.y += sin(player_direction) * move_speed

def colliding(position):
    return wall_map[int(position.y)][int(position.x)]

def cast_rays():
    ray_direction = player_direction - radians(fov / 2)
    if ray_direction > pi * 2:
        ray_direction -= pi * 2
    if ray_direction < 0:
        ray_direction += pi * 2

    ray_hits = []
    ray_distances = []
    ray_directions = []
    ray_brightnesses = []
    wall_ids = []
    for _ in range(fov):
        depth_of_feild = 0
        ray_direction_atan = -1 / tan(ray_direction - 0.0001)
        if ray_direction > pi:
            ray_y = int(player_position.y) - 0.0001
            ray_x = (player_position.y - ray_y) * ray_direction_atan + player_position.x
            offset_y = -1
            offset_x = -offset_y * ray_direction_atan
        elif ray_direction < pi:
            ray_y = int(player_position.y) + 1
            ray_x = (player_position.y - ray_y) * ray_direction_atan + player_position.x
            offset_y = 1
            offset_x = -offset_y * ray_direction_atan
        elif ray_direction == 0 or ray_direction == pi:
            ray_x = player_position.x
            ray_y = player_position.y
            depth_of_feild = 8

        while depth_of_feild < 8:
            try:
                hit = wall_map[int(ray_y)][int(ray_x)]
            except IndexError:
                hit = 999
            if hit > 0:
                wall_id_1 = hit
                ray_1_x, ray_1_y = ray_x, ray_y
                distance_1 = pygame.Vector2.distance_to(player_position, pygame.Vector2(ray_1_x, ray_1_y))
                depth_of_feild = 8
            else:
                ray_x += offset_x
                ray_y += offset_y
                depth_of_feild += 1

        depth_of_feild = 0
        ray_direction_ntan = -tan(ray_direction)
        if pi / 2 < ray_direction < pi * 3 / 2:
            ray_x = int(player_position.x) - 0.0001
            ray_y = (player_position.x - ray_x) * ray_direction_ntan + player_position.y
            offset_x = -1
            offset_y = -offset_x * ray_direction_ntan
        elif ray_direction < pi / 2 or ray_direction > pi * 3 / 2:
            ray_x = int(player_position.x) + 1
            ray_y = (player_position.x - ray_x) * ray_direction_ntan + player_position.y
            offset_x = 1
            offset_y = -offset_x * ray_direction_ntan
        elif ray_direction == 0 or ray_direction == pi:
            ray_x = player_position.x
            ray_y = player_position.y
            depth_of_feild = 8

        while depth_of_feild < 8:
            try:
                hit = wall_map[int(ray_y)][int(ray_x)]
            except IndexError:
                hit = 999
            if hit > 0:
                wall_id_2 = hit
                ray_2_x, ray_2_y = ray_x, ray_y
                distance_2 = pygame.Vector2.distance_to(player_position, pygame.Vector2(ray_2_x, ray_2_y))
                depth_of_feild = 8
            else:
                ray_x += offset_x
                ray_y += offset_y
                depth_of_feild += 1

        if distance_2 > distance_1:
            ray_hits.append(pygame.Vector2(ray_1_x, ray_1_y))
            ray_distances.append(distance_1)
            ray_brightnesses.append(1)
            wall_ids.append(wall_id_1)
        if distance_1 > distance_2:
            ray_hits.append(pygame.Vector2(ray_2_x, ray_2_y))
            ray_distances.append(distance_2)
            ray_brightnesses.append(0.75)
            wall_ids.append(wall_id_2)
        ray_directions.append(ray_direction)

        ray_direction += radians(1)
        if ray_direction > pi * 2:
            ray_direction -= pi * 2
        if ray_direction < 0:
            ray_direction += pi * 2

    return ray_hits, ray_distances, ray_directions, ray_brightnesses, wall_ids

def render_displays():
    display.fill((255, 0, 255))
    render_world_2d(8)
    world_display.fill((0, 0, 0))
    render_world_3d()

def render_world_2d(size):
    player_size = size / 4
    scaled_player_position = pygame.Vector2(player_position.x * size, player_position.y * size)
    pygame.draw.circle(display, (0, 255, 0), scaled_player_position, player_size)

    ray_hits, ray_distances, ray_directions, ray_brightnesses, wall_ids = cast_rays()
    for ray in ray_hits:
        pygame.draw.line(display, (255, 0, 0), scaled_player_position, (ray.x * size, ray.y * size))
    pygame.draw.line(display, (0, 0, 255), scaled_player_position, (scaled_player_position.x + cos(player_direction) * player_size, scaled_player_position.y + sin(player_direction) * player_size))

    y = 0
    for row in wall_map:
        x = 0
        for tile in row:
            if tile > 0:
                pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x, y, size - 1, size - 1))
            x += size
        y += size

def render_world_3d():
    ray_hits, ray_distances, ray_directions, ray_brightnesses, wall_ids = cast_rays()
    x = 0
    for i, ray in enumerate(ray_distances):
        ca = player_direction - ray_directions[i]
        if ca > pi * 2:
            ca -= pi * 2
        if ca < 0:
            ca += pi * 2
        ray *= cos(ca)
        line_height = (world_display.get_height()) / ray
        ty_step = 64 / line_height
        ty_offset = 0
        if line_height > world_display.get_height():
            ty_offset = (line_height - world_display.get_height()) / 2
            line_height = world_display.get_height()
        brightness = ray_brightnesses[i]
        y = world_display.get_height() / 2 - line_height / 2
        ty = ty_offset * ty_step + (wall_ids[i] - 1) * 64
        if brightness == 1:
            tx = int(ray_hits[i].x * 64) % 64
            if ray_directions[i] < radians(180):
                tx = 63 - tx
        else:
            tx = int(ray_hits[i].y * 64) % 64
            if radians(90) < ray_directions[i] < radians(270):
                tx = 63 - tx
        for _ in range(int(line_height)):
            color = list(textures[int(ty) * 64 + int(tx)])
            color[0] *= brightness
            color[1] *= brightness
            color[2] *= brightness
            world_display.set_at((int(x), int(y)), color)
            y += 1
            ty += ty_step
        x += 1

def refresh_window(framerate):
    window.blit(pygame.transform.scale(world_display, window.get_size()), (0, 0))
    window.blit(pygame.transform.scale(display, window.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(framerate)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    move_player(0.075, 3)
    render_displays()
    refresh_window(60)

    pygame.display.set_caption("Raycaster | " + str(int(clock.get_fps())))
