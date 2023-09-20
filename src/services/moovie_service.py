from repositories.moovie_repository import moovie_repository as default_moovie_repository


class MoovieService:
    def __init__(self, moovie_repository=default_moovie_repository):
        self.moovie_repository = moovie_repository

    def get_moovie_by_id(self, id):
        return self.moovie_repository.get_moovie_by_id(id)

    def get_moovies(self):
        return self.moovie_repository.get_moovies()


moovie_service = MoovieService()
