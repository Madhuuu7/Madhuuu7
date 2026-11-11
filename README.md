## Madhura M R

Computer science undergraduate, 2027. I build systems that check their own
claims — every number below came from a measurement, and most of them re-run
on each push, so they cannot quietly go stale.

Six of them are public, each with a console you can open and a README that
also says what the project cannot do.

---

### gridcast — day-ahead load forecasting for the Delhi grid

**5.07% MAPE and 233 MW MAE across 32,391 out-of-sample blocks**, 51% better
than the seasonal-naive baseline, on three years of real SLDC readings. The
point forecast is table stakes: load is enormously predictable and every model
looks good in isolation. The product is the prediction interval, because
deviation from a declared schedule is settled per block — so its coverage is
measured rather than assumed, and conditional coverage is tested against a
simulated null with a Benjamini–Hochberg correction across 21 tests.

[Open the desk](https://madhuuu7.github.io/gridcast/) · [source](https://github.com/Madhuuu7/gridcast)

### relay — an LLM gateway that routes on live health

Picks a provider from **live p95 latency, error rate and queue depth** instead
of a static fallback list, and ships the benchmark that shows the difference is
real: **p95 4,640 ms → 1,308 ms, a 71.8% cut**, with circuit-breaker trips down
81% over the same 4,000-request trace. OpenAI-compatible, so an existing client
gains fail-over and per-request cost accounting by changing one base URL. The
console shows each routing decision split into its latency, error, queue and
price terms.

[Open the console](https://madhuuu7.github.io/relay-llm-gateway/) · [source](https://github.com/Madhuuu7/relay-llm-gateway)

### revenant — a crash-resumable agent runtime

An agent run is an append-only event log and a crash is a cursor position in
it. The usual claim for this kind of system is "crash-safe"; the claim here is
narrower and testable — **kill the process at all 140 journal boundaries and
check what comes out**. All 140 recover with identical output and zero
duplicate effects, including 20 crashes that land after an effect reached the
outside world but before the log recorded it.

[Open the crash matrix](https://madhuuu7.github.io/revenant/) · [source](https://github.com/Madhuuu7/revenant)

### transitlab — RAPTOR, routing in your browser tab

Most transit apps call a directions API. This implements RAPTOR
(Delling–Pajor–Werneck, 2012) from scratch over real GTFS data, proves it
against an independently written Dijkstra baseline, then ports it to TypeScript
so the routing runs in the page: **37 ms a query in the browser against 1,373 ms
for the same algorithm in Python**, over Bengaluru's 9,948 stops and 1.54M stop
times, from a 1.93 MB download and no server at all.

[Plan a journey](https://madhuuu7.github.io/transitlab/) · [source](https://github.com/Madhuuu7/transitlab)

### verdict — a regression gate for LLM pipelines

Answers one question — *is this candidate worse than what we ship today?* — and
is built around the four ways the usual answer is wrong. It calibrates the judge
against human labels before trusting it, pairs every comparison on the case,
and controls the false discovery rate across the whole family of metrics. The
headline measurement is about the habit everyone has: **re-testing after every
case turns a 5.9% false-alarm rate into 46.7%**, and a confidence sequence
brings it back to 0.0% while still letting you stop early.

[Open the console](https://madhuuu7.github.io/verdict/) · [source](https://github.com/Madhuuu7/verdict)

### nanofaas — a scale-to-zero function platform

Functions run in containers with hard memory, CPU and capability limits; idle
ones are stopped, and the next request pays to start one again. It measures
that bill rather than asserting it: a **1,319 ms cold start of which 75% is the
interpreter booting and importing the handler** — the only part a function
author can change — against a **1.64 ms warm call**, a factor of 1,028. Then it
recommends the idle timeout your own traffic argues for, swept over the real
arrival gaps.

[Open the console](https://madhuuu7.github.io/nanofaas/) · [source](https://github.com/Madhuuu7/nanofaas)

---

### How these are built

Four habits repeat across all six, and they are more the point than any one
project:

- **The benchmark is a test.** relay replays its 4,000-request trace on every
  push, revenant re-runs all 140 crash scenarios, nanofaas records a fresh
  session against a real Docker daemon, and transitlab fails the build if the
  browser port's answers drift from the Python implementation's.
- **A deployed console is a recording, and says so.** GitHub Pages runs no
  Python and no containers. Rather than mock a backend, each page replays
  responses captured from the real service and names the date and host they
  came from, so what you read is a measurement rather than a drawing of one.
- **The failure path is tested, not only the happy one.** A platform that is
  reported as healthy while its data plane is down, a gate that cannot rule, an
  effect that escaped before the log recorded it — those are the cases with
  tests.
- **The README says what the project cannot do.** No VM isolation, no egress
  control, a ledger that is paused because its free database expired. A claim is
  worth more when the limits next to it are stated too.

### Earlier

**[A blockchain evidence system](https://github.com/Madhuuu7/blockchain-based-evidence-system)** — tamper-evident chain of custody for digital
evidence: Solidity on Sepolia with four on-chain roles, IPFS content addressing,
and integrity violations recorded permanently on-chain. 193 tests.

**[A browser IDE with an AI teammate](https://github.com/Madhuuu7/Distributed-Cloud-IDE)** — Monaco in the browser, a hardened Docker
sandbox for running user code, and an assistant that cites the file and line
range it answered from and runs the tests before claiming a fix works.

### What I reach for

Python (FastAPI, scikit-learn, pandas, NumPy) · TypeScript and React · SQL and
Postgres · Docker · GitHub Actions · Solidity · and a stubborn preference for
measuring a thing over asserting it.

### Now

Final-year CSE, graduating 2027, looking for a software or machine-learning
engineering internship. The fastest way to judge the work is to open one of the
consoles above and then read the README that explains what it is not showing
you.
