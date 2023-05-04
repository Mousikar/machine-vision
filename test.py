# open3d rgb2pointcloud
# show point cloud
# ICP:Iterative Closest Point姿态精估计

import copy
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import cv2
import numpy as np

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size= 0.1, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([source_temp, target_temp, mesh_frame])



color_raw = o3d.io.read_image("image/7.jpg")
depth_raw = o3d.io.read_image("image/7.png")
rgbd_image = o3d.geometry.RGBDImage.create_from_sun_format(color_raw, depth_raw)
print(rgbd_image)

# plt.subplot(1, 2, 1)
# plt.title(' grayscale image')
# plt.imshow(rgbd_image.color)
# plt.subplot(1, 2, 2)
# plt.title(' depth image')
# plt.imshow(rgbd_image.depth)
# plt.show()

# http://www.open3d.org/docs/release/python_api/open3d.camera.PinholeCameraIntrinsic.html?highlight=pinholecameraintrinsic#open3d.camera.PinholeCameraIntrinsic
width, height = 640, 480    # Width of the image. Height of the image.
cx = 312.83380126953125     # X-axis focal length  x轴焦距
cy = 241.61764526367188     # Y-axis focal length.
fx = 622.0875244140625      # X-axis principle point.x轴原理点
fy = 622.0875854492188      # Y-axis principle point.
intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, fx, fy, cx, cy)    # PinholeCameraIntrinsic类存储固有的相机矩阵，以及图像的高度和宽度。
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsic)
# o3d.visualization.draw_geometries([pcd])


mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
target = o3d.io.read_point_cloud("image/shoes.ply",format='xyzrgb')
# o3d.visualization.draw_geometries([target, mesh_frame])


# draw_registration_result(pcd, target, np.identity(4))   #np.identity(4)：4*4单位矩阵 这一步是把模型和深度图放在了一起

icp = o3d.pipelines.registration.registration_icp(
        source=pcd,                         # The source point cloud 图片+深度图
        target=target,                      # The target point cloud 鞋子的ply文件
        max_correspondence_distance=1,    # 距离阈值 Maximum correspondence points-pair distance.
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
print(icp.transformation)

draw_registration_result(pcd, target, icp.transformation)