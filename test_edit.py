import os
import numpy as np
import open3d as o3d
 
 
 
#load pcd file
pcd_file = 'image/shoes.ply'
pcd = o3d.io.read_point_cloud(pcd_file)
 
print(pcd)
 
#The region we wanted using x-axis and y-axis
#Like a bird's eye view
bounding_ploy = np.array([
                            [ -100, -100, -100 ],
                            [ -100, -100, 100 ],
                            [ -100, 100, -100 ],
                            [ -100, 100, 100 ],
                            [ 100, -100, -100 ],
                            [ 100, -100, 100 ],
                            [ 100, 100, -100 ],
                            [ 100, 100, 100 ]
                         ], dtype = np.float32).reshape([-1, 3]).astype("float64")
 
print(bounding_ploy)
 
bounding_polygon = np.array(bounding_ploy, dtype = np.float64)
 
vol = o3d.visualization.SelectionPolygonVolume()
 
#The Z-axis is used to define the height of the selected region
vol.orthogonal_axis = "Z"
vol.axis_max = 8
vol.axis_min =-16
 
 
vol.bounding_polygon = o3d.utility.Vector3dVector(bounding_polygon)
comp = vol.crop_point_cloud(pcd)
print(comp)
xyz_load = np.asarray(comp.points)
 
#save the cropped region
np.savetxt( '1_' + '.txt', xyz_load)