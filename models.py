import json


class Movies:
    def __init__(self):
        try:
            with open("movies.json", "r") as f:
                self.movies = json.load(f)
        except FileNotFoundError:
            self.movies = []

    def all(self):
        return self.movies

    def get(self, id):
        return self.movies[id]

    def create(self, data):
        data.pop('csrf_token')
        self.movies.append(data)

    def delete(self, id):
        movie = self.get(id)
        if movie:
            self.movies.remove(movie)
            self.save_all()
            return True
        return False

    def save_all(self):
        with open("movies.json", "w") as f:
            json.dump(self.movies, f)

    def update(self, id, data):
        movie=self.get(id)
        if movie:
            index=self.movies.index(movie)
            self.movies[index]=data
            self.save_all()
            return True
        return False


movies = Movies()