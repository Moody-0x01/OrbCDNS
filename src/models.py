from dataclasses import dataclass

@dataclass
class Response:
    status: int
    data: dict|str
    def digest(self) -> tuple: return self.data, self.status

def unwrap_response(re):
    if isinstance(re, Response): return re.digest()
    return re

def makeResponse(code: int = 200, data: dict|str = "No data") -> Response: return Response(code, data)
