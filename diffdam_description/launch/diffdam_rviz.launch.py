import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    gui = LaunchConfiguration('gui')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    xacro_file_name = 'diffdam.xacro'
    xacro_file = os.path.join(
        get_package_share_directory('diffdam_description'), 'urdf/',
        xacro_file_name)
    #with open(urdf, 'r') as infp:
    #    robot_desc = infp.read()
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
            # Publish the joint state values for the non-fixed joints in the URDF file.
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher'),

            # A GUI to manipulate the joint state values
        # Node(
        #     condition=IfCondition(gui),
        #     package='joint_state_publisher_gui',
        #     executable='joint_state_publisher_gui',
        #     name='joint_state_publisher_gui'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}]
            ),
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen')
            #arguments=['-d', rviz_config_file])
    ])