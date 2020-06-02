import logging
import pathlib
import sys

repos_path = pathlib.Path("./repos")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


logger = logging.getLogger(__name__)


def rename_tests():
    for test_dir in repos_path.rglob("*/actors/*/tests"):
        actor_name = test_dir.parent.name
        for test_module in test_dir.rglob("*test*.py"):
            if actor_name not in test_module.name:
                new_test_module = test_module.rename(
                    pathlib.Path(
                        test_module.parent,
                        f"{test_module.stem}_{actor_name}{test_module.suffix}",
                    )
                )
                logger.info(
                    f"Actor name: {actor_name}:  {test_module.name} renamed to {new_test_module.name}"
                )


def rename_libs():
    for lib_dir in repos_path.rglob("*/actors/*/*/libraries"):
        actor_name = lib_dir.parent.name
        for lib_module in lib_dir.rglob("library.py"):
            new_lib_module = lib_module.rename(
                pathlib.Path(
                    lib_module.parent, f"{actor_name}{lib_module.suffix}",
                )
            )
            logger.info(
                f"Actor name: {actor_name}:  {lib_module.name} renamed to "
                f"{new_lib_module.name}"
            )


if __name__ == "__main__":
    pass
    # rename_libs()
