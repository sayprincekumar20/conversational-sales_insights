import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    NW_DB_PATH: str = os.getenv("NW_DB_PATH", "./northwind.db")

    LANGGRAPH_API_URL: str | None = os.getenv("LANGGRAPH_API_URL")
    LANGGRAPH_API_KEY: str | None = os.getenv("LANGGRAPH_API_KEY")
    
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    GROQ_API_URL: str = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "gpt-4o-mini")
    SYSTEM_SQL: str = """You translate natural-language analytics questions about the Northwind database into SAFE, minimal SQL for SQLite.
Return ONLY the SQL, no commentary. Prefer the view OrderDetailsExtended (columns: OrderID, OrderDate, Region, Country, ProductName, CustomerID, LineTotal, CategoryName, SupplierName, EmployeeName, ShipperName).
Examples:
- "total sales last month" -> SELECT SUM(LineTotal) AS TotalSales FROM OrderDetailsExtended WHERE strftime('%Y-%m', OrderDate)=strftime('%Y-%m','now','-1 month');
- "sales by region" -> SELECT Region, SUM(LineTotal) AS Sales FROM OrderDetailsExtended GROUP BY Region ORDER BY Sales DESC;
Use ISO date filters via strftime; never use DROP/ALTER/INSERT/UPDATE.
"""

    INSIGHT_SYSTEM: str = """You are a sales analyst. Given the user's question and a small JSON table of results,
write a crisp 1–3 sentence insight (mention leading categories, % share if possible, and a takeaway).
Keep it factual and non-hallucinatory.
"""

settings = Settings()


# from pydantic import BaseSettings
# from dotenv import load_dotenv
# import requests

# load_dotenv()

# class Settings(BaseSettings):
#     GROQ_API_KEY: str
#     GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"

#     def __post_init__(self):
#         self.verify_endpoint()

#     def verify_endpoint(self):
#         """Check if the given endpoint is valid; fall back if not."""
#         try:
#             resp = requests.post(self.GROQ_API_URL, 
#                                  headers={"Authorization": f"Bearer {self.GROQ_API_KEY}"},
#                                  json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "test"}]},
#                                  timeout=5)
#             if resp.status_code == 404:
#                 # fall back to response-based endpoint
#                 fallback = "https://api.groq.com/openai/v1/responses"
#                 print(f"WARNING: {self.GROQ_API_URL} returned 404. Falling back to {fallback}")
#                 self.GROQ_API_URL = fallback
#         except Exception as e:
#             print("Groq endpoint verification failed:", str(e))


# settings = Settings()
