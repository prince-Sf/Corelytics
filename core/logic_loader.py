import json
import os
import logging

logger = logging.getLogger(__name__)


def load_email_logic():
    """
    Load the email logic tree from JSON file.

    Returns:
        dict: The email logic tree structure

    Raises:
        FileNotFoundError: If email_logic_map.json is not found
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "data", "email_logic_map.json")

        if not os.path.exists(json_path):
            raise FileNotFoundError(
                f"email_logic_map.json not found at: {json_path}"
            )

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"✓ Loaded email logic from {json_path}")
        return data

    except FileNotFoundError as e:
        logger.error(f"✗ {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"✗ Invalid JSON in email_logic_map.json: {e}")
        raise


def get_children(node):
    """
    Get children from a node.

    Args:
        node: Node object (dict) or list

    Returns:
        list: List of children, empty list if none
    """
    if isinstance(node, dict):
        return node.get("children", [])
    return []


def get_labels(nodes):
    """
    Extract labels from a list of nodes.

    Args:
        nodes (list): List of node dictionaries

    Returns:
        list: List of label strings
    """
    if isinstance(nodes, list):
        return [node.get("label", "") for node in nodes if node.get("label")]
    return []


def find_child_by_label(node, label):
    """
    Find a child node by its label.
    Handles whitespace and special characters.

    Args:
        node: Parent node (dict or list)
        label (str): Label to search for

    Returns:
        dict: Child node if found, None otherwise
    """
    if isinstance(node, dict):
        node = node.get("children", [])

    if not isinstance(node, list):
        return None

    for child in node:
        if child.get("label", "").strip() == label.strip():
            return child

    return None


def find_node_by_id(node, node_id):
    """
    Find a node by its ID (for future use).

    Args:
        node: Node to search in
        node_id (str): ID to search for

    Returns:
        dict: Node if found, None otherwise
    """
    if node.get("id") == node_id:
        return node

    children = node.get("children", [])
    for child in children:
        result = find_node_by_id(child, node_id)
        if result:
            return result

    return None


def get_node_path(root, target_label):
    """
    Get the path to a node from root.

    Args:
        root: Root node
        target_label (str): Label of target node

    Returns:
        list: Path of labels from root to target, empty if not found
    """

    def search(node, path):
        if node.get("label", "").strip() == target_label.strip():
            return path + [node.get("label", "")]

        for child in node.get("children", []):
            result = search(child, path + [node.get("label", "")])
            if result:
                return result

        return None

    result = search(root, [])
    return result or []