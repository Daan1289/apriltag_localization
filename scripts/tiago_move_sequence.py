#!/usr/bin/python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(x, y, rotation):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.orientation.w = rotation

    client.send_goal(goal)
    wait = client.wait_for_result()
	

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        for position in [(-2.0, -1.0, 1.0), (-2.0, 1.0, 0.5), (0.0, 0.0, 0.5)]:
            result = movebase_client(position[0], position[1], position[2])
            if result:
                rospy.loginfo("Goal execution done!")

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
