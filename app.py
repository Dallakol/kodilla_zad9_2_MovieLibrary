from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from wtforms.fields.core import SelectField
from forms import MovieForm
from models import movies


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/movie_library/", methods=["GET", "POST"])
def movies_list():
    form = MovieForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            movies.create(form.data)
            movies.save_all()
        return redirect(url_for("movies_list"))

    return render_template("form.html", form=form, movies=movies.all(), error=error)


@app.route("/movie_library/<int:movie_id>/", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = movies.get(movie_id)
    form = MovieForm(data=movie)

    if request.method == "POST":
        if form.validate_on_submit():
            movies.update(movie_id, form.data)
        return redirect(url_for("movies_list"))
    return render_template("movie_details.html", form=form, movie_id=movie_id)


@app.route("/api/v1/movie_library/", methods=["POST"])
def create_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    movie = {
            'Title': request.json['Title'],
            'Description': request.json['Description'],
            'Rating': request.json.get('Rating'),
            'Time': request.json.get('Time')
    }
    movies.create(movie)
    return jsonify({'movie': movie}), 201


@app.route("/api/v1/movie_library/", methods=["GET"])
def movie_library_api_v1():
    return jsonify(movies.all())


@app.route("/api/v1/movie_library/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    return jsonify({"movie": movie})


@app.route("/api/v1/movie_library/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    result = movies.delete(movie_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/movie_library/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'Title' in data and not isinstance(data.get('Title'), str),
        'Description' in data and not isinstance(data.get('Description'), str),
        'Rating' in data and not isinstance(data.get('Rating'), SelectField),
        'Time' in data and not isinstance(data.get('Time'), str)
    ]):
        abort(400)
    movie = {
        'id': movie_id,
        'Title': data.get('Title', movie['Title']),
        'Description': data.get('Description', movie['Description']),
        'Rating': data.get('Rating', movie['Rating']),
        'Time': data.get('Time', movie['Time'])
    }
    movies.update(movie_id, movie)
    return jsonify({'movie': movie})


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found', 'status_code': 404}), 404
    )


@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad request', 'status_code': 400}), 400
    )


if __name__ == "__main__":
    app.run(debug=True)