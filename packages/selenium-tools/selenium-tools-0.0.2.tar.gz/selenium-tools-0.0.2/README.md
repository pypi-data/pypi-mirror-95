Selenium-Tools provides the following tools for use with [Selenium](https://selenium-python.readthedocs.io/):

1. Send/receive `datetime.datetime` objects from web forms.
2. Drag range sliders to specified values.

## Installation

```
$ pip install selenium-tools
```

## Quickstart

First, clone an example file from the Selenium-Tools repo.

```bash
$ curl https://raw.githubusercontent.com/dsbowen/selenium-tools/master/form.html --output form.html
```

Let's send the current date and time to all input in the form.

```python
from selenium_tools import get_datetime, send_datetime

from selenium.webdriver import Chrome

from datetime import datetime

driver = Chrome()
driver.get('data:text/html,'+open('form.html').read())

datetime_ = datetime.utcnow()

css_selectors = (
    'input[type=date]',
    'input[type=datetime-local]',
    'input[type=month]',
    'input[type=time]',
    'input[type=week]'
)
for selector in css_selectors:
    input_ = driver.find_element_by_css_selector(selector)
    send_datetime(input_, datetime_)
    print(get_datetime(
        input_.get_attribute('type'), 
        input_.get_property('value')
    ))
```

You'll see the form filled in in your selenium browser and receive the following output in your terminal:

```
2020-06-30 00:00:00
2020-06-30 15:47:00
2020-06-01 00:00:00
1900-01-01 15:47:00
2020-01-01 00:00:00
```

We can also drag the range slider as follows:

```python
from selenium_tools import drag_range

range_ = driver.find_element_by_css_selector('input[type=range]')
drag_range(driver, range_, 80)
range_.get_property('value')
```

Out:

```
'80'
```

## Citation

```
@software{bowen2020selenium-tools,
  author = {Dillon Bowen},
  title = {Selenium-Tools},
  url = {https://dsbowen.github.io/selenium-tools/},
  date = {2020-06-29},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/selenium-tools/blob/master/LICENSE).