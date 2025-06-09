from nicegui import ui


def update_situation_select(situations: list[str], element):
    if situations:
        element.options = situations
        element.props(remove="disable")
        if len(situations) == 1:
            element.value = situations[0]
            ui.notify(f"🧠 Auto-detected situation: {situations[0]}", type="info")
        else:
            element.value = ""
            ui.notify(
                f"🧠 Multiple situations found: {', '.join(situations)}", type="info"
            )
    else:
        element.options, element.value = [], ""
        element.props("disable")
        ui.notify("❓ No known situation elements found in XML.", type="warning")


def reset_situation(label: str, situation_element, state):
    state["uploaded_files"].pop(label, None)
    state["file_extensions"][label] = None
    situation_element.value = ""
    situation_element.props("disable")
    ui.notify(f"🗑️ {label.upper()} file removed. Situation reset.", type="warning")
