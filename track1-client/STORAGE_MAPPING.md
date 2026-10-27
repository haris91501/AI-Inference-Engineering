# System Storage & Development Paths Mapping (C: -> B: Drive)

> **Important Note for AI Agents & Developers:**
> Due to storage optimization on `C:`, all heavy Linux distributions, package caches, AI models, and migrated developer runtimes have been relocated to **Drive `B:`** (which has over 900 GB of free space).

---

## 1. WSL (Windows Subsystem for Linux)
- **Distro Name:** `Ubuntu-24.04`
- **Previous Location:** `C:\Users\NICE C0MP\AppData\Local\wsl\...`
- **Current Active Location:** `B:\WSL\Ubuntu\ext4.vhdx`
- **Default WSL User:** `nice_c0mp`
- **Behavior:** All Linux operations (`apt install`, Python virtualenvs inside Linux, Docker in WSL, root filesystem) write directly into `B:\WSL\Ubuntu`.

---

## 2. Windows Development & Package Caches
The following global environment variables and config pointers are set to Drive `B:`:

| Cache / Tool | New Location on B: | Environment Variable / Config |
| :--- | :--- | :--- |
| **NPM Global Cache** | `B:\.npm-cache` | `npm config set cache "B:\.npm-cache" --global` |
| **Python Pip Cache** | `B:\.cache\pip` | `PIP_CACHE_DIR=B:\.cache\pip` |
| **Hugging Face Models** | `B:\.cache\huggingface` | `HF_HOME=B:\.cache\huggingface` |
| **PyTorch Models / Hub** | `B:\.cache\torch` | `TORCH_HOME=B:\.cache\torch` |

---

## 3. Server & Database Migrations (C: -> B:)
If MongoDB, PostgreSQL, or XAMPP are relocated from `C:`:

| Software | Previous Path (C:) | Destination / Active Path (B:) |
| :--- | :--- | :--- |
| **XAMPP** | `C:\xampp` | `B:\xampp` |
| **MongoDB 8.3** | `C:\Program Files\MongoDB` | `B:\Software files\MongoDB` *(Directory Junction)* |
| **PostgreSQL 18** | `C:\Program Files\PostgreSQL` | `B:\Software files\PostgreSQL` *(Directory Junction)* |
| **Docker Desktop Data** | `C:\Users\NICE C0MP\AppData\Local\Docker\...` | `B:\Docker\` |

---

## 4. Workspaces & Projects
- **Primary AI & Code Projects:** `B:\AI Inference Engineering\`
- **General Workspace:** `B:\`
