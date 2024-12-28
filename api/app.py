from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/filme/<int:vod_id>', methods=['GET'])
def get_filme(vod_id):
    # URL base com as credenciais
    base_url = "https://cdnbrr.click/player_api.php"
    username = "146301758"
    password = "024295079"

    # Monta a URL completa
    url = f"{base_url}?username={username}&password={password}&action=get_vod_info&vod_id={vod_id}"

    try:
        # Faz a requisição para a URL
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Pega os dados como JSON

        # Retorna o JSON completo
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # Retorna erro com detalhes
        return jsonify({"error": str(e)}), 500

# Para rodar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
