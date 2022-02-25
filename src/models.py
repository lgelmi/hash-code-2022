from collections import defaultdict
from dataclasses import dataclass

from utils import compose


@dataclass(frozen=True)
class Role:
    name: str
    level: int


@dataclass(frozen=True)
class Contributor:
    name: str
    skills: defaultdict[str, int]

    def learn(self, skill: str) -> "Contributor":
        new_skills = self.skills.copy()
        new_skills[skill] += 1
        return Contributor(self.name, new_skills)

    def __hash__(self):
        return hash((self.name, tuple(zip(self.skills.keys(), self.skills.values()))))

    def can_mentor(self, role: Role) -> bool:
        return self.skills[role.name] >= role.level

    def can_be_assigned_mentors(self, role: Role, mentors: set["Contributor"]) -> bool:
        return self.skills[role.name] >= role.level - (
            1 if any(mentor.can_mentor(role) for mentor in mentors) else 0
        )


@dataclass(frozen=True)
class Project:
    name: str
    duration: int
    score: int
    best_before: int
    roles: tuple[Role]

    def current_score(self, today: int) -> int:
        return self.score - max((self.best_before - today), 0)

    def max_score(self, today: int) -> int:
        return max(self.current_score(today) - self.duration, 0)

    @classmethod
    def dummy_project(cls, name) -> "Project":
        return cls(name, 0, 0, 0, tuple())


@dataclass(frozen=True)
class ProjectTeam:
    project: Project
    started: int
    team: frozenset[Contributor]

    def can_close(self, today: int) -> bool:
        return self.project.duration + (self.started - today) <= 0

    @classmethod
    def dummy_team(cls, name: str, names: list[str]) -> "ProjectTeam":
        return cls(
            Project.dummy_project(name),
            0,
            frozenset(Contributor(c_name, defaultdict(int)) for c_name in names),
        )


@dataclass(frozen=True)
class State:
    day: int
    todo: frozenset(Project)
    running: frozenset(ProjectTeam)
    done: frozenset(ProjectTeam)
    idle: frozenset(Contributor)


class Engine:

    scoring: callable
    assigning: callable

    def next_day(self, state: State) -> State:
        return compose(self.prioritize, self.assign, self.work)(state)

    def work(self, state: State) -> State:
        pass

    def assign(self, state: State) -> State:
        pass

    def prioritize(self, state: State) -> State:
        pass
