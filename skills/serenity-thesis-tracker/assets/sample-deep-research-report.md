# Global Inference Token Demand Model 2026 to 2030

The right way to rebuild this model is as a **v0.4, segment-first, cross-checked, physical-served-token model**. The headline denominator should be **physical served inference tokens**, not just API-billed tokens and not just visible chat turns. For this report, that means counting visible input and output, retrieval or tool context that is sent back into the model, internal reasoning when providers meter or account for it inside model usage, and cache writes. I treat **pure cache reads** as a separate ledger item because OpenAI, Anthropic, and Google all price cached tokens differently from normal input, and Salesforce explicitly distinguishes raw token processing from higher-level agentic work units. That accounting choice is the only way to make user behavior, revenue, and supply all fit the same story. citeturn14search10turn31view0turn30search3turn30search0turn8search1

Using that ledger, my reconstructed headline range for the **current 2026 annualized global market** is:

| Scenario | Annual physical served tokens | Average tokens per second |
|---|---:|---:|
| Low | **50Q** | **1.6B tok/s** |
| Base | **85Q** | **2.7B tok/s** |
| High | **140Q** | **4.4B tok/s** |

Here, **Q = quadrillion = 10^15 tokens**. The reason the range is already this high is simple: Google alone says it now processes **more than 3.2 quadrillion tokens per month across its surfaces**, which annualizes to **38.4Q/year** before adding OpenAI, Anthropic, Microsoft, Meta, or the rest of the market. OpenAI also says its API platform was already at **6 billion tokens per minute** by DevDay 2025, which annualizes to roughly **3.15Q/year** on API traffic alone. Any 2026 global model materially below ~50Q/year is therefore too small on physical-load grounds. citeturn37view0turn15view0

My reconstructed **2030 physical served-token range** is:

| Scenario | Annual physical served tokens | CAGR from 2026 |
|---|---:|---:|
| Low | **180Q** | **~38%** |
| Base | **480Q** | **~54%** |
| High | **1,200Q** | **~71%** |

The key conclusion is that **2030 growth is not mostly “more people chatting.”** Consumer reach is already near mass scale in 2026. The dominant 2030 growth driver is the rise of **agent loops**: coding agents, office agents, customer support and sales agents, and background automations that run continuously or semi-continuously. citeturn37view0turn17view0turn27view0turn27view1turn36view2

## Boundary and token ledger

I recommend keeping **two ledgers** in the model.

The first, and the one I headline, is **physical served tokens**. This is the best denominator for usage anchors and compute sanity checks, because that is the level at which Google’s **3.2Q/month** figure, OpenAI’s **6B tokens/minute** API figure, and vendor capacity disclosures make sense. The second is **billable-equivalent tokens**, which compresses physical served load after accounting for flat-rate subscriptions, free tiers, discounts, prompt caching, and highly subsidized search or consumer usage. Revenue sanity checks should be run on the second ledger, not on the first. citeturn37view0turn15view0turn14search10turn30search3turn30search0

This distinction matters because **visible chat** is now a minority share of many important workloads. OpenAI’s own consumer-usage paper says that by July 2025 ChatGPT users were sending **18 billion messages per week** from **700 million weekly users**, and that about **70%** of consumer queries were unrelated to work; it also says only **4.2%** of messages were computer programming. That is a warning against using power-coder behavior as the average human baseline. At the same time, the sheer mismatch between message counts and provider-scale token disclosures implies that **hidden retrieval, context packing, tool traces, reasoning, and cache-heavy re-reads** are now central to the physical token economy. citeturn15view2turn25view0turn38view0turn38view1

For practical modeling, I would make the denominator explicit in every table:

| Ledger | Include | Exclude | Best used for |
|---|---|---|---|
| Physical served tokens | visible input/output, reasoning, tool-context fed to model, retrieval context, cache writes | pure cache storage hours; optionally report cache reads separately | usage anchors, supply, total demand |
| Billable-equivalent tokens | whatever a vendor effectively monetizes after discounts and plan design | non-monetized free/search-supported traffic | revenue sanity checks |

