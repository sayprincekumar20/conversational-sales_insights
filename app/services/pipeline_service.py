# app/services/pipeline_service.py
from typing import TypedDict
from langgraph.graph import StateGraph
from sqlalchemy import text
from app.services.llm_service import LLMService
from app.services.forecast_service import forecast_sales
from app.database import SessionLocal

class PipelineState(TypedDict, total=False):
    prompt: str
    sql: str
    data: list
    summary: str
    forecast: dict
    forecast_needed: bool

def build_langgraph_pipeline():
    graph = StateGraph(PipelineState)

    # Step 1: Generate SQL
    def sql_node(state: PipelineState):
        sql = LLMService().prompt_to_sql(state["prompt"])["sql"]
        return {"sql": sql}

    # Step 2: Execute SQL
    def db_node(state: PipelineState):
        with SessionLocal() as db:
            try:
                result = db.execute(text(state["sql"])).fetchall()
                data = [dict(r._mapping) for r in result]
            except Exception as e:
                raise RuntimeError(f"SQL execution failed: {state['sql']}\nError: {e}")
        return {"data": data}

    # Step 3: Generate Insights
    def insight_node(state: PipelineState):
        data = state.get("data", [])
        summary = LLMService().generate_insight(state["prompt"], data)
        return {"summary": summary}

    # Step 4: Smart Forecasting
    def forecast_node(state: PipelineState):
        data = state.get("data", [])
        if data and all(col in data[0] for col in ["OrderDate", "LineTotal"]):
            forecast = forecast_sales(data)
            forecast_needed = True
        else:
            forecast = None
            forecast_needed = False
        return {"forecast": forecast, "forecast_needed": forecast_needed}

    # Add nodes
    graph.add_node("sql", sql_node)
    graph.add_node("db", db_node)
    graph.add_node("insight", insight_node)
    graph.add_node("forecast", forecast_node)

    # Define flow
    graph.set_entry_point("sql")
    graph.add_edge("sql", "db")
    graph.add_edge("db", "insight")
    graph.add_edge("insight", "forecast")

    return graph.compile()
