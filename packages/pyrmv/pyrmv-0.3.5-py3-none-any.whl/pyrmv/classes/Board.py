from datetime import datetime
from pyrmv.classes.Message import Message

class LineArrival():

    def __init__(self, data, client, retrieve_stops: bool = True):
        self.journey = client.journey_detail(data["JourneyDetailRef"]["ref"])
        self.status = data["JourneyStatus"]
        self.messages = []
        if "Messages" in data:
            self.messages.extend(
                Message(message) for message in data["Messages"]["Message"]
            )
        self.name = data["name"]
        self.type = data["type"]
        self.stop_name = data["stop"]
        self.stop_id = data["stopid"]
        self.stop_id_ext = data["stopExtId"]
        if retrieve_stops:
            self.stop = client.stop_by_id(self.stop_id)
        else:
            self.stop = None
        self.stop = client.stop_by_id(self.stop_id)
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        if ("rtTime" in data) and ("rtDate" in data):
            self.time_real_time = datetime.strptime(data["rtTime"], "%H:%M:%S")
            self.date_real_time = datetime.strptime(data["rtDate"], "%Y-%m-%d")
        self.reachable = data["reachable"]
        self.origin = data["origin"]

    def __str__(self) -> str:
        return f"{self.name} coming from {self.origin} at {self.time.time()} {self.date.date()}"

class LineDeparture():

    def __init__(self, data, client, retrieve_stops: bool = True):
        self.journey = client.journey_detail(data["JourneyDetailRef"]["ref"])
        self.status = data["JourneyStatus"]
        self.messages = []
        if "Messages" in data:
            self.messages.extend(
                Message(message) for message in data["Messages"]["Message"]
            )
        self.name = data["name"]
        self.type = data["type"]
        self.stop_name = data["stop"]
        self.stop_id = data["stopid"]
        self.stop_id_ext = data["stopExtId"]
        if retrieve_stops:
            self.stop = client.stop_by_id(self.stop_id)
        else:
            self.stop = None
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        if ("rtTime" in data) and ("rtDate" in data):
            self.time_real_time = datetime.strptime(data["rtTime"], "%H:%M:%S")
            self.date_real_time = datetime.strptime(data["rtDate"], "%Y-%m-%d")
        self.reachable = data["reachable"]
        self.direction = data["direction"]
        self.direction_flag = data["directionFlag"]
        
    def __str__(self) -> str:
        return f"{self.name} heading {self.direction} at {self.time.time()} {self.date.date()}"
            
class BoardArrival(list):

    def __init__(self, data: dict, client, retrieve_stops: bool = True):
        super().__init__([])
        if "Arrival" not in data:
            return
        for line in data["Arrival"]:
            self.append(LineArrival(line, client, retrieve_stops=retrieve_stops))

    def __str__(self) -> str:
        lines = []
        for line in self:
            lines.append(str(line))
        return "Arrival board\n" + "\n".join(lines)

class BoardDeparture(list):

    def __init__(self, data: dict, client, retrieve_stops: bool = True):
        super().__init__([])
        if "Departure" not in data:
            return
        for line in data["Departure"]:
            self.append(LineDeparture(line, client, retrieve_stops=retrieve_stops))

    def __str__(self) -> str:
        lines = []
        for line in self:
            lines.append(str(line))
        return "Departure board\n" + "\n".join(lines)