import open3d as o3d
import laspy
import numpy as np
import os




def las_to_ply(las_file_path, output_ply_path, voxel_size=0.1):
    
    
    las = laspy.read(las_file_path)
    
    
    points = np.vstack((las.x, las.y, las.z)).transpose()
    colors = np.vstack((las.red, las.green, las.blue)).transpose()
    
  
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors / 255)  # if 16-bit color, divide by 65535
    
    
    downpcd = pcd.voxel_down_sample(voxel_size)
    
    o3d.io.write_point_cloud(output_ply_path, downpcd)
    
    print("Point cloud saved to", output_ply_path)



def main():

      
    las_file_path = "./data/SaMo_topo_sep_tiles_colored.las"

    if not os.path.exists(las_file_path):
        print("File not found:", las_file_path)
        return

    if not las_file_path.lower().endswith('.las'):
        print("The file is not a .las file:", las_file_path)
        return

    
    las_to_ply(las_file_path, "output.ply")

    

if __name__ == "__main__":
    main()
