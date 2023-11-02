import numpy as np
import laspy
import pyvista as pv
import open3d as o3d

las_file_path = "/data/ind_scans/SaMo_topo_4.las"


las = laspy.read(las_file_path)

points = np.vstack((las.x, las.y, las.z)).transpose()

if hasattr(las, 'red') and hasattr(las, 'green') and hasattr(las, 'blue'):
    colors = np.vstack((las.red, las.green, las.blue)).transpose() / 255.0  # Normalize to [0, 1]
else:
    colors = None

point_cloud = pv.PolyData(points)

if colors is not None:
    point_cloud['colors'] = colors

surface_mesh = point_cloud.delaunay_3d(alpha=1.0)

surface = surface_mesh.extract_surface()

vertices = np.asarray(surface.points)
faces = np.asarray(surface.faces).reshape((-1, 4))[:, 1:4]
o3d_mesh = o3d.geometry.TriangleMesh()
o3d_mesh.vertices = o3d.utility.Vector3dVector(vertices)
o3d_mesh.triangles = o3d.utility.Vector3iVector(faces)


if colors is not None:
    o3d_mesh.vertex_colors = o3d.utility.Vector3dVector(np.asarray(surface['colors']))


o3d.visualization.draw_geometries([o3d_mesh])
