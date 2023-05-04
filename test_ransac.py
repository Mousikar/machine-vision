import open3d as o3d
import copy
import matplotlib.pyplot as plt
import numpy as np

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size= 0.1, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([source_temp, target_temp, mesh_frame])


color_raw = o3d.io.read_image("image/4.jpg")
depth_raw = o3d.io.read_image("image/4.png")
rgbd_image = o3d.geometry.RGBDImage.create_from_sun_format(color_raw, depth_raw)
print(rgbd_image)

plt.subplot(1, 2, 1)
plt.title(' grayscale image')
plt.imshow(rgbd_image.color)
plt.subplot(1, 2, 2)
plt.title(' depth image')
plt.imshow(rgbd_image.depth)
plt.show()

# http://www.open3d.org/docs/release/python_api/open3d.camera.PinholeCameraIntrinsic.html?highlight=pinholecameraintrinsic#open3d.camera.PinholeCameraIntrinsic
width, height = 640, 480    # Width of the image. Height of the image.
cx = 312.83380126953125     # X-axis focal length  x轴焦距
cy = 241.61764526367188     # Y-axis focal length.
fx = 622.0875244140625      # X-axis principle point.x轴原理点
fy = 622.0875854492188      # Y-axis principle point.
intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, fx, fy, cx, cy)    # PinholeCameraIntrinsic类存储固有的相机矩阵，以及图像的高度和宽度。
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsic)

# pcd = o3d.io.read_point_cloud("D:/PCL/RANSAC/RANSAC/204.pcd")
'''
使用RANSAC从点云中分割平面，用segement_plane函数。这个函数需要三个参数：

destance_threshold：定义了一个点到一个估计平面的最大距离，这些距离内的点被认为是内点（inlier），
ransac_n：定义了使用随机抽样估计一个平面的点的个数，
num_iterations：定义了随机平面采样和验证的频率（迭代次数）。
这个函数返回（a,b,c,d）作为一个平面，对于平面上每个点(x,y,z)满足ax+by+cz+d=0。这个函数还会返回内点索引的列表。
————————————————
原文链接：https://blog.csdn.net/qq_35706216/article/details/108420011
'''

# plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
#                                          ransac_n=10,
#                                          num_iterations=1000) # 图片1
plane_model, inliers = pcd.segment_plane(distance_threshold=0.008,
                                         ransac_n=10,
                                         num_iterations=1000)  # 图片2 # 图片3# 图片4

[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = pcd.select_by_index(inliers, invert=True)
outlier_cloud.paint_uniform_color([0, 1, 0])
# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
o3d.visualization.draw_geometries([inlier_cloud])  # 平面
# o3d.visualization.draw_geometries([outlier_cloud])  # 鞋子

mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
o3d.visualization.draw_geometries([outlier_cloud, mesh_frame])

# print("按键 K 锁住点云，并进入裁剪模式")
# print("用鼠标左键拉一个矩形框选取点云，或者用 《ctrl+左键单击》 连线形成一个多边形区域")
# print("按键 C 结束裁剪并保存点云")
# print("按键 F 解除锁定，恢复自由查看点云模式")
# o3d.visualization.draw_geometries_with_editing([outlier_cloud])

# # 原文链接：https://blog.csdn.net/u014072827/article/details/112147656
# # 读取指定裁剪多边形的json文件
# vol = o3d.visualization.read_selection_polygon_volume("cropped_1.json")
# # 裁剪点云
# outlier_cloud = vol.crop_point_cloud(outlier_cloud)
# # 可视化
# o3d.visualization.draw_geometries([outlier_cloud],
#                                   zoom=0.7,
#                                   front=[0.5439, -0.2333, -0.8060],
#                                   lookat=[2.4615, 2.1331, 1.338],
#                                   up=[-0.1781, -0.9708, 0.1608])

#The region we wanted using x-axis and y-axis
#Like a bird's eye view
# bounding_ploy = np.array([
#                             [ -0.15, -1, 0 ],
#                             [ 0.1, -1, 0 ],
#                             [ 0.1, 1, 0 ],
#                             [ -0.1, 1, 0 ]                            
#                          ], dtype = np.float32).reshape([-1, 3]).astype("float64") # 图片1
# bounding_ploy = np.array([
#                             [ -0.2, -1, 0 ],
#                             [ 0.1, -1, 0 ],
#                             [ 0.1, 1, 0 ],
#                             [ -0.2, 1, 0 ]                            
#                          ], dtype = np.float32).reshape([-1, 3]).astype("float64") # 图片2
# bounding_ploy = np.array([
#                             [ -0.2, -0.08, 0 ],
#                             [ 0.01, -0.08, 0 ],
#                             [ 0.01, 1.5, 0 ],
#                             [ -0.2, 1.5, 0 ]                            
#                          ], dtype = np.float32).reshape([-1, 3]).astype("float64") # 图片3
bounding_ploy = np.array([
                            [ -0.2, -0.8, 0 ],
                            [ 0.08, -0.8, 0 ],
                            [ 0.08, 1.5, 0 ],
                            [ -0.2, 1.5, 0 ]                            
                         ], dtype = np.float32).reshape([-1, 3]).astype("float64") # 图片4
print(bounding_ploy) 
bounding_polygon = np.array(bounding_ploy, dtype = np.float64) 
vol = o3d.visualization.SelectionPolygonVolume() 
#The Z-axis is used to define the height of the selected region
vol.orthogonal_axis = "Z"
vol.axis_max = 8
vol.axis_min =0 
vol.bounding_polygon = o3d.utility.Vector3dVector(bounding_polygon)
comp = vol.crop_point_cloud(outlier_cloud)
print(comp)
xyz_load = np.asarray(comp.points)
#save the cropped region
np.savetxt( '1_' + '.txt', xyz_load)
o3d.visualization.draw_geometries([comp,mesh_frame])

# # 密度聚类
# eps = 0.02  # 同一聚类中最大点间距
# min_points = 150  # 有效聚类的最小点数
# with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
#     labels = np.array(pcd.cluster_dbscan(eps, min_points, print_progress=True))
# max_label = labels.max()
# print(f"point cloud has {max_label + 1} clusters")  # label = -1 为噪声，因此总聚类个数为 max_label + 1
# colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
# print(colors)
# colors[labels < 0] = 0  # labels = -1 的簇为噪声，以黑色显示
# print(colors[:, :3])
# pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
# o3d.visualization.draw_geometries([pcd])

# 来自test.py
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
target = o3d.io.read_point_cloud("image/shoes.ply",format='xyzrgb')
# o3d.visualization.draw_geometries([target, mesh_frame])
# draw_registration_result(pcd, target, np.identity(4))   #np.identity(4)：4*4单位矩阵 这一步是把模型和深度图放在了一起
icp = o3d.pipelines.registration.registration_icp(
        source=comp,                         # The source point cloud 图片+深度图
        target=target,                      # The target point cloud 鞋子的ply文件
        max_correspondence_distance=1,    # 距离阈值 Maximum correspondence points-pair distance.
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
print(icp.transformation)

draw_registration_result(comp, target, icp.transformation)