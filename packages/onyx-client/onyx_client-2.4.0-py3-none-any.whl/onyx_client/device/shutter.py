"""Shutter class."""
from onyx_client.data.boolean_value import BooleanValue
from onyx_client.data.device_mode import DeviceMode
from onyx_client.data.numeric_value import NumericValue
from onyx_client.device.device import Device
from onyx_client.enum.device_type import DeviceType


# not mapped properties:
# - auto_calibration
# - heart_beat_enabled
# - sun_guard_lower_action
# - sun_guard_lower_angle
# - sun_guard_lower_position
# - sun_guard_lower_threshold
# - sun_guard_upper_action
# - sun_guard_upper_angle
# - sun_guard_upper_position
# - sun_guard_upper_threshold
# - system_state
# - wind_guard_enabled
# - wind_peak_threshold
class Shutter(Device):
    """A ONYX controlled shutter device."""

    def __init__(
        self,
        identifier: str,
        name: str,
        device_type: DeviceType,
        device_mode: DeviceMode,
        actions: list,
        target_position: NumericValue = None,
        target_angle: NumericValue = None,
        actual_angle: NumericValue = None,
        actual_position: NumericValue = None,
        drivetime_down: NumericValue = None,
        drivetime_up: NumericValue = None,
        rotationtime: NumericValue = None,
        switch_button_direction: BooleanValue = None,
        switch_drive_direction: BooleanValue = None,
    ):
        """Initialize the shutter device."""
        super(Shutter, self).__init__(
            identifier, name, device_type, device_mode, actions
        )
        self.target_position = target_position
        self.target_angle = target_angle
        self.actual_angle = actual_angle
        self.actual_position = actual_position
        self.drivetime_down = drivetime_down
        self.drivetime_up = drivetime_up
        self.rotationtime = rotationtime
        self.switch_button_direction = switch_button_direction
        self.switch_drive_direction = switch_drive_direction

    def update_with(self, update):
        super().update_with(update)

        self.target_position = (
            self.target_position
            if update.target_position is None
            else update.target_position
        )
        self.target_angle = (
            self.target_angle if update.target_angle is None else update.target_angle
        )
        self.actual_angle = (
            self.actual_angle if update.actual_angle is None else update.actual_angle
        )
        self.actual_position = (
            self.actual_position
            if update.actual_position is None
            else update.actual_position
        )
        self.drivetime_down = (
            self.drivetime_down
            if update.drivetime_down is None
            else update.drivetime_down
        )
        self.drivetime_up = (
            self.drivetime_up if update.drivetime_up is None else update.drivetime_up
        )
        self.rotationtime = (
            self.rotationtime if update.rotationtime is None else update.rotationtime
        )
        self.switch_button_direction = (
            self.switch_button_direction
            if update.switch_button_direction is None
            else update.switch_button_direction
        )
        self.switch_drive_direction = (
            self.switch_drive_direction
            if update.switch_drive_direction is None
            else update.switch_drive_direction
        )

    @staticmethod
    def keys() -> list:
        return [
            "target_position",
            "target_angle",
            "actual_angle",
            "actual_position",
            "drivetime_down",
            "drivetime_up",
            "rotationtime",
            "switch_button_direction",
            "switch_drive_direction",
        ]
