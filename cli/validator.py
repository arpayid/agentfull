import argparse
import sys
import os
import re
import json
import yaml

# Unicode Emojis and shortcode patterns
EMOJI_PATTERN = re.compile(
    r'[\U0001F300-\U0001F5FF]'
    r'|[\U0001F600-\U0001F64F]'
    r'|[\U0001F680-\U0001F6FF]'
    r'|[\u2600-\u27BF]'
    r'|[\U0001F900-\U0001F9FF]'
    r'|:[a-zA-Z0-9_+ -]+:'
)
HEADER_PATTERN = re.compile(r'^\s*#+\s+\S+', re.MULTILINE)
SEPARATOR_PATTERN = re.compile(r'^\s*\|?\s*:?-+:?\s*\|(?:\s*:?-+:?\s*\|)*\s*$')

SECRET_PATTERNS = {
    "OpenAI API Key": re.compile(r'\bsk-[a-zA-Z0-9]{48}\b'),
    "GitHub Token": re.compile(r'\b(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}\b'),
    "Generic Credentials Assignment": re.compile(r'(?i)(api[-_]?key|secret|token|password|passwd|auth)\s*[:=]\s*[\'"]([a-zA-Z0-9_\-\.\~]{8,})[\'"]')
}

def check_rule_02(agent_outputs: list[str]) -> dict:
    """Validate Rule 02: Emojis, headers, tables present in outputs."""
    combined_text = "\n".join(agent_outputs)
    
    # Check emojis
    has_emoji = bool(EMOJI_PATTERN.search(combined_text))
    
    # Check headers
    has_header = bool(HEADER_PATTERN.search(combined_text))
    
    # Check tables
    lines = combined_text.splitlines()
    table_lines = [l for l in lines if '|' in l]
    has_table = False
    if len(table_lines) >= 2:
        has_table = any(SEPARATOR_PATTERN.match(l) for l in table_lines)
        
    passed = has_emoji and has_header and has_table
    
    details = []
    if not has_emoji:
        details.append("Missing emojis")
    if not has_header:
        details.append("Missing markdown headers")
    if not has_table:
        details.append("Missing markdown tables")
        
    return {
        "passed": passed,
        "has_emoji": has_emoji,
        "has_header": has_header,
        "has_table": has_table,
        "details": details
    }

def check_rule_10(all_texts: list[str]) -> dict:
    """Validate Rule 10: Check if any output contains hardcoded secrets."""
    secrets_found = []
    for text in all_texts:
        for name, pattern in SECRET_PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                # If it's a tuple (generic assignment), get the matched value or assignment
                for m in matches:
                    if isinstance(m, tuple):
                        secrets_found.append(f"{name} ({m[0]})")
                    else:
                        secrets_found.append(name)
                        
    # Deduplicate
    secrets_found = list(set(secrets_found))
    passed = len(secrets_found) == 0
    return {
        "passed": passed,
        "secrets": secrets_found
    }

def check_rule_13(tool_calls: list[dict]) -> dict:
    """Validate Rule 13: Detect infinite loops (identical consecutive tool calls)."""
    if len(tool_calls) < 2:
        return {"passed": True, "loops": []}
        
    def normalize_args(args):
        if isinstance(args, dict):
            return json.dumps(args, sort_keys=True)
        return str(args)
        
    normalized = []
    for tc in tool_calls:
        name = tc.get("name", "")
        args = normalize_args(tc.get("arguments", ""))
        normalized.append((name, args))
        
    loops = []
    run_length = 1
    for i in range(1, len(normalized)):
        if normalized[i] == normalized[i-1]:
            run_length += 1
            if run_length >= 3:
                loops.append({
                    "tool": normalized[i][0],
                    "arguments": normalized[i][1],
                    "consecutive_calls": run_length
                })
        else:
            run_length = 1
            
    passed = len(loops) == 0
    return {
        "passed": passed,
        "loops": loops
    }

def check_rule_21(log_data: dict, task_type: str = "coding", custom_limit: int = None) -> dict:
    """Validate Rule 21: Financial token budgeting (alert if token count > limits)."""
    limits = {
        "file_search": 100000,
        "coding": 500000,
        "debugging": 1000000
    }
    limit = custom_limit if custom_limit is not None else limits.get(task_type, 500000)
    
    total_tokens = 0
    
    if isinstance(log_data, dict):
        # 1. Try to read from top-level telemetry
        telemetry = log_data.get("telemetry", {})
        if isinstance(telemetry, dict):
            # Check metrics
            metrics = telemetry.get("metrics", {})
            if isinstance(metrics, dict):
                for k in ["total_tokens", "tokens_total", "tokens"]:
                    if k in metrics:
                        total_tokens = metrics[k]
                        break
            if not total_tokens:
                for k in ["total_tokens", "tokens_total", "tokens"]:
                    if k in telemetry:
                        total_tokens = telemetry[k]
                        break
                        
        # 2. Check steps and aggregate token usage
        steps_tokens = 0
        steps = log_data.get("steps", [])
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict):
                    usage = step.get("token_usage") or step.get("tokens")
                    if isinstance(usage, dict):
                        steps_tokens += usage.get("total") or usage.get("total_tokens") or 0
                    elif isinstance(usage, (int, float)):
                        steps_tokens += usage
        if steps_tokens > total_tokens:
            total_tokens = steps_tokens
            
    elif isinstance(log_data, list):
        # Flat list of steps
        for step in log_data:
            if isinstance(step, dict):
                usage = step.get("token_usage") or step.get("tokens")
                if isinstance(usage, dict):
                    total_tokens += usage.get("total") or usage.get("total_tokens") or 0
                elif isinstance(usage, (int, float)):
                    total_tokens += usage
                    
    passed = total_tokens <= limit
    return {
        "passed": passed,
        "total_tokens": int(total_tokens),
        "limit": limit,
        "task_type": task_type
    }

