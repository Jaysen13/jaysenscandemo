from flask import Flask, request, jsonify
from __jaysendata import JaysenReqData,JaysenRespData
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import re
import urllib.parse
def url_decode(encoded_str, plus_to_space=True):
    try:
        if plus_to_space:
            # unquote_plus：自动将 '+' 转为空格（常见于表单提交的URL编码）
            return urllib.parse.unquote_plus(encoded_str)
        else:
            # unquote：仅解码 %xx 格式，不处理 '+'（标准URL路径解码）
            return urllib.parse.unquote(encoded_str)
    except Exception as e:
        raise ValueError(f"URL解码失败：{str(e)}") from e

def url_encode(raw_str, space_to_plus=False):
    try:
        if space_to_plus:
            # quote_plus：空格转为 '+'，其他特殊字符转%xx（表单提交常用）
            return urllib.parse.quote_plus(raw_str)
        else:
            return urllib.parse.quote(raw_str)
    except Exception as e:
        raise ValueError(f"URL编码失败：{str(e)}") from e

def extract_encrypted_user(param_string: str) -> str | None:
    pattern = r'encryptedUser=([^&]+)'
    # 搜索匹配（忽略大小写，可选）
    match = re.search(pattern, param_string, re.IGNORECASE)
    # 返回匹配结果（未找到返回None）
    return match.group(1) if match else None

def extract_encrypted_pass(param_string: str) -> str | None:
    pattern = r'encryptedPass=([^&]+)'
    # 搜索匹配（忽略大小写，可选）
    match = re.search(pattern, param_string, re.IGNORECASE)
    # 返回匹配结果（未找到返回None）
    return match.group(1) if match else None

def aes_encrypt(plaintext):
    # 固定参数（与截图完全一致）
    KEY = "1234567890123456"  # 截图中的Text密钥
    MODE = AES.MODE_ECB
    ENCODING = "utf-8"
    PAD_STYLE = "pkcs7"
    # 密钥转字节（Text类型直接编码）
    key_bytes = KEY.encode(ENCODING)
    # 验证密钥长度（128bits=16字节，截图密钥正好16字符）
    if len(key_bytes) * 8 != 128:
        raise ValueError("密钥长度必须为16字节（对应128bits）")
    # 明文转字节 → 填充 → 加密 → Base64编码
    plaintext_bytes = plaintext.encode(ENCODING)
    padded_data = pad(plaintext_bytes, AES.block_size, style=PAD_STYLE)
    cipher = AES.new(key_bytes, MODE)
    encrypted_bytes = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_bytes).decode(ENCODING)


def aes_decrypt(ciphertext_b64):
    # 固定参数（与截图完全一致）
    KEY = "1234567890123456"
    MODE = AES.MODE_ECB
    ENCODING = "utf-8"
    PAD_STYLE = "pkcs7"
    # 密钥转字节
    key_bytes = KEY.encode(ENCODING)
    if len(key_bytes) * 8 != 128:
        raise ValueError("密钥长度必须为16字节（对应128bits）")
    # Base64解码密文 → 解密 → 去填充 → 转明文
    ciphertext_bytes = base64.b64decode(ciphertext_b64)
    cipher = AES.new(key_bytes, MODE)
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    plaintext_bytes = unpad(decrypted_bytes, AES.block_size, style=PAD_STYLE)
    return plaintext_bytes.decode(ENCODING)

app = Flask(__name__)

# 对请求数据包进行解密操作
@app.route('/RequestReceived', methods=['POST'])
def request_received():
    request_json = request.get_json()
    # 初始化原始数据
    jaysendata = JaysenReqData(
        method=request_json.get("method", ""),
        paramters=request_json.get("paramters", {}),
        headers=request_json.get("headers", {}),
        body=request_json.get("body", ""),
    )
    # 提取加密数据
    user = url_decode(extract_encrypted_user(jaysendata.body))
    passwd = url_decode(extract_encrypted_pass(jaysendata.body))
    de_user = aes_decrypt(user)
    de_pass = aes_decrypt(passwd)
    # 将解密的数据拼接回去
    jaysendata.body = f"encryptedUser={de_user}&encryptedPass={de_pass}"
    # 返回修改后的数据包
    return jsonify(jaysendata)

# 对解密后的请求进行加密操作
@app.route('/RequestToBeSent', methods=['POST'])
def handle_request():
    request_json = request.get_json()
    # 初始化原始数据
    jaysendata = JaysenReqData(
        method=request_json.get("method", ""),
        paramters=request_json.get("paramters", {}),
        headers=request_json.get("headers", {}),
        body=request_json.get("body", ""),
    )
    # 提取加密数据
    user = extract_encrypted_user(jaysendata.body)
    passwd = extract_encrypted_pass(jaysendata.body)
    en_user = url_encode(aes_encrypt(user))
    en_pass = url_encode(aes_encrypt(passwd))
    # 将加密的数据拼接回去
    jaysendata.body = f"encryptedUser={en_user}&encryptedPass={en_pass}"
    # 返回修改后的数据包
    return jsonify(jaysendata)

# 解密响应数据包
@app.route('/ResponseReceived', methods=['POST'])
def ResponseReceived():
    resp_json = request.get_json()
    jaysendata = JaysenRespData(
        headers=resp_json.get("headers"),
        body=resp_json.get("body")
    )
    # 不修改响应包
    return jsonify(jaysendata)

#加密响应数据包
@app.route('/ResponseToBeSent', methods=['POST'])
def ResponseToBeSent():
    resp_json = request.get_json()
    jaysendata = JaysenRespData(
        headers=resp_json.get("headers"),
        body=resp_json.get("body")
    )
    # 不修改响应包
    return jsonify(jaysendata)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)