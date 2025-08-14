# 함수 정의
# 이름
def greet1():
    print("Hello!")  # greet가 함수 이름

# 매개변수
def add(a, b):  # a, b가 매개변수
    return a + b

# 기본값이 있는 매개변수
def greet2(name="Guest"):
    print(f"Hello, {name}!")

# return 값
def multiply(a, b):
    return a * b  # 곱한 값을 반환

# 함수 호출
greet1()
greet2("Alice")  # "Hello, Alice!" 출력
greet2()  # "Hello, Guest!" 출력
result = multiply(4, 5)  # result에는 20이 저장됨
