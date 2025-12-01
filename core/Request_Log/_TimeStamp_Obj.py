from dataclasses import dataclass, field, asdict
import time

@dataclass
class TimeStamp:
    time_stamp: int = field(default_factory=lambda: time.time_ns())
    monotonic: int = field(default_factory=lambda: time.monotonic_ns())

    def record(self, update_time: bool = True, update_monotonic: bool = True) -> None:
        """
        Record the current time
        """
        if update_time:
            self.time_stamp = time.time_ns()
        if update_monotonic:
            self.monotonic = time.monotonic_ns()
    
    def __add__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp + other.time_stamp, self.monotonic + other.monotonic)
    
    def __radd__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp + other.time_stamp, self.monotonic + other.monotonic)
    
    def __iadd__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp += other.time_stamp
        self.monotonic += other.monotonic
        return self
    
    def __sub__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp - other.time_stamp, self.monotonic - other.monotonic)
    
    def __rsub__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp - self.time_stamp, other.monotonic - self.monotonic)
    
    def __isub__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp -= other.time_stamp
        self.monotonic -= other.monotonic
        return self
    
    def __mul__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp * other.time_stamp, self.monotonic * other.monotonic)
    
    def __rmul__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp * self.time_stamp, other.monotonic * self.monotonic)
    
    def __imul__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp *= other.time_stamp
        self.monotonic *= other.monotonic
        return self

    def __truediv__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp / other.time_stamp, self.monotonic / other.monotonic)
    
    def __floordiv__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp // other.time_stamp, self.monotonic // other.monotonic)
    
    def __rtruediv__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp / self.time_stamp, other.monotonic / self.monotonic)
    
    def __rfloordiv__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp // self.time_stamp, other.monotonic // self.monotonic)
    
    def __itruediv__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp /= other.time_stamp
        self.monotonic /= other.monotonic
        return self
    
    def __ifloordiv__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp //= other.time_stamp
        self.monotonic //= other.monotonic
        return self
    
    def __mod__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp % other.time_stamp, self.monotonic % other.monotonic)
    
    def __rmod__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp % self.time_stamp, other.monotonic % self.monotonic)
    
    def __imod__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp %= other.time_stamp
        self.monotonic %= other.monotonic
        return self
    
    def __pow__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(self.time_stamp ** other.time_stamp, self.monotonic ** other.monotonic)
    
    def __rpow__(self, other: "TimeStamp") -> "TimeStamp":
        return TimeStamp(other.time_stamp ** self.time_stamp, other.monotonic ** self.monotonic)

    def __ipow__(self, other: "TimeStamp") -> "TimeStamp":
        self.time_stamp **= other.time_stamp
        self.monotonic **= other.monotonic
        return self
    
    def __neg__(self) -> "TimeStamp":
        return TimeStamp(-self.time_stamp, -self.monotonic)
    
    def __pos__(self) -> "TimeStamp":
        return TimeStamp(+self.time_stamp, +self.monotonic)
    
    def __abs__(self) -> "TimeStamp":
        return TimeStamp(abs(self.time_stamp), abs(self.monotonic))
    
    def __eq__(self, other: "TimeStamp") -> bool:
        return self.time_stamp == other.time_stamp and self.monotonic == other.monotonic
    
    def __ne__(self, other: "TimeStamp") -> bool:
        return self.time_stamp != other.time_stamp or self.monotonic != other.monotonic
    
    def __hash__(self) -> int:
        return hash((self.time_stamp, self.monotonic))
    
    def __repr__(self) -> str:
        return f"TimeStamp({self.time_stamp}, {self.monotonic})"
    
    @property
    def as_dict(self) -> dict:
        return asdict(self)