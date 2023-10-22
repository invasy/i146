import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin

from i146.numsys.positional import Numeral
from i146.util import subscript


@dataclass
class NumSysProblem(DataClassJSONMixin, DataClassYAMLMixin, metaclass=ABCMeta):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def has_solution(self) -> bool:
        return False

    @property
    def solution(self) -> Optional[str]:
        return None

    @property
    @abstractmethod
    def answer(self) -> str:
        pass

    @abstractmethod
    def with_answer(self) -> str:
        pass


@dataclass
class NumSysConvertionProblem(NumSysProblem):
    a: str
    base1: int
    base2: int

    def __post_init__(self) -> None:
        self._a = Numeral(self.a, self.base1)
        self._b = self._a.convert(self.base2)

    def __str__(self) -> str:
        return f'{self._a} = ?{subscript(self._b.base)}'

    @property
    def answer(self) -> str:
        return str(self._b)

    def with_answer(self) -> str:
        return f'{self._a} = {self._b}'


@dataclass
class NumSysMultiplicationProblem(NumSysProblem):
    a: str
    b: str
    base: int

    def __post_init__(self) -> None:
        self._numeral = Numeral(self.a, self.base) * Numeral(self.b, self.base)

    def __str__(self) -> str:
        return str(self._numeral.computation)

    def has_solution(self) -> bool:
        return True

    @property
    def solution(self) -> str:
        return self._numeral.solution

    @property
    def answer(self) -> str:
        return str(self._numeral)

    def with_answer(self) -> str:
        return self._numeral.answer


@dataclass
class NumSysProblemSet(DataClassJSONMixin, DataClassYAMLMixin):
    problems: List[Union[*NumSysProblem.__subclasses__()]]

    def __str__(self) -> str:
        return '\n'.join([f'{i}) {p}' for i, p in enumerate(self.problems, start=1)])

    def answers(self) -> str:
        s = []
        for i, p in enumerate(self.problems, start=1):
            line = f'{i}) {p.with_answer()}'
            if p.has_solution():
                line += '\n' + p.solution
            s.append(line)
        return '\n\n'.join(s)