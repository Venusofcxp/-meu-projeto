from flask import Flask, jsonify
import requests
from collections import OrderedDict

app = Flask(__name__)

@app.route('/api/filme/<int:vod_id>', methods=['GET'])
def get_filme(vod_id):
    # URL base com as credenciais
    base_url = "http://solutta.shop:80"
    username = "881101381017"
    password = "896811296068"

    # Monta a URL completa
    url = f"{base_url}?username={username}&password={password}&action=get_vod_info&vod_id={vod_id}"

    try:
        # Faz a requisição para a URL
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Pega os dados como JSON

        # Ajusta o valor de backdrop_path, se necessário
        if "info" in data and "backdrop_path" in data["info"]:
            backdrop = data["info"]["backdrop_path"]
            if isinstance(backdrop, list) and len(backdrop) > 0:
                data["info"]["backdrop_path"] = backdrop[0]  # Substitui o array pelo primeiro item

        # Ordena os dados conforme o JSON original
        ordered_data = OrderedDict([
            ("info", OrderedDict([
                ("kinopoisk_url", data["info"].get("kinopoisk_url")),
                ("tmdb_id", data["info"].get("tmdb_id")),
                ("name", data["info"].get("name")),
                ("o_name", data["info"].get("o_name")),
                ("cover_big", data["info"].get("cover_big")),
                ("movie_image", data["info"].get("movie_image")),
                ("release_date", data["info"].get("release_date")),
                ("episode_run_time", data["info"].get("episode_run_time")),
                ("youtube_trailer", data["info"].get("youtube_trailer")),
                ("director", data["info"].get("director")),
                ("actors", data["info"].get("actors")),
                ("cast", data["info"].get("cast")),
                ("description", data["info"].get("description")),
                ("plot", data["info"].get("plot")),
                ("age", data["info"].get("age")),
                ("mpaa_rating", data["info"].get("mpaa_rating")),
                ("rating_count_kinopoisk", data["info"].get("rating_count_kinopoisk")),
                ("country", data["info"].get("country")),
                ("genre", data["info"].get("genre")),
                ("backdrop_path", data["info"].get("backdrop_path")),
                ("duration_secs", data["info"].get("duration_secs")),
                ("duration", data["info"].get("duration")),
                ("bitrate", data["info"].get("bitrate")),
                ("rating", data["info"].get("rating")),
                ("releasedate", data["info"].get("releasedate")),
                ("subtitles", data["info"].get("subtitles")),
            ])),
            ("movie_data", OrderedDict([
                ("stream_id", data["movie_data"].get("stream_id")),
                ("name", data["movie_data"].get("name")),
                ("title", data["movie_data"].get("title")),
                ("year", data["movie_data"].get("year")),
                ("added", data["movie_data"].get("added")),
                ("category_id", data["movie_data"].get("category_id")),
                ("category_ids", data["movie_data"].get("category_ids")),
                ("container_extension", data["movie_data"].get("container_extension")),
                ("custom_sid", data["movie_data"].get("custom_sid")),
                ("direct_source", data["movie_data"].get("direct_source")),
            ]))
        ])

        # Retorna os dados ordenados
        return jsonify(ordered_data)
    except requests.exceptions.RequestException as e:
        # Retorna erro com detalhes
        return jsonify({"error": str(e)}), 500

# Para rodar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
