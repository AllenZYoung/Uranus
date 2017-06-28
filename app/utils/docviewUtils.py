import urllib.parse

from Uranus.settings import STATIC_URL

URL_API = 'https://view.officeapps.live.com/op/view.aspx?src='
URL_BASE = 'http://uranus.kahsolt.tk' + STATIC_URL

def path2url(path):
    url = URL_BASE + path
    url = urllib.parse.quote(url)
    url = URL_API + url
    return url


# Test Entry
print(path2url('uploads/user/学生.xlsx'))
print(path2url('uploads/file/作业1.docx'))