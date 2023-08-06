A extractor to extract product id from an provided url of specific platforms.


# Installation
```
pip install product-id-extractor-yimian
```


# Examples

```python
from product_id_extractor import Extractor

# Initialize Extractor Object
# Leave platform parameter None to use auto detection
example = Extractor("https://item.taobao.com/item.htm?spm=a230r.1.14.141.34655b0c4rO8sl&id=637790875524&ns=1&abbucket=16#detail",platform=None)

# specify platform if needed by passing it to Extractor object
example.platform = 'taobao'

# call Extractor.extract() function to get product_id
example.extract()

print(example) # 637790875524
```
 
# Notes
1. Only support URL of items from following platforms:
    1. taobao
    2. tmall
    3. jd
    4. suning
    5. amazon(.co.uk)