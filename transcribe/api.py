from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from transcribe.services import (
    handle_transcription_upload,
    handle_transcription_status,
    handle_transcription_fetch,
)

router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@router.post(
    "/transcribe_upload",
    tags=["Transcription"],
    summary="Upload Audio File and Start Transcription",
    description="Uploads an audio file to S3 and starts a transcription job.",
)
async def transcribe_upload(file: UploadFile):
    try:
        response = await handle_transcription_upload(file)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/transcribe_status/{job_name}",
    tags=["Transcription"],
    summary="Fetch Transcription Status",
    description="Fetches the status of a transcription job.",
)
async def transcribe_status(job_name: str):
    try:
        response = await handle_transcription_status(job_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/transcribe_fetch/{job_name}",
    tags=["Transcription"],
    summary="Fetch Transcription Result",
    description="Fetches the transcription result once the job is completed.",
)
async def transcribe_fetch(job_name: str):
    try:
        response = await handle_transcription_fetch(job_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
