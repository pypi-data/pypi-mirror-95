# No docstring here as it would appear in the rules docs.
# Rule definitions for the standard ruleset, dynamically imported from the directory.
# noqa

import os
from importlib import import_module
from glob import glob

# All rule files are expected in the format of L*.py
rules_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "L*.py")

# Create a rules dictionary for importing in sqlfluff/src/sqlfluff/core/rules/__init__.py
rules = []

# Sphinx effectively runs an import * from this module in rules.rst, so initialise
# __all__ with an empty list before we populate it with the rule names.
__all__ = []

for module in sorted(glob(rules_path)):
    # Manipulate the module path to extract the filename without the .py
    rule_id = os.path.splitext(os.path.basename(module))[0]
    # All rule classes are expected in the format of Rule_L*
    rule_class_name = f"Rule_{rule_id}"
    try:
        rule_class = getattr(
            import_module(f"sqlfluff.core.rules.std.{rule_id}"), rule_class_name
        )
    except AttributeError:
        raise (AttributeError("Rule classes must be named in the format of L*."))
    # Add the rules to the rules dictionary for sqlfluff/src/sqlfluff/core/rules/__init__.py
    rules.append(rule_class)
    # Add the rule_classes to the module namespace with globals() so that they can
    # be found by Sphinx automodule documentation in rules.rst
    # The result is the same as declaring the classes in this file.
    globals()[rule_class_name] = rule_class
    # Add the rule class names to __all__ for Sphinx automodule discovery
    __all__.append(rule_class_name)
