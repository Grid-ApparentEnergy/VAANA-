"""
AI Orchestrator - Intelligent response composition agent
Makes decisions about:
- Response narrative and tone
- Which columns to display in tables
- Whether to create charts and which type
- Data insights and recommendations
"""
import pandas as pd
import openai
from typing import Dict, List, Any
from config.settings import settings
import json


class ResponseDecision:
    """Structured decisions made by the AI orchestrator"""
    def __init__(self):
        self.narrative: str = ""
        self.show_charts: bool = True
        self.chart_recommendations: List[Dict[str, Any]] = []
        self.table_columns: List[str] = []
        self.insights: List[str] = []
        self.tone: str = "professional"  # professional, urgent, informative


class AIOrchestrator:
    """
    Intelligent agent that analyzes data and orchestrates the response.
    Uses GPT to make decisions about presentation and insights.
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    def orchestrate_response(
        self,
        df: pd.DataFrame,
        user_query: str,
        device_id: str,
        period_type: str,
        sql_used: str
    ) -> ResponseDecision:
        """
        Main orchestration method - analyzes data and decides how to present it
        """
        decision = ResponseDecision()
        
        if df is None or df.empty:
            decision.narrative = "I couldn't find any data matching your query. This could mean there are no records for the specified time period or device."
            decision.show_charts = False
            decision.table_columns = []
            return decision
        
        # Analyze the data structure and content
        analysis = self._analyze_data(df, user_query, device_id, period_type, sql_used)
        
        # Get AI decisions on presentation
        decision = self._get_ai_decisions(df, user_query, analysis)
        
        return decision
    
    def _analyze_data(
        self,
        df: pd.DataFrame,
        user_query: str,
        device_id: str,
        period_type: str,
        sql_used: str
    ) -> Dict[str, Any]:
        """Analyze the dataframe to extract key characteristics"""
        analysis = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
            "has_time_series": any(col in df.columns for col in ['timestamp', 'date', 'time', 'occurrence_time', 'period']),
            "has_events": 'event' in ' '.join(df.columns).lower(),
            "has_energy_metrics": any('energy' in col.lower() or 'kwh' in col.lower() for col in df.columns),
            "has_power_metrics": any('power' in col.lower() or 'kw' in col.lower() for col in df.columns),
            "has_voltage": any('voltage' in col.lower() or 'volt' in col.lower() for col in df.columns),
            "has_current": any('current' in col.lower() or 'amp' in col.lower() for col in df.columns),
            "sample_data": df.head(5).to_dict('records'),
            "summary_stats": {}
        }
        
        # Get summary statistics for numeric columns
        for col in analysis["numeric_columns"][:5]:  # Limit to first 5 numeric columns
            try:
                analysis["summary_stats"][col] = {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "mean": float(df[col].mean()),
                    "sum": float(df[col].sum()) if df[col].sum() < 1e10 else None
                }
            except:
                pass
        
        return analysis
    
    def _get_ai_decisions(
        self,
        df: pd.DataFrame,
        user_query: str,
        analysis: Dict[str, Any]
    ) -> ResponseDecision:
        """Use GPT to make intelligent decisions about response presentation"""
        
        prompt = f"""You are an AI agent orchestrating a response to a user's energy data query.
Analyze the data and make intelligent decisions about how to present it.

USER QUERY: "{user_query}"

DATA ANALYSIS:
- Rows: {analysis['row_count']}
- Columns: {', '.join(analysis['columns'])}
- Numeric columns: {', '.join(analysis['numeric_columns'])}
- Has time series: {analysis['has_time_series']}
- Has events: {analysis['has_events']}
- Has energy metrics: {analysis['has_energy_metrics']}
- Has power metrics: {analysis['has_power_metrics']}

SAMPLE DATA (first 3 rows):
{json.dumps(analysis['sample_data'][:3], indent=2, default=str)}

SUMMARY STATISTICS:
{json.dumps(analysis['summary_stats'], indent=2, default=str)}

YOUR TASK:
Make decisions about how to present this data effectively. Respond in JSON format:

{{
  "narrative": "A 3-5 sentence natural response explaining what the data shows, written as if you're an AI assistant talking to the user. Be conversational but professional. Highlight key findings.",
  "tone": "professional|urgent|informative",
  "show_charts": true|false,
  "chart_recommendations": [
    {{
      "type": "bar|line|pie|metric",
      "title": "Chart title",
      "reason": "Why this chart is useful",
      "x_column": "column name for x-axis",
      "y_columns": ["column(s) for y-axis"],
      "priority": 1-3
    }}
  ],
  "table_columns": ["most relevant columns to show in table - max 8 columns"],
  "insights": ["Key insight 1", "Key insight 2"]
}}

GUIDELINES:
- narrative: Write as an AI assistant, use "I found", "The data shows", etc.
- tone: Use "urgent" if there are critical events or anomalies
- show_charts: Only true if visualization adds value (not for single values)
- chart_recommendations: Suggest 1-3 most useful charts, prioritize by importance
- table_columns: Select the most relevant columns (exclude IDs, redundant data)
- insights: Extract 2-3 meaningful patterns or notable findings

Respond ONLY with valid JSON, no other text."""

        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=1000,
                timeout=30.0,
                response_format={"type": "json_object"}
            )
            
            decisions_json = json.loads(response.choices[0].message.content)
            
            # Parse into ResponseDecision object
            decision = ResponseDecision()
            decision.narrative = decisions_json.get("narrative", "")
            decision.tone = decisions_json.get("tone", "professional")
            decision.show_charts = decisions_json.get("show_charts", True)
            decision.chart_recommendations = decisions_json.get("chart_recommendations", [])
            decision.table_columns = decisions_json.get("table_columns", analysis['columns'][:8])
            decision.insights = decisions_json.get("insights", [])
            
            return decision
            
        except Exception as e:
            print(f"[AI_ORCHESTRATOR] Error getting AI decisions: {e}")
            # Fallback to basic decisions
            decision = ResponseDecision()
            decision.narrative = f"I found {analysis['row_count']} records matching your query."
            decision.table_columns = analysis['columns'][:8]
            decision.show_charts = len(analysis['numeric_columns']) > 0
            return decision
