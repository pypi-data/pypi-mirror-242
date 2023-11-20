from .const import UNITS_DE, UNITS_EN, ChannelMode, ChannelType, Languages


class Channel:
    """Class to display a data point"""

    def __init__(
        self,
        mode: ChannelType | None,
        type: ChannelMode,
        index: int,
        value: float,
        unit: str,
    ) -> None:
        """Initialize and parse json to get properties."""
        self.mode = mode
        self.type = type
        self.index = index
        self.value = value
        self.unit = unit

    def get_unit(self, language: Languages = Languages.EN) -> str:
        """Get the unit of the channel."""
        if language == Languages.EN:
            return UNITS_EN.get(self.unit, "Unknown")
        else:
            return UNITS_DE.get(self.unit, "Unknown")

    def __eq__(self, other) -> bool:
        return (
            self.mode == other.mode
            and self.type == other.type
            and self.index == other.index
            and self.value == other.value
            and self.unit == other.unit
        )

    def __repr__(self) -> str:
        return f"Channel {self.index}: Type: {self.type}, Mode: {self.mode}, Value: {self.value} {self.get_unit()}"
