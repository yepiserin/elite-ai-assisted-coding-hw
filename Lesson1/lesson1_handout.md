# Lesson 1 — Orientation & Intro To AI-Assisted Coding

AI is now part of everyday software work. This lesson sets expectations for how to use it well: why it matters, what “AI-assisted” actually means, the goals we’re aiming for, and the two principles that make the tools dependable. Think of this as a short chapter that closely follows the talk and the lesson plan. It is designed to be readable in one sitting and practical enough to keep beside you while you code.

## The Promise

AI-assisted development is about raising the bar while shortening the path from idea to release. Used well, it helps you produce more reliable, more sophisticated software, and it lightens the cognitive load that slows engineering down. Crucially, it doesn’t replace engineers; it **augments** them. The fundamentals still govern outcomes: good design, clean code, robust tests, sound architecture.

We emphasise three benefits:

- **Improve software quality** — more reliable and dependable systems with fewer defects and clearer intent.
- **Enhance capabilities and velocity** — developers ship features, fix bugs, and evolve systems faster.
- **Democratise software development** — adjacent roles and motivated hobbyists can contribute meaningfully when guardrails are in place.

These benefits reinforce one another. Better quality reduces rework, which increases velocity; clearer conventions and context make it safer for more people to contribute. The aim is a development process that is both faster and more dependable.

## What “AI-Assisted” Means In Practice

There isn’t a single workflow. You’ll move between complementary **modalities**, often within the same task. The shape of the task dictates the mode; you can switch as you go without losing momentum.

### In-Editor Assistance
AI meets you in the IDE. You can chat to plan or understand code, accept code completion in real time, and request edits or generated snippets while you remain in control. This is the familiar “pair-programmer” experience where you steer and the tool accelerates routine steps.

### Analysis & Review
AI acts like a tireless teammate. It reviews pull requests and change sets, audits parts of the codebase, compares work to requirements, and helps turn ideas and data into specifications and plans. When complexity or volume climbs, this mode keeps quality high without slowing you down.

### Agentic & Autonomous Systems
You delegate multi-step tasks that span files and systems. This includes **agentic coding** for end-to-end feature work, **AI as a DevOps operator** (source control, deployments, monitoring), and **Continuous AI** inside CI/CD—scheduled or event-driven jobs that run without constant human intervention. It’s the same engineering you already do, expressed as repeatable tasks that an agent can carry.

These modes are additive. You might draft a change with in-editor help, ask an agent to propagate a refactor, and rely on CI to run policy checks and update documentation. The handoff between modes is where much of the time saving occurs.

## Goals We’re Optimising For

The course prioritises outcomes that matter across a project’s lifecycle—planning and specification through implementation, testing, integration, and deployment—without tying you to a single vendor or tool. Keep these aims in mind when you choose a tool or a mode; they’re the yardsticks for success.

- **Improve software quality.** Lower cognitive load and raise reliability, clarity, and safety.
- **Increase development velocity.** Compress the loop from idea to feature in production, not only the pace of typing.
- **Enhance developer efficacy.** Make unfamiliar languages, techniques, libraries, and tools accessible.
- **Democratise participation.** Enable non-developers or adjacent roles to contribute directly and safely.

When your practice aligns with these aims, the benefits of AI assistance show up in day-to-day work: clearer code, faster reviews, fewer handoffs, and a codebase that is easier to change.

## Two Core Principles (Remember These)

These are the through-lines for the entire course. You’ll see them applied in every exercise and demo; they are simple to state and powerful in practice.

### 1) The Value Of Specificity — *“Use More Words”*
Vague prompts yield average guesses. Models rarely say “insufficient instruction”; they just produce something plausible. Be explicit about intent, constraints, acceptance criteria, style, and boundaries. Assume anything you don’t state will be guessed.

Short checklist when you brief an AI assistant or agent:
- What are we building, exactly?
- What does “good” look like (acceptance criteria)?
- What must not change? Any constraints or non-goals?
- Style, conventions, and integration points to follow?

Specificity is not verbosity; it is clarity. The more precisely you define the target and the edges, the more consistently the outputs match your intent.

### 2) Curating And Preparing Context
Generic models don’t know your project. Provide the context that makes them behave like your teammate:

