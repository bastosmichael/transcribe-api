import unittest
from unittest.mock import patch, MagicMock
from transcribe.services import (
    upload_to_s3,
    start_transcription_job,
    transcription_status,
    transcription_result
)

class TestAdditionalServices(unittest.TestCase):
    @patch('transcribe.services.boto_client')
    def test_start_transcription_job_invalid_format(self, mock_boto_client):
        mock_transcribe = MagicMock()
        mock_boto_client.return_value = mock_transcribe
        s3_file_uri = "s3://test-bucket/test.txt"  # Invalid extension
        with self.assertRaises(Exception) as context:
            start_transcription_job(s3_file_uri, job_name)
        self.assertTrue("Invalid media format" in str(context.exception))
    
    @patch('transcribe.services.boto_client')
    def test_transcription_status_failed(self, mock_boto_client):
        mock_transcribe = MagicMock()
        mock_boto_client.return_value = mock_transcribe
        job_name = "test-job"
        mock_transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "FAILED"}
        }
        result = transcription_status(job_name)
        self.assertEqual(result["TranscriptionJob"]["TranscriptionJobStatus"], "FAILED")

    @patch('transcribe.services.transcription_result')
    def test_transcription_result_case_completed(self, mock_transcription_result):
        job_name = "test-job"
        mock_transcription_result.return_value = {
            "transcript": "test transcription"
        }
        result = transcription_result(job_name)
        self.assertEqual(result, {"transcript": "test transcription"})

if __name__ == "__main__":
    unittest.main()
