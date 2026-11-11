<p align="center">
  <img src="assets/header.svg" alt="Madhura M R — growing one commit at a time" width="100%">
</p>

<!-- Prefer your own cherry blossom GIF banner? Swap the line above for:
<p align="center"><img src="assets/banner.gif" alt="" width="100%"></p> -->

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Georgia&size=21&duration=3400&pause=900&color=C890A6&center=true&vCenter=true&width=620&height=40&lines=Hi%2C+I'm+Madhura+%F0%9F%8C%B8;I+build+systems+that+check+their+own+claims;Growing+one+commit+at+a+time" alt="Hi, I'm Madhura. I build systems that check their own claims.">
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Madhuuu7&color=C890A6&style=flat-square&label=visitors" alt="">
</p>

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## 🌷 About

- 🎓 Computer science undergraduate, graduating **2027**, looking for a software or ML engineering internship.
- 🌱 I build **six public systems**, each with a console you can open and a benchmark that re-runs in CI.
- 📐 My habit: measure the thing rather than assert it — and write down what the project *cannot* do, next to what it can.
- 🍃 Mostly **Python** and **TypeScript**, with a soft spot for the part where a claim gets tested.

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## ✨ What the work measured

<p align="center">
  <img src="assets/garden.svg" alt="gridcast 5.07% MAPE; relay p95 −71.8%; revenant 140 of 140 crash boundaries; transitlab 37 ms a query; verdict 5.9% to 46.7% false alarms; nanofaas 1,028× warm" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/gridcast/tests.yml?style=flat-square&label=gridcast&labelColor=F5E6EE&color=C890A6" alt="">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/relay-llm-gateway/tests.yml?style=flat-square&label=relay&labelColor=F5E6EE&color=C890A6" alt="">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/revenant/tests.yml?style=flat-square&label=revenant&labelColor=F5E6EE&color=C890A6" alt="">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/transitlab/tests.yml?style=flat-square&label=transitlab&labelColor=F5E6EE&color=C890A6" alt="">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/verdict/tests.yml?style=flat-square&label=verdict&labelColor=F5E6EE&color=C890A6" alt="">
  <img src="https://img.shields.io/github/actions/workflow/status/Madhuuu7/nanofaas/tests.yml?style=flat-square&label=nanofaas&labelColor=F5E6EE&color=C890A6" alt="">
</p>

<p align="center"><sub>Live status, not a decoration — these go red if a test breaks.</sub></p>

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## 🌸 Featured projects

<p align="center"><i>Like a cup of coffee, every great idea starts with a little spark ☕</i></p>

<table>
<tr>
<td width="50%" valign="top">

### 🌷 [gridcast](https://github.com/Madhuuu7/gridcast)

Day-ahead load forecasting for the Delhi grid, on three years of real SLDC readings. The point forecast is table stakes; the product is a **prediction interval whose coverage is measured, not assumed**.

`Python` · `scikit-learn` · `FastAPI` · `PostgreSQL` · `React`

