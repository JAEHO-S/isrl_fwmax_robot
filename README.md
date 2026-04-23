# isrl_fwmax_robot

`isrl_fwmax_robot`은 FWMAX Pro 로봇의 커스텀 ROS 2 패키지 모음입니다. 이 디렉토리는 세 개의 주요 패키지로 구성되어 있습니다:

- `isrl_robot_description`
- `isrl_fwmax_nav2`
- `isrl_fwmax_slam`

## 패키지 구성

### 1. isrl_robot_description
- 목적: FWMAX Pro 로봇의 URDF/xacro 모델과 메시(mesh)를 제공합니다.
- 주요 파일:
  - `urdf/robot.xacro`
  - `meshes/isrl_fwmax_pro.dae`
  - `launch/robot.launch.py`, `launch/robot_no_arm.launch.py`
- 특징:
  - `mobile_base_link`와 `base_footprint`를 정의하는 간단한 로봇 모델
  - 3D 메시를 시각화 및 충돌 모델로 사용
  - `yhs_can_control` 패키지에 대한 런타임 의존성 있음

### 2. isrl_fwmax_nav2
- 목적: Nav2 기반 자율 주행을 위한 런치 패키지 및 파라미터
- 주요 파일:
  - `launch/nav2.launch.py`
  - `params/nav2_params2.yaml`
  - `maps/lab_map.pgm`, `maps/lab_map.yaml`
- 특징:
  - `nav2_bringup`의 `bringup_launch.py`를 포함하여 전체 Nav2 스택을 실행
  - 로봇 프레임은 `base_footprint`, `odom`, `map` 사용
  - `cmd_vel_nav` 토픽으로 Nav2 출력을 내보내고 `cmd_vel`로 변환하는 `velocity_smoother` 설정
  - `planner_server`로 `nav2_smac_planner/SmacPlannerHybrid` 사용
  - 센서 입력은 Ouster LiDAR를 기반으로 `ouster/scan` 및 `ouster/points` 토픽을 참조

### 3. isrl_fwmax_slam
- 목적: `slam_toolbox`를 이용한 실시간 SLAM 실행
- 주요 파일:
  - `launch/slam_toolbox.launch.py`
  - `params/slam_toolbox_online_param.yaml`
- 특징:
  - `slam_toolbox`의 `online_async_launch.py`를 호출
  - `scan_topic`은 `/ouster/scan`
  - `mode: mapping`으로 지도 생성
  - `use_scan_matching: true`, `map_update_interval: 2.0`, `resolution: 0.05`

## 사용 방법

### 1. 빌드
```bash
cd /home/jhgod/fwmax_ws
colcon build --packages-select isrl_robot_description isrl_fwmax_nav2 isrl_fwmax_slam
```

### 2. 환경 설정
```bash
source install/setup.bash
```

### 3. Nav2 실행
```bash
ros2 launch isrl_fwmax_nav2 nav2.launch.py
```

### 4. SLAM 실행
```bash
ros2 launch isrl_fwmax_slam slam_toolbox.launch.py
```

### 5. 로봇 설명 실행
```bash
ros2 launch isrl_robot_description robot.launch.py
```

## 참고 사항

- `isrl_fwmax_nav2`의 `params/nav2_params2.yaml` 내부에 있는 `map_server.yaml_filename` 항목은 현재 절대 경로(`/home/jhgod/maps/lab_map.yaml`)로 설정되어 있습니다. 워크스페이스를 옮기거나 공유할 때 이 경로를 수정해야 할 수 있습니다.
- `isrl_fwmax_nav2` 패키지는 `map_file`을 패키지 내부 `maps/lab_map.yaml`로 참조하지만, Nav2 파라미터 자체에서 별도 `map_server` 설정이 있습니다.
- 센서 토픽은 Ouster 기반 설정으로 되어 있으므로, 실제 로봇 환경이나 시뮬레이션에서 센서 토픽 이름을 맞춰줘야 합니다.

## 패키지 빌드 타입

- `isrl_robot_description`: `ament_cmake`
- `isrl_fwmax_nav2`: `ament_python`
- `isrl_fwmax_slam`: `ament_python`

## 요약

이 저장소는 FWMAX Pro 로봇의 기본 설명(`isrl_robot_description`), Nav2 자율 주행 스택(`isrl_fwmax_nav2`), 그리고 SLAM 스택(`isrl_fwmax_slam`)을 구성하는 세 개의 패키지를 포함합니다. 각 패키지는 ROS 2 런치와 파라미터 구성을 중심으로 설계되어 있으며, 실제 로봇 센서 토픽 및 맵 경로를 현장 환경에 맞게 조정하는 것이 중요합니다.
