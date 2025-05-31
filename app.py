"""
Flask приложение для работы с API "Academy"
"""

from flask import Flask, jsonify, request
from utils import get_group_by_id

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Конфигурация приложения - выключим ascii режим для поддержки кириллицы
app.config["JSON_AS_ASCII"] = False

# Делаем первый маршрут для дщобычи группы по ID
@app.route("/group/<int:group_id>", methods=["GET"])
def get_group(group_id):
    group = get_group_by_id(group_id)
    group_dict = {
        "id": group.id,
        "group_name": group.group_name,
        "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    if group:
        return jsonify(group_dict), 200
    return jsonify({"error": "Group not found"}), 404

# Запускаем приложение
if __name__ == "__main__":
    app.run(debug=True)