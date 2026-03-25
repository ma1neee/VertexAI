import json
from typing import Dict, Any
from src.core.agent import agent
from src.core import prompts


async def analyze_risks_and_opportunities(text: str) -> Dict[str, Any]:
    """Анализирует текст на наличие рисков и возможностей"""
    system_prompt = prompts.NLP_ANALYSIS_PROMPT
    truncated_text = text[:5000] if len(text) > 5000 else text

    try:
        response = await agent.request(
            chat_id="nlp-analysis-chat",
            message=f"Проанализируй текст финансового отчета:\n\n{truncated_text}",
            system=system_prompt
        )

        if response and "content" in response:
            content = response["content"]
            try:
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    result = json.loads(json_str)
                    return {
                        "risks": result.get("risks", []),
                        "opportunities": result.get("opportunities", []),
                        "summary": result.get("summary", "")
                    }
            except json.JSONDecodeError:
                pass

            return {
                "risks": [],
                "opportunities": [],
                "summary": content
            }
    except Exception as e:
        print(f"NLP analysis error: {e}")

    return {
        "risks": [],
        "opportunities": [],
        "summary": "NLP анализ временно недоступен"
    }