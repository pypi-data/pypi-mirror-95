# macops
It is a python module which can help you to change the current mac address of a certain interface, generate a mac address, get the current mac address and also reset the current mac address to the original one.
Developed by Shounak Kulkarni (c) 2021

_Not supported in Python 2.x_

# Installation
```bash
pip install macops
```

# Functions

**Get Current Mac**

`get_current_mac`: As it's name describes itself, this function will **get** the current mac address.

How this function should be used:-
```python
import MacOps
current_mac = MacOps.get_current_mac()
print(current_mac)
```
**Generate Mac**

`generate_mac`: This function generates a **random** mac address.

How this function should be used:-
```python
import MacOps
new_mac = MacOps.generate_mac()
print(new_mac)
```
**Change Mac**

`change_mac`: This will **change** the mac address to the generated mac address.
 _Note: This function can only be performed in unix/linux systems_.

How this function should be used:-
```python
import MacOps
MacOps.change_mac()
```
_No parameter is required as it takes input fom the user and the new mac address is automatically generated._

**Reset to Original Mac**

`reset_original_mac`: This function will **reset** the permanent mac address. 
 _Note: This function can only be performed in unix/linux systems_.

How this function should be used:-
```python
import MacOps
MacOps.reset_original_mac()
```
# License 
Github repository: [macops:Github](https://github.com/ShounakKulkarni/MacOps/)

You can find the license here: [License:macops](https://github.com/ShounakKulkarni/MacOps/blob/main/LICENSE)