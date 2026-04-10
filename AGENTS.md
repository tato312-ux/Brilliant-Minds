# Brilliant Minds AGENT GUIDE

## Mission

- DocSimplify is a dual experience: FastAPI backend (`src/`) and Next.js 16 App Router frontend (`frontend/`). Agents should keep both sides aligned and respectful of neurodiverse readers.
- This guide explains how to build, lint, test, and code within the repo conventions. Update it whenever you add new tooling, scripts, or rules.
- Before touching the frontend, read `frontend/AGENTS.md`; Next.js ships with breaking changes so the `node_modules/next/dist/docs/` notes matter.

## Build / Lint / Test Matrix

### Backend (FastAPI)

- Python 3.13 is required. From the repository root, install dependencies in editable mode so `src` is importable:

  ```bash
  py -3.13 -m pip install -e .
  ```

- Run the dev API with hot reload to keep `/docs` up-to-date:

  ```bash
  py -3.13 -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
  ```

- Execute the backend test suite from the repo root:

  ```bash
  py -3.13 -m pytest
  ```

- Add new tests under `tests/` and follow the existing fixture patterns (monkeypatch env vars, reload modules, cleanup `sys.modules`).

### Frontend (Next.js 16 + App Router)

- Use Node.js 18+. From `frontend/`, install dependencies:

  ```bash
  cd frontend
  npm install
  ```

- Launch the dev server (port 3000) with mocked APIs by default:

  ```bash
  npm run dev
  ```

- Switch to the real backend by setting `NEXT_PUBLIC_USE_MOCK_API=false` and `NEXT_PUBLIC_API_URL` in `frontend/.env.local` before restarting.
- Build and start the production preview:

  ```bash
  npm run build
  npm run start
  ```

- Run ESLint via `npm run lint`; this is the main quality gate for frontend changes and uses `eslint-config-next`.

### Running a Single Test

- Backend: use pytest selection syntax. Example:

  ```bash
  py -3.13 -m pytest tests/test_auth_service.py::test_login_with_wrong_password
  ```

- Add `-k <pattern>` for fuzzy matches and `-vv` for verbose output when diagnosing.
- Frontend: no test harness yet; if you add one (Vitest, Jest, etc.), tie it to an npm script (`npm run test:unit` or similar) and document the command here.
- Always rerun the lint scripts after editing UI surfaces to catch JSX/Next issues early.

## Code Style Guidelines

### Python / FastAPI

- Import only from the `src` package (e.g., `from src.services import auth_service`) so routers load cleanly when uvicorn boots.
- Route handlers must be `async def`; delegate blocking I/O to dedicated services. Avoid `time.sleep`, `requests`, or other blocking calls inside FastAPI endpoints.
- Use `src/models/schemas/` for all request/response models. Keep them precise and versioned per endpoint; reuse them across routers when semantics align.
- Services living under `src/services/` or `src/agents/` expose descriptive `snake_case` functions and raise the custom errors listed in `src/core/exceptions.py` rather than raw Python errors.
- Guard shared dependencies (security, blob containers, Azure Search) with `src/core/dependencies.py`, which allows FastAPI overrides for tests.
- Keep configuration within `src/config/settings.py`; tests override env vars via fixtures (see `tests/test_auth_service.py`) and reload the module to apply changes.
- Use the `logging` module instead of `print`; annotate each log with context (user, request id, stage). Wrap Azure/OpenAI/Redis calls with helpers that log retries and bubble final errors.
- Document non-obvious invariants with docstrings. Inline comments should explain *why* the code is necessary, not *what* it does.
- Annotate every helper, coroutine, and return value with static types (even simple ones) so IDEs can alert you if something drifts.
- Favor `async with` for clients and release resources quickly; keep context scope tight.

### TypeScript / Next.js / Tailwind

- Files in `frontend/app/` are Server Components by default. Only add `"use client"` inside files that truly need browser APIs/hooks.
- Prefer Tailwind utility classes for layout and theming; create reusable component classes inside `frontend/components/` for repeated patterns.
- Keep hook orders consistent (`useState`, `useMemo`, `useEffect`, etc.) and memoize derived values so Server Components render predictably.
- Lift repeated UI into shared components, pass clearly typed props, and avoid implicit dependencies (e.g., rely on provided palette values rather than reading globals directly).
- Use `Link` from `next/link` for navigation with descriptive link text and proper focus/aria states for accessibility.
- Store constants (palette data, option lists) near the top of pages or in `frontend/lib/`, type them with `type/interface`, and reuse them across the app.
- Keep `globals.css` geared toward semantic font stacks, CSS variables for colors, and atomic utility classes. Avoid ad-hoc inline CSS unless you need per-instance overrides.
- Always type props and state with `type`/`interface` definitions; rely on shared helper types like `ExperienceDraft` and `PalettePreference` from `frontend/lib/types.ts`.

### Imports & Formatting

- On the backend, group imports as: standard library → third-party → internal `src.*`. Keep them sorted alphabetically within each group.
- Frontend imports should also follow: React/Next → external libs → local modules. Use path aliases (e.g., `lib/`, `components/`) consistently.
- Format code with Prettier-style conventions: two spaces, trailing commas in multiline contexts (arrays/objects), and single quotes unless JSX/manipulation requires double quotes.
- Favor early returns and guard clauses. Keep the main happy path at the top of functions to reduce indentation and cognitive load.

