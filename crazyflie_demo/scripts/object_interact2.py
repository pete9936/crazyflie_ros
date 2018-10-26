def base_follow(human, cf1):
    base_position = swarmlib.get_coord(base)
    drone1_position = swarmlib.get_coord(cf1)
    drone1_pose_goal = np.array([ base_position[0]-1, base_position[1], base_position[2] ])
    swarmlib.publish_goal_pos(drone1_pose_goal, 0, "crazyflie1")

def follower():
    base_sub = message_filters.Subscriber('/vicon/base/base', TransformStamped)
    cf1_sub = message_filters.Subscriber('/vicon/cf1/cf1', TransformStamped)
    ts = message_filters.TimeSynchronizer([base_sub, cf1_sub], 10)
    ts.registerCallback(base_follow)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('test_high_level')
    cf = crazyflie.Crazyflie("cf1", "/vicon/cf1/cf1")
    cf.setParam("commander/enHighLevel", 1)
    cf.takeoff(targetHeight = 0.5, duration = 2.0)
    time.sleep(3.0)

    print "\nfollowing base!"
    try:
        follower()
    except KeyboardInterrupt:
        pass

