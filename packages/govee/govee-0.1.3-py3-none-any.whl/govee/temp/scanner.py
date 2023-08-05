from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from govee.temp.advertisement import process_advertisement


class GoveeScanner:
    def __init__(self):
        self._callbacks = []
        self._scanner = None

    def register(self, callback):
        self._callbacks.append(callback)

    def unregister(self, callback):
        self._callbacks.remove(callback)

    async def start(self):
        def _callback(device: BLEDevice, adv: AdvertisementData):
            adv = process_advertisement(device, adv)
            if adv:
                for callback in self._callbacks:
                    callback(adv.dict())
        self._scanner = BleakScanner()
        self._scanner.register_detection_callback(_callback)
        await self._scanner.start()

    async def stop(self):
        await self._scanner.stop()
