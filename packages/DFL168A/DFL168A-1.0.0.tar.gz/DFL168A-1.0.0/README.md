# DFL168A Python Module

Simply import DFL168A module and use function to get motor data.  Don't need to know OBD2 and J1939/J1708/J1587 protocol, don't need to read DFL168A data sheet, just need to know DFL168A pinout, so easily get vehicle parameters values in real time.

You can get User Manual from
http://www.dafulaielectronics.com/DFL168A_python.pdf 

## Getting Started

Please go to http://www.dafulaielectronics.com/DFL168A_python.pdf and read "How to use Library?" section


### Prerequisites

Python version should be 3.6 or higher. You should install pyserial version 3.5 or higher 

```
pip install pyserial
```
If it does not work, you can try command below:
```
py -m pip install pyserial

```
### Installing

You just use command below

```
pip install DFL168A
```

or 

```
py -m pip install DFL168A
```


## Running the tests

There are lots of example in examples folder.

Please download examples folder from 

https://github.com/Dafulai/DFL168A_python/examples

You just modify your serial port Name to your actual Serial port such as "COM1" (or "/dev/ttyS0" ) instead of default "COM4". You can run it directly.



## Authors

* **Jack Xia** 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


