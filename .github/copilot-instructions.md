# Project Guidelines

## Workflow
- **Small Verifiable Steps**: Always work in small, verifiable steps. Make incremental changes, test or verify them, and commit frequently.

## Conventions
- **Commits**: Always use [Conventional Commits](https://www.conventionalcommits.org/) format when writing commit messages or executing git commits. Examples include:
  - `feat: add new feature`
  - `fix: resolve issue`
  - `build(scope): update dependencies`
  - `chore: minor maintenance tasks`
  - `docs: update readme`
- **Before Committing**: Always prompt the user on whether they want to commit changes before executing the commit.

## Package Management
- **Tooling**: We use [uv](https://docs.astral.sh/uv/) for package management.
- Always use `uv add <package>` to add new dependencies and `uv remove <package>` to remove them.
- To execute scripts or commands in the project's environment, prepend them with `uv run`.

## Imports
- Always use **absolute imports** (proper names) starting with the package name `peda` instead of relative imports.
- Example: `from peda.models import Event` instead of `from .models import Event`.

## Linting and Type Checking
- **Tooling**: We use `ruff` for linting/formatting and `ty` for static type checking.
- **Commands**: Run `uv run ruff check` to lint, `uv run ruff format` to format, and `uv run ty check` for type checking. Ensure code passes these checks before committing.
