from peewee import *

db =SqliteDatabase('academy_orm.db')


#  Группы
class Groups(Model):
    group_name = CharField()
    created_at = DateTimeField(constraints=[SQL('CURRENT_TIMESTAMP')])

    class Meta:
        database = db
        
# Первые орм запросы
all_groups = Groups.select()
[print(group.group_name) for group in all_groups]

all_groups = all_groups.order_by(Groups.group_name.desc())
[print(group.group_name) for group in all_groups]

group_413 = Groups.get(Groups.group_name.contains('413'))
print(group_413.group_name)