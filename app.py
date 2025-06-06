"""
Flask приложение для работы с API "Academy"
"""

from flask import Flask, jsonify, request
from utils import get_group_by_id, get_groups_list, get_student_by_id, create_group, update_group_id, delete_group_id, create_student
from peewee import DoesNotExist, IntegrityError

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Конфигурация приложения - выключим ascii режим для поддержки кириллицы
app.config["JSON_AS_ASCII"] = False

# Делаем первый маршрут для добычи группы по ID 
# http://127.0.0.1:5000/group/1
@app.route("/group/<int:group_id>", methods=["GET"])
def get_group(group_id):
    try:
        group = get_group_by_id(group_id)
    
    except DoesNotExist:
        return jsonify({"error": "Группа не найдена"}), 404
    
    else:
        group_dict = {
            "id": group.id,
            "group_name": group.group_name,
            "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        return jsonify(group_dict), 200
    

# /group/list/?sort_direction=desc&name_filter=413
# /group/list/
# http://127.0.0.1:5000/group/list/?sort_direction=desc&name_filter=1
@app.route("/group/list/", methods=["GET"])
def list_groups():
    
    # Пробуем добыть параметры из URL запроса
    sort_direction = request.args.get("sort_direction", "asc")
    name_filter = request.args.get("name_filter")
    
    if sort_direction not in ["asc", "desc"]:
        return jsonify({"error": "Неверное направление сортировки"}), 400
    
    groups = get_groups_list(sort_direction, name_filter)

    groups_list = []
    for group in groups:
        group_dict = {
            "id": group.id,
            "group_name": group.group_name,
            "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        groups_list.append(group_dict)

    return jsonify(groups_list), 200


# create_group
@app.route("/group/create/", methods=["POST"])
def group_create():
    # Получаем данные из запроса
    data = request.get_json()
    group_name = data.get("group_name")

    if not group_name:
        return jsonify({"error": "Название группы обязательно"}), 400

    try:
        group = create_group(group_name)  # Предполагается, что функция создает группу в БД
    except IntegrityError:
        return jsonify({"error": "Группа с таким названием уже существует"}), 400

    group_dict = {
        "id": group.id,
        "group_name": group.group_name,
        "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return jsonify(group_dict), 201

@app.route("/group/update/<int:group_id>", methods=["PUT"])
def update_group(group_id):
    # Получаем данные из запроса
    data = request.get_json()
    group_name = data.get("group_name")

    if not group_name:
        return jsonify({"error": "Название группы обязательно"}), 400

    try:
        updated_group = update_group_id(group_id, group_name)

    except DoesNotExist:
        return jsonify({"error": "Группа не найдена"}), 404
    
    except IntegrityError:
        return jsonify({"error": "Группа с таким названием уже существует"}), 400

    group_dict = {
        "id": updated_group.id,
        "group_name": updated_group.group_name,
        "created_at": updated_group.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return jsonify(group_dict), 200

@app.route("/group/delete/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    try:
        delete_group_id(group_id)  # Предполагается, что функция удаляет группу по ID

    except DoesNotExist:
        return jsonify({"error": "Группа не найдена"}), 404
    
    return jsonify({"message": "Группа успешно удалена"}), 200


# Добыть студента по ID
@app.route("/student/<int:student_id>", methods=["GET"])
def get_student(student_id):
    try:
        student = get_student_by_id(student_id)  # Предполагается, что функция работает с ID студента

    except DoesNotExist:
        return jsonify({"error": "Студент не найден"}), 404
    
    else:
        student_dict = {
            "id": student.id,
            "first_name": student.first_name,
            "middle_name": student.middle_name,
            "last_name": student.last_name,
            "group_id": student.group_id.id,
            "group_name": student.group_id.group_name,
            "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        return jsonify(student_dict), 200
    
# Создание студента
@app.route("/student/create/", methods=["POST"])
def student_create():
    # Получаем данные из запроса
    data = request.get_json()
    
    # Получаем необходимые поля из JSON
    first_name = data.get("first_name")
    middle_name = data.get("middle_name")
    last_name = data.get("last_name")
    group_id = data.get("group_id")
    notes = data.get("notes")

    if not first_name or not last_name or not group_id:
        return jsonify({"error": "Имя, фамилия и ID группы обязательны"}), 400

    try:
        student = create_student(first_name, last_name, group_id, middle_name, notes)  # Предполагается, что функция создает студента в БД
    except DoesNotExist:
        return jsonify({"error": "Группа не найдена"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    student_dict = {
        "id": student.id,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "group_id": student.group_id.id,
        "group_name": student.group_id.group_name,
        "notes": student.notes,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return jsonify(student_dict), 201

# Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)