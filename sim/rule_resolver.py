import re
import random
from typing import Any, Dict, Union, List
from .config import DataRule
from .faker_utils import get_faker

class RuleResolver:
    """Resolves dynamic field generation rules in event data."""
    
    RULE_PATTERN = re.compile(r'^(\w+)\((.*)\)$')
    
    def __init__(self):
        self.faker = get_faker()
        self._register_resolvers()

    def _register_resolvers(self):
        """Register all available rule resolvers."""
        self._resolvers = {
            'random': self._resolve_random,
            'static': self._resolve_static,
            'random_text': self._resolve_random_text
        }

    def parse_rule(self, rule_str: str) -> DataRule:
        """Parse a rule string into a DataRule object."""
        if not isinstance(rule_str, str):
            return None
            
        match = self.RULE_PATTERN.match(rule_str)
        if not match:
            return None
            
        rule_type, args_str = match.groups()
        
        # Parse arguments
        args: List[Union[int, float, str]] = []
        kwargs: Dict[str, Union[int, float, str]] = {}
        
        if args_str:
            # Split by comma, handling quoted strings
            parts = re.findall(r'[^,]+|"[^"]*"', args_str)
            for part in parts:
                part = part.strip()
                if '=' in part:
                    key, value = part.split('=', 1)
                    kwargs[key.strip()] = self._parse_value(value.strip())
                else:
                    args.append(self._parse_value(part))
        
        return DataRule(type=rule_type, args=args, kwargs=kwargs)

    def _parse_value(self, value: str) -> Union[int, float, str]:
        """Parse a string value into the appropriate type."""
        value = value.strip('"\'')
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def resolve_rule(self, rule: DataRule) -> Any:
        """Resolve a DataRule into a concrete value."""
        if rule.type not in self._resolvers:
            raise ValueError(f"Unknown rule type: {rule.type}")
        
        return self._resolvers[rule.type](rule.args, rule.kwargs)

    def _resolve_random(self, args: List[Any], kwargs: Dict[str, Any]) -> Union[int, float]:
        """Resolve a random number rule."""
        if len(args) != 2:
            raise ValueError("Random rule requires exactly 2 arguments: min and max")
        
        min_val, max_val = args
        if isinstance(min_val, float) or isinstance(max_val, float):
            return random.uniform(min_val, max_val)
        return random.randint(min_val, max_val)

    def _resolve_static(self, args: List[Any], kwargs: Dict[str, Any]) -> Any:
        """Resolve a static value rule."""
        if len(args) != 1:
            raise ValueError("Static rule requires exactly 1 argument")
        return args[0]

    def _resolve_random_text(self, args: List[Any], kwargs: Dict[str, Any]) -> str:
        """Resolve a random text generation rule."""
        if len(args) != 1:
            raise ValueError("Random text rule requires exactly 1 argument: category")
        
        category = args[0]
        # Use faker to generate contextual random text
        if category == "onboarding":
            templates = [
                "Complete user onboarding flow",
                "Setup initial workspace configuration",
                "First-time user experience improvements",
                "Onboarding checklist implementation"
            ]
            return random.choice(templates)
        
        return self.faker.sentence()

    def resolve_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively resolve all rules in a data dictionary."""
        resolved = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                rule = self.parse_rule(value)
                if rule:
                    resolved[key] = self.resolve_rule(rule)
                else:
                    resolved[key] = value
            elif isinstance(value, dict):
                resolved[key] = self.resolve_data(value)
            elif isinstance(value, list):
                resolved[key] = [
                    self.resolve_data(item) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            else:
                resolved[key] = value
                
        return resolved
