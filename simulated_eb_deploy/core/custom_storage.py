from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"  
    file_overwrite = False
    object_parameters = {"CacheControl": "max-age=86400"}
    default_acl = "public-read"


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    file_overwrite = True
    cache_control = "max-age=86400"
