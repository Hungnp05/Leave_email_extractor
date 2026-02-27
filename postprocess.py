import json
from datetime import datetime
from dateutil.parser import parse

def postprocess_phot5_output(raw_output: str, reference_date=None) -> dict:
    if reference_date is None:
        reference_date = datetime.now()

    try:
        # Parse JSON từ model
        data = json.loads(raw_output)
        print("[postprocess] Raw JSON:", data)

        # Chuẩn hóa leave_periods
        periods = data.get("leave_periods", [])
        for period in periods:
            # Chuẩn hóa start_date / end_date nếu là string
            for key in ["start_date", "end_date"]:
                val = period.get(key)
                if isinstance(val, str) and val.strip():
                    try:
                        dt = parse(val, fuzzy=True, dayfirst=True)
                        period[key] = dt.strftime("%Y-%m-%d")
                    except Exception as e:
                        print(f"[postprocess] Parse date fail for {key}: {val} → {str(e)}")
                        period[key] = ""
                else:
                    period[key] = ""

            period["start_session"] = period.get("start_session", "full_day").lower()
            period["end_session"] = period.get("end_session", "full_day").lower()

        result = {
            "employee_id": data.get("employee_id", ""),
            "employee_name": data.get("employee_name", ""),
            "leave_periods": periods
        }

        print("[postprocess] Final output:", result)
        return result

    except json.JSONDecodeError as e:
        print(f"[postprocess] JSON parse error: {str(e)}")
        return {"error": "Invalid JSON from model", "raw": raw_output}
    except Exception as e:
        print(f"[postprocess] General error: {str(e)}")
        return {"error": str(e), "raw": raw_output}