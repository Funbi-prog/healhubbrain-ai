def compose_answer(user_msg: str, hits: list):
    # 1) Lead with empathetic framing + 1-sentence direct answer
    lead = (
        "I’ve got you. Here’s the short take:\n"
    )
    # 2) Summarize best snippet first
    best = hits[0]["content"][:280].strip().replace("\n"," ")
    # 3) Middle: concise bullets from other hits
    bullets = []
    for h in hits[1:3]:
        bullets.append(f"• {h['title']}: {h['content'][:200].strip().replace('\n',' ')}")
    mid = "\n".join(bullets)
    # 4) Close with concrete next steps
    steps = (
        "\nNext steps I can take for you now:\n"
        "1) Match you to a roundtable topic.\n"
        "2) Draft a check-in plan (DM/SMS template).\n"
        "3) Pull resources you qualify for.\n"
        "Tell me which number to start with."
    )
    return f"{lead}{best}\n\n{mid}\n{steps}"
