# 🚄 imxInsightsApps

**imxInsightsApps** is the frontend and API layer for the [imxInsights](https://github.com/open-imx/imxInsights) library — a toolkit for analyzing and visualizing IMX data. This project wraps core functionality into a sleek [NiceGUI](https://nicegui.io/) web interface and a robust [FastAPI](https://fastapi.tiangolo.com/) backend.

***THIS LIBRARY*** is a personal project and therefore no responsibility for the functionality, accuracy, or usage of this library. 
***THE PUBLIC retains full ownership and responsibility for the codebase.***

---

## ✨ Features

- 🖥️ **Web Interface (NiceGUI)**  
  A modern, interactive UI for inspecting IMX files, running diffs, exporting reports, and more.

- 🔌 **API (FastAPI)**  
  Programmatic access to core functionality:
  - IMX file comparison
  - Population validation
  - Excel and geojson support

⚠️ Heads up! We use Sentry.io to monitor and improve our application's stability. It helps us detect and resolve issues faster.

---

## 🚀 Getting Started

### ▶️ Run the App

```bash
# Start the NiceGUI app
python imxInsightsApps\gui\main.py

# OR start the FastAPI api
python run_api.py
```

---

## Open-IMX Initiative
**imxInsights** is part of the **Open-IMX initiative**, which is dedicated to enhancing the accessibility and usability of IMX data. 
This initiative aims to provide a collaborative environment for developers, data analysts and railway professionals to effectively work with IMX data.

### 🗪 Discord Community Channel 🤝

💥 We invite you to join the [👉 open-imx community on Discord](https://discord.gg/wBses7bPFg). 

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
├── gui/              # NiceGUI-based frontend
├── shared/           # Shared utils and logic
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