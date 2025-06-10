# 🤝 Contributing Guidelines

We welcome contributions! Here's how to get started with our Git flow and versioning strategy.

---

## ✅ Linting & Testing Expectations

Before submitting code, make sure it passes linting and tests.

### 🧪 Run tests

```bash
hatch run test-fast
```

Uses `pytest` to check your changes don't break anything.

### 🧼 Linting (auto-fix)

```bash
hatch run lint
```

This will:
- Sort imports with `isort`
- Format code using `ruff`
- Check types with `mypy`

### 🔍 Lint check (CI-style, no auto-fixes)

```bash
hatch run lint-check
```

Runs:
- Format check: `ruff format --check`
- Static checks: `ruff check`
- Type checks: `mypy`
- GitHub workflow linter: `zizmor .github/workflows/`

> 💡 Tip: Run `lint` before committing to avoid CI failures.

## 🌱 Git Flow: Feature → Dev → Main

Our team follows a streamlined Git workflow:

1. **🌿 Feature branches**
   - Branch from `dev`:  
     ```bash
     git checkout -b feature/your-awesome-feature dev
     ```
   - Build features or fix bugs here.

2. **🌊 Development branch (`dev`)**
   - Merge all feature branches here.
   - Triggers **pre-releases** (`1.3.0-dev.2`).
   - Used for internal testing. Can be unstable — and that’s okay.

3. **🚀 Main branch (`main`)**
   - Only merges **tested and reviewed** code from `dev`.
   - Triggers **stable releases** (`1.3.0`).
   - Always stays in a **deployable** state.

> ### 🔁 You break it, you fix it.
> - Applies to both `dev` and `main` — no exceptions.
> - If you break something, patch or revert it!
> - Communicate issues early — we're a team.

🧼 Clean `dev` → ⚙️ Smooth `main` → 🟢 Green CI → 🍻 Happy team

---

## 📦 Versioning Rules

| Type                  | Bump Type | Example           |
|-----------------------|-----------|-------------------|
| 🐞 Bug fix             | `patch`   | `1.2.4 → 1.2.5`    |
| ✨ New feature         | `minor`   | `1.2.5 → 1.3.0`    |
| 💥 Breaking change     | `major`   | `1.3.0 → 2.0.0`    |

### 🧪 Pre-releases

Versioning is handled by [`hatch`](https://hatch.pypa.io/)` version`
- 
- Development: `-dev.N` (e.g. `1.3.0-dev.2`)
- Release candidates: `-rc.N` (e.g. `1.3.0-rc.1`)

| Command                   | Result              | New Version  |
|---------------------------| ------------------- | ------------ |
| `hatch version dev`       | Next dev version    | `0.2.0.dev2` |
| `hatch version rc`        | First release cand. | `0.2.0rc1`   |
| `hatch version release`   | Final release       | `0.2.0`      |
| `hatch version patch`     | Next patch dev      | `0.2.1.dev0` |
| `hatch version minor`     | Next minor dev      | `0.3.0.dev0` |
| `hatch version major`     | Next major dev      | `1.0.0.dev0` |

The version lives in `imxInsightsApps/__init__.py`.

---

## 🚀 Release Automation

| Workflow         | Trigger                  | Action                                                            |
|------------------|--------------------------|-------------------------------------------------------------------|
| 🧪 Pre-release    | Push to `dev` or `main`  | Publishes pre-release if version is new                          |
| 🤖 Auto-release   | Dependency updates       | Bumps patch, opens PR, merges, releases                          |

- Version diffs are checked via GitHub Releases API vs `__init__.py`.
- Dev branch triggers pre-releases automatically.
- Main branch triggers **stable releases** — only when the version has increased.

---

Let us know if you have questions or suggestions. Happy coding! 🛤️✨
