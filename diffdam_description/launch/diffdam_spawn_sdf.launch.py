# import os
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration
# from launch_ros.actions import Node
# from launch.actions import ExecuteProcess
# from launch.conditions import IfCondition
# from ament_index_python.packages import get_package_share_directory

# def generate_launch_description():

#     pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
#     pkg_diffdam_robot = get_package_share_directory('diffdam_description')

#     gazebo = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
#         )
#     )

#     spawn_entity = Node(
#         package='diffdam_description', 
#         executable='diffdam',
#         output='screen')


#     # rviz = Node(
#     #     package='rviz2',
#     #     executable='rviz2',
#     #     arguments=['-d', os.path.join(pkg_diffdam_robot, 'rviz', 'diffdam_model.rviz')],
#     #     condition=IfCondition(LaunchConfiguration('rviz'))
#     # )

#     return LaunchDescription([
#         gazebo,
#         spawn_entity,
#     ])

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    sdf = os.path.join(
        get_package_share_directory('diffdam_description'), "models",
        "diffdam_robot", "diffdam_model.sdf")

    assert os.path.exists(sdf), "diffdam_model.sdf doesnt exist in "+str(sdf)
    
    with open(sdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(package='diffdam_description', executable='spawn.py', arguments=[sdf], output='screen'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[sdf]),
    ])