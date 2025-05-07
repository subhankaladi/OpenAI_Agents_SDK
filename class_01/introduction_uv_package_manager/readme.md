# uv Package Manager Learning

Welcome to my learning repository for **uv**, a modern and ultra-fast Python package manager developed by [Astral](https://astral.sh/).  
This repo is part of my hands-on journey to understand faster, reliable, and developer-friendly tools for Python environments and package management.

---

## 🚀 What is uv?

**uv** is a next-generation Python package manager that replaces the combination of:

- `pip` (for installing packages)
- `virtualenv` (for creating isolated environments)
- `pip-tools` (for dependency resolution and locking)

### 🔥 Built with Rust, uv offers:

- 🚀 Blazing-fast installs (10x faster than pip)
- 🔒 Secure dependency resolution and lockfiles
- 🧪 Reproducible environments
- 🛠️ Easy-to-use CLI commands
- 🧩 Compatible with `pyproject.toml` and `requirements.txt`

---

## 📚 Why I Am Learning uv

As a Python developer learning modern tools like Docker, Agents SDK, and AI frameworks, I want to ensure my development environment is:

- Fast to set up
- Easy to maintain
- Reproducible across projects

That’s why I’m learning **uv** — to boost my Python workflow performance and reduce environment setup pain.

---

## ⚙️ uv vs pip + virtualenv

| Feature                     | uv                        | pip + virtualenv                  |
|----------------------------|---------------------------|-----------------------------------|
| Speed                      | 🚀 Very fast (Rust-based) | 🐢 Slower                        |
| Environment creation       | ✅ Built-in               | 🔧 Requires virtualenv/separately |
| Dependency resolution      | ✅ Integrated             | 🔶 External (pip-tools, etc.)     |
| Lockfile support           | ✅ Yes (`uv pip compile`) | ❌ No native support              |
| Reproducibility            | ✅ Strong                 | 🔶 Depends on setup               |
| Modern Python standards    | ✅ Full `pyproject.toml`  | 🔶 Mixed support                  |

---

## 🔧 Basic uv Commands

### 1. Install uv  
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
