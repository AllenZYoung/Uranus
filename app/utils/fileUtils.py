import urllib.parse

from Uranus.settings import STATIC_URL
URL_API = 'https://view.officeapps.live.com/op/view.aspx?src='
URL_BASE = 'http://uranus.kahsolt.tk' + STATIC_URL


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


# Test Entry
if __name__ == '__main__':
    print('PreviewOnline Links Like:')
    print(docPreviewUrl('uploads/user/学生.xlsx'))
    print(docPreviewUrl('uploads/file/作业1.docx'))
    print(docPreviewUrl('uploads/file/5.ppt'))
    print('Download Links Like:')
    print(fileDownloadUrl('uploads/user/学生.xlsx'))
    print(fileDownloadUrl('uploads/file/作业1.docx'))