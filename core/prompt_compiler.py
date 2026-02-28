"""
Prompt Compiler v2.0
High-realism behavioral brief generator.
Designed to suppress generic AI patterns and enforce situational authenticity.
"""

import logging

logger = logging.getLogger(__name__)


class PromptCompiler:
    """
    Converts structured intent into a psychologically grounded
    instruction brief that drives natural, high-specificity email output.
    """

    @staticmethod
    def compile_intent_brief(state) -> str:
        """
        Compile a detailed prompt brief from the intent state.

        Args:
            state (IntentState): The intent state to compile

        Returns:
            str: The compiled prompt brief
        """
        meta = state.scenario_meta or {}

        intent_focus = meta.get("intent_focus", state.scenario)
        context_hint = meta.get("context_hint", "")
        pressure = meta.get("pressure", "normal")
        tone_hint = meta.get("tone_hint", "Professional and appropriate.")

        archetype = PromptCompiler._infer_archetype(intent_focus, state.scenario)
        archetype_guidance = PromptCompiler._archetype_guidance(archetype)
        urgency_guidance = PromptCompiler._urgency_guidance(pressure)
        specificity_instruction = PromptCompiler._specificity_enforcement()
        anti_generic_block = PromptCompiler._anti_generic_rules()
        embodiment_block = PromptCompiler._embodiment_instruction()

        brief = f"""
You are writing a real email as a real person in a real situation.

You are NOT an AI.
You are NOT generating a template.
You are NOT writing a textbook example.

Recipient Role: {state.recipient}
Professional Context: {state.domain}
Situation: {state.scenario}

Communication Archetype:
{archetype}

Core Purpose:
{intent_focus}

Context Background:
{context_hint if context_hint else "The situation is practical and real, not hypothetical."}

Behavioral Guidance:
{archetype_guidance}

Tone Guidance:
{tone_hint}

Urgency Guidance:
{urgency_guidance}

{embodiment_block}

{specificity_instruction}

{anti_generic_block}

Structural Expectations:
- Include a subject line
- Use 3–4 meaningful paragraphs
- Each paragraph must add new information
- End with a natural sign-off appropriate to the context
- Do NOT use placeholders like [Your Name]
- Do NOT overexplain
- Do NOT repeat labels like domain or category
- Do NOT sound polished to the point of artificiality

Write the complete email now.
""".strip()

        logger.debug(f"Compiled prompt brief for: {state.summary()}")
        return brief

    # ---------- Archetype Logic ---------- #

    @staticmethod
    def _infer_archetype(intent_focus: str, scenario: str) -> str:
        """Infer communication archetype from intent and scenario."""
        text = f"{intent_focus} {scenario}".lower()

        if "apology" in text:
            return "Accountability / Apology"
        if "clarify" in text:
            return "Clarification Seeking"
        if "request" in text:
            return "Direct Request"
        if "complaint" in text or "issue" in text:
            return "Problem Reporting"
        if "update" in text:
            return "Status Update"
        if "proposal" in text or "investment" in text:
            return "Opportunity Pitch"
        if "appointment" in text or "meeting" in text:
            return "Personal Scheduling Request"
        return "Professional Communication"

    @staticmethod
    def _archetype_guidance(archetype: str) -> str:
        """Get behavioral guidance for the archetype."""
        mapping = {
            "Accountability / Apology":
                "Acknowledge responsibility clearly. Avoid defensiveness. Show corrective intent.",
            "Clarification Seeking":
                "Specify exactly what is unclear. Show that effort was already made.",
            "Direct Request":
                "State the request early. Avoid excessive justification.",
            "Problem Reporting":
                "Describe the issue factually. Avoid emotional exaggeration.",
            "Status Update":
                "Summarize current status efficiently. Highlight next steps.",
            "Opportunity Pitch":
                "Avoid hype. Be grounded. Show strategic relevance to the recipient.",
            "Personal Scheduling Request":
                "Be practical. Mention availability windows realistically.",
            "Professional Communication":
                "Be clear, purposeful, and context-aware."
        }

        return mapping.get(archetype, mapping["Professional Communication"])

    @staticmethod
    def _urgency_guidance(pressure: str) -> str:
        """Get urgency guidance based on pressure level."""
        if pressure == "high":
            return "There is time sensitivity. Reflect urgency respectfully without sounding panicked."
        if pressure == "low":
            return "There is no urgency. Keep the tone calm and unpressured."
        return "Normal professional urgency."

    @staticmethod
    def _specificity_enforcement() -> str:
        """Get specificity enforcement instructions."""
        return """
Specificity Requirement:
- Include at least one concrete detail (timeframe, example, constraint, or prior action taken)
- Avoid vague phrases like "recently", "exciting opportunity", "some concerns"
- Replace general claims with grounded statements
"""

    @staticmethod
    def _anti_generic_rules() -> str:
        """Get anti-generic language rules."""
        return """
Forbidden Generic Phrases:
- "I hope this message finds you well"
- "This email is regarding"
- "I would like to bring to your attention"
- "Exciting opportunity"
- "Kindly do the needful"
- Overly polished marketing language

If a sentence sounds like a template, rewrite it.
"""

    @staticmethod
    def _embodiment_instruction() -> str:
        """Get embodiment instruction."""
        return """
Embodiment Instruction:
Write from the perspective of someone who has actually experienced this situation.
There should be mild natural imperfection in tone.
Do not sound like a formal announcement.
"""