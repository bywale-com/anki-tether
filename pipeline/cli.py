from __future__ import annotations

import argparse
import json
import sys

from pipeline.approve import set_status
from pipeline.coverage import coverage
from pipeline.generate import generate
from pipeline.ingest import ingest
from pipeline.publish import publish
from pipeline.validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="COIS-1020 content pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest")
    p_ing.add_argument("--force", action="store_true")

    p_gen = sub.add_parser("generate")
    p_gen.add_argument("--no-ai", action="store_true")

    p_val = sub.add_parser("validate")
    p_val.add_argument("--compile-csharp", action="store_true")

    sub.add_parser("coverage")

    p_ap = sub.add_parser("approve")
    p_ap.add_argument("--ids", nargs="*")
    p_ap.add_argument("--high-confidence", action="store_true")
    p_ap.add_argument("--reject", action="store_true")

    p_pub = sub.add_parser("publish")
    p_pub.add_argument("--url")
    p_pub.add_argument("--token")

    p_run = sub.add_parser("run")
    p_run.add_argument("--force", action="store_true")
    p_run.add_argument("--no-ai", action="store_true")
    p_run.add_argument("--approve-high-confidence", action="store_true")
    p_run.add_argument("--publish", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd == "ingest":
        result = ingest(force=args.force)
        print(json.dumps(result, indent=2))
        if result["failures"]:
            return 1
    elif args.cmd == "generate":
        cards = generate(include_ai=not args.no_ai)
        print(json.dumps({"cards": len(cards)}, indent=2))
    elif args.cmd == "validate":
        print(json.dumps(validate(compile_csharp=args.compile_csharp), indent=2))
    elif args.cmd == "coverage":
        report = coverage()
        print(json.dumps({"sections": report["sections"], "covered": report["covered"],
                          "unaddressed": len(report["unaddressed"])}, indent=2))
    elif args.cmd == "approve":
        if not args.ids and not args.high_confidence:
            p_ap.error("select card IDs or use --high-confidence")
        status = "rejected" if args.reject else "approved"
        print(json.dumps(set_status(args.ids, status, high_confidence_only=args.high_confidence), indent=2))
    elif args.cmd == "publish":
        print(json.dumps(publish(url=args.url, token=args.token), indent=2))
    elif args.cmd == "run":
        result = ingest(force=args.force)
        print(json.dumps(result, indent=2))
        if result["failures"]:
            return 1
        cards = generate(include_ai=not args.no_ai)
        print(json.dumps({"cards": len(cards)}, indent=2))
        print(json.dumps(validate(), indent=2))
        cov = coverage()
        print(json.dumps({"covered": cov["covered"], "unaddressed": len(cov["unaddressed"])}, indent=2))
        if args.approve_high_confidence:
            print(json.dumps(set_status(None, "approved", high_confidence_only=True), indent=2))
        if args.publish:
            print(json.dumps(publish(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
