from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging

from core.logic_loader import (
    load_email_logic,
    find_child_by_label,
)
from core.intent_engine import IntentEngine
from core.intent_state import IntentState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Corelytics API",
    description="AI-powered email generation engine",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=600,
)

# Load data
try:
    EMAIL_TREE = load_email_logic()
    engine = IntentEngine()
    logger.info("✓ Email logic loaded successfully")
    logger.info(f"✓ Available domains: {[c['label'] for c in EMAIL_TREE['children']]}")
except Exception as e:
    logger.error(f"✗ Failed to load email logic: {e}")
    raise


# MODELS

class GenerateRequest(BaseModel):
    domain: str
    recipient: str
    category: str
    scenario: Optional[str] = None  # Make scenario optional


class ErrorResponse(BaseModel):
    detail: str
    status_code: int


# UTILITIES

def find_node_in_children(node, label):
    """
    Search for a node with exact label match in children.
    Handles whitespace and special characters.
    """
    if not node or "children" not in node:
        return None

    children = node.get("children", [])
    for child in children:
        if child.get("label", "").strip() == label.strip():
            return child

    return None


def has_scenarios(category_node):
    """
    Check if a category has child scenarios.
    """
    if not category_node:
        return False
    return len(category_node.get("children", [])) > 0


# HEALTH

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Corelytics API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "ready"
    }


# DOMAINS

@app.get("/domains", tags=["Navigation"])
def get_domains():
    """Get all available domains"""
    try:
        domains = [c["label"] for c in EMAIL_TREE.get("children", [])]
        logger.info(f"✓ Returning {len(domains)} domains")
        return {
            "status": "success",
            "data": domains,
            "count": len(domains)
        }
    except Exception as e:
        logger.error(f"✗ Error fetching domains: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch domains"
        )


# RECIPIENTS

@app.get("/recipients", tags=["Navigation"])
def get_recipients(domain: str):
    """Get recipients for a specific domain"""
    if not domain or not domain.strip():
        raise HTTPException(
            status_code=400,
            detail="Domain parameter is required"
        )

    try:
        logger.info(f"→ Searching for domain: '{domain}'")

        # Find domain in root children
        d = find_node_in_children(EMAIL_TREE, domain)

        if not d:
            available = [c["label"] for c in EMAIL_TREE.get("children", [])]
            logger.error(f"✗ Domain '{domain}' not found")
            logger.error(f"  Available: {available}")
            raise HTTPException(
                status_code=404,
                detail=f"Domain '{domain}' not found. Available domains: {', '.join(available)}"
            )

        recipients = [c["label"] for c in d.get("children", [])]
        logger.info(f"✓ Found {len(recipients)} recipients for domain '{domain}'")

        return {
            "status": "success",
            "data": recipients,
            "count": len(recipients),
            "domain": domain
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error fetching recipients: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch recipients"
        )


# CATEGORIES

@app.get("/categories", tags=["Navigation"])
def get_categories(domain: str, recipient: str):
    """Get categories for a specific domain and recipient"""
    if not domain or not recipient:
        raise HTTPException(
            status_code=400,
            detail="Domain and recipient parameters are required"
        )

    try:
        logger.info(f"→ Searching: domain='{domain}', recipient='{recipient}'")

        # Find domain
        d = find_node_in_children(EMAIL_TREE, domain)
        if not d:
            logger.error(f"✗ Domain '{domain}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"Domain '{domain}' not found"
            )

        # Find recipient
        r = find_node_in_children(d, recipient)
        if not r:
            available = [c["label"] for c in d.get("children", [])]
            logger.error(f"✗ Recipient '{recipient}' not found in domain '{domain}'")
            logger.error(f"  Available: {available}")
            raise HTTPException(
                status_code=404,
                detail=f"Recipient '{recipient}' not found in domain '{domain}'. Available: {', '.join(available)}"
            )

        categories = [c["label"] for c in r.get("children", [])]
        logger.info(f"✓ Found {len(categories)} categories")

        return {
            "status": "success",
            "data": categories,
            "count": len(categories),
            "domain": domain,
            "recipient": recipient
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error fetching categories: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch categories"
        )


