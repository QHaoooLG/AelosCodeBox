import CMDcontrol as CMD
import threading
import time
import action_includ as action

real = 1
i=0

#动作指令监听线程
def move_action():
    if real :
        CMD.CMD_transfer()
th1 = threading.Thread(target=move_action)
th1.setDaemon(True)
th1.start()

while True:
    while i<3:
        action.go_fast(1)
        i+=1
    break
