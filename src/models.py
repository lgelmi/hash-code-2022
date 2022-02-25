from collections import defaultdict
from dataclasses import dataclass


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


@dataclass(frozen=True)
class ProjectTeam:
    project: Project
    started: int
    team: frozenset[Contributor]

    def is_done(self, today: int) -> bool:
        return self.project.duration + (self.started - today) <= 0
