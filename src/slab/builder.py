from pathlib import Path
from .containers import ContainerRunner


class Builder:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.containers = ContainerRunner()
        self.containers.build_cross_compile_images()

    def build_strace(self) -> None:
        print("build strace")
