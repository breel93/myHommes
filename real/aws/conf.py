import datetime
import os



AWS_GROUP_NAME = os.environ.get("AWS_GROUP_NAME")
AWS_USERNAME = os.environ.get("AWS_USERNAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")



AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

AWS_S3_REGION_NAME = 'eu-west-2'

AWS_ENDPOINT='s3-eu-west-2.amazonaws.com/'

DEFAULT_FILE_STORAGE = 'real.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'real.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'real-hommie'
S3DIRECT_REGION = 'eu-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

# AWS_QUERYSTRING_AUTH = True

