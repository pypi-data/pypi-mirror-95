# fellow-py

Huge thanks to [emlove](https://github.com/emlove) for paving the way on using Bleak in a library used in implementing a [custom bluetooth component](https://github.com/emlove/pyzerproc) in HA. Any similarities my library may take to hers are not deliberate copying and pasting, but her library was an awesome example to follow and so my patterns were likely heavily influenced by her work.

Also huge thanks to [u/bobobalooga](https://www.reddit.com/user/bobobalooga/) on Reddit. They posted a _fantastic_ breakdown of their discovery of how the Fellow kettle app talked to the kettle over BLE which enabled me to implement the logic in Python. Definitely standing on their shoulders here.

fellow-py is a library for controlling Fellow bluetooth devices (of which I am only aware of one at this time). So, more precisely speaking, it is a library for controlling their Stagg EKG+ Kettle.

This library currently supports connecting, turning on, setting the target temperature, turning off, and disconnecting. The library automatically subscribes to the 2a80 characteristic of the 1820 service on the kettle. The handler for the notifications the device sends to the connecting device will set the current and target temperature properties on the kettle object for the user to observe. The kettle object also implements a temperature graph that helps determine an average warming rate of the kettle. The purpose of this is to be able to identify if there's not enough water in the kettle. The library currently doesn't support device discovery, but it easily could in the near future. For now it simply implements a discover module that allows for obtaining a kettle given a mac address so as to instantiate the StaggEKGPlusKettle class.

## Usage
```python
import asyncio
import fellow

async def main()
    kettle = fellow.StaggEKGPlusKettle("MA:CA:DD:RE:SS:01")

    try:
        await kettle.connect()
        await kettle.turn_on()

        await asyncio.sleep(5)

        print(kettle.current_temperature, kettle.target_temperature)

        await kettle.set_target_temperature(206)

        await asyncio.sleep(2)

        print(kettle.current_temperature, kettle.target_temperature)

        await kettle.turn_off()
        await kettle.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

Tests coming soon :)