That framing directly fixes the failure mode you flagged in v0.1 and v0.2: average visible chat minutes understate real physical load, while revenue-only backsolves are hypersensitive to effective blended price. citeturn14search10turn31view0turn30search3turn30search0turn8search1

## Public anchor map

The model should be pinned to a small set of **high-confidence public anchors**. These are the ones doing the most work.

| Anchor | Why it matters |
|---|---|
| **Google:** more than **3.2Q tokens/month** across its surfaces; **AI Overviews >2.5B MAU**; **AI Mode >1B MAU**; **Gemini app >900M MAU**. citeturn37view0turn37view1 | Hard floor for 2026 physical served-token demand; proves that free consumer AI search and free assistant usage are already at quadrillion-per-month scale. |
| **OpenAI:** **>900M weekly active users**, **>50M consumer subscribers**, **>9M paying business users**, **1.6M weekly Codex users**. citeturn17view0 | Strong anchor for paid vs free consumer mix and for the existence of a rapidly scaling coding-agent cohort. |
| **OpenAI API:** **6B tokens/minute** by DevDay 2025. citeturn15view0 | API-only lower bound for non-consumer application traffic. |
| **OpenAI revenue and compute:** **$20B+ ARR** at end-2025; compute grew to about **1.9GW** in 2025; OpenAI later disclosed **3GW of dedicated inference capacity** in expanded infrastructure plans. citeturn15view1turn15view3turn17view0 | Lets the model check whether token totals are large enough to explain revenue and small enough to fit disclosed compute expansion. |
| **Anthropic:** run-rate revenue **>$30B** in April 2026 and **>$47B** by early June 2026; Claude Code run-rate revenue **>$2.5B** in February 2026. citeturn18search3turn18search6turn18search0 | Confirms that coding and enterprise agentic demand is already large enough to move major vendor revenue. |
| **Anthropic compute:** one 2026 deal added **>300MW** and **>220,000 NVIDIA GPUs**. citeturn10search0turn18search7 | Important supply-side anchor. |
| **Microsoft:** **150M** monthly active first-party Copilot users, **900M** monthly active AI-feature users, **20M paid Microsoft 365 Copilot seats**, **26M GitHub Copilot users**, **4.7M paid Copilot subscribers**, and AI business **>$37B run-rate**. citeturn27view0turn34view1turn33search2 | Strong anchor for enterprise-seat and developer-seat demand; also supports “usage intensity is rising” rather than just seats rising. |
| **Salesforce:** **3.2T tokens processed**, **9,500+ paid Agentforce deals**, **1.6B AWUs in Q1**. citeturn36view1turn36view2 | Anchors enterprise workflow and customer-service-style agent demand outside chat and coding. |

One more source deserves special weight because it prevents overfitting to power users. OpenAI’s economics paper says ChatGPT consumer use in July 2025 was broad-based, heavily non-work, and still dominated by practical guidance, writing, and information-seeking rather than coding. That is exactly why the model must separate **ordinary consumer use** from **developer and agentic heavy tails** instead of smearing them together into one average. citeturn25view0turn38view1

## The 2026 reconstructed model

The cleanest way to answer “who is using the tokens?” is with explicit segments. In the base case below, **non-human segments** such as background automation and API workloads use “active workload unit” rather than a human seat.

| Segment | 2026 active users or units | Monthly physical tokens per user or unit | Annual physical tokens | Share |
|---|---:|---:|---:|---:|
| Free consumer chat and search assistants | 2.8B | 1.0M | 33.6Q | 40% |
| Paid consumer chat | 90M | 14M | 15.1Q | 18% |
| Developer interactive assistant | 32M | 8M | 3.1Q | 4% |
| Developer agentic power user | 4.5M | 220M | 11.9Q | 14% |
| Enterprise knowledge-worker agent | 75M | 10M | 9.0Q | 11% |
| Customer support and sales ops agent | 5M | 50M | 3.0Q | 4% |
| Background agent automation | 0.9M | 250M | 2.7Q | 3% |
| API application workload | 0.5M workloads | 1.0B | 6.0Q | 7% |
| **Total** |  |  | **84.4Q** | **100%** |

