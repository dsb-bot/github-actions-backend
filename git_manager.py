import os
import subprocess

from utils import logger


class GitManager:
    """Commit saved plans to the repository containing the running application."""

    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

    def initialize_repo(self):
        if not os.path.isdir(os.path.join(self.repo_dir, ".git")):
            raise RuntimeError(f"Kein Git-Repository gefunden: {self.repo_dir}")

        # Scheduled runs may start from a checkout that predates a manual commit.
        # Do not pull here: the Actions workflow serializes runs and checks out HEAD.
        logger.info(f"Verwende Repository in {self.repo_dir}.")

    def push_changes(self, message="Automated plan update"):
        self._run_git(["add", "--", "plans/", ".plan_state.json"])
        staged = self._run_git(
            ["diff", "--cached", "--quiet", "--", "plans/", ".plan_state.json"],
            check=False,
        )
        if staged.returncode == 0:
            logger.debug("Keine Änderungen zum Committen gefunden.")
            return

        branch = self._run_git(
            ["branch", "--show-current"], capture_output=True
        ).stdout.strip()
        if not branch:
            raise RuntimeError("Der aktuelle Git-Branch ist nicht bestimmt.")

        self._run_git(["config", "user.name", "github-actions[bot]"])
        self._run_git(
            ["config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"]
        )
        self._run_git(["commit", "-m", message, "--", "plans/", ".plan_state.json"])
        self._run_git(["push", "origin", f"HEAD:{branch}"])
        logger.info("Planänderungen wurden ins aktuelle Repository gepusht.")

    def _run_git(self, args, capture_output=False, check=True):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_dir,
            check=check,
            capture_output=capture_output,
            text=True,
        )
