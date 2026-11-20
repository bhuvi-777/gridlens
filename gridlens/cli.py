"""Command-line interface for GridLens."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from .analysis import compute_intervals
from .events import detect_events
from .generator import apply_event, sine_wave
from .loaders import load
from .reports import write_report
from .standards import check_en50160, check_ieee519_voltage


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def _build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="gridlens")
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=_Parser
    )

    analyze = subparsers.add_parser("analyze", help="Analyze a waveform file")
    analyze.add_argument("file")
    analyze.add_argument("--standard", choices=["en50160", "ieee519"], default="en50160")
    analyze.add_argument("--nominal", type=float, default=230.0)
    analyze.add_argument("--freq", type=float, default=50.0)
    analyze.add_argument("--voltage-col", default="voltage")
    analyze.add_argument("--current-col")
    analyze.add_argument("--time-col", default="time")
    analyze.add_argument("--fs", type=float)
    analyze.add_argument("--interval", type=float, default=600.0)
    analyze.add_argument("--bus-kv", type=float)
    analyze.add_argument("--report")
    analyze.add_argument("--json")

    generate = subparsers.add_parser("generate", help="Generate a demo waveform")
    generate.add_argument("out")
    generate.add_argument("--duration", type=float, default=60.0)
    generate.add_argument("--fs", type=float, default=10_000.0)
    generate.add_argument("--rms", type=float, default=230.0)
    generate.add_argument("--freq", type=float, default=50.0)
    generate.add_argument("--harmonic", action="append", default=[], metavar="ORDER=RATIO")
    generate.add_argument("--sag", action="append", default=[], metavar="START:DURATION:FACTOR")
    generate.add_argument("--seed", type=int)
    return parser


def _print_summary(result) -> None:
    print(f"{result.standard}: {'PASS' if result.passed else 'FAIL'}")
    print("Name | Limit | Measured | Unit | Status")
    for check in result.checks:
        print(
            f"{check.name} | {check.limit} | {check.measured} | "
            f"{check.unit} | {'PASS' if check.passed else 'FAIL'}"
        )


def _generate(args: argparse.Namespace) -> int:
    harmonics = {}
    try:
        for item in args.harmonic:
            order, ratio = item.split("=", 1)
            harmonics[int(order)] = float(ratio)
        t, voltage = sine_wave(
            freq=args.freq,
            rms=args.rms,
            fs=args.fs,
            duration=args.duration,
            harmonics=harmonics,
        )
        for item in args.sag:
            start, duration, factor = item.split(":")
            voltage = apply_event(
                t, voltage, float(start), float(duration), float(factor)
            )
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    output = Path(args.out)
    pd.DataFrame({"time": t, "voltage": voltage}).to_csv(output, index=False)
    return 0


def _analyze(args: argparse.Namespace) -> int:
    try:
        suffix = Path(args.file).suffix.lower()
        if suffix in (".cfg", ".dat"):
            wave = load(args.file)
        else:
            wave = load(
                args.file,
                time_col=args.time_col,
                voltage_col=args.voltage_col,
                current_col=args.current_col,
                fs=args.fs,
            )
        intervals = compute_intervals(
            wave, interval_s=args.interval, f0=args.freq, max_harmonic=40
        )
        intervals.attrs["interval_s"] = args.interval
        events = detect_events(
            wave.voltage, wave.fs, nominal=args.nominal, f0=args.freq
        )
        if args.standard == "en50160":
            result = check_en50160(
                intervals, nominal=args.nominal, f0=args.freq, events=events
            )
        else:
            if args.bus_kv is None:
                raise ValueError("--bus-kv is required for the ieee519 standard")
            result = check_ieee519_voltage(intervals, args.bus_kv)
        _print_summary(result)
        if args.report:
            write_report(
                args.report,
                result,
                wave=wave,
                events=events,
                intervals=intervals,
            )
        if args.json:
            Path(args.json).write_text(
                json.dumps(result.to_dict(), indent=2),
                encoding="utf-8",
            )
        return 0 if result.passed else 1
    except (OSError, KeyError, ValueError, ImportError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    """Run the GridLens command-line interface."""
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.command == "generate":
        return _generate(args)
    return _analyze(args)
