from flask import Flask, request, jsonify
import movement_chips_3d
import numpy as np
def convert_floats(obj):
    if isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return [convert_floats(x) for x in obj]
    elif isinstance(obj, (list, tuple)):
        return [convert_floats(x) for x in obj]
    return obj


app = Flask(__name__)

@app.route('/api/movement_chip', methods=['POST'])
def receive_data():
    try:
        # Получаем данные из тела запроса в формате JSON
        data = request.get_json()

        # Проверяем, что данные были отправлены
        if not data:
            return jsonify({'error': 'No data provided'}), 400  # Bad Request

        # Получаем нужные поля из данных
        chip_uid = data.get('chip_uid')
        chip_move = data.get('chip_move')

        # Проверяем, что все обязательные поля присутствуют
        if not chip_uid or not chip_move:
            return jsonify({'error': 'chip_uid and chip_move are required fields'}), 400
        
        result = movement_chips_3d.main(movement_chips_3d.playing_arena, chip_uid, chip_move)
        result['matrix'] = convert_floats(result['matrix'])
        # Возвращаем ответ
        return jsonify({'Result': result}), 201 # 201 Created

    except Exception as e:
        return jsonify({'error': str(e)}), 500 # Internal Server Error

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
