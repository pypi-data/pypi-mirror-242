from dataclasses import dataclass
from requests import post, get
from typing import Optional, List, Callable
from itertools import chain

def variable_value_proposition_todict(variable_prop) -> dict:
    return {
        "id": variable_prop.id,
        "type": variable_prop.__class__.__name__,
        "value": float(variable_prop.value),
        "variables": list(
            map(
                lambda variable: variable.to_dict(),
                variable_prop.variables,
            )
        )
    }

def hash_variable_value_proposition(variable_prop) -> int:
    return hash(
        sum(
            map(
                hash,
                variable_prop.variables
            )
        ) + variable_prop.value + hash(variable_prop.id)
    )

def variable_proposition_todict(variable_prop) -> dict:
    return {
        "id": variable_prop.id,
        "type": variable_prop.__class__.__name__,
        "variables": list(
            map(
                lambda variable: variable.to_dict(),
                variable_prop.variables,
            )
        )
    }

def hash_variable_proposition(variable_prop) -> int:
    return hash(
        sum(
            map(
                hash,
                variable_prop.variables
            )
        ) + hash(variable_prop.id)
    )

@dataclass
class Proposition:
    
    def explode_variables(self) -> list:
        if hasattr(self, "variables"):
            return list(
                filter(
                    lambda x: x is not None,
                    set(
                        chain(
                            *map(
                                lambda variable: variable.explode_variables(),
                                self.variables,
                            ),
                            [self.id]
                        )
                    )
                )
            )
        else:
            return [self.id]
        
@dataclass
class Variable(Proposition):
    id: str

    def __hash__(self) -> int:
        return hash(self.id)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": "Variable",
        }

@dataclass
class AtLeast(Proposition):
    value: int
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_value_proposition(self)

    def to_dict(self) -> dict:
        return variable_value_proposition_todict(self)

@dataclass
class AtMost(Proposition):
    value: int
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_value_proposition(self)

    def to_dict(self) -> dict:
        return variable_value_proposition_todict(self)

@dataclass
class And(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_proposition(self)

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Or(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_proposition(self)

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Xor(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_proposition(self)

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class XNor(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def __hash__(self) -> int:
        return hash_variable_proposition(self)

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Implies(Proposition):
    left:   Proposition
    right:  Proposition
    id: Optional[str] = None

    @property
    def variables(self):
        return [self.left, self.right]

    def __hash__(self) -> int:
        return hash(
            sum([
                hash(self.left),
                hash(self.right),
                hash(self.id),
            ])
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

@dataclass
class Evaluation:
    data: Optional[List[List[str]]]
    error:  Optional[str]
    
class evaluation_composer:

    def __init__(self, backend_url: str):
        assert evaluation_composer.__check_health__(backend_url), f"Backend {backend_url} is not up/healthy"
        self.backend_url = backend_url
    
    @staticmethod
    def __check_health__(backend_url: str): 
        return get(
            f"{backend_url}/health",
        ).status_code == 200

    def __call__(self, propositions: List[Proposition], interpretations: List[dict]) -> Callable[[List[Proposition], dict], Evaluation]:
        try:
            response = post(
                f"{self.backend_url}/evaluate",
                json={
                    "propositions": list(
                        map(
                            lambda p: p.to_dict(),
                            propositions,
                        )
                    ),
                    "interpretations": interpretations,
                }
            )
            if response.status_code == 200:
                data = response.json()
                return Evaluation(
                    data=list(
                        chain(
                            *map(
                                lambda i: map(
                                    lambda j: (i,j), 
                                    data[i]
                                ), 
                                filter(
                                    lambda i: data[i], 
                                    range(len(data))
                                )
                            )
                        )
                    ),
                    error=None,
                )
            else:
                return Evaluation(
                    data=None,
                    error=response.text,
                )
        except Exception as e:
            return Evaluation(
                data=None,
                error=str(e),
            )