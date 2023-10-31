import open3d as o3d
import laspy
import numpy as np
import os




def las_to_ply(las_file_path, voxel_size=0.1):
    
    las = laspy.read(las_file_path)
    
    points = np.vstack((las.x, las.y, las.z)).transpose()
    
    colors = np.vstack((las.red, las.green,
    las.blue)).transpose()
    
    # factor=100
    # decimated_points = points[::factor]
        
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors/65535)
    
    

    downpcd = pcd.voxel_down_sample(voxel_size)
    o3d.visualization.draw_geometries([downpcd])



def main():

      
    las_file_path = "/mnt/c/Users/ybinb/VS/lidar-processing/2020_Drone_M.las"

    if not os.path.exists(las_file_path):
        print("File not found:", las_file_path)
        return

    if not las_file_path.lower().endswith('.las'):
        print("The file is not a .las file:", las_file_path)
        return

    las_to_ply(las_file_path)

    # las = pylas.read('/mnt/c/Users/ybinb/VS/lidar-processing/2020_Drone_M.las')
    # num_points = len(las.points)
    # print('Number of points:', num_points)
 
    




if __name__ == "__main__":
    main()