This base case says that **2026 is already an ~85Q/year physical-token market**, and that **ordinary consumer chat/search still accounts for the biggest single share**, but not the whole story. Consumer free plus paid usage is about **49Q/year**, or roughly **58%** of all physical tokens. Coding assistance and coding agents together are about **15Q/year**, or roughly **18%**. Enterprise workflow agents plus customer-support/sales agents contribute roughly **12Q/year**, while API apps plus background automations add another **9Q/year**. In other words: **2026 is still consumer-heavy in surface area, but already heavily shaped by agentic and workflow backends.** This is exactly the pattern you wanted the model to capture. The base case is calibrated against Google’s surfaces, OpenAI’s user and API disclosures, Microsoft seat counts, GitHub scale, Anthropic monetization, and Salesforce workflow volume. citeturn37view0turn17view0turn15view0turn27view0turn34view1turn18search0turn36view1

The free-consumer row looks high only if one imagines visible typing. It does **not** look high once the model is tied to real platform disclosures. Google alone reports **3.2Q/month** across its surfaces, while AI Overviews, AI Mode, and the Gemini app are already serving billions or near-billions of monthly users. That makes million-token-per-user-per-month averages quite plausible on a **physical served** basis, because a single “assistant experience” can hide large retrieval packs, answer synthesis, planning traces, and repeated context use. citeturn37view0turn37view1

The paid-consumer row also needs to be interpreted as **flat-rate heavy usage**, not API pricing. OpenAI says it now has **more than 50 million consumer subscribers**, while its product help pages describe much higher usage allowances on paid plans, including effectively unlimited or very high-limit access on some premium plans subject to abuse guardrails. Anthropic, GitHub, and Google also all sell paid tiers aimed at higher-intensity users. That makes **double-digit millions of physical tokens per subscriber per month** reasonable in the base case, while still leaving billion-token months as a heavy-tail phenomenon rather than a population average. citeturn17view0turn12search5turn12search0turn18search9turn34view0turn37view2

The developer rows are where older models most often broke. GitHub alone now reports **26 million Copilot users** and **4.7 million paid Copilot subscribers**, while OpenAI says weekly Codex users have risen to **1.6 million** and Anthropic says Claude Code has already become a **multi-billion-run-rate** business. Vendor plan design points the same way: GitHub Max is explicitly for **“sustained, high-volume agent workflows”** and bundles **$200/month** of AI credits; OpenAI’s token-based Codex pricing says a **typical task uses 5–45 credits** and average Codex cost is around **$100–$200 per developer per month**; Anthropic says average Claude Code enterprise cost is around **$150–$250 per developer per month** with wide variance. Those are not chat-like usage profiles. citeturn17view0turn34view0turn31view0turn11search5turn18search0

## The 2030 scenarios and what is actually growing

My 2030 base case keeps the same segmentation but shifts the center of gravity toward agents and background loops.

| Segment | 2030 base active users or units | Monthly physical tokens per user or unit | Annual physical tokens |
|---|---:|---:|---:|
| Free consumer chat and search assistants | 4.4B | 1.25M | 66.0Q |
| Paid consumer chat | 250M | 22M | 66.0Q |
| Developer interactive assistant | 70M | 12M | 10.1Q |
| Developer agentic power user | 25M | 300M | 90.0Q |
| Enterprise knowledge-worker agent | 180M | 35M | 75.6Q |
| Customer support and sales ops agent | 25M | 180M | 54.0Q |
| Background agent automation | 6M | 1.0B | 72.0Q |
| API application workload | 1.4M workloads | 2.0B | 33.6Q |
| **Total** |  |  | **467.3Q** |

I round that to a **~480Q/year 2030 base case**. The low case, **180Q/year**, is a world where agents grow mostly in seats but not yet in loop intensity. The high case, **1,200Q/year**, is a world where agentic usage reaches the lower bound implied by very aggressive workload assumptions. The shape of the growth matters more than the single number. Relative to the 2026 base case, only about **one-fifth to one-quarter** of added demand comes from broader consumer adoption. The majority comes from **developer agents, knowledge-worker agents, customer-facing workflow agents, and especially background automation**. That is the core answer to your question: **2030 growth is mostly from token intensity and loop frequency, not from raw user-count growth alone.** This is the natural consequence of 2026 already having billions of users on Google, OpenAI, and Microsoft surfaces. citeturn37view0turn17view0turn27view0

