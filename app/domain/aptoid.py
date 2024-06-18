from app.utils.requests import AbstractHttpRequests


class Aptoid:
    def __init__(self, request: AbstractHttpRequests):
        self.request = request
