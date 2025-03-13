from insightface.app import FaceAnalysis
from app.minio.config import minio_client, bucket_name
from app.minio.config import get_all_embeddings_from_minio
from app.services.studentService import get_student_details

from sqlalchemy.ext.asyncio import AsyncSession


from sklearn.metrics.pairwise import cosine_similarity



import numpy as np
import logging
import cv2
import io
import base64


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

face_app = FaceAnalysis(
    name='buffalo_l',
    root='insightface_model',
    providers=['CPUExecutionProvider']
)
face_app.prepare(ctx_id=0, det_size=(640,640), det_thresh=0.5)


async def process_frame(image_data: str, db: AsyncSession):
    # image_bytes = base64.b64decode(image_data)
    # nparr = np.frombuffer(image_bytes, np.uint8)
    # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    nparr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces = face_app.get(frame)

    logger.debug(f"Students faces successfully received!: {len(faces)}")
    student_info = []
    
    stored_embeddings = get_all_embeddings_from_minio()
    logger.debug(f"Embeddings from minio successfully received: {len(stored_embeddings)}")

    for face in faces:
        bbox = face.bbox.astype(int).tolist()  # Bounding box (x1, y1, x2, y2)
        embedding = face.embedding  # Extract embedding
        logger.debug("Embedding is received")
        
        # Match detected face with MinIO embeddings
        matched_student = ml_search_algorithm(stored_embeddings, embedding, thresh=0.5)
        logger.debug("Ml search algorithm worked")
        if matched_student != "Unknown":
            student = await get_student_details(matched_student, db, bbox)
            if not student:
                return {"error": "Student not found!"}
            student_info.append(student)
            # label = f"{student['name']} {student['surname']} ({student['student_id']})"
            # color = (0, 255, 0)  # Green for recognized students
        else:
            label = "Unknown"
            color = (0, 0, 255)  # Red for unknown faces

        # # Draw rectangle and label
        # cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        # cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # cv2.imshow('Test image', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    # Encode image back to base64
    # _, buffer = cv2.imencode('.jpg', frame)
    # processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

    return {"students": student_info}
\

def ml_search_algorithm(stored_embeddings, test_vector, thresh=0.5):

    if not stored_embeddings:
        return 'Unknown'
    logger.debug("IT is not Unknown")
    student_ids = list(stored_embeddings.keys())
    logger.debug(f"Ids of students: {student_ids}")
    X_list = np.asarray(list(stored_embeddings.values()))  # Convert to array
    logger.debug(f"array: {X_list.shape}")
    logger.debug(f"X list: {X_list}")
    similarity = cosine_similarity(X_list, test_vector.reshape(1, -1))
    similarity_arr = np.asarray(similarity).flatten()
    
    best_match_idx = np.argmax(similarity_arr)
    best_match_score = similarity[best_match_idx]
    logger.debug(f"Match score: {best_match_score}")
    
    if best_match_score >= thresh:
        return student_ids[best_match_idx]  # Return matched student ID
    return 'Unknown'



async def process_images_while_saving(file_contents, student_id):
    embeddings = []
    logger.debug("Starting background image processing")

    try:
        # Process each file asynchronously in the background
        for contents in file_contents:
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                logger.error("Failed to decode image")
                return {"error": "Failed to decode image"}
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



