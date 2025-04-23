from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "images"
    file_overwrite = False
    object_parameters = {
        'CacheControl': 'max-age=86400'
    }
    # default_acl = "public-read"