def check_rule_24(log_data: dict) -> dict:
    """Validate Rule 24: Telemetry generation."""
    has_telemetry = False
    details = []
    
    if isinstance(log_data, dict):
        telemetry = log_data.get("telemetry")
        if telemetry and isinstance(telemetry, dict):
            has_telemetry = True
            # Validate standard keys
            required_keys = ["session", "metrics"]
            missing = [k for k in required_keys if k not in telemetry]
            if missing:
                details.append(f"Telemetry missing fields: {', '.join(missing)}")
        else:
            details.append("No top-level 'telemetry' key found in JSON/YAML object")
    else:
        # Flat list, look for telemetry step or session step
        for step in log_data:
            if isinstance(step, dict) and (step.get("role") == "telemetry" or "telemetry" in step):
                has_telemetry = True
                break
        if not has_telemetry:
            details.append("No telemetry block or step found in list log")
            
    return {
        "passed": has_telemetry and len(details) == 0,
        "has_telemetry": has_telemetry,
        "details": details
    }

def extract_log_elements(log_data) -> tuple[list[str], list[str], list[dict]]:
    """Extract agent outputs, all texts, and tool calls from log data."""
    agent_outputs = []
    all_texts = []
    tool_calls = []
    
    steps = []
    if isinstance(log_data, dict):
        steps = log_data.get("steps", [])
    elif isinstance(log_data, list):
        steps = log_data
        
    for step in steps:
        if not isinstance(step, dict):
            continue
            
        role = step.get("role", "")
        content = step.get("content", "")
        thought = step.get("thought", "")
        
        # Add to all text to scan for secrets
        if content:
            all_texts.append(str(content))
        if thought:
            all_texts.append(str(thought))
            
        # Collect agent outputs (only from agent role)
        if role in ("agent", "assistant"):
            if content:
                agent_outputs.append(str(content))
            if thought:
                agent_outputs.append(str(thought))
                
        # Collect tool calls
        t_calls = step.get("tool_calls", [])
        if isinstance(t_calls, list):
            for tc in t_calls:
                if isinstance(tc, dict):
                    tool_calls.append(tc)
                    all_texts.append(tc.get("name", ""))
                    all_texts.append(str(tc.get("arguments", "")))
        elif isinstance(t_calls, dict):
            tool_calls.append(t_calls)
            all_texts.append(t_calls.get("name", ""))
            all_texts.append(str(t_calls.get("arguments", "")))
            
    return agent_outputs, all_texts, tool_calls

def validate_trajectory(log_data: dict | list, task_type: str = "coding", custom_limit: int = None) -> dict:
    agent_outputs, all_texts, tool_calls = extract_log_elements(log_data)
    
    r02 = check_rule_02(agent_outputs)
    r10 = check_rule_10(all_texts)
    r13 = check_rule_13(tool_calls)
    r21 = check_rule_21(log_data, task_type, custom_limit)
    r24 = check_rule_24(log_data)
    
    all_passed = r02["passed"] and r10["passed"] and r13["passed"] and r21["passed"] and r24["passed"]
    
    return {
        "all_passed": all_passed,
        "rules": {
            "Rule 02": r02,
            "Rule 10": r10,
            "Rule 13": r13,
            "Rule 21": r21,
            "Rule 24": r24
        }
    }