**[Open the desk →](https://madhuuu7.github.io/gridcast/)**

</td>
<td width="50%" valign="top">

### 🌷 [relay](https://github.com/Madhuuu7/relay-llm-gateway)

An LLM gateway that picks a provider from **live latency, error rate and queue depth** instead of a static fallback list. Point an OpenAI client at it and it gains fail-over and cost accounting.

`Python` · `FastAPI` · `asyncio` · `React` · `TypeScript`

**[Open the console →](https://madhuuu7.github.io/relay-llm-gateway/)**

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🌷 [revenant](https://github.com/Madhuuu7/revenant)

A durable agent runtime where a crash is just a cursor position in an append-only log. **Killed at all 140 journal boundaries**; all 140 recover with identical output and no duplicate effects.

`Python` · `FastAPI` · `MongoDB` · `React` · `TypeScript`

**[Open the crash matrix →](https://madhuuu7.github.io/revenant/)**

</td>
<td width="50%" valign="top">

### 🌷 [transitlab](https://github.com/Madhuuu7/transitlab)

RAPTOR implemented from scratch over real GTFS data, then ported to TypeScript so **the routing runs in your tab** — Bengaluru's 9,948 stops, no server behind the page.

`Python` · `TypeScript` · `GTFS` · `Vite`

**[Plan a journey →](https://madhuuu7.github.io/transitlab/)**

</td>
</tr>
</table>

<p align="center">
  Two more: <b><a href="https://github.com/Madhuuu7/verdict">verdict</a></b>, a regression gate for LLM pipelines that calibrates its judge before trusting it ·
  <b><a href="https://github.com/Madhuuu7/nanofaas">nanofaas</a></b>, a scale-to-zero function platform that measures its own cold-start tax
</p>

<details>
<summary><b>🌸 How these are built</b> — four habits that repeat across all six</summary>

<br>

- **The benchmark is a test.** relay replays its 4,000-request trace on every push, revenant re-runs all 140 crash scenarios, nanofaas records a fresh session against a real Docker daemon, and transitlab fails the build if the browser port's answers drift from the Python implementation's. A number cannot quietly go stale.
- **A deployed console is a recording, and says so.** GitHub Pages runs no Python and no containers. Rather than mock a backend, each page replays responses captured from the real service and names the date and host they came from — so what you read is a measurement, not a drawing of one.
- **The failure path is tested, not only the happy one.** A platform reported as healthy while its data plane is down, a gate that cannot rule, an effect that escaped before the log recorded it: those are the cases with tests.
- **The README says what the project cannot do.** No VM isolation, no egress control, a ledger that is paused because its free database expired. A claim is worth more when the limits are stated next to it.

</details>

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## 🍃 Tech I reach for

<p align="center">
  <img src="https://img.shields.io/badge/Python-C890A6?style=flat-square&logo=python&logoColor=FFFDFB" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-C890A6?style=flat-square&logo=typescript&logoColor=FFFDFB" alt="TypeScript">
  <img src="https://img.shields.io/badge/React-E0BAC6?style=flat-square&logo=react&logoColor=574A50" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-C890A6?style=flat-square&logo=fastapi&logoColor=FFFDFB" alt="FastAPI">
  <img src="https://img.shields.io/badge/scikit--learn-E0BAC6?style=flat-square&logo=scikitlearn&logoColor=574A50" alt="scikit-learn">
  <img src="https://img.shields.io/badge/pandas-C890A6?style=flat-square&logo=pandas&logoColor=FFFDFB" alt="pandas">
  <br>
  <img src="https://img.shields.io/badge/PostgreSQL-E0BAC6?style=flat-square&logo=postgresql&logoColor=574A50" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/MongoDB-C890A6?style=flat-square&logo=mongodb&logoColor=FFFDFB" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-E0BAC6?style=flat-square&logo=docker&logoColor=574A50" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub%20Actions-C890A6?style=flat-square&logo=githubactions&logoColor=FFFDFB" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Solidity-E0BAC6?style=flat-square&logo=solidity&logoColor=574A50" alt="Solidity">
  <img src="https://img.shields.io/badge/Vite-C890A6?style=flat-square&logo=vite&logoColor=FFFDFB" alt="Vite">
</p>

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## 📊 Stats

<p align="center">
  <img src="assets/stats.svg" alt="Eight public projects, six live consoles, 183 commits, fifteen CI workflows. 61.5% Python, 14.5% TypeScript, 13.9% JavaScript." width="100%">
</p>

<p align="center"><sub>Counted from the repositories, so it cannot break when someone else's free tier does.</sub></p>

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## ☕ Currently

- 🌱 **Building** — a portfolio site to tie the six together
- 📖 **Reading** — the papers these came out of: RAPTOR, conformal prediction, confidence sequences
- 🔭 **Next** — more of the systems side: schedulers, storage, and things that have to survive being killed
- ☕ **Drinking** — coffee, mostly

<p align="center">🌸 ･ ﾟ ✧ ･ ﾟ 🌸</p>

## 💌 Let's connect

<p align="center">
  <a href="https://www.linkedin.com/in/madhura-m-r">
    <img src="https://img.shields.io/badge/LinkedIn-C890A6?style=flat-square&logo=linkedin&logoColor=FFFDFB" alt="LinkedIn">
  </a>
  <a href="mailto:mrmadhura610@gmail.com">
    <img src="https://img.shields.io/badge/Email-E0BAC6?style=flat-square&logo=gmail&logoColor=574A50" alt="Email">
  </a>
  <a href="https://github.com/Madhuuu7?tab=repositories">
    <img src="https://img.shields.io/badge/Repositories-C890A6?style=flat-square&logo=github&logoColor=FFFDFB" alt="Repositories">
  </a>
</p>

<!-- A cute coding/coffee illustration fits nicely here:
<p align="center"><img src="assets/coding.gif" alt="" width="320"></p> -->

<p align="center">
  <img src="assets/footer.svg" alt="" width="100%">
</p>

<!-- Falling petals GIF, if you find one you like:
<p align="center"><img src="assets/petals.gif" alt="" width="100%"></p> -->
