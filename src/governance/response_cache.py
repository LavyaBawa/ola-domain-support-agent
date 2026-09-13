class ResponseCache:
    def __init__(self):
        self.cache = {}

    def normalize(self, query: str) -> str:
        return " ".join(query.lower().strip().split())

    def get(self, query: str):
        key = self.normalize(query)

        if key in self.cache:
            return self.cache[key]

        return None

    def set(self, query: str, response):
        key = self.normalize(query)
        self.cache[key] = response