In this base case, consumer free plus paid usage is still enormous at roughly **132Q/year**, but it falls to only about **28%** of total physical tokens. Developer and enterprise agentic work becomes the majority. That is the structural transition the model should emphasize: **2026 is the era of mass consumer reach with a rapidly rising heavy tail; 2030 is the era where loops, not prompts, dominate the token budget.** citeturn37view0turn17view0turn27view1turn36view2

This also clarifies what “agent adoption” means in a self-consistent model. A 2030 world where “most programmers” use agents is easy to reconcile with the base case. A 2030 world where **10–20% of knowledge workers** use real agentic workflows is also easy to reconcile. What is **not** easy to reconcile in a midline scenario is a claim that **hundreds of millions** of agent users all average **1B physical tokens per month**. That is not because such users cannot exist; it is because that assumption mechanically explodes the total market into a much larger endpoint. The sensitivity table below makes that visible. citeturn27view0turn17view0turn37view0

## Revenue and supply cross-checks

On the revenue side, the market only becomes self-consistent when you separate **physical throughput** from **monetized throughput**. API list prices remain high for frontier models: OpenAI’s GPT‑5.5 lists at **$5/MTok input**, **$0.50/MTok cached input**, and **$30/MTok output**; Anthropic’s Opus pricing is **$5/MTok input**, **$0.50/MTok cache hits**, and **$25/MTok output**; Google’s Gemini pricing is lower on many tiers and explicitly notes that output pricing includes **thinking tokens**. At the same time, developer and consumer products increasingly wrap usage inside subscriptions or seat licenses rather than charging pure pass-through token rates. citeturn14search10turn31view0turn30search3turn30search0turn35search3turn34view0

Current revenue anchors are already in the tens of billions. OpenAI’s disclosed annualized revenue exceeded **$20B** by end-2025. Anthropic disclosed a run-rate above **$30B** in April 2026 and above **$47B** by early June 2026, though Reuters notes that Anthropic’s run-rate definition is particularly sensitive because it extrapolates recent consumption-based sales and large businesses account for most of its revenue. Microsoft reported **$37B** AI annual revenue run-rate, but that number includes cloud, platform, and product layers and therefore overlaps with direct model vendors; Salesforce reported nearly **$1.4B ARR** for Agentforce and Data 360. So the right interpretation is not “add all of these cleanly,” but rather “the ecosystem already supports a direct and semi-direct revenue envelope well into the tens of billions.” citeturn15view1turn15view3turn18search3turn18search6turn15view4turn33search2turn36view1

At the **2026 base case of ~85Q/year**, even a conservative **$40B–$80B** direct or semi-direct revenue envelope implies only about **$0.47–$0.94 per MTok** on a physical served-token basis. That is far below API list pricing, but it is absolutely plausible given the observed mix of free/search-supported traffic, flat-rate subscriptions, cheap cached tokens, bundled SaaS pricing, and subsidized customer acquisition. This is why a revenue-only backsolve with one marketwide $/MTok parameter fails: the physical token economy and the monetized token economy are not the same ledger. The public rate cards practically shout this at you. citeturn14search10turn30search3turn30search0turn31view0turn35search3turn34view0

On the supply side, the model also passes a common-sense test. Google’s **3.2Q/month** figure already implies about **1.23B tok/s** on its own. OpenAI’s **6B tokens/minute** API figure implies roughly **100M tok/s** on API traffic alone. Against those anchors, the **2026 base case of 2.7B tok/s** is demanding but not absurd. It is roughly “Google-sized surfaces plus the rest of the frontier market.” OpenAI says its compute reached about **1.9GW** in 2025 and is now expanding with **3GW of dedicated inference capacity**; Anthropic says one new partnership alone added **>300MW** and **>220,000 GPUs**; Microsoft describes its infrastructure program as a “planet-scale cloud and AI factory.” The supply story is therefore consistent with a multi-billion-token-per-second global market in 2026 and a much larger one by 2030, provided current power and capacity build-outs keep compounding. citeturn37view0turn15view0turn15view1turn17view0turn10search0turn18search7turn27view1

