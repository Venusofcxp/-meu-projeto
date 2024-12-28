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

        # Filtra os dados desejados
        info = data.get("info", {})
        movie_data = data.get("movie_data", {})

        filtered_data = {
            "banner": info.get("backdrop_path", [None])[0],  # Pega o primeiro item do array
            "genre": info.get("genre"),
            "description": info.get("description"),
            "releasedate": info.get("releasedate"),  # Usa o campo releasedate
            "stream_id": movie_data.get("stream_id"),
            "category_id": movie_data.get("category_id"),
            "tmdb_id": info.get("tmdb_id"),
        }

        return jsonify(filtered_data)
    except requests.exceptions.RequestException as e:
        # Retorna erro com detalhes
        return jsonify({"error": str(e)}), 500

# Para rodar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
