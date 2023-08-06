# cyclone ai-platform python framework
thanks ibm max framework

## Dependencies
* [flask-restx](https://pypi.org/project/flask-restx/0.1.1/)
* [flask-cors](https://pypi.org/project/Flask-Cors/)

## Installation

```shell script
pip install -U cyclonefw
```

## Demo

```python

#!/usr/bin/env python3

from cyclonefw import MAXApp

app = MAXApp()
app.run()


```
## 注意事项
随着开源软件的演进，框架依赖的flask_restplus模块已经停止维护，因此随着基础框架IBM maxfw一起，cyclonefw框架以及本示例已经将flask_restplus替换为[flask_restx](https://github.com/python-restx/flask-restx)。

`flask_restx是flask的扩展，提供对应用API的描述/可视化展示/调测功能。`

**开发者如果需要使用flask_restplus中的模块，请使用flask_restx**。否则，可能影响应用的API可视化展示与调测功能。

