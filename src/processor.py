from __future__ import annotations

import csv
import itertools
import time
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

from yattag import Doc, indent

if TYPE_CHECKING:
    from yattag import SimpleDoc

DATA_DIR = Path("data")
SENATE_DATA = DATA_DIR / "senate-candidates.csv"
REPS_DATA = DATA_DIR / "house-candidates.csv"

start = time.time()


def classlist(*classes: str) -> list[str]:
    return [*itertools.chain.from_iterable(cls.split() for cls in classes)]


def navbar(state: str, division: str) -> SimpleDoc:
    doc = Doc()

    with doc.tag("nav", klass="bg-white border-gray-200 print:hidden"):
        with doc.tag(
            "div",
            klass="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4",
        ):
            with doc.tag(
                "a", href="/", klass="flex items-center space-x-3 rtl:space-x-reverse"
            ):
                doc.stag(
                    "img", src="/img/icon.png", klass="h-8", alt="Below The Line logo"
                )
                doc.line(
                    "span",
                    "Below The Line",
                    klass="self-center text-2xl font-semibold whitespace-nowrap",
                )
            with doc.tag(
                "div",
                klass="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse",
            ):
                doc.line(
                    "button",
                    "Reset",
                    klass="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center",
                )
            with doc.tag(
                "div",
                klass="items-center justify-between hidden w-full md:flex md:w-auto md:order-1",
            ):
                doc.line(
                    "span",
                    f"{division}, {state}",
                    klass="flex flex-col text-xl font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white",
                )

    return doc


def ballot(state: str, division: str, reps: SimpleDoc, senate: SimpleDoc) -> SimpleDoc:
    doc = Doc()
    doc.asis("<!DOCTYPE html>")

    with doc.tag("html"):
        with doc.tag("head"):
            doc.line("title", f"{division}, {state}")
            doc.stag("meta", charset="UTF-8")
            doc.stag(
                "meta",
                name="viewport",
                content="width=device-width, initial-scale=1.0",
            )
            doc.stag("link", href="../site.css", rel="stylesheet")
            doc.line("script", "", src="../ballot.js", defer="")

        with doc.tag(
            "body", klass="font-sans text-slate-800 bg-gray-50 print:bg-white!"
        ):
            doc.asis(navbar(state, division).getvalue())
            with doc.tag("div", klass="grid place-items-center my-[2em]"):
                with doc.tag(
                    "div",
                    id="ballot-reps",
                    klass=(
                        "relative grid items-center place-items-center "
                        "justify-center bg-green-50 shadow-sm border border-slate-200 "
                        "divide-solid divide-slate-200 divide-y-1 "
                        "min-w-[240px] max-w-[100em] print:bg-white!"
                    ),
                ):
                    doc.asis(reps.getvalue())
                doc.asis(senate.getvalue())
            with doc.tag(
                "div",
                klass=(
                    "float absolute top-[4em] w-screen "
                    "rotate-315 opacity-30 "
                    "text-gray-500 text-5xl text-center "
                    "hidden print:block!"
                ),
            ):
                doc.asis("THIS IS NOT AN<br/>OFFICIAL BALLOT PAPER")

    return doc


def senate_ballot(candidates: list[dict[str, str]]) -> SimpleDoc:
    doc = Doc()

    with doc.tag(
        "div",
        id="ballot-senate",
        klass=(
            "relative grid items-center place-items-center "
            "justify-center bg-white shadow-sm border border-slate-200 "
            "divide-solid divide-slate-200 divide-y-1 "
            "min-w-[240px] my-[3em] print:bg-white!"
        ),
    ):
        for index, candidate in enumerate(candidates, start=1):
            with doc.tag(
                "div",
                id=f"senate-{candidate['column']}-{candidate['ballotPosition']}",
                klass=(
                    f"order-{index} print:order-{index}! overflow-visible "
                    "w-full justify-self-center transition-all duration-100 "
                    "hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 p-2"
                ),
            ):
                doc.stag(
                    "input",
                    name=f"senate-{index}",
                    type="text",
                    value=str(index),
                    klass="bg-white border border-gray-300 w-[2em] text-center mr-1",
                )
                doc.line("span", candidate["surname"], klass="font-bold")
                doc.line("span", candidate["ballotGivenName"], klass="")
                doc.line(
                    "span",
                    candidate["column"],
                    klass="float-right text-sm border border-slate-500 rounded-xl bg-gray-200 pl-2 pr-2",
                )
                doc.line(
                    "span",
                    candidate["partyBallotName"],
                    klass="ml-[3em] mr-[1em] float-right text-sm",
                )

    return doc


output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

senate_candidates = defaultdict(list)

with SENATE_DATA.open() as data:
    for row in csv.DictReader(data):
        state = row.pop("state")
        senate_candidates[state].append(row)

senate_ballots = {
    state: senate_ballot(candidates) for state, candidates in senate_candidates.items()
}

with REPS_DATA.open() as data:
    last_state = None
    last_division = None
    doc = None

    for row in csv.DictReader(data):
        state = row.pop("state")
        division = row.pop("division")

        if last_division is not None and division != last_division:
            assert last_state is not None
            assert doc is not None
            page = ballot(last_state, last_division, doc, senate_ballots[last_state])

            path = output_dir / last_state.lower() / f"{last_division.lower()}.html"
            path.parent.mkdir(exist_ok=True, parents=True)

            path.write_text(indent(page.getvalue()))

        if last_division is None or division != last_division:
            doc = Doc()
            last_state = state
            last_division = division

        assert doc is not None

        with doc.tag(
            "div",
            id=f"reps-{row['ballotPosition']}",
            klass=(
                f"order-{row['ballotPosition']} print:order-{row['ballotPosition']}! "
                "w-full justify-self-center transition-all duration-500"
                "hover:bg-slate-100 focus:bg-slate-100 active:bg-slate-100 p-2"
            ),
        ):
            doc.stag(
                "input",
                name=f"reps-{row['ballotPosition']}",
                type="text",
                value=str(row["ballotPosition"]),
                klass="bg-white border border-gray-300 w-[2em] text-center mr-1",
            )
            doc.line("span", row["surname"], klass="font-bold")
            doc.line("span", row["ballotGivenName"], klass="")
            doc.line(
                "span",
                row["partyBallotName"],
                klass="ml-[5em] float-right text-sm",
            )

print(f"content generated in {time.time() - start:0.3f} seconds")
