from pathlib import Path
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__)
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        choices=["qa", "stage", "prod"],
        help="Environment to run tests against"
    )

def pytest_configure(config):
    env = config.getoption("--env")

    env_file = Path(f"config/.env.{env}")

    if not env_file.exists():
        raise FileNotFoundError(f"Required environment file not found: {env_file}")

    load_dotenv(env_file)
    print(f"Loading environment from {env_file}")

    env_local_file = Path(f"config/.env.{env}.local")

    if env_local_file.exists():
        load_dotenv(env_local_file, override=True)
        print(f"Loaded environment variables from {env_local_file}")

def pytest_runtest_setup(item):
    description_mark = item.get_closest_marker("description")
    if description_mark and description_mark.args:
        logger.info(f"Test Description: {description_mark.args[0]}")

def pytest_json_runtest_metadata(item, call):
    if call.when == "call":
        description_mark = item.get_closest_marker("description")
        if description_mark and description_mark.args:
            return {"description": description_mark.args[0]}
    return {}
