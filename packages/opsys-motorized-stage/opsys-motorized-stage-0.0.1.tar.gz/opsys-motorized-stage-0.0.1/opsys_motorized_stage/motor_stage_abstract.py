from abc import ABC, abstractmethod


class MotorStageAbstract(ABC):
    @abstractmethod
    def connect_stage(self):
        pass

    @abstractmethod
    def disconnect_stage(self):
        pass

    @abstractmethod
    def set_stage_home(self):
        pass

    @abstractmethod
    def stop_movement(self):
        pass

    @abstractmethod
    def get_position(self, units: str):
        pass

    @abstractmethod
    def move_abs(self, position: float, units: str):
        pass

    @abstractmethod
    def move_rel(self, distance: float, units: str):
        pass
