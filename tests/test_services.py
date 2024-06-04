import json
import os
import unittest
from unittest.mock import patch, MagicMock
from transcribe.services import (
    boto_client,
    upload_to_s3,
    start_transcription_job,
    transcription_status,
    transcription_result,
    transcription_upload,
    transcription_status_api,
    transcription_fetch,
)
from fastapi import UploadFile
from io import BytesIO


class TestTranscriptionService(unittest.TestCase):
    @patch("transcribe.services.boto3.client")
    def test_upload_to_s3(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        local_file_path = "test.txt"
        bucket_name = "test-bucket"
        s3_file_name = "test.txt"
        expected_uri = f"s3://{bucket_name}/{s3_file_name}"

        with open(local_file_path, "w") as f:
            f.write("test content")

        uri = upload_to_s3(local_file_path, bucket_name, s3_file_name)
        mock_s3.upload_file.assert_called_once_with(
            local_file_path, bucket_name, s3_file_name
        )
        self.assertEqual(uri, expected_uri)
        os.remove(local_file_path)

    @patch("transcribe.services.boto_client")
    def test_start_transcription_job(self, mock_boto_client):
        mock_transcribe = MagicMock()
        mock_boto_client.return_value = mock_transcribe
        s3_file_uri = "s3://test-bucket/test.mp3"
        job_name = "test-job"

        start_transcription_job(s3_file_uri, job_name)
        mock_transcribe.start_transcription_job.assert_called_once()

    @patch("transcribe.services.boto_client")
    def test_transcription_status(self, mock_boto_client):
        mock_transcribe = MagicMock()
        mock_boto_client.return_value = mock_transcribe
        job_name = "test-job"

        transcription_status(job_name)
        mock_transcribe.get_transcription_job.assert_called_once_with(
            TranscriptionJobName=job_name
        )

    @patch("transcribe.services.transcription_status")
    @patch("transcribe.services.boto_client")
    def test_transcription_result(self, mock_boto_client, mock_transcription_status):
        mock_transcribe = MagicMock()
        mock_boto_client.return_value = mock_transcribe
        job_name = "test-job"
        mock_transcription_status.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "COMPLETED"}
        }
        mock_transcribe.get_object.return_value = {
            "Body": BytesIO(json.dumps({"transcript": "test"}).encode("utf-8"))
        }

        result = transcription_result(job_name)
        self.assertEqual(result, {"transcript": "test"})

    @patch("transcribe.services.transcription_result")
    async def test_transcription_fetch(self, mock_transcription_result):
        job_name = "test-job"
        mock_transcription_result.return_value = {"transcript": "test"}

        result = await transcription_fetch(job_name)
        self.assertEqual(result, {"transcript": "test"})

    @patch("transcribe.services.upload_to_s3")
    @patch("transcribe.services.start_transcription_job")
    async def test_transcription_upload(
        self, mock_start_transcription_job, mock_upload_to_s3
    ):
        file = UploadFile(filename="test.mp3", file=BytesIO(b"test content"))
        mock_upload_to_s3.return_value = "s3://test-bucket/test.mp3"

        result = await transcription_upload(file)
        self.assertIn("job_name", result)


if __name__ == "__main__":
    unittest.main()
