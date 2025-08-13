# Lecture 1: 파이썬 빠르게 살펴보기
본 강의는 파이썬(Python)의 핵심 문법과 객체 지향 프로그래밍의 기초를 짧은 시간 안에 이해할 수 있도록 구성되어 있습니다. 리스트, 딕셔너리, 조건문, 반복문, 함수와 같은 기본 문법부터 클래스 정의, 생성자, 메서드 사용법까지 단계적으로 살펴봅니다.

## 목차
- [Lecture 1: 파이썬 빠르게 살펴보기](#lecture-1-파이썬-빠르게-살펴보기)
  - [목차](#목차)
  - [1. python 기본 문법](#1-python-기본-문법)
    - [1.1 리스트 (List)](#11-리스트-list)
    - [1.2 딕셔너리 (Dictionary)](#12-딕셔너리-dictionary)
    - [1.3 조건문 (if)](#13-조건문-if)
    - [1.4 반복문 (while/for)](#14-반복문-whilefor)
    - [1.5 함수 (Function)](#15-함수-function)
    - [1.6 더 해보기](#16-더-해보기)
  - [2. 클래스 기초](#2-클래스-기초)
    - [2.1 클래스 정의와 생성자](#21-클래스-정의와-생성자)
    - [2.2 인스턴스 생성과 속성 접근](#22-인스턴스-생성과-속성-접근)
    - [2.3 메서드 정의](#23-메서드-정의)
    - [2.4 클래스 예제: Person](#24-클래스-예제-person)
    - [2.5 더 해보기](#25-더-해보기)
  - [3. 마무리](#3-마무리)

## 1. python 기본 문법
### 1.1 리스트 (List)
리스트는 여러 개의 항목을 하나의 변수에 저장할 수 있는 데이터 타입입니다.  
항목들은 순서가 있으며, **인덱스(index)**를 통해 접근할 수 있습니다.

#### 리스트의 특징
- 여러 자료형을 함께 저장 가능 (정수, 문자열, 리스트 등)
- 항목의 순서가 유지되며, 0부터 시작하는 인덱스를 가집니다.
- 항목을 추가, 삭제, 변경할 수 있는 **가변(mutable)** 자료형입니다.
- 중복된 값을 가질 수 있습니다.

#### 인덱싱(Indexing)
- `fruits[0]` → 첫 번째 요소
- `fruits[-1]` → 마지막 요소
- 인덱스 범위를 벗어나면 `IndexError` 발생

#### 슬라이싱(Slicing)
- `fruits[1:3]` → 인덱스 1부터 2까지의 요소
- `fruits[:2]` → 처음부터 인덱스 1까지
- `fruits[::2]` → 처음부터 끝까지 2칸씩 건너뛰며 선택

#### 주요 메서드
- `append(x)`: 리스트 끝에 항목 추가
- `insert(i, x)`: i번째 위치에 항목 삽입
- `remove(x)`: 항목 삭제(값 기준, 없으면 오류)
- `pop(i)`: i번째 항목 삭제 후 반환 (인덱스 생략 시 마지막 항목)
- `sort()`: 정렬
- `reverse()`: 순서 뒤집기

#### 예제코드(1_list_example.py):
```python
# 리스트 예제
fruits = ["apple", "banana", "cherry"]

print(fruits[0])  # 0번째 원소 출력하기( "apple")

fruits.append("orange") # 리스트에 "orange" 추가
print(fruits)

fruits.remove("banana") # 리스트에서 "banana" 제거
print(fruits)

print(len(fruits))  # 리스트의 길이 출력하기 (3)
```

### 1.2 딕셔너리 (Dictionary)
딕셔너리는 **키-값(key-value) 쌍**을 저장하는 데이터 타입입니다.  
각 키는 **고유**하며, 이를 통해 값에 접근할 수 있습니다.

#### 딕셔너리의 특징
- **key**: 고유해야 하며, 변경 불가능한(immutable) 자료형만 사용 가능 (문자열, 숫자, 튜플 등)
- **value**: 어떤 자료형이든 가능 (숫자, 문자열, 리스트, 다른 딕셔너리 등)
- Python 3.7부터 입력 순서를 유지합니다.
- JSON 데이터 구조와 유사하여 API 응답, 설정 파일 등에 자주 사용됩니다.

#### 주요 동작
- **값 접근**
  - `person["name"]`: 키로 직접 접근 (키가 없으면 `KeyError` 발생)
  - `person.get("country", "없음")`: 키가 없으면 기본값 반환
- **값 수정/추가**
  - `person["age"] = 31`: 기존 값 수정
  - `person["job"] = "Engineer"`: 새로운 키-값 추가
- **값 삭제**
  - `del person["city"]`: 항목 삭제
  - `person.pop("city")`: 삭제하면서 값 반환
- **길이 확인**
  - `len(person)`: 키-값 쌍의 개수 반환

#### 예제코드(2_dict_example.py):
```python
# 딕셔너리 생성: 이름, 나이, 도시 정보를 저장
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# 딕셔너리에서 key가 "name"인 값을 출력 -> John
print(person["name"])  

# 딕셔너리에서 key가 "age"인 값을 31로 변경
person["age"] = 31

# 딕셔너리에 새로운 key-value 쌍 추가 (job: "Engineer")
person["job"] = "Engineer"

# 딕셔너리에서 key가 "city"인 항목 삭제
del person["city"]

# 딕셔너리의 항목 개수를 출력 -> 현재 3개 (name, age, job)
print(len(person)) 
```

### 1.3 조건문 (if)
조건문은 주어진 조건이 참인지 거짓인지에 따라 다른 코드를 실행할 수 있게 합니다. Python에서는 `if`, `elif`, `else` 키워드를 사용하여 조건 분기를 작성합니다.


- **if**: 첫 번째로 조건을 검사하고, 조건이 참(`True`)이면 해당 코드 블록을 실행합니다.
- **elif**: 앞의 `if`나 다른 `elif` 조건이 거짓(`False`)일 때, 새로운 조건을 검사합니다. 여러 개 작성할 수 있습니다.
- **else**: 앞의 모든 조건이 거짓일 경우 실행되며, 조건식을 작성하지 않습니다.

#### 조건식
- 비교 연산자: `==`(같다), `!=`(다르다), `<`, `>`, `<=`, `>=`
- 논리 연산자: `and`, `or`, `not`
- 조건식은 반드시 `True` 또는 `False`로 평가되는 값이어야 합니다.

#### 들여쓰기
- Python은 들여쓰기로 코드 블록을 구분하므로, 조건문 안의 실행 코드는 같은 들여쓰기 간격을 맞춰야 합니다.


#### 예제코드(3_if_example.py):
```python
x = 10
y = 20

if x > y:
    print("x는 y보다 큽니다.")  # 조건이 참일 때 실행
elif x < y:
    print("x는 y보다 작습니다.")  # 첫 조건이 거짓이고, 이 조건이 참일 때 실행
else:
    print("x와 y는 같습니다.") # else 문: 위 조건들이 모두 거짓일 때 실행
```


### 1.4 반복문 (while/for)
반복문은 특정 조건이 참인 동안 또는 주어진 시퀀스의 각 항목에 대해 코드를 반복 실행합니다. Python에서는 대표적으로 **while문**과 **for문**이 있습니다.


#### while문
- **특정 조건이 참(True)** 인 동안 계속 반복 실행합니다.
- 반복 횟수가 정해져 있지 않거나, 조건이 만족될 때까지 실행해야 할 때 유용합니다.
- 조건이 영원히 참이면 무한 루프가 되므로, 내부에서 조건을 변경하는 코드가 필요합니다.
  
#### 예제코드(4_while_example.py):
```python
# 변수 count를 0으로 초기화
count = 0

# while 반복문: count가 5보다 작은 동안 반복 실행
while count < 5:
    print(count)
    count += 1 # count 값을 1 증가시킴 (증가시키지 않으면 무한 루프 발생)
```

#### for문
- **정해진 범위**나 **시퀀스(리스트, 튜플, 문자열 등)**의 각 항목을 순서대로 꺼내며 반복 실행합니다.
- 반복 횟수가 명확하거나, 데이터 집합의 모든 항목을 순회할 때 유용합니다.
- Python의 for문은 **반복 가능한 객체(iterable)**와 함께 사용됩니다.

#### 예제코드(5_for_example.py):
```python
# 리스트의 각 항목을 반복하며 출력하는 for문 예제
fruits = ["apple", "banana", "cherry"]  # 과일 이름이 담긴 리스트 생성

for fruit in fruits:  # 리스트의 각 항목(fruit)에 대해 반복
    print(fruit)      # 현재 항목을 출력
```

### 1.5 함수 (Function)
Python에서 함수(Function)는 **특정 작업을 수행하는 재사용 가능한 코드 블록**입니다. 함수는 호출될 때 실행되며, 입력값(매개변수)을 받아서 결과값(반환값)을 줄 수 있습니다.

#### 예제코드(6_function_example.py):
#### 함수 이름 (Function Name)
- 함수를 식별하는 고유한 이름입니다.
- 이름을 통해 함수를 호출(call)할 수 있습니다.
- 변수명 규칙과 동일하게, 알파벳·숫자·언더스코어(`_`)를 사용할 수 있으며, 숫자로 시작할 수 없습니다.
- 의미 있는 이름을 사용하는 것이 좋습니다.

```python
def greet1():
    print("Hello!")  # greet가 함수 이름
```

#### 매개변수 (Parameter)
- 함수에 **외부 값(인자, argument)** 을 전달받기 위해 선언하는 변수입니다.
- 함수 내부에서 입력값처럼 사용됩니다.
- 여러 개의 매개변수를 쉼표로 구분해서 정의할 수 있습니다.
- 매개변수에는 기본값(Default value)을 설정할 수도 있습니다.

```python
def add(a, b):  # a, b가 매개변수
    return a + b

# 기본값이 있는 매개변수
def greet2(name="Guest"):
    print(f"Hello, {name}!")
```

#### 반환값 (Return Value)
- 함수가 실행된 후 결과를 호출한 곳에 되돌려주는 값입니다.
- `return` 키워드를 사용하며, 함수는 `return`을 만나면 실행을 종료합니다.
- 반환값이 없으면 `None`을 반환합니다.

```python
def multiply(a, b):
    return a * b  # 곱한 값을 반환
```

#### 함수 호출 (Function Call)
- 정의한 함수를 실행하기 위해 **함수 이름**과 **필요한 인자**를 작성합니다.
- 함수 호출 시, 매개변수에 맞는 개수와 순서대로 인자를 전달해야 합니다.
- 기본값(Default value)이 있는 매개변수는 인자를 생략할 수 있습니다.

```python
greet1()
greet2("Alice")  # "Hello, Alice!" 출력
greet2()  # "Hello, Guest!" 출력
result = multiply(4, 5)  # result에는 20이 저장됨
```

### 1.6 더 해보기
다음 조건을 만족하는 **학생 성적 관리 프로그램**을 만들어보자.

#### 리스트 작성
- 학생의 이름과 성적을 `students`라는 이름의 리스트로 저장합니다. 
- 각 리스트의 원소는 딕셔너리이고, 키 값으로 `name`, `math`, `science`를 가집니다. 
- 각 학생의 이름과 수학, 과학 점수는 다음과 같습니다. 

<p align="center">

| 이름     | 수학 점수 | 과학 점수 |
|----------|-----------|-----------|
| Alice    | 88        | 92        |
| Bob      | 75        | 85        |
| Charlie  | 95        | 90        |

</p>

#### 함수 작성
- 학생의 이름을 인자로 받아 그 학생의 평균 점수를 return하는 함수 `avg_score()`를 작성합니다. 그 후에 `avg_score()`의 return 값을 받아와서 출력하는 부분도 작성합니다.
- 전체 학생의 수학, 과학 과목별 평균 점수를 출력하는 `result()`함수를 작성합니다. `result()`함수는 매개변수가 없습니다. 출력예시: `수학 평균: 00점, 과학 평균: 00점`  




## 2. 클래스 기초

클래스(Class)는 데이터를 구조화하고 관련 기능을 하나의 세트로 묶어 코드의 재사용성과 유지보수성을 높이는 중요한 파이썬 개념입니다. 이 섹션에서는 클래스의 구조와 사용 방법을 간단한 예제를 통해 배워봅니다.

### 2.1 클래스 정의와 생성자
클래스를 정의할 때는 `class` 키워드를 사용하고, 생성자 메서드인 `__init__`를 통해 객체가 생성될 때 필요한 속성들을 초기화할 수 있습니다.

#### 예제코드(7_class_robot_basic.py):
```python
class Robot:
    def __init__(self, name, model):
        self.name = name
        self.model = model
```

### 2.2 인스턴스 생성과 속성 접근
클래스 정의 후, 해당 클래스를 기반으로 실제 객체(인스턴스)를 생성할 수 있습니다.

#### 예제코드(7_class_robot_basic.py):
```python
my_robot = Robot("Indy", "MK-7")
print(my_robot.name)   # Indy
print(my_robot.model)  # MK-7
```

### 2.3 메서드 정의
클래스 안에 정의된 함수는 '메서드'라고 부르며, `self`를 첫 번째 인자로 받아 해당 인스턴스에 접근할 수 있습니다.

#### 예제코드(8_class_robot_method.py):
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

#### 예제코드(9_class_person.py):
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

### 2.5 더 해보기
다음 조건을 만족하는 **`Car`** 클래스를 작성하세요.


#### 1. 속성(Attributes)
- `brand` : 자동차 브랜드 이름 (문자열)  
- `speed` : 현재 속도 (정수, 기본값 0)  
- `fuel` : 남은 연료량(리터 단위, 정수, 기본값 50)  

#### 2. 메서드(Methods)
- `accelerate(amount)` :  
  - `amount` 만큼 속도를 증가시킵니다.  
  - 증가한 속도만큼 연료(`fuel`)를 1 감소시킵니다.  
  - 연료가 0이면 속도를 올릴 수 없으며 `"No fuel left!"`를 출력합니다.

- `brake(amount)` :  
  - `amount` 만큼 속도를 줄입니다.  
  - 속도는 0 미만이 될 수 없습니다.

- `refuel(liters)` :  
  - `liters` 만큼 연료를 채웁니다.



## 3. 마무리

이번 세션에서는 파이썬의 기초 문법부터 클래스 구조까지 간단히 살펴보았습니다. 
