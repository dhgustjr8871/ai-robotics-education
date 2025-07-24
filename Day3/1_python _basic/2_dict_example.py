# 딕셔너리 예제
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
print(person["name"])  # John
person["age"] = 31
person["job"] = "Engineer"
del person["city"]
print(len(person))  # 3
