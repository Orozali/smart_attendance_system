from minio import Minio
import numpy as np
import io

minio_client = Minio(
    endpoint="localhost:9000",
    access_key="admin",
    secret_key="password",
    secure=False
)

# Ensure the bucket exists
bucket_name = "embeddings"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)



def get_all_embeddings_from_minio():
    """
    Fetch all embeddings from MinIO for comparison.
    """
    embeddings = {}
    try:
        objects = minio_client.list_objects(bucket_name)
        
        for obj in objects:
            data = minio_client.get_object(bucket_name, obj.object_name)
            embedding_bytes = io.BytesIO(data.read())
            
            embedding = np.frombuffer(embedding_bytes.getvalue(), dtype=np.float32)
            student_id = obj.object_name.rsplit('.npy', 1)[0]
            embeddings[student_id] = embedding
            
        return embeddings
    except Exception as e:
        return {"Error": e}
