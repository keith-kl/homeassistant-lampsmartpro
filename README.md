# homeassistant-lampsmartpro
implementation of lampsmartpro in home assistant custom integration

This integration is push-only, because it is not possible to get state of the light. On startup the state is `off`.

## Installation

Copy this folder to `<config_dir>/custom_components/homeassistant-lampsmartpro/`.

Add the following entry in your `configuration.yaml`:

```yaml
light:
  - platform: lampsmartpro
    name: NAME_HERE
```

The integration will try to pair the BLE light when it is turned on. Keep turning on and off the light from the frontend until the light goes off and on and this indicates that the pairing is completed.

## Dependencies
This is the list of packages providing the files required. Be aware that package names usually do vary across different linux distributions.

Debian / Ubuntu

- libbluetooth-dev
- lampify

This custom component contains a wrapper shared libary from a CLI C program Lampify from another author (https://github.com/MasterDevX/lampify)

## Compatibility
This was tested with a BLE ceiling light from Taobao which uses the below iOS/Andriod app to control. 

- Developed by [XuRenNan](https://play.google.com/store/apps/developer?id=XuRenNan)
  - [LampSmart Pro](https://play.google.com/store/apps/details?id=com.jingyuan.lamp)
  
## Features
The project offers the following functionality in home assistant similar to the original LampSmartPro app:
- Turning the lamp on / off
- Controlling lamp brightness
- Controlling lamp temperature

