from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_directional_light((1, 1, 1), 0.1, (1, 1, 1))
scene.set_floor(height=-0.65, color=(0, 0, 0))
scene.set_background_color((0, 0, 0))


@ti.func
def make_octahedron_hack(center, n, h):
    ci, ck = center
    for i, j, k in ti.ndrange((ci-n+1, ci+n), (0, h), (ck-n+1, ck+n)):
        x = ivec3(i, j, k)
        is_border = int(i >= ci-n+1+j and k >= ck-n+1+j and i <= ci+n-1-j and k <= ck+n-1-j and
         (ti.max(i-ci, k-ck) == n-1-j or ti.min(i-ci, k-ck) == j+1-n))
        scene.set_voxel(vec3(i, j, k), is_border, vec3(0, 0.1, 0.6))
        scene.set_voxel(vec3(i, -j, k), is_border, vec3(0, 0.1, 0.6))

@ti.kernel
def initialize_voxels():
    make_octahedron_hack((0, 0), 15, 15)

initialize_voxels()
scene.finish()
