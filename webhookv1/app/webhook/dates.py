from datetime import datetime
from datetime import timezone

def convert_timestamp(timestamp_str):
    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    day = timestamp.strftime("%d")
    suffix = "th" if 11 <= int(day) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(int(day) % 10, "th")
    formatted_date = timestamp.strftime(f"%d{suffix} %B %Y - %I:%M %p UTC")
    return formatted_date

# def get_day_of_month_suffix(n):
#     if not 1 <= n <= 31:
#         raise ValueError("illegal day of month: {}".format(n))
#     if 11 <= n <= 13:
#         return "th"
#     if n % 10 == 1:
#         return "st"
#     elif n % 10 == 2:
#         return "nd"
#     elif n % 10 == 3:
#         return "rd"
#     else:
#         return "th"