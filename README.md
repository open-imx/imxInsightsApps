
---

## 🌱 Git Flow: Feature → Dev → Main

Our development workflow follows a simple Git flow 🛤️✨.

1. **🌿 Feature branches**
   - 🛠️ Created from `dev`
   - 🧪 Used for building features or fixing bugs
   - 💡 Example: `git checkout -b feature/add-theme-toggle`

2. **🌊 Development branch (`dev`)**
   - 🔗 Integrates all feature branches
   - 🚧 Every push triggers a **pre-release** (e.g. `1.3.0-dev.2`)
   - 🧫 Used for internal testing — may be unstable, and that’s OK

3. **🚀 Main branch (`main`)**
   - ✅ Only receives tested & reviewed code from `dev`
   - 📦 Every push triggers a **stable release** (e.g. `1.3.0`)
   - 🟢 Should always be in a deployable state — no excuses
   
### 🔁 **You break it, you fix it.**  

> 
> 🧯 Applies to both `dev` and `main` — no exceptions.  
> 🕵️‍♂️ Find the issue • 🔧 Patch or revert it!  
> 🤝 We're all in this together • 📣 Let us know 
>
> 🧼 Clean `dev` = ⚙️ Smooth `main` = 🟢 Green CI = 🍻 = 😎 Happy you 

---

## 🔁 Version Rules

🔧 Bug fix or dependency update → `PATCH` bump (`1.2.4 → 1.2.5`)  
✨ New feature added → `MINOR` bump (`1.2.5 → 1.3.0`)  
🚨 Breaking change → `MAJOR` bump (`1.3.0 → 2.0.0`)

🧪 **Pre-releases**:
- 🌱 Dev branch → `-dev.N` (e.g. `1.3.0-dev.2`)
- 🔍 Final test candidate → `-rc.N` (e.g. `1.3.0-rc.1`)

🛠️ Versioning is powered by [`hatch`](https://hatch.pypa.io/) and 📦 Stored in `imxInsightsApps/__init__.py`

---

## 🧩 Release Workflow Summary

| 🛠️ Workflow        | ⚡ Trigger                   | 🚀 Action                                                       |
|--------------------|-----------------------------|-----------------------------------------------------------------|
| 🧪 `Pre Release`   | 🔄 Push to `dev` or `main`   | 🏗️ Builds and publishes new version if it differs from latest    |
| 🤖 `Auto Release`  | 📦 Dependency update | 🔁 Bumps `patch`, creates PR, merges it, builds and releases     |


🔍 Version comparison is done using the GitHub Releases API and the version in `__init__.py`  
🧃 Pre-releases are **automatically flagged** when releasing from `dev`  
🛳️ Stable releases are created from `main` — **only if the version number has increased**

---

## 🛠 Hatch Commands

```bash
hatch version patch       # 🐞 Bug fix or 📦 dependency update
hatch version minor       # ✨ New feature
hatch version major       # 💥 Breaking change

hatch version dev         # 🧪 Development version
hatch version rc          # 🔍 Release candidate
