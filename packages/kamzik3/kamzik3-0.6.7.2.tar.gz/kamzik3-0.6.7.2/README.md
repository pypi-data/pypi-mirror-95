Kamzik3 is a modular and lightweight experiment control framework written in Python3.
It is focused on minimalist yet unified way to control and orchestrate wide range of devices used in experimental setup.
It uses ZeroMQ to exchange messages between server and clients. Qt5 is used for graphical interface. 
Kamzik3 provides tools for logging, visualizing and evaluation of experimental data. Users can create and execute custom macros and scans using built in macro-server. 
Experimental setup is defined in one configuration file written in YAML, human-readable data serialization standard.
Framework can be downloaded from PyPI (https://pypi.org/project/kamzik3/).

Requirements
------------

  * Python: 3.7 and higher

  **Python Modules: Backend**

  * numpy
  * pyzmq
  * pint
  * bidict
  * pyqt5
  * pyqtgraph
  * pyserial
  * oyaml
  * psutil
  * natsort
  * reportlab
  * pandas

  **Python Modules: Optional**

  * pytango
  * pyopengl
  * sysutil
  * pydaqmx
  * pypiwin32
  * rocketchat-API

Example experiment
------------

Copy content of example folder into writable directory of Your choice.<br>
Choose that directory as a working directory.

Start server:
  * python server.py

Start client:
  * python client.py

Optionally You can start listener:
  * python listener.py