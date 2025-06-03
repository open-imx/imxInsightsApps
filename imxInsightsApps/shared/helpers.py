from pathlib import Path

from imxInsights import ImxContainer, ImxSingleFile
from imxInsights.file.singleFileImx.imxSituationEnum import ImxSituationEnum


def load_imxinsights_container_or_file(path: Path, situation: ImxSituationEnum | None):
    if path.suffix == ".zip":
        return ImxContainer(path)
    elif path.suffix == ".xml":
        if not situation:
            raise ValueError(f"Situation must be specified for single IMX file: {path}")
        imx = ImxSingleFile(path)
        return {
            ImxSituationEnum.InitialSituation: imx.initial_situation,
            ImxSituationEnum.NewSituation: imx.new_situation,
            ImxSituationEnum.Situation: imx.situation,
        }.get(situation)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
