def detect_security_alert(stats):

    alert = 0

    reasons = []


    if stats["connections"] > 10:
        alert = 1
        reasons.append(f"High number of connections is: {stats['connections']}")


    if stats["tcp"] > 80:
        alert = 1
        reasons.append(f"High TCP connections is: {state['tcp']}")


    if stats["download"] > 5000:
        alert = 1
        reasons.append(f"High download traffic is: {state['download']}")

    if stats["upload"] > 2000:
        alert = 1
        reasons.append(f"High upload traffic is: {state['upload']}")

    return alert, reasons