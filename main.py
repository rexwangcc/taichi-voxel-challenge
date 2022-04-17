from scene import Scene
import taichi as ti
from taichi.math import *
@ti.func
def add_button(r, pad, origin, button_dir, button_c_col, button_s_col, button_r, button_i_r, xyz, i, j, k):
    if button_dir == 0:
        if k == r:  # button dir: z -> k, -z -> -k, x -> i, -x -> -i, countour then texture
            if button_r ** 2 <= xyz.xy.dot(xyz.xy) < (button_r+pad) ** 2:
                scene.set_voxel(vec3(i, j, r) + origin, 1, button_c_col)
            if xyz.xy.dot(xyz.xy) < r: scene.set_voxel(vec3(i, j, r) + origin, 2, button_s_col)
            if button_i_r ** 2 <= xyz.xy.dot(xyz.xy) < (button_i_r+pad) ** 2:
                scene.set_voxel(vec3(i, j, r) + origin, 1, button_c_col)
    if button_dir == 1:
        if -k == r:  # button dir: z -> k, -sz -> -k, x -> i, -x -> -i, countour then texture
            if button_r ** 2 <= xyz.xy.dot(xyz.xy) < (button_r+pad) ** 2:
                scene.set_voxel(vec3(i, j, -r) + origin, 1, button_c_col)
            if xyz.xy.dot(xyz.xy) < r: scene.set_voxel(vec3(i, j, -r) + origin, 2, button_s_col)
            if button_i_r ** 2 <= xyz.xy.dot(xyz.xy) < (button_i_r+pad) ** 2:
                scene.set_voxel(vec3(i, j, -r) + origin, 1, button_c_col)
    if button_dir == 2:
        if i == r:  # button dir: z -> k, -z -> -k, x -> i, -x -> -i, countour then texture
            if button_r ** 2 <= xyz.yz.dot(xyz.yz) < (button_r+pad) ** 2:
                scene.set_voxel(vec3(r, j, k) + origin, 1, button_c_col)
            if xyz.yz.dot(xyz.yz) < r: scene.set_voxel(vec3(r, j, k) + origin, 2, button_s_col)
            if button_i_r ** 2 <= xyz.yz.dot(xyz.yz) < (button_i_r+pad) ** 2:
                scene.set_voxel(vec3(r, j, k) + origin, 1, button_c_col)
    if button_dir == 3: 
        if -i == r:  # button dir: z -> k, -z -> -k, x -> i, -x -> -i, countour then texture
            if button_r ** 2 <= xyz.yz.dot(xyz.yz) < (button_r+pad) ** 2:
                scene.set_voxel(vec3(-r, j, k) + origin, 1, button_c_col)
            if xyz.yz.dot(xyz.yz) < r: scene.set_voxel(vec3(-r, j, k) + origin, 2, button_s_col)
            if button_i_r ** 2 <= xyz.yz.dot(xyz.yz) < (button_i_r+pad) ** 2:
                scene.set_voxel(vec3(-r, j, k) + origin, 1, button_c_col)
@ti.func
def add_pokeball(r, pad, origin, shim, color, shim_color, button_dir, button_r, button_c_col, button_s_col):
    for i, j, k in ti.ndrange((-r-pad, r+pad), (0, r+pad), (-r-pad, r+pad)):  # upper sphere
        xyz= ivec3(i, j, k)
        if xyz.dot(xyz) < r ** 2: scene.set_voxel(vec3(i, j, k) + origin, 1, color)
        add_button(r, pad, origin, button_dir, button_c_col, button_s_col, button_r, button_r * 0.33, xyz, i, j, k)
    for i, j, k in ti.ndrange((-r-pad, r+pad), (-r-pad, -shim), (-r-pad, r+pad)):  # lower sphere
        xyz= ivec3(i, j, k)
        if xyz.dot(xyz) < r ** 2: scene.set_voxel(vec3(i, j, k) + origin, 1, vec3(1, 1, 1))
        add_button(r, pad, origin, button_dir, button_c_col, button_s_col, button_r, button_r * 0.33, xyz, i, j, k)
    for i, j, k in ti.ndrange((-r-pad, r+pad), (-shim, 0), (-r-pad, r+pad)):  # sphere shim
        xyz= ivec3(i, j, k)
        if (r-pad) ** 2 <= xyz.dot(xyz) <= r ** 2: scene.set_voxel(vec3(i, -pad, k) + origin, 2, shim_color)
        add_button(r, pad, origin, button_dir, button_c_col, button_s_col, button_r, button_r * 0.33, xyz, i, j, k)
