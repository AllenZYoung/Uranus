import os
import urllib.parse

from Uranus.settings import STATIC_URL

URL_API = 'https://view.officeapps.live.com/op/view.aspx?src='
URL_BASE = 'http://uranus.kahsolt.tk' + STATIC_URL

TEXT_EXT = ['txt', 'html', 'htm']
DOCUMENT_EXT = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']
VIDEO_EXT = ['mp4', 'webm', 'mpg', 'ogg', 'flv', 'f4v']


# 关于文件资源和URL的工具集
# by kahsolt


# 文档在线预览url：doc/ppt/xls
def docPreviewUrl(path):
    url = URL_BASE + path
    url = urllib.parse.quote(url)
    url = URL_API + url
    return url


# 文件下载url
def fileDownloadUrl(path):
    url = urllib.parse.quote(path)
    url = URL_BASE + url
    return url


# 枚举：获取文件类型(后缀名判定)
def getFileTpye(path):
    ext = os.path.splitext(path)
    if ext in TEXT_EXT:
        return 'text'
    elif ext in DOCUMENT_EXT:
        return 'document'
    elif ext in VIDEO_EXT:
        return 'video'
    else:
        return 'unkown'


# 判断：是Excel表
def isXls(path):
    ext = os.path.splitext(path)
    return ext == 'xls' or ext =='xlsx'


##
# Test Entry
if __name__ == '__main__':
    print('PreviewOnline Links Like:')
    print(docPreviewUrl('stu.xlsx'))
    print(docPreviewUrl('file/作业1.docx'))
    print(docPreviewUrl('file/8第四章Camellia.ppt'))
    print('Download Links Like:')
    print(fileDownloadUrl('user/学生.xlsx'))
    print(fileDownloadUrl('file/作业1.docx'))