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