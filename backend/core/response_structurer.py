"""
Converts raw DataFrame results into a structured response:
- AI-orchestrated presentation decisions
- Intelligent chart generation based on data characteristics
- Smart column selection for tables
- Natural language summary with insights
- Metadata (device, period, row count)
"""
import json
import pandas as pd
import openai
from config.settings import settings
from config.event_codes import ALLOWED_EVENTS
from core.ai_orchestrator import AIOrchestrator

SECTION_CHART_MAP = {
    "Energy Summary":    {"chart_type": "bar",     "kpi": True},
    "Load & Demand":     {"chart_type": "line",    "kpi": True},
    "Voltage & Current": {"chart_type": "line",    "kpi": False},
    "Device & Period":   {"chart_type": "none",    "kpi": True},
}

def structure_response(
    df: pd.DataFrame,
    user_query: str,
    device_id: str,
    period_type: str,
    row_count: int,
    truncated: bool,
    sql_used: str = "",
) -> dict:
    """
    AI-orchestrated response structuring.
    The AI agent decides what to show and how to present it.
    """
    
    # Initialize AI orchestrator
    orchestrator = AIOrchestrator()
    
    # Get AI decisions about presentation
    decision = orchestrator.orchestrate_response(
        df=df,
        user_query=user_query,
        device_id=device_id,
        period_type=period_type,
        sql_used=sql_used
    )
    
    if df is None or df.empty:
        return {
            "status": "no_data",
            "message": decision.narrative,
            "charts": [],
            "kpis": [],
            "tables": [],
            "summary": decision.narrative,
            "insights": [],
            "metadata": {
                "device_id": device_id,
                "period_type": period_type,
                "row_count": 0,
                "truncated": False,
                "tone": decision.tone,
            }
        }

    # Build charts based on AI recommendations
    charts = _build_intelligent_charts(df, decision.chart_recommendations) if decision.show_charts else []
    
    # Build KPIs from numeric data
    kpis = _build_smart_kpis(df, decision.table_columns)
    
    # Build tables with AI-selected columns
    tables = _build_smart_tables(df, decision.table_columns)

    return {
        "status": "success",
        "metadata": {
            "device_id": device_id,
            "period_type": period_type,
            "row_count": row_count,
            "truncated": truncated,
            "tone": decision.tone,
        },
        "summary": decision.narrative,
        "insights": decision.insights,
        "kpis": kpis,
        "charts": charts,
        "tables": tables,
    }

def _group_by_section(df: pd.DataFrame) -> dict:
    if "section" not in df.columns:
        return {"All Data": df}
    return {sec: group for sec, group in df.groupby("section")}

def _build_kpis(sections: dict) -> list[dict]:
    kpis = []
    for section, df in sections.items():
        chart_meta = SECTION_CHART_MAP.get(section, {})
        if not chart_meta.get("kpi"):
            continue
        for _, row in df.iterrows():
            if pd.notna(row.get("numeric_value")):
                kpis.append({
                    "section": section,
                    "label": row.get("metric_name", ""),
                    "value": float(row["numeric_value"]),
                    "unit": row.get("unit", ""),
                    "context": row.get("context", ""),
                })
            elif pd.notna(row.get("text_value")):
                kpis.append({
                    "section": section,
                    "label": row.get("metric_name", ""),
                    "value": row["text_value"],
                    "unit": "",
                    "context": row.get("context", ""),
                })
    return kpis

