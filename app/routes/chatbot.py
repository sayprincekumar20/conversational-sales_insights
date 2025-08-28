# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.schemas.query import QueryRequest
# from app.services.query_service import run_user_query

# router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# @router.post("/query")
# def query_endpoint(payload: QueryRequest, db: Session = Depends(get_db)):
#     try:
#         return run_user_query(db, payload.prompt, payload.chart_type or "auto")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.query import QueryRequest
from app.services.query_service import run_user_query
import traceback

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/query")
def query_endpoint(payload: QueryRequest, db: Session = Depends(get_db)):
    try:
        return run_user_query(db, payload.prompt, payload.chart_type or "auto")
    except Exception as e:
        # Print full error in server logs
        print("❌ ERROR in /chatbot/query:", str(e))
        traceback.print_exc()

        # Return more info in response for debugging
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "prompt": payload.prompt
            }
        )
