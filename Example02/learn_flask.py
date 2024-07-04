import json
import logging
from flask import Flask, request, jsonify


def init_log():
    # 配置基本的日志记录设置，设置打印的格式和等级，打印到控制台的日志
    logging.basicConfig(
        # 定义日志消息的格式，包括时间戳、文件名、日志级别和日志消息
        format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',

        # 定义时间戳的格式，例子：Wed, 04 Jul 2024 14:55:26
        datefmt='%a, %d %b %Y %H:%M:%S',

        # 设置日志记录的最低级别为 DEBUG，意味着记录 DEBUG 及以上级别的所有日志消息
        level=logging.INFO
    )
    # 设置输出到文件和编码
    file_handler = logging.FileHandler("ocr.log", mode="a", encoding="utf-8")
    # 设置输出等级
    file_handler.setLevel(logging.INFO)
    # 设置输出到文件的日志格式
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s'))
    # 添加到日志对象
    logging.getLogger().addHandler(file_handler)


init_log()

# name 是 Python 中的特殊变量，如果文件作为主程序执行那么 __name__ 的值为 __main__，如果文件被其他文件引入那么 __name__ 的值为其它模块文件的名称也就是模块名称
# app = Flask(__name__)：创建一个 Flask 实例，Flask 类的构造函数需要传入一个参数，这个参数通常是 Python 的特殊变量 __name__，这个参数的作用是确定 Flask 应用的根目录，以便找到相对于应用的资源文件位置
app = Flask(__name__)


# @app.route("/learn/hello"): 使用 app.route() 装饰器将 URL 路由到 hello_world() 函数
@app.route("/learn/hello")
def hello_world():
    return "Hello, World!"


# @app.route("/learn/path/<string:name>"): 使用 app.route() 装饰器将 URL 路由到 learn_path() 函数
# <string:name>：表示 URL 中的 name 参数是一个字符串类型，可以通过 name 参数获取 URL 中的参数值
# 默认数据类型是字符串，如果想要指定为其它类型需要自己去更改例如：<int:name>，所以说如果是字符串可以省略不写 string
# 这种传参是将参数放在 URL 中，例如：http://localhost:8888/learn/path/abc
@app.route("/learn/path/<name>")
def learn_path(name):
    return name;


# 通过 URL 传参，例如：http://localhost:8888/learn/query?name=abc
# 通过 request.args.get() 获取 URL 中的参数值
# request.args.get("name")：获取 URL 中的 name 参数值
# request.args.get("age")：获取 URL 中的 age 参数值
# request.args.get("name", "default")：获取 URL 中的 name 参数值，如果没有获取到则返回默认值 default
@app.route("/learn/query", methods=["GET"])
def learn_query():
    name = request.args.get("name")
    logging.info("name: %s", name)
    return "SUCCESS", 200


# 通过 POST 方式获取参数，参数是 json 字符串
@app.route("/learn/post", methods=["POST"])
def learn_post():
    # request.data：获取请求的数据，数据是 json 字符串
    data = request.data
    logging.info("data: %s", data)

    # data = json.loads(data)：将 json 字符串转换为 json 对象
    data = json.loads(data)

    age = data['age']
    name = data['name']

    logging.info("name: %s, age: %s", name, age)

    # 一般开发接口都是返回 json 数据，所以需要将数据转换为 json 字符串
    return jsonify(data), 200


if __name__ == '__main__':
    init_log()
    # app.run()：启动 Flask 的开发 Web 服务器，Flask 会自动检测代码的变化并重启服务器
    # host='0.0.0.0': 使服务器公开可用，可以通过局域网 IP 访问
    # debug=True: 启用调试模式，服务器会在代码修改后自动重启
    # port=8888: 设置服务器端口为 8888
    app.run(host='0.0.0.0', debug=True, port=8888)
