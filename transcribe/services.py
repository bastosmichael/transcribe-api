import boto3
import time
import json
import os
from fastapi import UploadFile
from transcribe.config import get_config
import logging

config = get_config()
logger = logging.getLogger(__name__)


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
        region_name=config.region,
    )


def get_transcribe_client():
    return boto3.client(
        "transcribe",
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
        region_name=config.region,
    )


def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    s3 = get_s3_client()
    s3.upload_file(local_file_path, bucket_name, s3_file_name)
    s3_file_uri = f"s3://{bucket_name}/{s3_file_name}"
    return s3_file_uri


def start_transcription_job(s3_file_uri, job_name, language_code="en-US"):
    transcribe = get_transcribe_client()
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": s3_file_uri},
        MediaFormat=s3_file_uri.split(".")[-1],
        LanguageCode=language_code,
        OutputBucketName=config.s3_bucket_name,
        OutputKey=f"{job_name}.json",
    )
    return response


def get_transcription_status(job_name):
    transcribe = get_transcribe_client()
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return status


def fetch_transcription_result(job_name):
    status = get_transcription_status(job_name)
    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        s3 = get_s3_client()
        transcription_response = s3.get_object(
            Bucket=config.s3_bucket_name,
            Key=f"{job_name}.json",
        )
        transcription_text = json.loads(
            transcription_response["Body"].read().decode("utf-8")
        )
        return transcription_text
    elif status["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
        raise Exception("Transcription job failed")
    return {"status": status["TranscriptionJob"]["TranscriptionJobStatus"]}


async def handle_transcription_upload(file: UploadFile):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        s3_file_uri = upload_to_s3(file_location, config.s3_bucket_name, file.filename)
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise

    job_name = f"transcription-{int(time.time())}"

    try:
        start_transcription_job(s3_file_uri, job_name)
    except Exception as e:
        logger.error(f"Error starting transcription job: {e}")
        raise
    finally:
        os.remove(file_location)

    return {"job_name": job_name}


async def handle_transcription_status(job_name: str):
    try:
        status = get_transcription_status(job_name)
        return {"status": status["TranscriptionJob"]["TranscriptionJobStatus"]}
    except Exception as e:
        logger.error(f"Error fetching transcription job status: {e}")
        raise


async def handle_transcription_fetch(job_name: str):
    try:
        result = fetch_transcription_result(job_name)
        return result
    except Exception as e:
        logger.error(f"Error fetching transcription result: {e}")
        raise
