# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Python Development Guidelines

## Code Style & Quality

### Type Annotations
- Use modern Python 3.13 type hints everywhere except for `kwargs`, `self`, and `cls`
- Use built-in generic types (`list[str]`, `dict[str, int]`) instead of `typing.List`, `typing.Dict`
- Avoid `typing.Any` whenever possible - use specific types, unions, or protocols instead
- Do NOT use `from __future__ import annotations`

### Documentation
- Use NumPy-style docstrings for all functions, methods, and classes
- Include `Parameters`, `Returns`, and `Raises` sections when applicable
- Avoid meaningless descriptions like "Returns None" - omit Returns section if function returns None
- Example:
```python
def process_data(items: list[str], threshold: int = 10) -> dict[str, int]:
    """Process items and count occurrences above threshold.

    Parameters
    ----------
    items : list[str]
        List of items to process
    threshold : int, default=10
        Minimum count threshold for inclusion

    Returns
    -------
    dict[str, int]
        Mapping of items to their counts

    Raises
    ------
    ValueError
        If threshold is negative
    """
```

### Design Principles
- Follow SOLID principles:
  - Single Responsibility: Each class/function has one clear purpose
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes must be substitutable for base types
  - Interface Segregation: Many specific interfaces over one general
  - Dependency Inversion: Depend on abstractions, not concretions

### Linting
- Code must pass Ruff and WPS (wemake-python-styleguide) checks
- NEVER use `# noqa` comments to bypass linter errors
- If a violation cannot be fixed without `# noqa`, leave the code unchanged rather than suppressing the warning

## Testing

### Coverage & Framework
- Achieve 100% test coverage using pytest
- Use pytest features: parametrize, fixtures, mocks

### Test Organization
- When tests are grouped in classes, use `@classmethod` for test methods
- Avoid duplicate tests - use `@pytest.mark.parametrize` instead
- Example:
```python
class TestDataProcessor:
    @classmethod
    @pytest.mark.parametrize("input_data,expected", [
        ([1, 2, 3], 6),
        ([0], 0),
        ([], 0),
    ])
    def test_sum_calculation(cls, input_data: list[int], expected: int) -> None:
        """Test sum calculation with various inputs."""
        assert sum_data(input_data) == expected
```

### Best Practices
- Use fixtures for shared test setup
- Mock external dependencies (APIs, databases, file I/O)
- Prefer `pytest.raises` for exception testing
- Use `pytest-mock` for mocking instead of `unittest.mock` when possible

## Task Management

### Large Tasks
When facing a large or complex task:
1. Call the agent-organizer first
2. The organizer will:
   - Break down the task into subtasks
   - Create a structured plan
   - Assign specialized sub-agents to each subtask
3. Execute subtasks in logical order
4. Integrate results coherently

### Workflow
- Start with analysis and planning
- Implement incrementally with tests
- Validate with linters after each change
- Document as you go, not at the end

## General Rules

- Write clean, readable, maintainable code
- Prefer explicit over implicit
- Choose clarity over cleverness
- Validate inputs at boundaries
- Handle errors gracefully with specific exceptions
- Keep functions small and focused
