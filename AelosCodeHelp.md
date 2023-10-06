## Aelos
##### 启动Aelos主程序的指令
```shell
# 人工智能赛时期运行Aelos主程序的指令
aelos-smart
$ cd /home/lemon/catkin_ws/src/college_caai/launch
$ roslaunch AI_competition.launch
$ cd /home/lemon/catkin_ws/src/robot_demo/scripts
$ python college_tag_traker_fast_right.py

aelos-pro
$ roslaunch robot_demo ar_track.launch
$ cd /home/lemon/catkin_ws/src/robot_demo/scripts
$ python  college_tag_traker_fast_right.py
```
```shell
# 仿人竞速适用指令
aelos-pro-7013
# 若需要先打开节点则输入
# $ cd ./catkin_ws/src/aelos_race_demo/robot_demo/launch
# $ roslaunch ar_tracker.launch
$ cd ./catkin_ws/src/aelos_race_demo/robot_demo/scripts
$ python follow_lines.py

aelos-pro-700C
# 若需要先打开节点则输入
# $ cd ./catkin_ws/src/aelos_race_demo/robot_demo/launch
# $ roslaunch ar_tracker.launch
$ cd ./catkin_ws/src/aelos_race_demo/robot_demo/scripts
$ python follow_lines.py
```
##### 1. 各机型连接手机热点后的ip地址
+ 700C : 192.168.43.218
+ 7013 : 192.168.43.252
+ 其他两台Aelos都不能进行手机热点连接，应该是手动版的

##### 2. 