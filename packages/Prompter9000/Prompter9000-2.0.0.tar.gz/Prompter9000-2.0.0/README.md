## Prompter9000
Quick &amp; easy way to edit dictionaries and create counters. Console & programmatic usages are supported.

### Programatic
Edit a dictionary:
```
from Prompter9000.PyEdit import *
params = {"NAME":'My', "PHONE":'123-456', "EMAIL":'a.Geekbo@zbobo.com'}
EditDict.edit(params)
```

Create a click-counter:
```
from Prompter9000.PyCount import *
params = {'Hits': '0', 'Miss': '0', 'Other': '10'}
Counter.edit(params)
```
*GUI*: Dictionary results will be returned ONLY IF the data was changed. Otherwise an empty dictionary will be returned.

May also be used from the C.L.I:

### Console

Dynamically edit a dictionary:
```
python PyEdit.py "{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com'}"
{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com', '__btn_ok': True}
```

Dynamic click-to-update counters:
```
python PyCount.py "{'Hits': '0', 'Miss': '0', 'Other': '10'}"
{'Hits': '12', 'Miss': '10', 'Other': '44', '__btn_ok': True}
```

*CLI*: The **__btn_ok** will be either **True** when user-selected, else **False**.

### PyPi

Now available on [PyPi](https://pypi.org/project/Prompter9000/)
