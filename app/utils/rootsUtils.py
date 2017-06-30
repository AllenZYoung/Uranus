from Uranus.settings import BASE_DIR
from Uranus.settings import STATICFILES_DIRS
from Uranus.settings import MEDIA_ROOT

# 自定义根目录的工具集
# by kahsolt

RESOURCE_ROOT = BASE_DIR + 'resource'
PHOTO_ROOT = RESOURCE_ROOT + 'photos'
REPORT_ROOT = RESOURCE_ROOT + 'reports'
UPLOAD_ROOT = MEDIA_ROOT

ATTACHMENT_ROOT = UPLOAD_ROOT + 'attachment'
IMPORT_ROOT = UPLOAD_ROOT + 'import'
IMPORT_SKELETON_ROOT = IMPORT_ROOT + 'skeleton'
HANDOUT_ROOT = UPLOAD_ROOT + 'handout'