def print_report(results: dict):
    rules = results["rules"]
    
    def status_emoji(passed):
        return "🟢 PASS" if passed else "🔴 FAIL"
        
    print("# 🧠 Agentfull Trajectory Validation Report\n")
    print("## 📋 Summary")
    print("| Principle | Status | Details |")
    print("| :--- | :--- | :--- |")
    
    # Rule 02 details
    r02_desc = "Emojis, headers, and tables present." if rules["Rule 02"]["passed"] else f"Missing: {', '.join(rules['Rule 02']['details'])}"
    print(f"| **Rule 02: Comm Style** | {status_emoji(rules['Rule 02']['passed'])} | {r02_desc} |")
    
    # Rule 10 details
    r10_desc = "No hardcoded secrets detected." if rules["Rule 10"]["passed"] else f"Secrets found: {', '.join(rules['Rule 10']['secrets'])}"
    print(f"| **Rule 10: Security** | {status_emoji(rules['Rule 10']['passed'])} | {r10_desc} |")
    
    # Rule 13 details
    r13_desc = "No infinite loops detected." if rules["Rule 13"]["passed"] else f"Detected {len(rules['Rule 13']['loops'])} loops."
    print(f"| **Rule 13: Loops** | {status_emoji(rules['Rule 13']['passed'])} | {r13_desc} |")
    
    # Rule 21 details
    r21 = rules["Rule 21"]
    r21_desc = f"Token count: {r21['total_tokens']:,} / limit: {r21['limit']:,} ({r21['task_type']})."
    print(f"| **Rule 21: Budgeting** | {status_emoji(r21['passed'])} | {r21_desc} |")
    
    # Rule 24 details
    r24_desc = "Telemetry generation detected." if rules["Rule 24"]["passed"] else f"Telemetry check failed: {', '.join(rules['Rule 24']['details'])}"
    print(f"| **Rule 24: Telemetry** | {status_emoji(rules['Rule 24']['passed'])} | {r24_desc} |")
    
    print("\n## 🔍 Detailed Results")
    
    print("### 💬 Rule 02 - Communication Style")
    print(f"- **Emojis Present**: {'yes 🟢' if rules['Rule 02']['has_emoji'] else 'no 🔴'}")
    print(f"- **Headers Present**: {'yes 🟢' if rules['Rule 02']['has_header'] else 'no 🔴'}")
    print(f"- **Tables Present**: {'yes 🟢' if rules['Rule 02']['has_table'] else 'no 🔴'}")
    
    print("\n### 🛡️ Rule 10 - Security Boundaries")
    if rules["Rule 10"]["passed"]:
        print("- 🟢 No credentials or keys leaked in outputs or commands.")
    else:
        print("- 🔴 WARNING: Found potential hardcoded credentials:")
        for s in rules["Rule 10"]["secrets"]:
            print(f"  - Detected type: {s}")
            
    print("\n### 🔄 Rule 13 - Behavioral Guardrails (Loops)")
    if rules["Rule 13"]["passed"]:
        print("- 🟢 No consecutive identical tool calls (infinite loops).")
    else:
        print("- 🔴 WARNING: Infinite loops detected:")
        for l in rules["Rule 13"]["loops"]:
            print(f"  - Tool '{l['tool']}' was called consecutively {l['consecutive_calls']} times with arguments: `{l['arguments']}`")
            
    print("\n### 🪙 Rule 21 - Token Budgeting")
    if r21["passed"]:
        print(f"- 🟢 Usage is within bounds. Total tokens: {r21['total_tokens']:,} <= Limit: {r21['limit']:,}")
    else:
        print(f"- 🔴 OVER BUDGET: Total tokens: {r21['total_tokens']:,} > Limit: {r21['limit']:,}")
        
    print("\n### 📊 Rule 24 - Performance Telemetry")
    if rules["Rule 24"]["passed"]:
        print("- 🟢 Telemetry record structure is valid.")
    else:
        print("- 🔴 Telemetry validation failed:")
        for detail in rules["Rule 24"]["details"]:
            print(f"  - {detail}")
            
    if results["all_passed"]:
        print("\n🟢 **VALIDATION SUCCESSFUL**: All Agentfull Core Principles followed.")
    else:
        print("\n🔴 **VALIDATION FAILED**: Some Agentfull Core Principles violated.")

def main():
    parser = argparse.ArgumentParser(description="Agentfull Trajectory Log Validator CLI")
    parser.add_argument("log_file", help="Path to the trajectory log file (JSON or YAML)")
    parser.add_argument("--task-type", choices=["file_search", "coding", "debugging"], default="coding",
                        help="Task type for token budgeting check (default: coding)")
    parser.add_argument("--token-limit", type=int, help="Override default token limit")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.log_file):
        print(f"Error: Log file not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(args.log_file, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Failed to read file {args.log_file}: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Attempt JSON first, then YAML
    try:
        log_data = json.loads(content)
    except json.JSONDecodeError:
        try:
            log_data = yaml.safe_load(content)
        except Exception as e:
            print(f"Error: Failed to parse {args.log_file} as JSON or YAML: {e}", file=sys.stderr)
            sys.exit(1)
            
    if not isinstance(log_data, (dict, list)):
        print("Error: Trajectory log must be a JSON/YAML object or list", file=sys.stderr)
        sys.exit(1)
        
    results = validate_trajectory(log_data, task_type=args.task_type, custom_limit=args.token_limit)
    print_report(results)
    
    if not results["all_passed"]:
        sys.exit(2)

if __name__ == "__main__":
    main()
