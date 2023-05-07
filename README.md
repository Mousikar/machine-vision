# machine-vision
Here are my codes for machine vision course.

## 课程大作业

运行：

`python .\test_ransac.py`

## 机器人扫描
仿真环境运行：

`roslaunch jaka_minicobo_moveit_config demo_mini_cam.launch`

点云订阅与发布：

`rosrunaka_sim_env robot_scan.py`

路径规划运行：

`rosrun jaka_sim_env pathplan_sim.py`

订阅发布的路径：

`rostop echo /pathplanning`
