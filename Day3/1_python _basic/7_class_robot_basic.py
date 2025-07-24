# 클래스 정의 및 생성자 예제
class Robot:
    def __init__(self, name, model):
        self.name = name
        self.model = model

my_robot = Robot("Indy", "MK-7")
print(my_robot.name)   # Indy
print(my_robot.model)  # MK-7
