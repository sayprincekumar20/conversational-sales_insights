# import requests
# from sqlalchemy import text
# from app.config import settings
# from app.services.forecast_service import forecast_sales
# from langgraph.graph import StateGraph
# from typing import TypedDict
# from app.services.llm_service import LLMService
# from app.database import SessionLocal  # ✅ so we can run SQL inside pipeline


# class LLMService:
#     def __init__(self):
#         self.groq_url = settings.GROQ_API_URL
#         self.groq_key = settings.GROQ_API_KEY
#         self.langgraph_url = settings.LANGGRAPH_API_URL
#         self.langgraph_key = settings.LANGGRAPH_API_KEY

#     def _groq_call(self, messages, max_tokens=512, temperature=0):
#         headers = {
#             "Authorization": f"Bearer {self.groq_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": settings.GROQ_MODEL,
#             "messages": messages,
#             "max_tokens": max_tokens,
#             "temperature": temperature
#         }

#         resp = requests.post(self.groq_url, json=payload, headers=headers, timeout=30)

#         # 🔄 fallback: if /chat/completions fails, retry /responses
#         if resp.status_code == 404 and "/chat/completions" in self.groq_url:
#             fallback_url = self.groq_url.replace("/chat/completions", "/responses")
#             print(f"⚠️ {self.groq_url} returned 404, retrying with {fallback_url}")
#             resp = requests.post(fallback_url, json=payload, headers=headers, timeout=30)

#         resp.raise_for_status()
#         data = resp.json()

#         # Groq supports both OpenAI-style and responses-style outputs
#         if "choices" in data:
#             return data["choices"][0]["message"]["content"].strip()
#         elif "output_text" in data:
#             return data["output_text"].strip()
#         else:
#             raise RuntimeError(f"Unexpected Groq API response: {data}")

#     def prompt_to_sql(self, prompt: str) -> dict:
#         if self.langgraph_url:
#             headers = {"Content-Type": "application/json"}
#             if self.langgraph_key:
#                 headers["Authorization"] = f"Bearer {self.langgraph_key}"
#             resp = requests.post(self.langgraph_url, json={"prompt": prompt}, headers=headers, timeout=30)
#             resp.raise_for_status()
#             return resp.json()

#         sql = self._groq_call(
#             [{"role": "system", "content": settings.SYSTEM_SQL},
#              {"role": "user", "content": prompt}],
#             max_tokens=512, temperature=0
#         )
#         return {"sql": sql}

#     def generate_insight(self, prompt: str, data: list) -> str:
#         return self._groq_call(
#             [{"role": "system", "content": settings.INSIGHT_SYSTEM},
#              {"role": "user", "content": f"Question: {prompt}\n\nData: {data[:10]}"}],
#             max_tokens=200,
#             temperature=0.2
#         )


# # -------------------------------
# # LangGraph pipeline definition
# # -------------------------------

# class PipelineState(TypedDict, total=False):
#     prompt: str
#     sql: str
#     data: list
#     summary: str
#     forecast: dict
#     forecast_needed: bool


# # -------------------------------
# # Build LangGraph pipeline
# # -------------------------------
# def build_langgraph_pipeline():
#     graph = StateGraph(PipelineState)

#     # Step 1: Generate SQL
#     def sql_node(state: PipelineState):
#         sql = LLMService().prompt_to_sql(state["prompt"])["sql"]
#         return {"sql": sql}

#     # Step 2: Execute SQL
#     def db_node(state: PipelineState):
#         with SessionLocal() as db:
#             try:
#                 result = db.execute(text(state["sql"])).fetchall()
#                 data = [dict(r._mapping) for r in result]
#             except Exception as e:
#                 raise RuntimeError(f"SQL execution failed: {state['sql']}\nError: {e}")
#         return {"data": data}

#     # Step 3: Generate Insights
#     def insight_node(state: PipelineState):
#         data = state.get("data", [])
#         summary = LLMService().generate_insight(state["prompt"], data)
#         return {"summary": summary}

#     # Step 4: Smart Forecasting
#     def forecast_node(state: PipelineState):
#         data = state.get("data", [])
#         # Only run forecasting if sales-related columns exist
#         if data and all(col in data[0] for col in ["OrderDate", "LineTotal"]):
#             forecast = forecast_sales(data)
#             forecast_needed = True
#         else:
#             forecast = None
#             forecast_needed = False
#         return {"forecast": forecast, "forecast_needed": forecast_needed}

#     # Add nodes to graph
#     graph.add_node("sql", sql_node)
#     graph.add_node("db", db_node)
#     graph.add_node("insight", insight_node)
#     graph.add_node("forecast", forecast_node)

#     # Define pipeline flow
#     graph.set_entry_point("sql")
#     graph.add_edge("sql", "db")        # SQL → DB
#     graph.add_edge("db", "insight")    # DB → Insight
#     graph.add_edge("insight", "forecast")  # Insight → Forecast (conditionally)

#     return graph.compile()




# app/services/llm_service.py
import requests
from app.config import settings

class LLMService:
    def __init__(self):
        self.groq_url = settings.GROQ_API_URL
        self.groq_key = settings.GROQ_API_KEY
        self.langgraph_url = settings.LANGGRAPH_API_URL
        self.langgraph_key = settings.LANGGRAPH_API_KEY

    def _groq_call(self, messages, max_tokens=512, temperature=0):
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        resp = requests.post(self.groq_url, json=payload, headers=headers, timeout=30)

        # fallback for /responses
        if resp.status_code == 404 and "/chat/completions" in self.groq_url:
            fallback_url = self.groq_url.replace("/chat/completions", "/responses")
            resp = requests.post(fallback_url, json=payload, headers=headers, timeout=30)

        resp.raise_for_status()
        data = resp.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        elif "output_text" in data:
            return data["output_text"].strip()
        else:
            raise RuntimeError(f"Unexpected Groq API response: {data}")

    def prompt_to_sql(self, prompt: str) -> dict:
        if self.langgraph_url:
            headers = {"Content-Type": "application/json"}
            if self.langgraph_key:
                headers["Authorization"] = f"Bearer {self.langgraph_key}"
            resp = requests.post(self.langgraph_url, json={"prompt": prompt}, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()

        sql = self._groq_call(
            [{"role": "system", "content": settings.SYSTEM_SQL},
             {"role": "user", "content": prompt}],
            max_tokens=512, temperature=0
        )
        return {"sql": sql}

    def generate_insight(self, prompt: str, data: list) -> str:
        return self._groq_call(
            [{"role": "system", "content": settings.INSIGHT_SYSTEM},
             {"role": "user", "content": f"Question: {prompt}\n\nData: {data[:10]}"}],
            max_tokens=200,
            temperature=0.2
        )
