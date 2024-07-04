import json
import logging
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR


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


# name 是 Python 中的特殊变量，如果文件作为主程序执行那么 __name__ 的值为 __main__，如果文件被其他文件引入那么 __name__ 的值为其它模块文件的名称也就是模块名称
# app = Flask(__name__)：创建一个 Flask 实例，Flask 类的构造函数需要传入一个参数，这个参数通常是 Python 的特殊变量 __name__，这个参数的作用是确定 Flask 应用的根目录，以便找到相对于应用的资源文件位置
app = Flask(__name__)

# 创建一个 PaddleOCR 对象
# usr_angle_cls=True：开启文本方向检测识别器
# use_gpu=False：不使用 GPU，通过 CPU 进行计算
# PaddleOCR只需要初始化一次，会将模型加载到内存中，后续的识别操作都会使用这个模型
ocr = PaddleOCR(usr_angle_cls=True, use_gpu=False)


# 通过 POST 方法识别图片，传入参数为图片的 URL路径
@app.route("/ocr", methods=['POST'])
def learn_post():
    try:
        # 获取请求的数据
        data = json.loads(request.data)

        # 验证 imgPath 参数
        if 'imgPath' not in data:
            return jsonify({"code": -1, "msg": "Missing imgPath parameter"}), 400

        img_path = data['imgPath']
        logging.info("ocr imgPath : %s", img_path)

        # 调用 OCR 识别
        ocr_result = ocr.ocr(img_path, cls=True)

        # 返回识别结果
        return jsonify({"code": 0, "msg": "ok", "data": ocr_result}), 200
    except json.JSONDecodeError:
        logging.error("Invalid JSON format")
        return jsonify({"code": -1, "msg": "Invalid JSON format"}), 400
    except Exception as e:
        logging.error("ocr error : %s", str(e))
        return jsonify({"code": -1, "msg": str(e)}), 500


if __name__ == '__main__':
    init_log()

    # 设置可以返回中文字符
    app.config['JSON_AS_ASCII'] = False

    # app.run()：启动 Flask 的开发 Web 服务器，Flask 会自动检测代码的变化并重启服务器
    # host='0.0.0.0': 使服务器公开可用，可以通过局域网 IP 访问
    # debug=True: 启用调试模式，服务器会在代码修改后自动重启
    # port=8888: 设置服务器端口为 8888
    app.run(host='0.0.0.0', debug=True, port=8888)
