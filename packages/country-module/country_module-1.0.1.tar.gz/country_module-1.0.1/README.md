# Country
#### Package published at: [PyPI](https://pypi.org/project/country_module/)
[![Downloads](https://static.pepy.tech/personalized-badge/country-module?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/country-module)

---

Python module for country codes with ISO codes.

#### Install:
```bash
pip install country_module
```

#### Use:
Create a python script, for example **`example.py`**:
```python
from country_module import country

print('Country code: {}'.format(country.see(country_name='India', option=0)))
print('ISO code: {}'.format(country.see(country_name='India', option=1)))
```
Save and run:
```bash
❯❯❯ py example.py
Country code: +91
ISO code: IN
```

---
#### Author: [Harshil Darji](https://github.com/harshildarji)
