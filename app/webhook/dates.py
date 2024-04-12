def get_day_of_month_suffix(n):
    if not 1 <= n <= 31:
        raise ValueError("illegal day of month: {}".format(n))
    if 11 <= n <= 13:
        return "th"
    if n % 10 == 1:
        return "st"
    elif n % 10 == 2:
        return "nd"
    elif n % 10 == 3:
        return "rd"
    else:
        return "th"
