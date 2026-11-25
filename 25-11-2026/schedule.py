from datetime import datetime

def t(s):  # "2:00 PM" -> minutes since midnight
    d = datetime.strptime(s.strip(), "%I:%M %p")
    return d.hour * 60 + d.minute

def pick_slot(slots, duration_min, blocked, latest_end):
    """slots: [(start, end)] strings. blocked: [(start, end)] strings. latest_end: string."""
    blocked = [(t(a), t(b)) for a, b in blocked]
    for a, b in sorted(slots, key=lambda x: t(x[0])):  # earliest start first
        s, e = t(a), t(b)
        if e - s < duration_min:                       continue  # too short
        if e > t(latest_end):                          continue  # too late
        if any(s < be and bs < e for bs, be in blocked): continue  # overlaps a block
        return f"{a} – {b}"                                      # earliest valid slot
    return "NO_AVAILABLE_SLOT"

if __name__ == "__main__":
    slots = [("10:00 AM", "11:00 AM"), ("11:00 AM", "12:00 PM"), ("2:00 PM", "3:00 PM")]
    print(pick_slot(slots, 60, [("10:00 AM", "12:00 PM")], "4:00 PM"))
    print(pick_slot(slots[:2], 60, [("10:00 AM", "12:00 PM")], "4:00 PM"))
    print(pick_slot([("3:30 PM", "4:30 PM")], 60, [], "4:00 PM"))
