# ytproofreading

A python module to use the proofreading support api of Yahoo! japan

## Requirement
* beautifulsoup4
* certifi
* chardet
* idna
* lxml
* requests
* soupsieve
* urllib3

## Installation

```bash
$ pip install ytproofreading
```

## Usage

```python
import ytproofreading

appid = "Client ID obtained from the Yahoo! japan Developer Network"

kousei = ytproofreading.Kousei(appid)

text = "遙か彼方に小形飛行機が見える。"

print(kousei.proofreading_support(text))
"""
[{'startpos': '0', 'length': '2', 'surface': '遙か', 'shitekiword': '●か', 'shitekiinfo': '表外漢字あり'},
{'startpos': '2', 'length': '2', 'surface': '彼方', 'shitekiword': '彼方（かなた）', 'shitekiinfo': '用字'},
{'startpos': '5', 'length': '5', 'surface': '小形飛行機', 'shitekiword': '小型飛行機', 'shitekiinfo': '誤変換'}]
"""

print(kousei.proofreading_support(text, 1))
"""
[{'startpos': '5', 'length': '5', 'surface': '小形飛行機', 'shitekiword': '小型飛行機', 'shitekiinfo': '誤変換'}]
"""

print(kousei.proofreading_support(text, 0, 1))
"""
[{'startpos': '0', 'length': '2', 'surface': '遙か', 'shitekiword': '●か', 'shitekiinfo': '表外漢字あり'},
{'startpos': '2', 'length': '2', 'surface': '彼方', 'shitekiword': '彼方（かなた）', 'shitekiinfo': '用字'}]
"""
```

## Note
For more information about arguments and errors, please refer to the following URL.
* arguments: https://developer.yahoo.co.jp/webapi/jlp/kousei/v1/kousei.html
* errors: https://developer.yahoo.co.jp/appendix/errors.html




## Author
* 6ast1an979
* email: 6ast1an979@gmail.com
* twitter: [@6ast1an979](https://twitter.com/6ast1an979)

## License
"ytproofreading" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
