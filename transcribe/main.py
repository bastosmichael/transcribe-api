import sys
import logging
from fastapi import FastAPI, Depends
from transcribe.api import router
from transcribe.config import get_config
import argparse

app = FastAPI(title="TranscribeAPI", dependencies=[Depends(get_config)])

# Include routers
app.include_router(router)


def main():
    parser = argparse.ArgumentParser(description="TranscribeAPI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    import uvicorn

    uvicorn.run(
        "transcribe.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug" if args.verbose else "info",
    )


if __name__ == "__main__":
    main()
