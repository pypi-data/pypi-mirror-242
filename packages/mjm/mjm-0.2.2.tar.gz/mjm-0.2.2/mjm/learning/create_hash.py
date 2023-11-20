# 导入哈希库
import hashlib

# 定义一个函数，接受一个字符串作为输入，返回其SHA-1哈希值
def hash_sha1(s):
  # 将字符串转换为字节
  b = s.encode()
  # 计算字节的SHA-1哈希值
  h = hashlib.sha1(b)
  # 将哈希值转换为10进制的整数
  r = int(h.hexdigest(), 16)
  # 返回结果
  return r

# 定义一个函数，接受一个整数作为输入，返回其16位的取余值
def mod_16(n):
  # 计算10的16次方
  m = 10 ** 16
  # 对输入进行模运算
  r = n % m
  # 返回结果
  return r

# 测试一下
user_id = "12345678910"
web_id = "abcdefg"
hash_uid_user = hash_sha1(user_id)
hash_uid_web = hash_sha1(web_id)
hash_uid_user_16 = mod_16(hash_uid_user)
hash_uid_web_16 = mod_16(hash_uid_web)
print("user_id:", user_id)
print("hash_uid_user:", hash_uid_user)
print("hash_uid_user_16:", hash_uid_user_16)
print("web_id:", web_id)
print("hash_uid_web:", hash_uid_web)
print("hash_uid_web_16:", hash_uid_web_16)
