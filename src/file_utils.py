from collections import defaultdict
from pathlib import Path
from typing import IO

from consts import OUT_PATH, RSC_PATH, files
from models import Contributor, Project, Role


def read_challenge_file(filename: str):
    return read_file(RSC_PATH / f"{filename}.in.txt")


def read_file(file: Path) -> tuple[list[Contributor], list[Project]]:
    with file.open() as content:
        contr_n, proj_n = map(int, content.readline().split(" "))
        contrs = [read_contributor(content) for _ in range(contr_n)]
        print(*contrs, sep="\n")
        projs = [read_projects(content) for _ in range(contr_n)]
        print(*projs, sep="\n")
    return contrs, projs


def read_contributor(content: IO) -> Contributor:
    name, skill_n = content.readline().split(" ")
    return Contributor(
        name, defaultdict(int, tuple(read_skill(content) for _ in range(int(skill_n))))
    )


def read_skill(content: IO) -> tuple[str, int]:
    name, level = content.readline().split()
    return name, int(level)


def read_projects(content: IO) -> Project:
    name, *others = content.readline().split(" ")
    days, score, best_before, roles_n = map(int, others)
    return Project(
        name,
        days,
        score,
        best_before,
        tuple(read_role(content) for _ in range(int(roles_n))),
    )


def read_role(content: IO) -> Role:
    name, level = content.readline().split()
    return Role(name, int(level))


if __name__ == "__main__":
    read_challenge_file(files[0])
