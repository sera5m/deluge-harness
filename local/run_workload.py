"""Run a workload file. Director is deepseek-r1:32b. After each step,
bonsai summarizes and Engels writes slots.

  python -m local.run_workload workloads/language.json --workspace ws/lang
"""
import argparse

from local.engels import to_slots, write_slots
from local.loop import call_ollama, iki
from local.prompt import load_prompt, render
from local.roles import DIRECTOR, SUMMARIZER
from local.summarize import summarize
from local.tasks import load_workload, mark, next_open, save_workload
from local.workspace import Workspace

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("workload")
    ap.add_argument("--workspace", default="ws/lang")
    ap.add_argument("--director", default=DIRECTOR)
    ap.add_argument("--summarizer", default=SUMMARIZER)
    args = ap.parse_args()

    ws = Workspace(args.workspace)
    steps = load_workload(args.workload)

    while (step := next_open(steps)) is not None:
        system = render(load_prompt(step["prompt"]),
                        workspace=ws.listing(), task=step["task"])
        turns = [{"role": "system", "content": system},
                 {"role": "user", "content": step["task"]}]
        reply = call_ollama(args.director, "\n".join(
            f"{t['role']}: {t['content']}" for t in turns))
        print(f"[{step['id']}]\n{reply}\n---")
        if "IKI:" in reply:
            q = reply.split("IKI:", 1)[1].strip().splitlines()[0]
            print(iki(q))
        turns.append({"role": "assistant", "content": reply})
        summary = summarize(turns, model=args.summarizer)
        slots = to_slots(summary, model=args.summarizer)
        write_slots(args.workspace, slots, f"engels-{step['id']}.json")
        mark(steps, step["id"], "done")
        save_workload(args.workload, steps)

if __name__ == "__main__":
    main()
