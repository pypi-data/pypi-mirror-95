# bibimbap

bibimbap is a Python library for selenium based visual automation testing.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bibimbap.

```bash
pip install bibimbap
```

## Usage

```python
from bibimbap import ganjang, gochujang

print('spam')
g1 = ganjang.Ganjang('https://example.com/page_to_test','https://example.com/page_to_test2', example.com')
s = gochujang.Gochujang()
s.add_ganjang(g1)
s.set_webdriver("c:/geckodriver.exe")
s.set_window_size(380,5000)
s.set_xpath_to_element_to_capture("/html/body")
s.set_path_to_save("c:/bibimbap_test/")
s.capture_screens()

```