@ti.func
def hardcoded_pika(origin):
    for i, j, k in ti.ndrange((-10, 10), (0, 2), (-10, 20)):
        if (i == 1 or i == 3) and 0 <= k < 2: scene.set_voxel(vec3(i, j, k)+origin, 2, BLACK)  # ear tip 
        if (i == 1 or i == 3) and k == 2: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW)  # ear
        if 1 <= i < 4 and 3 <= k < 6: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW)  # head
        if (i == 1 or i == 3) and k == 4: scene.set_voxel(vec3(i, 1, k)+origin, 2, BLACK)  # eyes
        if (i == 1 or i == 3) and k == 5: scene.set_voxel(vec3(i, 1, k)+origin, 2, PINK)  # cheek
        if 0 <= i < 5 and 6 <= k < 12: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW)  # body
        if (-1 <= i < 1 or 5 <= i < 6) and k == 6: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW)  # arms
        if (i == 0 or i == 4) and 11 <= k < 13:  # legs
            scene.set_voxel(vec3(i, 2, k)+origin, 2, YELLOW)
            scene.set_voxel(vec3(i, 3, k)+origin, 2, BLACK)
        if i == 2 and 12 <= k < 14: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW) # tail
        if (i == 3 or i == 4) and 14 <= k < 18: scene.set_voxel(vec3(i, j, k)+origin, 2, YELLOW)  # tail body
        if i == 4 and 18 <= k < 20: scene.set_voxel(vec3(i, j, k)+origin, 2, BLACK)  # tail tip
largest, origin_y, floor_h = 28, lambda largest, r: -(largest-r)-1, lambda largest: -1 / 64 * largest
BLACK, WHITE, YELLOW, PINK = vec3(0, 0, 0), vec3(1, 1, 1), vec3(1,1,0), vec3(1,0.5,0.8)
POKE, GREAT, MASTER = vec3(0.9, 0, 0.1), vec3(0, 0.5, 1), vec3(0.2, 0.2, 0.6)
@ti.kernel
def initialize_voxels():
    # r, pad, origin, shim, color, button_dir (0-front, 1-back, 2-right, 3-left), button_r
    add_pokeball(24, 1, vec3(-38, origin_y(largest, 24), 0), 1, POKE, BLACK, 0, 5, BLACK, WHITE)
    add_pokeball(6, 1, vec3(17, origin_y(largest, 6), -2), 1, WHITE, POKE, 0, 1.5, POKE, WHITE)
    add_pokeball(largest, 1, vec3(14, origin_y(largest, largest), -34), 1, MASTER, WHITE, 0, 5, BLACK, WHITE)
    add_pokeball(12, 1, vec3(-2, origin_y(largest, 12), 24), 1, GREAT, WHITE, 2, 4, BLACK, WHITE)
    hardcoded_pika(vec3(-2, origin_y(largest, 1), -11))
scene = Scene(voxel_edges=0, exposure=1)
scene.set_directional_light((-1, 1, 1), 0.2, (1, 1, 1))
scene.set_background_color((1, 1, 1))
scene.set_floor(height=floor_h(largest), color=(1, 1, 1))  # set to the largest ball -1/64*r
initialize_voxels()
scene.finish()
