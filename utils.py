from models import (
    Groups,
    Students, 
    OnlineLessons,
    StudentsOnlineLessons,
    HomeworksStudents,
    StudentsReviews,
)

from peewee import DoesNotExist

group_name = "Python413"


try:
    group = Groups.get(group_name=group_name)
except DoesNotExist:
    group = None

print(f'Результат поиска группы по запросу "{group_name}": {group}')
print(type(group))

if group:
    print(f"Группа: {group.group_name}")
    print(f"Дата создания: {group.created_at}")


group_name_like = "python"

groups_like = Groups.select().where(
    Groups.group_name.contains(group_name_like)
)
groups_like2 = Groups.get(Groups.group_name.contains("413"))

print(type(groups_like))
print(type(groups_like2))

print(f"Содержание переменной groups_like: {groups_like}")
print(f"Содержание переменной groups_like2: {groups_like2}")

print(f"Длина коллекции groups_like: {len(groups_like)}")
if len(groups_like) > 0:
    print(f"Название группы из первого элемента коллекции groups_like: {groups_like[0].group_name}")


group_0 = groups_like[0]
all_students = group_0.students

[print(f'{student.first_name} {student.last_name}') for student in all_students]

where_1 = "python"
where_2 = "413"

all_groups = Groups.select()

all_groups = all_groups.where(Groups.group_name.contains(where_1))
all_groups = all_groups.where(Groups.group_name.contains(where_2))

print(f"Тип данных all_groups: {type(all_groups)}")
print(f"Длина коллекции all_groups: {len(all_groups)}")

[print(group) for group in all_groups]

# 4. Выборка ВСЕ СТУДЕТЫ + JOIN GROUPS - чтобы отобразить читаемые названия групп
group_name = "python413"
group = Groups.get(Groups.group_name == group_name)
 
# Выборка всех студентов из группы python413
all_students = Students.select() # Доступ к названим групп тут будет, НО для каждого студента будет отдельный запрос к БД
 
# Выборка студентов из группы python413 если у нас на руках есть объект группы
students_413 = Students.select().where(Students.group_id == group)
 
 
# Если у нас только название группы в виде строки, то нам нужен явный JOIN
# Так же эта штука поможет решить проблему N+1 запросов, когда мы получаем студентов и для каждого студента делаем отдельный запрос к БД для получения названия группы (как в прошлом примере)
students_413 = (
    Students.select()
    .join(Groups)
    .where(Groups.group_name == group_name)
)
 
# Тесты - просто подствим сюда разные переменные выше из пункта 4
print(f"Тип данных all_students: {type(students_413)}")
print(f"Длинна коллекции all_students: {len(students_413)}")
 
[print(f"{student.first_name} {student.last_name} - {student.group_id.group_name}") for student in students_413]
 

# 5
students_413 = (
    Students.select(Students.first_name, Students.last_name, Groups.group_name)
    .join(Groups)
    .where(Groups.group_name == group_name)
)

for student in students_413:
    print(f"{student.first_name} {student.last_name} - {student.group_id.group_name}")

# 6
students_413 = (
    Students.select()
    .join(Groups)
    .where(Groups.group_name == "python413")
    .prefetch(Groups)
)

for student in students_413:
    print(f"{student.first_name} {student.last_name} - {student.group_id.group_name}")

#  7 Найти всех студентов где в first_name входит алекс или влад
print(f'*' * 50)

students = (
    Students.select()
    .where(
        (Students.first_name.contains("лекс"))
        | (Students.first_name.contains("лад"))
    )
    .prefetch(Groups)
)

for student in students:
    print(f"{student.first_name} {student.last_name} - {student.group_id.group_name}")


# Создание новой группы 
# new_group = Groups.create(group_name="python412")

# Метод, который не создаст объект, он уже существует
new_group, created = Groups.get_or_create(group_name="python412")
print(f"Группа создана: {created}, объект: {new_group}")

new_groups = [
    {"group_name": "python419"},
    {"group_name": "python422"},
]

new_groups_objects = [Groups(**group) for group in new_groups]

#  Создаем группы в БД
# Groups.bulk_create(new_groups_objects)

# Проверим, что группы создались
new_groups = Groups.select()
print(f"Количество групп в БД: {len(all_groups)}")

new_student_data = {
    "first_name": "Утрэд", "last_name": "Рагнарсон", "middle_name": "Беббанбургский", "group_name": "python413", "notes": "Студент из Южной Дании",
    
}

# new_student = Students.create(
#     **new_student_data
# )

# Поиск студента Утрэд Рагнарсон Беббанбургский
baggins = Students.get(Students.last_name == "Рагнарсон")
print(f"Студент найден: {baggins.first_name} {baggins.last_name}")