### Naming Conventions

- Backend functions/variables are `snake_case`; classes, dataclasses, and Pydantic models are `PascalCase`. Keep names descriptive and focused on behavior (e.g., `register_user`, `process_document`).
- Frontend variables, props, and hooks use `camelCase`; components and value objects use `PascalCase`. Prefix boolean props with `is`/`has`/`should` when it clarifies truthiness checks.

### Error Handling & Observability

- Propagate custom errors from service layers to routers. Let FastAPI translate them into HTTP responses or wrap them with `HTTPException` when needed.
- Never swallow exceptions silently. Log unexpected failures with context and re-raise or translate into a structured error response.
- Wrap retryable operations (Azure clients, blob uploads, search requests) with helpers that log attempts, apply exponential backoff, and expose root causes after final failure.

## Cursor & Copilot Rules

- No `.cursor/` or `.cursorrules` directories exist today; if they appear later, document their instructions here verbatim.
- No `.github/copilot-instructions.md` file currently. Should it be added, summarize the instructions in this section so future agents know whether Copilot is allowed or restricted.

## Workflow Tips

- When touching both backend/frontend, keep commits scoped (e.g., `feat(api): add simplified docs`), and mention new env vars in the PR description.
- Run `npm run lint` before pushing frontend changes and `py -3.13 -m pytest` before merging backend work to keep CI friendly.
- Update this AGENT guide whenever you add scripts, change build commands, or discover new constraints so future agents can work without surprises.
- If a new tool or script is introduced, briefly explain why it exists and how to run it (include command, purpose, and targets).

## Backend Testing & Debugging Habits

- Use the existing `tests/test_auth_service.py` fixtures as templates: monkeypatch environment, reload modules via `_reload_module`, and cleanup `sys.modules` so each test starts from a blank state.
- Preserve `AUTH_DB_PATH` overrides per test; inject a `tmp_path / "users.db"` so you never write to shared storage.
- When debugging, run a single test with `pytest -vv` and `-k` filters, and re-run `py -3.13 -m pytest tests/test_auth_service.py -k register` if you change fixtures.
- For quick sanity checks, run `python -m pytest tests/test_auth_service.py::test_register_and_login` before pushing to ensure auth flows remain intact.
- Log output in tests via the `logging` module rather than print to keep logs consistent with production; configure pytest `log_cli` if you need realtime logs.

## Frontend Visual & Accessibility Guidelines

- Avoid collapsing into bland layouts: every page should have a rhythm (textures, gradient accents, purposeful typography) that matches DocSimplify’s brand.
- Use expressive fonts via CSS variables in `globals.css`. Avoid default stacks—pick complementary serif+sans pairs, then document them in `globals.css` comments.
- Introduce gentle motion (page load fades, staggered reveals in the hero) via `framer-motion`—no random micro-transitions. Keep animations intentional and accessible.
- Provide high-contrast options; palette data resides in `frontend/lib/profile.tsx`/`lib/types.ts`. Reference these constants instead of hardcoding colors to keep them in sync.
- Ensure every interactive element (buttons, links, toggles) is keyboard reachable and has `aria-label` or descriptive text. Reuse shared components to avoid missing focus states.
- Keep responsive behavior consistent by testing at key breakpoints: 375px, 768px, 1280px. Use Tailwind breakpoint helpers for layout shifts and base them on the `app/globals.css` grid tokens.
- Avoid relying solely on dark mode. Provide neutral/bright palettes with meaningful gradients that echo the `paletteCards` in `app/page.tsx`.

## Observability & Alerts

- For backend telemetry, wrap Azure/Search/OpenAI calls inside services such as `src/services/search_service.py` so you capture retries, latency, and errors centrally.
- Emit structured logs with `json.dumps` or `structlog` (if configured) and include context tags: request id, user id, intent summary. Keep log statements in services, not spread across routers.
- Configure `logging` in `src/main.py` or `src/config/settings.py` to send errors to Sentry/Azure Monitor (if added later); keep log levels at `INFO` for success and `ERROR` for failures.
- For frontend error handling, show friendly fallback UI on fetch failures and log the underlying error via `console.error` or a telemetry hook; ensure the user sees a calm message.
- Document new observability endpoints (`/health`, `/docs`) and ensure they stay in sync with README notes whenever you add new services.

## Security & Secrets Handling

- Never commit secrets. Keep `.env` files out of git and share them via secure channels.
- Use `python-dotenv` (backend) and `.env.local` (frontend) for local overrides; document required keys in README and this guide so future agents can replicate the environment.
- For auth, rely on `JWT_SECRET_KEY`, `COSMOS_*`, and `AZURE_SEARCH_*` variables defined in `.env.example`; if you add new secrets, append them to the example immediately.
- For clipboard or developer helpers, avoid logging raw tokens or keys—mask them when logging or raise sanitized errors.

## Documentation & Learning

- When you add new endpoints or UI flows, update README + this AGENT guide so future agents know how to run and test them.
- If you build a shareable workflow (e.g., a detailed doc simplification pipeline), document it in `docs/` or the `README` rather than only in code comments.
- Encourage future agents to explain architectural tradeoffs in the AGENT guide before merging—this maintains the “concepts > code” philosophy.
