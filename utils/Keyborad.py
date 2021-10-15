import keyboard

print(0)
keyboard.wait('a')
#在按下a之前后面的语句都不会执行，下面同理
print(1)
keyboard.wait('b')
print(2)
keyboard.wait('c')
print(3)
keyboard.wait()

# 结果：
# 0
# 1
# 2
# 3

#继续监听
#只有按顺序按下abc（中间过程随便按不干扰）才能输出0123，但因为最后一个没设置按键，所以会一直监听下去
