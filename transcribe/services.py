import boto3
import time
import json
import os
from fastapi import UploadFile
from transcribe.config import config
import logging

config = config()
logger = logging.getLogger(__name__)


def boto_client(service_name):
    return boto3.client(
        service_name,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
        region_name=config.region,
    )


def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    s3 = boto_client("s3")
    s3.upload_file(local_file_path, bucket_name, s3_file_name)
    return f"s3://{bucket_name}/{s3_file_name}"


def start_transcription_job(s3_file_uri, job_name, language_code="en-US"):
    transcribe = boto_client("transcribe")
    return transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": s3_file_uri},
        MediaFormat=s3_file_uri.split(".")[-1],
        LanguageCode=language_code,
        OutputBucketName=config.s3_bucket_name,
        OutputKey=f"{job_name}.json",
    )


def transcription_status(job_name):
    transcribe = boto_client("transcribe")
    return transcribe.get_transcription_job(TranscriptionJobName=job_name)


def transcription_result(job_name):
    status = transcription_status(job_name)
    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        s3 = boto_client("s3")
        transcription_response = s3.get_object(
            Bucket=config.s3_bucket_name,
            Key=f"{job_name}.json",
        )
        return json.loads(transcription_response["Body"].read().decode("utf-8"))
    elif status["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
        raise Exception("Transcription job failed")
    return {"status": status["TranscriptionJob"]["TranscriptionJobStatus"]}


async def transcription_upload(file: UploadFile):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        s3_file_uri = upload_to_s3(file_location, config.s3_bucket_name, file.filename)
        job_name = f"transcription-{int(time.time())}"
        start_transcription_job(s3_file_uri, job_name)
    except Exception as e:
        logger.error(f"Error processing transcription job: {e}")
        raise
    finally:
        os.remove(file_location)

    return {"job_name": job_name}


async def transcription_status_api(job_name: str):
    try:
        return {
            "status": transcription_status(job_name)["TranscriptionJob"][
                "TranscriptionJobStatus"
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching transcription job status: {e}")
        raise


async def transcription_fetch(job_name: str):
    try:
        return transcription_result(job_name)
    except Exception as e:
        logger.error(f"Error fetching transcription result: {e}")
        raise
