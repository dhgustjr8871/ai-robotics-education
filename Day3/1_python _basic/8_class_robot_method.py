# 메서드 정의 예제
class Robot:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, I am robot {self.name}.")

r = Robot("Moby")
r.greet()
