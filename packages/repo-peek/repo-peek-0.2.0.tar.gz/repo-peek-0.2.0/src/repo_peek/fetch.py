"""fetch a remote repo and open in a local editor."""
import asyncio
import os
from pathlib import Path
import shutil

from .logging import logger
from .config import Config
from .config import EDITORS
from .config import init_dir
from .utils import fetch_repo
from .utils import extract


async def open_editor(editor="vim", path: Path = Path("")):
    """open editor with source."""
    editor = os.getenv("EDITOR", editor)
    if not editor in EDITORS:
        editor = "vim"
        logger.info("EDITOR not support, defaulting to vim")
    logger.info("opening in : {}".format(editor))
    process = await asyncio.create_subprocess_exec(editor, str(path))
    await process.communicate()


def is_old(config_file: Path) -> bool:
    """if count is zero, return True, else False"""
    with open(config_file, "r") as fh:
        line = fh.readline()
        count = int(line.split("=")[1])
        if count == 0:
            return True
        else:
            return False


def rm_stored_repos(home_dir):
    logger.info("removing cached dir: {}".format(home_dir))
    shutil.rmtree(home_dir, ignore_errors=True)


async def peek_repo(repo: str, caching=True):
    parsed_config = Config(".githubkeep.ini")
    cache_dir = Path.home() / ".githubkeep"
    repo_dir = init_dir(cache_dir / "repos" / repo)
    if os.path.isdir(repo_dir) and os.listdir(repo_dir):
        await open_editor(path=repo_dir)
    else:
        parsed_config = Config(".githubkeep.ini")
        tar_dirs = init_dir(cache_dir / "tars")
        logger.info("fetching repo: {}".format(repo))
        parsed_config.config.remove_section(repo)
        parsed_config.cache_repo(repo)
        repo_name = await fetch_repo(repo, tar_dirs)
        logger.info("extracting repo: {} to {}".format(repo_name, repo_dir))
        await extract(repo_name, repo_dir)
        await open_editor(path=repo_dir)
    if parsed_config.is_repo_stale(repo):
        rm_stored_repos(cache_dir)
        parsed_config.config.remove_section(repo)


# download readme from cdn to the dir in which editor is openend
# extract files to the same dir
# use gitlab api to clone
# types
# profile and imporve loading time


def main(repo="rahulunair/cloudstore"):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(peek_repo(repo))
