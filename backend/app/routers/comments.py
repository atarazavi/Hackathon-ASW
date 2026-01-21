from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(prefix="/comments", tags=["comments"])


class CreateCommentRequest(BaseModel):
    file_key: str
    node_id: str
    message: str
    figma_token: str


class CommentResponse(BaseModel):
    success: bool
    comment_id: str | None = None
    error: str | None = None


@router.post("/create", response_model=CommentResponse)
async def create_comment(data: CreateCommentRequest) -> CommentResponse:
    """
    Create a comment on a Figma node via the Figma REST API.

    The comment will be attached to the specified node using its ID.
    """
    figma_url = f"https://api.figma.com/v1/files/{data.file_key}/comments"

    headers = {
        "X-Figma-Token": data.figma_token,
        "Content-Type": "application/json",
    }

    # Use node_id in client_meta to attach comment to specific node
    payload = {
        "message": data.message,
        "client_meta": {
            "node_id": data.node_id,
            "node_offset": {"x": 0, "y": 0}
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                figma_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )

            if response.status_code == 200:
                result = response.json()
                return CommentResponse(
                    success=True,
                    comment_id=result.get("id")
                )
            elif response.status_code == 403:
                return CommentResponse(
                    success=False,
                    error="Invalid or expired Figma token. Please check your Personal Access Token."
                )
            elif response.status_code == 404:
                return CommentResponse(
                    success=False,
                    error="File not found. Make sure you have access to this file."
                )
            else:
                error_text = response.text
                return CommentResponse(
                    success=False,
                    error=f"Figma API error ({response.status_code}): {error_text}"
                )

        except httpx.TimeoutException:
            return CommentResponse(
                success=False,
                error="Request to Figma timed out. Please try again."
            )
        except Exception as e:
            return CommentResponse(
                success=False,
                error=f"Failed to create comment: {str(e)}"
            )
