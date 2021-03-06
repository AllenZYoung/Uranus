import os

from Uranus.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL

# 自定义根目录的工具集
# by kahsolt

RESOURCE_ROOT   = os.path.join(BASE_DIR, 'resource')
PHOTO_ROOT      = os.path.join(RESOURCE_ROOT, 'photos')
REPORT_ROOT     = os.path.join(RESOURCE_ROOT, 'reports')
UPLOAD_ROOT     = os.path.join(RESOURCE_ROOT, 'uploads')

RESOURCE_URL    = MEDIA_URL

##
# Test Entry
if __name__ == '__main__':
    print(RESOURCE_ROOT)
    print(PHOTO_ROOT)
    print(REPORT_ROOT)
    print(UPLOAD_ROOT)
