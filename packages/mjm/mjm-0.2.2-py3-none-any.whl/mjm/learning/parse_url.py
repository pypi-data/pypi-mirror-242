
import sys
import re
url = "http://ltscsy.qq.com/B_ql7v7wEvp66DWinQeWWlFMv_QraIYNv_yJJ26ZBcvJC0sPw07eNU29QKKAG2BSAH/9_LhmK9hFGl4we0DbkJMO6lYqgy7OVrmU-3CBQoI33tiasB5AfuxXwl9Ai5ugR67rYp4OEGCiNUnGL2FUBCdEZF18tuaKh29O_Z5D5lhKkr6XCDTnONtsAXD7pAObF0JUbVcswdkSvsTcOitFKkY67C5VpoUW-ypvknr8ZPh5hMMqeh_orkBZX5U_MmE0S8xVUtZfuaEdbq3X9KyHTzanCB7HfCGcpsAVLxRulg1Pun4mDnVKSut8A/gzc_1000102_0b53beadcaaa3yaoctoi2jsmacodgecqanka.f321003.ts.m3u8?ver=4"
pattern_tengxun = r"gzc_[^.]*"
pattern_youku = r"vid=[^&]*"
pattern_iqiyi = r"/mus/[^/]*"
pattern_bilibili = r"/ep[^/]*"
urls_domain_list = {"腾讯视频":"qq.com" , "优酷视频":"youku.com","爱奇艺":"iqiyi.com","bilibili":"bilibili.com"}

tengxun_re = re.compile(pattern_tengxun)
youku_re = re.compile(pattern_youku)
iqiyi_re = re.compile(pattern_iqiyi)
bilibili_re = re.compile(pattern_bilibili)

result_list = tengxun_re.findall(url)
media_match_id = ""
if result_list :
    media_match_id = result_list[0]
print(media_match_id)

# def parse_url(self,url):

#     url_domain = ""
#     media_match_id = ""
#     for k,v in self.urls_domain_list.items():
#         if url.find(v) != -1:
#             url_domain = k
#     if url_domain == '腾讯视频':
#         pass
#     elif url_domain == '优酷视频':
#         result_list = self.youku_re.findall(url)
#         if result_list :
#             media_match_id = result_list[0][4:]
#     elif url_domain == '爱奇艺':
#         result_list = self.iqiyi_re.findall(url)
#         if result_list :
#             media_match_id = result_list[0][5:]
#     elif url_domain == 'bilibili':
#         result_list = self.bilibili_re.findall(url)
#         if len(result_list) >= 1:
#             media_match_id = result_list[-1][3:]
#     else:
#         pass
#     return media_match_id

# def evaluate(self,url):
#     import requests
#     if url is None:
#         return None
#     decoded_url = requests.utils.unquote(url)
#     media_match_id = self.parse_url(decoded_url)
#     return media_match_id
