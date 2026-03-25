import base64
from io import BytesIO

from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from src.controllers.analyze import analyze_pdf
from src.models.requests import AnalyzePdfRequest
from src.exceptions.PdfExtractException import PdfExtractException

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("/pdf/file", response_model=dict)
async def post_analyze_pdf_file(file: UploadFile):
    """Анализ PDF файла"""
    if not file or not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    if file.content_type not in ("application/pdf", "application/octet-stream", ""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Expected PDF file, got: {file.content_type}")

    try:
        result = await analyze_pdf(file.file)
        return JSONResponse(content=result)
    except PdfExtractException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"PDF extraction error: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")
    finally:
        await file.close()


@router.post("/pdf/base64", response_model=dict)
async def post_analyze_pdf_base64(request: AnalyzePdfRequest):
    """Анализ PDF в base64"""
    try:
        decode_bytes: bytes = base64.b64decode(request.file_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to decode base64: {e}")

    try:
        result = await analyze_pdf(BytesIO(decode_bytes))
        return JSONResponse(content=result)
    except PdfExtractException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"PDF extraction error: {e.detail}")