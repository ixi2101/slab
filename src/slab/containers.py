from typing import Dict, Optional
import docker
from docker.client import DockerClient
from docker.models.images import Image
import os
from .logging_config import get_logger

logger = get_logger(__name__)


class ContainerRunner:
    def __init__(self) -> None:
        self.client: DockerClient = docker.from_env()
        self.images: Dict[str, Optional[Image]] = {}

    def build_cross_compile_images(self) -> None:
        """Build Docker images for cross-compilation targets"""
        logger.info("Starting cross-compilation image builds")
        dockerfile_dir = os.path.join(os.path.dirname(__file__), "dockerfiles")

        # Build armv7 image
        logger.info("Building armv7 cross-compilation image")
        self.images["armv7"] = self._build_image(
            dockerfile_path=os.path.join(dockerfile_dir, "Dockerfile.armv7"),
            tag="slab-armv7-builder",
            context=dockerfile_dir,
        )

        # Build aarch64 image
        logger.info("Building aarch64 cross-compilation image")
        self.images["aarch64"] = self._build_image(
            dockerfile_path=os.path.join(dockerfile_dir, "Dockerfile.aarch64"),
            tag="slab-aarch64-builder",
            context=dockerfile_dir,
        )

        logger.info("Cross-compilation image builds completed")

    def _build_image(
        self, dockerfile_path: str, tag: str, context: str
    ) -> Optional[Image]:
        """Build a Docker image from a Dockerfile"""
        try:
            logger.debug(f"Building image {tag} from {dockerfile_path}")
            image, build_logs = self.client.images.build(
                path=context,
                dockerfile=os.path.basename(dockerfile_path),
                tag=tag,
                rm=True,
                forcerm=True,
            )
            logger.success(f"Successfully built image: {tag}")
            return image
        except docker.errors.BuildError as e:
            logger.error(f"Failed to build image {tag}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error building image {tag}: {e}")
            return None
