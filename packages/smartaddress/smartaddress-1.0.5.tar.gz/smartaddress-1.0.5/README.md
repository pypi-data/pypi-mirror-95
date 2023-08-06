# 收货地址智能解析(PHP版和PYTHON版)
[PHP版](https://github.com/pupuk/address)来自github开源项目，PYTHON版是对其的改写

本项目包含2个功能
- 把字符串解析成姓名、收货电话、邮编、身份证号、收货地址
- 把收货地址解析成省、市、区县、街道地址

特色是：***简单易用***

该项目依然采用的是，统计特征分析，然后以最大的概率来匹配，得出大概率的解。因此只能解析中文的收货信息，不能保证100%解析成功，但是从生产环境的使用情况来看，解析成功率保持在96%以上，就算是百度基于人工智能的地址识别，经我实测，也是有一定的不能识别的情况。

**由于上个项目[address-smart-parse](https://github.com/pupuk/address-smart-parse)，地址解析的过程，是对照的数据库里面的地址库，有很多朋友看到相关代码的时候，不知如何改写，为了方便大家，写了一个纯PHP的，开箱即用。纯PHP版本采用遍历搜索，相对于DB的查询，有略微的性能损失，但解析一个地址仍然不到10ms，PHP开启Opcache更是解析1个地址不到5ms。**

### 使用
so easy；
```php
require 'address.php';
$string = '深圳市龙华区龙华街道1980科技文化产业园3栋317    张三    13800138000 518000 120113196808214821';
$r = Address::smart($string);
print_r($r);
```
```python
from pprint import pprint
from address import Address
addr = Address()
string = '深圳市龙华区龙华街道1980科技文化产业园3栋317    张三    13800138000 518000 120113196808214821'
r = addr.smart(string)
pprint(r)
```
结果为：
![image](https://user-images.githubusercontent.com/7934974/83218657-f0804980-a1a0-11ea-9c0e-e735ef35749e.png)
![image](./example.png)

`demo.php/demo.py`里面有使用示例，如果字符串里面不包含电话，姓名，身份证等，只需要解析地址，可以用：
```php
 Address::smart($string, $user = false);
```
```python
 addr.smart(string, user=False)
```
