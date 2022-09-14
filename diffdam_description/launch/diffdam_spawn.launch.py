import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import ExecuteProcess
import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    gui = LaunchConfiguration('gui')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    #world_file_name = 'empty.world'
    #world = os.path.join(get_package_share_directory(
    #    robot_name), 'worlds', world_file_name)
    xacro_file_name = 'diffdam.xacro'
    xacro_file = os.path.join(
        get_package_share_directory('diffdam_description'), 'urdf/',
        xacro_file_name)
    #with open(urdf, 'r') as infp:
    #    robot_desc = infp.read()
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    launch_file_dir = os.path.join(get_package_share_directory('diffdam_description'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
        ),
        
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_entity',
            output='screen',
            arguments=[
                '-entity', 'diffdam',
                '-x', '0',
                '-y', '0',
                '-z', '1',
                '-topic', robot_desc,
            ]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, 'diffdam_rviz.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])