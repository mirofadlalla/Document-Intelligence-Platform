from typing import List, Optional
import os
import tempfile
import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from app.api.dependencies import get_pipeline
from app.pipeline.processing_pipeline import ProcessingPipeline
from app.schemas.api import ProcessRequest, ProcessResponse

router = APIRouter()

@router.post("/process", tags=["Processing"], response_model=ProcessResponse)
async def process_document(
    subject: str = Form(...),
    body: str = Form(...),
    attachments: List[UploadFile] = File(...),
    source_email: Optional[str] = Form("dashboard@local"),
    pipeline: ProcessingPipeline = Depends(get_pipeline)
) -> ProcessResponse:
    request_data = ProcessRequest(subject=subject, body=body)
    
    temp_dir = tempfile.mkdtemp()
    file_paths = []
    try:
        for attachment in attachments:
            file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{attachment.filename}")
            with open(file_path, "wb") as buffer:
                content = await attachment.read()
                buffer.write(content)
            file_paths.append(file_path)
        
        response = await pipeline.process(
            request=request_data,
            file_paths=file_paths,
            source_email=source_email
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        for fp in file_paths:
            try:
                os.remove(fp)
            except Exception:
                pass
        try:
            os.rmdir(temp_dir)
        except Exception:
            pass
