from typing import List, Dict, Optional

def guess_chart_type(data: List[Dict]) -> str:
    if not data:
        return "bar"
    keys = list(data[0].keys())
    if any("date" in k.lower() for k in keys):
        return "line"
    if len(keys) == 2:
        return "pie"
    return "bar"

def prepare_chart_data(data: List[Dict], chart_type: Optional[str] = None) -> Dict:
    if not data:
        return {"type": chart_type or "bar", "labels": [], "values": []}
    ctype = chart_type or guess_chart_type(data)
    keys = list(data[0].keys())
    label_key = keys[0]
    value_key = keys[1] if len(keys) > 1 else keys[0]
    labels = [row[label_key] for row in data]
    values = [row[value_key] for row in data]
    return {"type": ctype, "labels": labels, "values": values}
