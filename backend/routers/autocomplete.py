from fastapi import APIRouter
from schemas import AutocompleteRequest, AutocompleteResponse
from services.autocomplete_service import get_mock_suggestion

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])

@router.post("", response_model=AutocompleteResponse)
def get_autocomplete_suggestion(request: AutocompleteRequest):
    """Get mocked autocomplete suggestion"""
    result = get_mock_suggestion(
        code=request.code,
        cursor_position=request.cursorPosition,
        language=request.language
    )
    return AutocompleteResponse(**result)