## Sensitivity and fragile assumptions

The most important sensitivity matrix is exactly the one you specified. If **agent users** are measured in millions and **monthly tokens per agent user** are measured in billions, then:

**annual tokens in Q/year = users_M × monthly_tokens_B × 12 ÷ 1,000?**

That expression is wrong if the output unit is quadrillions. The cleanest way to state it is:

**annual tokens in T/year = users_M × monthly_tokens_B × 12 × 1000**

or equivalently:

**annual tokens in Q/year = users_M × monthly_tokens_B × 12**

because **1M users × 1B tokens/user/month = 1Q tokens/month**.

Using that correct quadrillion-token form:

| Agent users | 0.1B / month | 0.5B / month | 1B / month | 3B / month |
|---|---:|---:|---:|---:|
| 50M | 60Q / year | 300Q / year | 600Q / year | 1,800Q / year |
| 100M | 120Q / year | 600Q / year | 1,200Q / year | 3,600Q / year |
| 250M | 300Q / year | 1,500Q / year | 3,000Q / year | 9,000Q / year |
| 400M | 480Q / year | 2,400Q / year | 4,800Q / year | 14,400Q / year |

This table is the single most useful antidote to endpoint hand-waving. It shows that **100M agent users at 1B tokens/month is not “a little high” — it is a 1,200Q/year assumption before adding ordinary consumer chat, search, or API traffic.** Likewise, **400M agent users at only 0.1B/month** already implies **480Q/year**, which by itself equals my 2030 base case. So if you want **100M, 250M, or 400M** agent users in a midline 2030 scenario, the physically consistent monthly average is usually closer to **0.05B–0.2B/month** than to **1B/month**, unless you are intentionally building a very large endpoint. That is the model’s clearest answer to the “agent users over 100M” question. citeturn37view0turn17view0turn27view0

At the same time, there is real evidence that **billion-token months exist in the heavy tail**. Anthropic says average Claude Code enterprise deployments cost around **$150–$250 per developer per month** and around **$13 per active developer-day**, with 90% of users staying below **$30 per active day**; OpenAI says a typical Codex task can consume **5–45 credits**, that Codex now has **1.6M weekly users**, and average Codex cost is around **$100–$200 per developer per month**; a high-profile OpenClaw fleet reportedly consumed **603B tokens in 30 days** across roughly **100 Codex agents**; and at least one community-reported Claude usage export showed **8.77B tokens** in a single month. Those examples support the existence of the heavy tail. They do **not** justify treating the heavy tail as the market average. citeturn11search5turn31view0turn17view0turn24news23turn23search7

The most fragile assumptions in this model are easy to name. The first is **Google’s token definition**: “tokens processed across our surfaces” is an extraordinarily valuable anchor, but it is not identical to a text-only API billable-token metric and may include multimodal-token accounting. The second is **overlap among user bases**: AI Overviews, AI Mode, Gemini, ChatGPT, Copilot, and Claude are not separate populations. The third is the treatment of **cache reads**: coding and retrieval-heavy workloads can look modest on compute-bearing uncached tokens and enormous on total served or logically consumed tokens. The fourth is **vendor revenue definition drift**, especially between ARR, run-rate, subscription-only, and metered sales. Reuters’ analysis of Anthropic’s run-rate methodology is especially important here. citeturn37view0turn30search3turn30search0turn15view4

The disclosures most likely to move the model are therefore straightforward: a cleaner provider-wide split between **uncached vs cached**, **subscription vs metered usage**, **consumer vs enterprise vs coding**, and any formal disclosure of **monthly active agent users** with associated average task volume. If Google were to clarify what is inside the **3.2Q/month** number, or if OpenAI, Anthropic, Microsoft, or GitHub were to publish segmented token or task-level usage by plan tier, the 2026 and 2030 endpoints could move materially. Until then, the safest headline is this: **2026 is already a tens-of-quadrillions physical-token market, and the 2030 endpoint is determined much more by agent-loop intensity than by simple user growth.** citeturn37view0turn17view0turn27view0turn31view0turn11search5