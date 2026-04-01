class GameTimer():
    def __init__(self, start_time: int):
        self.start_time = start_time
        self.time = 0
        self.is_stopped = False
        self.stop_time = 0

    def pause(self, is_paused: bool):
        self.is_stopped = is_paused

    def get_time(self) -> int:
        return self.time

    def update(self, time: int):
        if self.is_stopped:
            self.stop_time = time - (self.time + self.start_time)
        else:
            self.time = time - self.start_time - self.stop_time

    def reset_to(self, time: int):
        self.start_time = time
        self.time = 0
        self.stop_time = 0

    @staticmethod
    def convert_to_str(time: int) -> str:
        seconds = (time // 1000) % 60
        minutes = time // 60000
        return f"{minutes}:{seconds:0>2}"
