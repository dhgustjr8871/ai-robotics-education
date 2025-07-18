# Lecture 1: 파이썬 빠르게 살펴보기

이 트레이닝 세션은 파이썬을 잘 몰라도 전반적인 흐름을 이해할 수 있도록 답안이 제공되고 있습니다. 파이썬을 잘 모른다면 아래의 문법/기능 정도만 이해하면 진행이 수월할 것입니다.

우선 터미널 프롬프트에서 아래 명령어를 통해 Day3/1_python_basic 폴더로 이동하겠습니다. (해당 위치를 프로그램 실행/참조의 기준위치로 설정함)

    cd Day3/1_python_basic

## 1. python 기본 문법

### 1.1 리스트 (List)
리스트는 여러 개의 항목을 하나의 변수에 저장할 수 있는 데이터 타입입니다. 항목들은 순서가 있으며, 인덱스를 통해 접근할 수 있습니다.

#### 예시:
```python
# 리스트 생성
fruits = ["apple", "banana", "cherry"]

# 항목 접근
print(fruits[0])  # apple

# 리스트에 항목 추가
fruits.append("orange")

# 리스트 항목 제거
fruits.remove("banana")

# 리스트 길이 확인
print(len(fruits))  # 3
```

### 1.2 딕셔너리 (Dictionary)
딕셔너리는 키-값 쌍을 저장하는 데이터 타입입니다. 각 키는 고유하며, 이를 통해 값에 접근할 수 있습니다.

#### 예시:
```python
# 딕셔너리 생성
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# 값 접근
print(person["name"])  # John

# 값 변경
person["age"] = 31

# 키-값 쌍 추가
person["job"] = "Engineer"

# 키-값 쌍 제거
del person["city"]

# 딕셔너리 길이 확인
print(len(person))  # 3
```

### 1.3 조건문 (if)
조건문은 주어진 조건이 참인지 거짓인지에 따라 다른 코드를 실행할 수 있게 합니다.

#### 예시:
```python
x = 10
y = 20

if x > y:
    print("x는 y보다 큽니다.")
elif x < y:
    print("x는 y보다 작습니다.")
else:
    print("x와 y는 같습니다.")
```
### 1.4 반복문 (while/for)
반복문은 특정 조건이 참인 동안 또는 주어진 시퀀스의 각 항목에 대해 코드를 반복 실행합니다.

#### while 문 예시:
```python
count = 0

while count < 5:
    print(count)
    count += 1
```
### for 문 예시:
```python
코드 복사
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

### 1.5 함수 (Function)
함수는 재사용 가능한 코드 블록으로, 특정 작업을 수행하기 위해 호출될 수 있습니다.

```python
# 함수 정의
def greet(name):
    return f"Hello, {name}!"

# 함수 호출
print(greet("Alice"))  # Hello, Alice!

# 인자가 없는 함수
def say_hello():
    print("Hello!")

say_hello()  # Hello!
```



## 2. 클래스 기초

클래스(Class)는 데이터를 구조화하고 관련 기능을 하나의 청사진으로 묶어 코드의 재사용성과 유지보수성을 높이는 중요한 파이썬 개념입니다. 이 섹션에서는 클래스의 구조와 사용 방법을 간단한 예제를 통해 배워봅니다.

### 2.1 클래스 정의와 생성자 (`__init__`)
클래스를 정의할 때는 `class` 키워드를 사용하고, 생성자 메서드인 `__init__`를 통해 객체가 생성될 때 필요한 속성들을 초기화할 수 있습니다.

```python
class Robot:
    def __init__(self, name, model):
        self.name = name
        self.model = model
```

### 2.2 인스턴스 생성과 속성 접근
클래스 정의 후, 해당 클래스를 기반으로 실제 객체(인스턴스)를 생성할 수 있습니다.

```python
my_robot = Robot("Indy", "MK-7")
print(my_robot.name)   # Indy
print(my_robot.model)  # MK-7
```

### 2.3 메서드 정의
클래스 안에 정의된 함수는 '메서드'라고 부르며, `self`를 첫 번째 인자로 받아 해당 인스턴스에 접근할 수 있습니다.

```python
class Robot:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, I am robot {self.name}.")

r = Robot("Moby")
r.greet()  # Hello, I am robot Moby.
```

### 2.4 클래스 예제: Person
아래는 앞서 배운 개념을 모두 활용한 `Person` 클래스의 예시입니다.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

person1 = Person("Alice", 30)
person1.greet()

person2 = Person("Bob", 25)
person2.greet()
```




## 마무리

이번 세션에서는 파이썬의 기초 문법부터 클래스 구조까지 간단히 살펴보았습니다. 
