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

        # Função para coletar todas as chaves do JSON
        def get_all_keys(obj, parent_key=''):
            keys = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full_key = f"{parent_key}.{k}" if parent_key else k
                    keys.append(full_key)
                    keys.extend(get_all_keys(v, full_key))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    keys.extend(get_all_keys(item, f"{parent_key}[{i}]"))
            return keys

        # Obtem todas as chaves do JSON
        all_keys = get_all_keys(data)

        return jsonify({"all_keys": all_keys})
    except requests.exceptions.RequestException as e:
        # Retorna erro com detalhes
        return jsonify({"error": str(e)}), 500

# Para rodar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