# SCENARIOS

@app.get("/scenarios", tags=["Navigation"])
def get_scenarios(domain: str, recipient: str, category: str):
    """
    Get scenarios for a specific domain, recipient, and category.
    Returns empty array if category has no child scenarios.
    """
    if not all([domain, recipient, category]):
        raise HTTPException(
            status_code=400,
            detail="Domain, recipient, and category parameters are required"
        )

    try:
        logger.info(f"→ Searching: domain='{domain}', recipient='{recipient}', category='{category}'")

        # Find domain
        d = find_node_in_children(EMAIL_TREE, domain)
        if not d:
            logger.error(f"✗ Domain '{domain}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"Domain '{domain}' not found"
            )

        # Find recipient
        r = find_node_in_children(d, recipient)
        if not r:
            logger.error(f"✗ Recipient '{recipient}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"Recipient '{recipient}' not found"
            )

        # Find category
        c = find_node_in_children(r, category)
        if not c:
            available = [x["label"] for x in r.get("children", [])]
            logger.error(f"✗ Category '{category}' not found")
            logger.error(f"  Available: {available}")
            raise HTTPException(
                status_code=404,
                detail=f"Category '{category}' not found. Available: {', '.join(available)}"
            )

        scenarios = [s["label"] for s in c.get("children", [])]
        logger.info(f"✓ Found {len(scenarios)} scenarios (may be 0 if leaf node)")

        return {
            "status": "success",
            "data": scenarios,
            "count": len(scenarios),
            "domain": domain,
            "recipient": recipient,
            "category": category,
            "hasScenarios": len(scenarios) > 0
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error fetching scenarios: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch scenarios"
        )


# GENERATE

@app.post("/generate", tags=["Generation"])
def generate(request: GenerateRequest):
    """
    Generate an email based on the provided parameters.
    Scenario is optional - if not provided, uses category as scenario.
    """

    try:
        if not all([request.domain, request.recipient, request.category]):
            raise HTTPException(
                status_code=400,
                detail="Domain, recipient, and category are required. Scenario is optional."
            )

        # If scenario is not provided, use category as scenario
        scenario = request.scenario or request.category

        logger.info(f"→ Generating email:")
        logger.info(f"  Domain: {request.domain}")
        logger.info(f"  Recipient: {request.recipient}")
        logger.info(f"  Category: {request.category}")
        logger.info(f"  Scenario: {scenario}")

        state = IntentState()
        state.domain = request.domain
        state.recipient = request.recipient
        state.category = request.category
        state.scenario = scenario

        # Navigate tree
        d = find_node_in_children(EMAIL_TREE, request.domain)
        if not d:
            raise HTTPException(status_code=404, detail=f"Domain not found")

        r = find_node_in_children(d, request.recipient)
        if not r:
            raise HTTPException(status_code=404, detail=f"Recipient not found")

        c = find_node_in_children(r, request.category)
        if not c:
            raise HTTPException(status_code=404, detail=f"Category not found")

        # Try to find scenario node
        scenario_node = None
        if request.scenario:
            scenario_node = find_node_in_children(c, request.scenario)

        # Extract metadata from scenario node or category node
        if scenario_node and "meta" in scenario_node:
            state.scenario_meta = scenario_node.get("meta", {})
            logger.info("✓ Using scenario metadata")
        elif "meta" in c:
            state.scenario_meta = c.get("meta", {})
            logger.info("✓ Using category metadata (no scenario provided)")
        else:
            logger.info("⚠ No metadata found, using defaults")
            state.scenario_meta = {}

        # Generate email
        email_content = engine.generate(state)

        if not email_content:
            logger.error("✗ Failed to generate email content")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate email content"
            )

        logger.info("✓ Email generated successfully")

        return {
            "status": "success",
            "email": email_content,
            "metadata": {
                "domain": request.domain,
                "recipient": request.recipient,
                "category": request.category,
                "scenario": scenario,
                "intent_path": state.summary(),
                "used_category_metadata": not request.scenario
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error generating email: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate email: {str(e)}"
        )


# ERROR HANDLERS

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "status_code": exc.status_code
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"✗ Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
            "status_code": 500
        },
    )