def _build_charts(sections: dict) -> list[dict]:
    charts = []

    if "Energy Summary" in sections:
        energy_df = sections["Energy Summary"]
        energy_map = dict(zip(
            energy_df.get("metric_name", []),
            energy_df.get("numeric_value", [])
        ))
        charts.append({
            "id": "energy_bar",
            "title": "Energy Summary",
            "type": "bar",
            "data": {
                "labels": ["Import (kWh)", "Export (kWh)", "Net (kWh)", "Apparent (kVAh)"],
                "datasets": [{
                    "label": "Energy",
                    "data": [
                        energy_map.get("Total Import Energy"),
                        energy_map.get("Total Export Energy"),
                        energy_map.get("Net Energy"),
                        energy_map.get("Total Apparent Energy"),
                    ],
                    "backgroundColor": ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"],
                }]
            },
        })

    event_sections = {k: v for k, v in sections.items() if str(k).startswith("Events")}
    if event_sections:
        categories = list(event_sections.keys())
        high_counts = []
        medium_counts = []
        for cat, df in event_sections.items():
            high = df[df.get("metric_name", pd.Series()).str.contains("HIGH", na=False)]["numeric_value"].sum()
            medium = df[df.get("metric_name", pd.Series()).str.contains("MEDIUM", na=False)]["numeric_value"].sum()
            high_counts.append(float(high))
            medium_counts.append(float(medium))
        charts.append({
            "id": "events_grouped_bar",
            "title": "Events by Category & Severity",
            "type": "grouped_bar",
            "data": {
                "labels": [c.replace("Events — ", "") for c in categories],
                "datasets": [
                    {"label": "High Severity",   "data": high_counts,   "backgroundColor": "#EF4444"},
                    {"label": "Medium Severity",  "data": medium_counts, "backgroundColor": "#F59E0B"},
                ],
            },
        })

    if "Voltage & Current" in sections:
        v_df = sections["Voltage & Current"]
        v_map = dict(zip(v_df.get("metric_name", []), v_df.get("numeric_value", [])))
        charts.append({
            "id": "voltage_range",
            "title": "Voltage Range",
            "type": "range_bar",
            "data": {
                "labels": ["Voltage (V)"],
                "datasets": [
                    {"label": "Min",  "data": [v_map.get("Minimum Voltage")], "backgroundColor": "#3B82F6"},
                    {"label": "Avg",  "data": [v_map.get("Average Voltage")], "backgroundColor": "#10B981"},
                    {"label": "Max",  "data": [v_map.get("Maximum Voltage")], "backgroundColor": "#EF4444"},
                ],
            },
        })

    return charts

def _build_tables(sections: dict, df: pd.DataFrame) -> list[dict]:
    """Build table representations from the dataframe"""
    tables = []
    
    # Check for event-specific columns
    event_cols = ["event_description", "event_severity", "event_category",
                  "occurrence_time", "restoration_time", "duration_minutes"]
    available_event_cols = [c for c in event_cols if c in df.columns]
    
    if available_event_cols:
        tables.append({
            "id": "event_detail",
            "title": "Event Detail",
            "columns": available_event_cols,
            "rows": df[available_event_cols].head(100).to_dict("records"),
        })
    
    # If no event columns, create a generic table with all columns
    if not tables and not df.empty:
        tables.append({
            "id": "query_results",
            "title": "Query Results",
            "columns": df.columns.tolist(),
            "rows": df.head(100).to_dict("records"),
        })
    
    return tables

def _generate_nl_summary(
    df: pd.DataFrame,
    user_query: str,
    device_id: str,
    period_type: str,
) -> str:
    """Generate a concise NL summary of the results using GPT."""
    try:
        client = openai.OpenAI(api_key=settings.openai_api_key)

        sample = df.head(30).to_csv(index=False) if not df.empty else "No data"

        prompt = f"""You are an energy data analyst. Summarize the following meter data results
in 3-5 clear sentences for a utility operations team.

Original question: "{user_query}"
Device: {device_id}
Period: {period_type}

Key data (CSV):
{sample}

Rules:
- Be specific with numbers and units (kWh, kW, V, A, PF)
- Mention event counts and severities if present
- Flag anything anomalous (very low PF, high events, voltage issues)
- Do NOT mention SQL, databases, or technical implementation
- Do NOT mention which AI or model generated this"""

        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=250,
            timeout=30.0
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # Fallback: return basic summary from data
        print(f"[WARNING] Summary generation failed: {e}")
        if not df.empty:
            return f"Query returned {len(df)} row(s). Columns: {', '.join(df.columns.tolist())}. First row: {df.iloc[0].to_dict()}"
        return "Summary could not be generated."


