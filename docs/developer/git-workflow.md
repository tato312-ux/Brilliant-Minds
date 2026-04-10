# Development Practices & Git Workflow Guide

This document outlines the development practices, Git workflow standards, and conventions that our team follows to maintain code quality, consistency, and collaboration efficiency.

## Table of Contents

1. [Git Branch Naming Conventions](#git-branch-naming-conventions)
2. [Commit Message Standards](#commit-message-standards)
3. [Atomic Commit Workflow](#atomic-commit-workflow)
4. [Pull Request Guidelines](#pull-request-guidelines)
5. [Essential Git Commands](#essential-git-commands)
6. [Safety Protocols](#safety-protocols)

## Git Branch Naming Conventions

### Branch Structure

We follow a hierarchical branch naming convention that provides clarity about the purpose and scope of each branch.

#### Format: `{type}/{scope}/{description}`

### Branch Types

#### 1. Development Branches

- **Format**: `dev/{scope}`
- **Purpose**: Active development for specific features or components
- **Examples**:
  - `dev/agent` - Agent framework development
  - `dev/authentication` - Authentication system
  - `dev/api/v2` - API version 2 development
  - `dev/ui/dashboard` - Dashboard UI components

#### 2. Feature Branches

- **Format**: `feat/{scope}/{feature-name}`
- **Purpose**: New feature development
- **Examples**:
  - `feat/agent/teacher-mode` - Teacher agent functionality
  - `feat/api/file-upload` - File upload API endpoint
  - `feat/ui/dark-theme` - Dark theme implementation
  - `feat/storage/blob-integration` - Blob storage integration

#### 3. Bug Fix Branches

- **Format**: `fix/{scope}/{issue-description}`
- **Purpose**: Bug fixes and patches
- **Examples**:
  - `fix/agent/memory-leak` - Memory leak in agent system
  - `fix/api/auth-validation` - Authentication validation bug
  - `fix/ui/responsive-layout` - Responsive layout issues
  - `fix/storage/connection-timeout` - Storage connection timeout

#### 4. Release Branches

- **Format**: `release/{version}`
- **Purpose**: Release preparation and stabilization
- **Examples**:
  - `release/v1.0.0` - Version 1.0.0 release
  - `release/v1.1.0-beta` - Beta release preparation

#### 5. Hotfix Branches

- **Format**: `hotfix/{version}/{fix-description}`
- **Purpose**: Critical fixes for production releases
- **Examples**:
  - `hotfix/v1.0.0/security-patch` - Security patch for v1.0.0
  - `hotfix/v1.1.0/data-corruption` - Data corruption fix

### Scope Guidelines

Common scopes in our project:

- `agent` - Agent-related functionality
- `api` - Backend API endpoints
- `ui` - User interface components
- `storage` - Data storage and persistence
- `auth` - Authentication and authorization
- `infra` - Infrastructure and deployment
- `config` - Configuration and settings
- `docs` - Documentation
- `test` - Testing and quality assurance

## Commit Message Standards

### Format: `type: description`

All commit messages must follow this format:

- **type**: Lowercase, one of the approved types
- **description**: Imperative mood, concise description of the change

### Approved Types

| Type       | Purpose                           | Examples                                                |
| ---------- | --------------------------------- | ------------------------------------------------------- |
| `feat`     | New features                      | `feat: add teacher agent with educational instructions` |
| `fix`      | Bug fixes                         | `fix: resolve memory leak in session handler`           |
| `docs`     | Documentation                     | `docs: add api documentation for endpoints`             |
| `style`    | Code style (no functional change) | `style: format code with black linting`                 |
| `refactor` | Code refactoring                  | `refactor: simplify authentication flow`                |
| `test`     | Tests and testing infrastructure  | `test: add unit tests for agent provider`               |
| `chore`    | Maintenance, dependencies, build  | `chore: update dependencies to latest versions`         |

### Description Guidelines

- Use **imperative mood** ("add feature" not "added feature" or "adds feature")
- Keep it **concise** (50-72 characters max for the first line)
- Use **lowercase** throughout
- Be **specific** about what changed
- **No period** at the end

### Examples

✅ **Good**:

- `feat: add azure ai provider base framework`
- `fix: resolve async context management issue`
- `docs: update deployment guide with new steps`
- `refactor: simplify settings validation logic`

❌ **Bad**:

- `Added new features` (Wrong format, not imperative)
- `fix: bug` (Not specific)
- `FEAT: Add Agent` (Wrong case)
- `docs: updated the readme file.` (Has period)

## Atomic Commit Workflow

This workflow ensures every commit represents a single, isolated logical change.

### 1. Mandatory Deep Analysis

Always start by investigating changes to avoid "dirty" commits.

#### Step A: High-Level Status

```bash
git status
```

Identify all modified, new, and deleted files.

#### Step B: Granular Inspection

```bash
git diff <file_path>    # For each modified file
git diff --staged       # For staged changes
```

Examine each file individually to understand the changes.

#### Step C: Logical Mapping

Group files only if they strictly belong to the same functional change. Ask yourself:

- Do these changes solve the same problem?
- Will they make sense if reviewed separately?
- Can each change stand on its own?

### 2. Atomic Staging and Committing

#### Prohibited Actions

- ❌ `git add .` - Never stage entire directories
- ❌ `git add -A` - Never stage all changes
- ❌ `git add path/to/dir/` - Never stage directories

#### Required Actions

- ✅ `git add path/to/specific_file.py` - Stage individual files
- ✅ `git add -p` - Stage specific hunks within files

#### The Execution Cycle

1. **Stage**: Add specific files or hunks for one logical change
2. **Validate**: Run `git status` to ensure only intended changes are staged
3. **Commit**: Use proper commit message format
4. **Repeat**: Move to the next logical change

### Example Workflow

```bash
# 1. Check status
git status

# 2. Review changes
git diff src/config/settings.py
git diff src/agents/base_agent.py

# 3. Stage configuration changes (if related)
git add src/config/settings.py
git status
git commit -m "feat: add azure ai configuration settings"

# 4. Stage agent framework changes
git add src/agents/base_agent.py
git status
git commit -m "feat: implement azure ai provider base framework"

# 5. Continue with next logical change
```

## Pull Request Guidelines

### PR Construction

Generate PRs by analyzing the aggregate commit history of the branch.

#### PR Title

- Use the same format as commit messages: `type: description`
- Summarize the overall objective of the branch
- Be concise but descriptive

#### PR Description Structure

```markdown
## Description

Brief explanation of what this PR accomplishes and why it's needed.

## Key Changes

- High-level summary of the main changes
- Focus on the "what" and "why", not just the "how"

## Testing

How to test the changes:
1. Step-by-step testing instructions
2. Expected behavior
3. Any special setup required
```

### PR Template Example

**Title**: `feat: enhance agent framework with educational capabilities`

**Description**:

```markdown
## Description

This PR enhances the agent framework by adding a specialized teacher agent capable of providing educational explanations with analogies and structured content delivery.

## Key Changes

- Implemented TeacherAgent class with educational instruction prompts
- Enhanced base Azure AI provider with improved async context management
- Added configuration settings for Azure AI endpoints and model deployments
- Updated main application with teacher agent demonstration

## Testing

1. Deploy Azure infrastructure using provided Bicep templates
2. Configure environment variables from `.env.example`
3. Run `python -m src.main` to test teacher agent functionality
4. Verify agent provides clear, structured explanations
```

## Essential Git Commands

### Daily Workflow Commands

```bash
# Check current state
git status
git log --oneline -5

# Review changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff <file>            # Specific file changes

# Staging and committing
git add <file>             # Stage specific file
git add -p                 # Stage specific hunks
git commit -m "type: description"

# Branch management
git checkout -b feat/scope/feature-name    # Create new branch
git branch -d feature-branch               # Delete local branch
git push origin feature-branch              # Push to remote
```

### Advanced Commands

```bash
# History and analysis
git log --oneline --graph --all            # Visual branch history
git log --stat                             # Show file change statistics
git blame <file>                           # See line-by-line authorship

# Cleanup and maintenance
git clean -fd                              # Remove untracked files/dirs
git reset --soft HEAD~1                    # Undo last commit (keep changes)
git rebase -i HEAD~3                       # Interactive rebase for history cleanup

# Synchronization
git fetch origin                           # Update remote refs
git pull --rebase origin main              # Rebase pull instead of merge
```

## Safety Protocols

### Critical Rules

1. **NO BULK ADDS**: Never stage entire directories or use `git add .`
2. **One Change per Commit**: Each commit must represent one logical change
3. **No Destructive Actions**: Avoid `--force` or `reset --hard` without explicit request
4. **Linear History**: Prefer rebase over merge to maintain clean history

### Code Review Guidelines

- Review your own code before requesting reviews
- Ensure each commit can be understood independently
- Verify all tests pass before creating PRs
- Check for sensitive data or credentials before committing

### Emergency Procedures

If you make a critical mistake:

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Recover lost commit (if you reset by mistake)
git reflog                    # Find the lost commit hash
git checkout <hash>          # Recover the commit
```

## Best Practices Summary

### Do's ✅

- Write atomic, focused commits
- Use imperative mood in commit messages
- Review changes before staging
- Test your changes before committing
- Keep branch names descriptive and consistent
- Write clear PR descriptions

### Don'ts ❌

- Stage entire directories at once
- Write vague commit messages like "fix bugs"
- Commit unrelated changes together
- Use force push without consensus
- Include sensitive data in commits
- Merge without resolving conflicts properly
