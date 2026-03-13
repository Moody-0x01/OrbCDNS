from dataclasses import dataclass

@dataclass
class Response:
    status: int
    data: dict|str

    def make(self) -> tuple[dict, int]:
        return {
            "status": self.status,
            "data": self.data
        }, self.status

