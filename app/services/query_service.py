# import logging
# from sqlalchemy.orm import Session
# from app.utils.charts import prepare_chart_data, guess_chart_type
# from app.schemas.query import QueryResponse
# from app.services.llm_service import build_langgraph_pipeline

# # Use uvicorn's logger so logs appear with INFO / ERROR levels
# logger = logging.getLogger("uvicorn.error")

# def run_user_query(db: Session, prompt: str, requested_chart_type: str = "auto") -> QueryResponse:
#     pipeline = build_langgraph_pipeline()

#     logger.info("🔍 Starting pipeline for prompt: %s", prompt)

#     # Run full pipeline (SQL → DB → Insight → Forecast)
#     state = pipeline.invoke({"prompt": prompt})

#     sql = state.get("sql")
#     data = state.get("data", [])
#     summary = state.get("summary", "")
#     forecast = state.get("forecast", {})

#     # Logging each stage
#     logger.info("📝 Generated SQL: %s", sql)
#     logger.info("📊 Rows fetched: %d", len(data))
#     if summary:
#         logger.info("💡 Insight: %s", summary)
#     else:
#         logger.warning("⚠️ No insight generated.")
#     if forecast:
#         logger.info("📈 Forecast generated.")
#     else:
#         logger.warning("⚠️ No forecast available.")

#     # Chart handling
#     chart_type = requested_chart_type if requested_chart_type != "auto" else guess_chart_type(data)
#     chart = prepare_chart_data(data, chart_type)

#     logger.info("📊 Chart prepared of type: %s", chart_type)

#     return QueryResponse(sql=sql, data=data, chart=chart, summary=summary, forecast=forecast)
import logging
from sqlalchemy.orm import Session
from app.utils.charts import prepare_chart_data, guess_chart_type
from app.schemas.query import QueryResponse
from app.services.pipeline_service import build_langgraph_pipeline  # ✅ fixed import

logger = logging.getLogger("uvicorn.error")

def run_user_query(db: Session, prompt: str, requested_chart_type: str = "auto") -> QueryResponse:
    pipeline = build_langgraph_pipeline()
    logger.info("🔍 Starting pipeline for prompt: %s", prompt)

    state = pipeline.invoke({"prompt": prompt})

    sql = state.get("sql")
    data = state.get("data", [])
    summary = state.get("summary", "")
    forecast = state.get("forecast", {})

    # Logging
    logger.info("📝 Generated SQL: %s", sql)
    logger.info("📊 Rows fetched: %d", len(data))
    if summary:
        logger.info("💡 Insight: %s", summary)
    else:
        logger.warning("⚠️ No insight generated.")

    if forecast and forecast.get("forecast"):
        logger.info("📈 Forecast generated.")
    elif forecast and forecast.get("note"):
        logger.warning("⚠️ Forecast note: %s", forecast.get("note"))
    else:
        logger.warning("⚠️ No forecast available.")

    # Chart handling
    chart_type = requested_chart_type if requested_chart_type != "auto" else guess_chart_type(data)
    chart = prepare_chart_data(data, chart_type)
    logger.info("📊 Chart prepared of type: %s", chart_type)

    return QueryResponse(sql=sql, data=data, chart=chart, summary=summary, forecast=forecast)
