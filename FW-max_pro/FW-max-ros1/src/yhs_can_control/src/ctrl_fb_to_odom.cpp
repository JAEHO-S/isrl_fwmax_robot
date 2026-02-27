#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>

#include "yhs_can_msgs/ctrl_fb.h" 

class CtrlFbToOdom {
public:
  CtrlFbToOdom() : nh_(), pnh_("~") {
    pnh_.param<std::string>("odom_frame", odom_frame_, "odom");
    pnh_.param<std::string>("base_frame", base_frame_, "mobile_base_link");

    odom_pub_ = nh_.advertise<nav_msgs::Odometry>("odom", 20);
    sub_ = nh_.subscribe("/mobile_robot/ctrl_fb", 50, &CtrlFbToOdom::cb, this);
  }

private:
  ros::NodeHandle nh_, pnh_;
  ros::Subscriber sub_;
  ros::Publisher odom_pub_;
  tf::TransformBroadcaster tf_br_;
  std::string odom_frame_, base_frame_;

  double x_=0.0, y_=0.0, yaw_=0.0;
  bool have_last_=false;
  ros::Time last_stamp_;

  static inline double normYaw(double a){ return atan2(sin(a), cos(a)); }

  void cb(const yhs_can_msgs::ctrl_fb::ConstPtr& msg) {
    // 1) 선속도 v [m/s], 각속도 ω [deg/s] -> rad/s 변환
    const double v = msg->ctrl_fb_x_linear;               // m/s (필드명 확인)
    const double omega = msg->ctrl_fb_z_angular * M_PI/180.0; // rad/s (필드명 확인)

    const ros::Time stamp = ros::Time::now(); // 가능하면 msg 헤더/장치 시각 사용

    if (!have_last_) { last_stamp_ = stamp; have_last_=true; return; }
    const double dt = (stamp - last_stamp_).toSec();
    last_stamp_ = stamp;
    if (dt <= 0.0 || dt > 1.0) return; // 이상한 시간은 스킵

    // 2) 적분
    x_   += v * cos(yaw_) * dt;
    y_   += v * sin(yaw_) * dt;
    yaw_  = normYaw(yaw_ + omega * dt);

    // 3) TF: odom -> base
    tf::Transform T;
    T.setOrigin(tf::Vector3(x_, y_, 0.0));
    tf::Quaternion q; q.setRPY(0,0,yaw_);
    T.setRotation(q);
    tf_br_.sendTransform(tf::StampedTransform(T, stamp, odom_frame_, base_frame_));

    // 4) Odometry 메시지
    nav_msgs::Odometry od;
    od.header.stamp = stamp;
    od.header.frame_id = odom_frame_;
    od.child_frame_id  = base_frame_;
    od.pose.pose.position.x = x_;
    od.pose.pose.position.y = y_;
    od.pose.pose.position.z = 0.0;
    od.pose.pose.orientation.x = q.x();
    od.pose.pose.orientation.y = q.y();
    od.pose.pose.orientation.z = q.z();
    od.pose.pose.orientation.w = q.w();

    // 대충의 공분산(원하면 조정)
    for(int i=0;i<36;i++){ od.pose.covariance[i]=0; od.twist.covariance[i]=0; }
    od.pose.covariance[0]=1e-2; od.pose.covariance[7]=1e-2; od.pose.covariance[14]=1e3;
    od.pose.covariance[21]=1e3; od.pose.covariance[28]=1e3; od.pose.covariance[35]=1e-1;
    
    // 수정된 코드
    od.twist.twist.linear.x  = v;
    od.twist.twist.linear.y  = 0.0;
    od.twist.twist.linear.z  = 0.0;
    od.twist.twist.angular.x = 0.0;
    od.twist.twist.angular.y = 0.0;
    od.twist.twist.angular.z = omega;

    // 공분산도 필요하다면 별도로 채움
    for(int i=0;i<36;i++) od.twist.covariance[i]=0;
    od.twist.covariance[0]  = 1e-2;
    od.twist.covariance[7]  = 1e-2;
    od.twist.covariance[35] = 1e-1;


    odom_pub_.publish(od);
  }
};

int main(int argc, char** argv){
  ros::init(argc, argv, "ctrl_fb_to_odom");
  CtrlFbToOdom n;
  ros::spin();
  return 0;
}
