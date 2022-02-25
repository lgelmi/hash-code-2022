from pathlib import Path

from consts import OUT_PATH
from models import ProjectTeam


def write_challenge_file(filename: str, submissions: tuple[ProjectTeam]):
    return write_file(OUT_PATH / f"{filename}.out.txt", submissions)


def write_file(file: Path, submissions: tuple[ProjectTeam]):
    lines = [
        f"{len(submissions)}\n",
        "\n".join(write_submission(submission) for submission in submissions),
    ]
    with file.open("w") as stream:
        stream.writelines(lines)


def write_submission(submission: ProjectTeam) -> str:
    return f"{submission.project.name}\n{' '.join(contributor.name for contributor in submission.team)}"


if __name__ == "__main__":
    submissions = (
        ProjectTeam.dummy_team("WebServer", ["Bob", "Anna"]),
        ProjectTeam.dummy_team("Logging", ["Anna"]),
        ProjectTeam.dummy_team("WebChat", ["Maria", "Bob"]),
    )
    write_challenge_file("writer_test", submissions)
