"""Models the basic API data for a HomeSeer device."""

from homeassistant.const import CONF_PASSWORD
from .const import (
    REASON_DISCONNECTED,
    REASON_RECONNECTED,
)

from .const import (
    HS_UNIT_CELSIUS,
    HS_UNIT_FAHRENHEIT,
    HS_UNIT_LUX,
    HS_UNIT_PERCENTAGE,
    HS_UNIT_WATTS,
    HS_UNIT_KILOWATTS,
    HS_UNIT_AMPS,
    HS_UNIT_VOLTS,
)


class HomeSeerDevice:
    """Do not use this class directly, subclass it."""

    def __init__(self, raw, control_data, request):
        self._raw = raw
        self._control_data = control_data
        self._request = request
        self._value = self._raw["value"]
        self._on_value = None
        self._off_value = None
        self._lock_value = None
        self._unlock_value = None
        self._value_update_callback = None
        self._suppress_value_update_callback = False
        self._get_control_values()
        self._root = self

    @property
    def ref(self):
        return self._raw["ref"]

    @property
    def name(self):
        return self._raw["name"]

    @property
    def location(self):
        return self._raw["location"]

    @property
    def location2(self):
        return self._raw["location2"]

    @property
    def value(self):
        """Return int or float device value as appropriate."""
        if "." in str(self._value):
            return float(self._value)
        return int(self._value)

    @property
    def device_type_string(self):
        return self._raw["device_type_string"]

    @property
    def status(self):
        return self._raw["status"]

    @property
    def interface_name(self):
        return self._raw["interface_name"]

    @property
    def associated_devices(self):
        return self._raw["associated_devices"]

    @property
    def root(self):
        return self._root

    def _set_root(self, device):
        self._root = device

    def _get_control_values(self):
        for item in self._control_data:
            if item["ref"] == self.ref:
                control_pairs = item["ControlPairs"]
                for pair in control_pairs:
                    control_use = pair["ControlUse"]
                    control_label = pair["Label"]
                    if control_use == 1:
                        self._on_value = pair["ControlValue"]
                    elif control_use == 2:
                        self._off_value = pair["ControlValue"]
                    elif control_use == 18:
                        self._lock_value = pair["ControlValue"]
                    elif control_use == 19:
                        self._unlock_value = pair["ControlValue"]
                    elif control_label == "Lock":
                        self._lock_value = pair["ControlValue"]
                    elif control_label == "Unlock":
                        self._unlock_value = pair["ControlValue"]
                break

    def register_update_callback(self, callback, suppress_on_reconnect=False):
        self._suppress_value_update_callback = suppress_on_reconnect
        self._value_update_callback = callback

    def update_value(self, value, reason=None):
        if value is not None:
            self._value = value

        if reason == REASON_RECONNECTED and self._suppress_value_update_callback:
            return
        elif reason == REASON_DISCONNECTED and self._suppress_value_update_callback:
            return
        elif self._value_update_callback is not None:
            self._value_update_callback()


class GenericDevice(HomeSeerDevice):
    @property
    def is_on(self):
        return self.value > self._off_value

    async def on(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def off(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class GenericSwitch(HomeSeerDevice):
    @property
    def is_on(self):
        return self.value > self._off_value

    async def on(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def off(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class GenericSwitchMultilevel(GenericSwitch):
    @property
    def dim_percent(self):
        return self.value / self._on_value

    async def dim(self, percent: int):
        value = int(self._on_value * (percent / 100))

        params = {"request": "controldevicebyvalue", "ref": self.ref, "value": value}

        await self._request("get", params=params)


class GenericSensor(HomeSeerDevice):
    pass


class GenericMultiLevelSensor(GenericSensor):
    _unit_of_measurement = None

    def parse_uom(self):
        if "Lux" in self.status:
            return HS_UNIT_LUX
        if "%" in self.status:
            return HS_UNIT_PERCENTAGE
        if "F" in self.status:
            return HS_UNIT_FAHRENHEIT
        if "C" in self.status:
            return HS_UNIT_CELSIUS
        if "kW" in self.status:
            return HS_UNIT_KILOWATTS
        if "W" in self.status:
            return HS_UNIT_WATTS
        if "A" in self.status:
            return HS_UNIT_AMPS
        if "V" in self.status:
            return HS_UNIT_VOLTS

        return None

    @property
    def UnitOfMeasurement(self):
        if self._unit_of_measurement == None:
            self._unit_of_measurement = self.parse_uom()
        return self._unit_of_measurement


class GenericBatterySensor(GenericMultiLevelSensor):
    pass


class GenericHumiditySensor(GenericMultiLevelSensor):
    pass


class GenericLuminanceSensor(GenericMultiLevelSensor):
    pass


class GenericFanSensor(GenericMultiLevelSensor):
    pass


class GenericOperatingStateSensor(GenericMultiLevelSensor):
    pass


class GenericPowerSensor(GenericMultiLevelSensor):
    pass


class GenericBinarySensor(HomeSeerDevice):
    pass


class GenericDoorLock(HomeSeerDevice):
    pass


class GenericCover(HomeSeerDevice):
    pass


class GenericEvent(HomeSeerDevice):
    pass