from datetime import datetime


class Shipment:
    def __init__(self, size: str, provider: str, date: str):
        self.size = size
        self.provider = provider
        self.date = datetime.strptime(date, "%Y-%m-%d")
