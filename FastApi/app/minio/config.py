from minio import Minio

# MinIO Client Configuration
minio_client = Minio(
    endpoint="localhost:9000",  # Change if hosted remotely
    access_key="admin",
    secret_key="password",
    secure=False  # Set to True if using HTTPS
)

# Ensure the bucket exists
bucket_name = "embeddings"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
