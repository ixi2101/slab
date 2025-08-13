from dataclasses import dataclass
from pathlib import Path
from .containers import ContainerRunner


class Builder():
    def __init__(self, _output_dir: Path):
        output_dir = _output_dir
        containers = ContainerRunner()
        containers.build_cross_compile_images()


    def build_strace(self):
        print("build strace")
