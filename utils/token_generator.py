from datetime import datetime

def generate_token(last_token, department_code="GEN"):
    """
    Generates a token like GEN-20231025-001
    """
    today_str = datetime.now().strftime("%Y%m%d")
    
    if not last_token or today_str not in last_token:
        return f"{department_code}-{today_str}-001"
    
    # Extract the counter part
    try:
        parts = last_token.split('-')
        count = int(parts[-1])
        return f"{department_code}-{today_str}-{count + 1:03d}"
    except Exception:
        return f"{department_code}-{today_str}-001"
