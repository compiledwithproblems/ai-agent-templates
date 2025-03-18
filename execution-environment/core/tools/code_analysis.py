import ast
import json
from typing import Dict, List, Optional
from ..tools import register_tool
from ...utils.logger import setup_logger

logger = setup_logger(__name__)

@register_tool(
    name="analyze_code_structure",
    description="Analyzes Python code structure and returns insights"
)
async def analyze_code_structure(code: str) -> Dict:
    """Analyze Python code structure and return detailed insights."""
    try:
        tree = ast.parse(code)
        analysis = {
            "classes": [],
            "functions": [],
            "imports": [],
            "complexity_indicators": {
                "num_functions": 0,
                "num_classes": 0,
                "lines_of_code": len(code.splitlines()),
            }
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis["classes"].append({
                    "name": node.name,
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    "line_number": node.lineno
                })
                analysis["complexity_indicators"]["num_classes"] += 1
                
            elif isinstance(node, ast.FunctionDef):
                analysis["functions"].append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "line_number": node.lineno
                })
                analysis["complexity_indicators"]["num_functions"] += 1
                
            elif isinstance(node, ast.Import):
                analysis["imports"].extend(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                analysis["imports"].append(f"{node.module}.{node.names[0].name}")
        
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        return {"error": str(e)}

@register_tool(
    name="suggest_improvements",
    description="Suggests code improvements based on analysis"
)
async def suggest_improvements(analysis: Dict) -> List[Dict]:
    """Generate improvement suggestions based on code analysis."""
    suggestions = []
    
    # Check class complexity
    for class_info in analysis["classes"]:
        if len(class_info["methods"]) > 10:
            suggestions.append({
                "type": "class_complexity",
                "class_name": class_info["name"],
                "suggestion": "Consider splitting this class into smaller, more focused classes",
                "reason": f"Class has {len(class_info['methods'])} methods, which might indicate too many responsibilities"
            })
    
    # Check import organization
    if len(analysis["imports"]) > 15:
        suggestions.append({
            "type": "import_organization",
            "suggestion": "Consider organizing imports into logical groups",
            "reason": "Large number of imports might indicate need for better module organization"
        })
    
    # Check function complexity
    if analysis["complexity_indicators"]["num_functions"] > 20:
        suggestions.append({
            "type": "module_complexity",
            "suggestion": "Consider splitting this module into multiple files",
            "reason": "High number of functions might indicate too many responsibilities in one module"
        })
    
    return suggestions

@register_tool(
    name="track_code_changes",
    description="Tracks changes in code structure over time"
)
async def track_code_changes(current_analysis: Dict, previous_analysis: Optional[Dict]) -> Dict:
    """Track and analyze changes between code versions."""
    if not previous_analysis:
        return {"message": "No previous analysis available for comparison"}
    
    changes = {
        "added_classes": [],
        "removed_classes": [],
        "modified_classes": [],
        "added_functions": [],
        "removed_functions": [],
        "complexity_change": {}
    }
    
    # Track class changes
    current_classes = {c["name"] for c in current_analysis["classes"]}
    previous_classes = {c["name"] for c in previous_analysis["classes"]}
    
    changes["added_classes"] = list(current_classes - previous_classes)
    changes["removed_classes"] = list(previous_classes - current_classes)
    
    # Track complexity changes
    for metric, value in current_analysis["complexity_indicators"].items():
        prev_value = previous_analysis["complexity_indicators"].get(metric, 0)
        changes["complexity_change"][metric] = value - prev_value
    
    return changes 