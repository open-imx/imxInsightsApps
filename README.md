# 🚄 imxInsightsApps

**imxInsightsApps** is the frontend and API layer for the [imxInsights](https://github.com/open-imx/imxInsights) library — a toolkit for analyzing and visualizing ProRail IMX data. This project wraps core functionality into a sleek [NiceGUI](https://nicegui.io/) web interface and a robust [FastAPI](https://fastapi.tiangolo.com/) backend.

---

## ✨ Features

- 🖥️ **Web Interface (NiceGUI)**  
  A modern, interactive UI for inspecting IMX files, running diffs, exporting reports, and more.

- 🔌 **API (FastAPI)**  
  Programmatic access to core functionality:
  - IMX file comparison
  - Population validation

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/open-imx/imxInsightsApps.git
cd imxInsightsApps
pip install -e .[all]
```

### ▶️ Run the App

```bash
# Start the NiceGUI web app
python -m imxInsightsApps.web

# OR start the FastAPI backend
uvicorn imxInsightsApps.api:app --reload
```

---

## 🧪 Development

We follow a strict [Git Flow](./CONTRIBUTING.md#🌱-git-flow-feature-→-dev-→-main) to ensure stability and clean releases.

```bash
# Create a feature branch
git checkout -b feature/my-feature dev

# Bump version
hatch version minor  # or patch / major / dev / rc

# Run tests
pytest
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full development & release guidelines.

---

## 📁 Project Structure

```
imxInsightsApps/
├── api/              # FastAPI implementation
├── web/              # NiceGUI-based frontend
├── core/             # Shared utils and logic
├── __init__.py       # Version entry point
```

---

## 📚 Related Projects

- [`imxInsights`](https://github.com/open-imx/imxInsights) – Core engine for IMX data processing
- [`open-imx.nl`](https://open-imx.nl) – Community and documentation portal

---

## 💬 Feedback & Contributions

We welcome issues, suggestions, and PRs!  
Check out our [Contribution Guide](./CONTRIBUTING.md) and help improve railway data tools for everyone.

---

## 🛡 License

[MIT License](LICENSE) © Open-IMX contributors