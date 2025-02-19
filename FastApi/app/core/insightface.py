from fastapi import HTTPException
from insightface.app import FaceAnalysis

import cv2
import io
import numpy as np
import logging
from app.minio.config import minio_client, bucket_name



logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)

face_app = FaceAnalysis(
    name='buffalo_l',
    root='insightface_model',
    providers=['CPUExecutionProvider']
)
face_app.prepare(ctx_id=0, det_size=(640,640), det_thresh=0.5)



async def process_images(file_contents, student_id):
    embeddings = []
    logger.debug("Starting background image processing")

    try:
        # Process each file asynchronously in the background
        for contents in file_contents:
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            results = face_app.get(img, max_num=1)
            logger.debug("Reading image using face_app")

            for res in results:
                embedding = res['embedding']
                embeddings.append(embedding)

        if not embeddings:
            logger.warning("No valid embeddings received.")
            raise ValueError("No valid embeddings received.")
        
        x_mean = np.asarray(embeddings).mean(axis=0)
        x_mean_bytes = x_mean.tobytes()

        # Store embeddings in MinIO
        object_name = f"{student_id}.npy"
        logger.debug(f"Storing embeddings for student {student_id} in MinIO bucket")
        minio_client.put_object(bucket_name, object_name, io.BytesIO(x_mean_bytes), length=len(x_mean_bytes), content_type="application/octet-stream")
        
        logger.debug(f"Embedding for student {student_id} processed and stored successfully")

    except Exception as e:
        logger.exception(f"Error processing images for student {student_id}")


def get_student_embedding(student_id: str):
    # Construct the object name based on student ID
    object_name = f"{student_id}.npy"
    
    # Retrieve the object from MinIO
    try:
        response = minio_client.get_object(bucket_name, object_name)
        # Read the byte data
        byte_data = response.read()
        
        # Convert byte data back to numpy array
        embedding = np.frombuffer(byte_data, dtype=np.float32)
        
        return embedding
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error retrieving embedding: {str(e)}")
