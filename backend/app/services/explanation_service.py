def generate_explanation(signal_contributions: dict) -> str:
    if not signal_contributions:
        return "Forecast based on historical trends."

    # Remove zero/near-zero signals — they aren't actually driving anything
    filtered = {k: v for k, v in signal_contributions.items() if abs(v) > 0.01}

    if not filtered:
        return "Forecast driven primarily by historical demand patterns."

    sorted_signals = sorted(
        filtered.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    top = sorted_signals[:3]

    explanations = []
    for name, value in top:
        direction = "increase" if value > 0 else "decrease"
        explanations.append(f"{name} driving a {direction}")

    return "Forecast adjusted due to: " + ", ".join(explanations)