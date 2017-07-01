import os

from Uranus.settings import BASE_DIR
from Uranus.settings import STATICFILES_DIRS
from Uranus.settings import MEDIA_ROOT

# 自定义根目录的工具集
# by kahsolt

RESOURCE_ROOT   = os.path.join(BASE_DIR, 'resource')
PHOTO_ROOT      = os.path.join(RESOURCE_ROOT, 'photos')
REPORT_ROOT     = os.path.join(RESOURCE_ROOT, 'reports')
UPLOAD_ROOT     = MEDIA_ROOT    # os.path.join(RESOURCE_ROOT, 'uploads')

ATTACHMENT_ROOT = os.path.join(UPLOAD_ROOT, 'attachment')
IMPORT_ROOT     = os.path.join(UPLOAD_ROOT, 'import')
IMPORT_SKELETON_ROOT    = os.path.join(IMPORT_ROOT, 'skeleton')
HANDOUT_ROOT    = os.path.join(UPLOAD_ROOT, 'handout')


##
# Test Entry
if __name__ == '__main__':
    print(RESOURCE_ROOT)
    print(PHOTO_ROOT)
    print(REPORT_ROOT)
    print(UPLOAD_ROOT)
    print(ATTACHMENT_ROOT)
    print(IMPORT_ROOT)
    print(IMPORT_SKELETON_ROOT)
    print(HANDOUT_ROOT)
