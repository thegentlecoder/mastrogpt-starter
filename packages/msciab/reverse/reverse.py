def reverse(args):
    inp = args.get("input", "")
    out = "Plese provide some input"
    if inp != "":
        out = inp[::-1]
    return { "output": out}
    # return { "output": "reverse" }
