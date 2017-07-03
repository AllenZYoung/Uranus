import urllib.parse

from app.utils.rootsUtils import MEDIA_URL
from app.utils.logUtils import log, LOG_LEVEL
from app.models import *

URL_API = 'https://view.officeapps.live.com/op/view.aspx?src='
SITE_BASE = 'http://uranus.kahsolt.tk'
URL_BASE = SITE_BASE + MEDIA_URL


TEXT_EXT = ['.txt', '.html', '.htm']
XLS_EXT = ['.xls', '.xlsx']
DOCUMENT_EXT = ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
VIDEO_EXT = ['.mp4', '.webm', '.mpg', '.ogg', '.flv', '.f4v']


# 关于文件资源和URL的工具集
# by kahsolt


# 文档在线预览url：doc/ppt/xls
def docPreviewUrl(path):
    f = os.path.basename(path)
    if not isOfficeFile(f):
        log(f + '不是office文档文件', 'docPreviewUrl', LOG_LEVEL.ERROR)
        return '#'

    url = os.path.join(URL_BASE, path)
    url = urllib.parse.quote(url)
    url = URL_API + url
    log(url, 'docPreviewUrl')
    return url


# 文件下载url
def fileDownloadUrl(path):
    url = urllib.parse.quote(path)
    url = os.path.join(URL_BASE, url)
    log(url, 'fileDownloadUrl')
    return url


# 枚举：获取文件类型(后缀名判定)
def getFileTpye(path):
    ext = os.path.splitext(path)[1]
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
    ext = os.path.splitext(path)[1]
    return ext in XLS_EXT


# 判断：是Document
def isOfficeFile(path):
    ext = os.path.splitext(path)[1]
    return ext in DOCUMENT_EXT

##
# Test Entry
def test():
    log('='*50)
    log('File Utils Unit Test')

    fs = File.objects.filter()
    for f in fs:
        log(docPreviewUrl(f.file.url[1:]), 'docPreviewUrl')
        log(fileDownloadUrl(f.file.url[1:]), 'fileDownloadUrl')

    log('='*50)
