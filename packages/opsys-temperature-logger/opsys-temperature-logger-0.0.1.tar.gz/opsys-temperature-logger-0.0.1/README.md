# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is temperature logger implementation for temperature sensors device

### How do I get set up? ###

* pip install opsys-temperature-logger

### Unit Testing

* python -m unittest -v

### Reference Links

* Installation Software: 'R:\Lidar\Dima\Software\picolog-setup-6.2.7.exe'

### Usage Example
```
### PicoLog data logger

from opsys_temperature_logger.temperature_logger import TemperatureLogger

temperature_logger = TemperatureLogger()

temperature_logger.connect()
temperature_logger.set_channel(channel_number=1)
print(temperature_logger.read_temperature(channel=1))
temperature_logger.close_connection()
```