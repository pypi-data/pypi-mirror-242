import serial

class RS485Settings:
    rts_level_for_tx: bool
    rts_level_for_rx: bool
    loopback: bool
    delay_before_tx: float | None
    delay_before_rx: float | None
    def __init__(
        self,
        rts_level_for_tx: bool = ...,
        rts_level_for_rx: bool = ...,
        loopback: bool = ...,
        delay_before_tx: float | None = ...,
        delay_before_rx: float | None = ...,
    ) -> None: ...

class RS485(serial.Serial): ...