- **Project reality:** structure, naming, coding conventions and style.
- **Process:** branching model, PR requirements, release and deploy steps.
- **References:** library/framework documentation, APIs you use, goals and acceptance criteria.
- **Mechanisms:** rule files and living docs under version control (e.g., `AGENTS.md`, `.ruler`), specialised tools like MCP servers, and CLI utilities that inject contextual information.

Treat context as part of the codebase. Clear prompts plus rich, project-specific context produce dependable results. As the project evolves, keep this context up to date; it’s the backbone that allows agents to act safely and predictably.

## Course Scope

We look across the entire software lifecycle—planning and specification through implementation, testing, integration, and deployment—without tying you to a single vendor or tool. The focus is practical skills for individuals and for teams. Each week builds on the last so you can apply ideas immediately.

- **Week 1: Foundation & Personalisation.**
  How these tools work, how to configure them, and how to build a context stack that fits your project.
- **Week 2: Interactive Development & Collaboration.**
  Working with IDE and terminal agents; collaborating in teams; taking a feature from idea to a merge-ready PR.
- **Week 3: Async Agents, CI/CD & Advanced Techniques.**
  Background agents, schedule- and event-driven tasks, and ways to embed AI into delivery pipelines.

Read this handout before the live session if you can; it will make the demos easier to follow. After the session, return to it while you implement the exercises so the steps are fresh in mind.

## What This Course Is *Not*

Setting expectations helps:

- Not “vibe coding”: the techniques aim for precise, dependable outcomes.
- Not about replacing developers: the goal is to augment capability and raise standards.
- Not a general AI survey or a complete compendium of software best practice: we revisit only the concepts needed to use AI effectively in engineering.

This framing keeps the course focused on what improves your day-to-day work: disciplined practice that reliably produces better software.

## Participation: How To Learn Here

You’ll get the most value by engaging actively and keeping feedback loops short. Bring your own code and your own constraints into the conversation; that’s where the techniques pay off.

**Ask questions.** There’s a Q&A session each week; bring anything from your context. Use the community space (Discord / course forum) to ask asynchronously and compare notes. Questions that feel basic often surface assumptions everyone shares.

**Do the homework.** Each part includes core exercises and stretch goals. Attempt them independently first; a weekly live practice session then walks through complete solutions so you can compare approaches. Treat this as rehearsal for how you’ll use the tools on your own projects.

**Use the materials.** You have permanent access to recordings, slides/handouts, and deep-dive links (via Maven). Keep the handout open while you work; refer to it when shaping prompts or deciding which modality to use.

**Sharing.** Please keep course materials within the cohort. Share what you’ve learned on blogs or social media; let us know so we can help amplify. Public reflection is a good way to consolidate your own understanding.

## Tools (Vendor-Agnostic)

The course is tool-agnostic. Use what you already have, or any equivalents. Tool choice matters less than how you brief and review the work; that’s where quality comes from.

- **IDE with AI capabilities** — e.g., VS Code with GitHub Copilot Chat, Cursor, Windsurf, Zed, Kiro; or VS Code with extensions like Copilot, Codium, Claude, or Codex.
- **Terminal/CLI coding agent** — e.g., Claude Code, Codex CLI, Gemini CLI, Copilot CLI, opencode, Warp.
- **Asynchronous/background agent** — e.g., GitHub’s Copilot/SWE-agent, OpenHands, Devin, or a CLI tool running via a GitHub Action.

Many options include free tiers; some sponsors provide credits you can use for course work. If you don’t have a background agent, you can still follow along by running tasks non-interactively in a terminal agent. Review the results like a PR; the workflow is effectively the same.

## What You’ll See In The Demo

We’ll demonstrate how **specificity** and **context** change outcomes across modalities:

- **Modalities:** inline generation and completion; an IDE agent; a terminal agent.
- **Specificity levels:** a one-liner request → a clearer specification with requirements and acceptance criteria → the same spec **plus** project context (e.g., `AGENTS.md`, framework docs, MCP).

As we add clarity and context, quality and fit-to-project improve visibly. Watching the same task solved three ways makes the levers obvious—and gives you a template for your own work.

## Closing Thought

AI-assisted development is not separate from software engineering; it’s a way to apply established practice more effectively. If you remember only two things from Lesson 1, keep these: **be specific** and **curate context**. With those in place, the modalities—assistant, reviewer, agent, operator—become reliable parts of your day-to-day work. Bring this handout to the live session; it will serve as the map while we explore the territory.