def _build_intelligent_charts(df: pd.DataFrame, recommendations: list) -> list:
    """
    Build charts based on AI recommendations.
    The AI decides which charts are most useful for the data.
    """
    charts = []
    
    for rec in recommendations:
        try:
            chart_type = rec.get("type", "bar")
            x_col = rec.get("x_column")
            y_cols = rec.get("y_columns", [])
            title = rec.get("title", "Chart")
            
            # Validate columns exist
            if x_col and x_col not in df.columns:
                continue
            if not all(col in df.columns for col in y_cols):
                continue
            
            if chart_type == "metric":
                # Single value metric card
                if y_cols and len(y_cols) > 0:
                    value = df[y_cols[0]].iloc[0] if len(df) > 0 else 0
                    charts.append({
                        "id": f"metric_{y_cols[0]}",
                        "title": title,
                        "type": "metric",
                        "data": {
                            "value": float(value) if pd.notna(value) else 0,
                            "label": y_cols[0]
                        }
                    })
            
            elif chart_type == "bar":
                # Bar chart
                if x_col and y_cols:
                    chart_data = df[[x_col] + y_cols].dropna()
                    if len(chart_data) > 0:
                        datasets = []
                        colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"]
                        for idx, y_col in enumerate(y_cols):
                            datasets.append({
                                "label": y_col,
                                "data": chart_data[y_col].tolist(),
                                "backgroundColor": colors[idx % len(colors)]
                            })
                        
                        charts.append({
                            "id": f"bar_{x_col}",
                            "title": title,
                            "type": "bar",
                            "data": {
                                "labels": chart_data[x_col].astype(str).tolist(),
                                "datasets": datasets
                            }
                        })
            
            elif chart_type == "line":
                # Line chart for time series
                if x_col and y_cols:
                    chart_data = df[[x_col] + y_cols].dropna()
                    if len(chart_data) > 0:
                        datasets = []
                        colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"]
                        for idx, y_col in enumerate(y_cols):
                            datasets.append({
                                "label": y_col,
                                "data": chart_data[y_col].tolist(),
                                "borderColor": colors[idx % len(colors)],
                                "backgroundColor": colors[idx % len(colors)] + "33"  # Add transparency
                            })
                        
                        charts.append({
                            "id": f"line_{x_col}",
                            "title": title,
                            "type": "line",
                            "data": {
                                "labels": chart_data[x_col].astype(str).tolist(),
                                "datasets": datasets
                            }
                        })
            
            elif chart_type == "pie":
                # Pie chart
                if x_col and y_cols and len(y_cols) > 0:
                    chart_data = df[[x_col, y_cols[0]]].dropna()
                    if len(chart_data) > 0:
                        charts.append({
                            "id": f"pie_{x_col}",
                            "title": title,
                            "type": "pie",
                            "data": {
                                "labels": chart_data[x_col].astype(str).tolist(),
                                "datasets": [{
                                    "label": y_cols[0],
                                    "data": chart_data[y_cols[0]].tolist(),
                                    "backgroundColor": [
                                        "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", 
                                        "#EF4444", "#06B6D4", "#EC4899", "#14B8A6"
                                    ]
                                }]
                            }
                        })
        
        except Exception as e:
            print(f"[CHART_BUILDER] Error building chart: {e}")
            continue
    
    return charts


def _build_smart_kpis(df: pd.DataFrame, selected_columns: list) -> list:
    """
    Build KPIs from numeric columns intelligently.
    Focus on aggregate values and key metrics.
    """
    kpis = []
    
    # Get numeric columns that are in selected columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    relevant_numeric = [col for col in numeric_cols if col in selected_columns]
    
    # If we have aggregated data (few rows), show as KPIs
    if len(df) <= 10 and relevant_numeric:
        for col in relevant_numeric[:6]:  # Max 6 KPIs
            try:
                value = df[col].iloc[0] if len(df) == 1 else df[col].sum()
                if pd.notna(value):
                    # Determine unit from column name
                    unit = ""
                    col_lower = col.lower()
                    if 'kwh' in col_lower or 'energy' in col_lower:
                        unit = "kWh"
                    elif 'kw' in col_lower or 'power' in col_lower:
                        unit = "kW"
                    elif 'voltage' in col_lower or 'volt' in col_lower:
                        unit = "V"
                    elif 'current' in col_lower or 'amp' in col_lower:
                        unit = "A"
                    elif 'count' in col_lower or 'total' in col_lower:
                        unit = ""
                    
                    kpis.append({
                        "label": col.replace('_', ' ').title(),
                        "value": float(value),
                        "unit": unit
                    })
            except:
                pass
    
    return kpis


def _build_smart_tables(df: pd.DataFrame, selected_columns: list) -> list:
    """
    Build tables with AI-selected columns.
    Only show the most relevant columns as decided by the AI.
    """
    tables = []
    
    if df.empty:
        return tables
    
    # Use AI-selected columns, fallback to all if none selected
    columns_to_show = selected_columns if selected_columns else df.columns.tolist()
    
    # Ensure selected columns exist in dataframe
    columns_to_show = [col for col in columns_to_show if col in df.columns]
    
    if not columns_to_show:
        columns_to_show = df.columns.tolist()
    
    # Limit to 100 rows for performance
    table_df = df[columns_to_show].head(100)
    
    tables.append({
        "id": "main_results",
        "title": "Data Results",
        "columns": columns_to_show,
        "rows": table_df.to_dict("records"),
    })
    
    return tables
