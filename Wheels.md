# Wheels

**Reusable machinery already in Tesseract City.** Read this before you build a fourth version of
something that exists.

Verified against the running substrate on 2026-10-21. Paths are relative to `V:\`.

> The docs publishing pipeline is not a new system. It is five small scripts dropped into
> `00_Tasks/docsPublish/`, riding the task master that already existed. That is the intended way
> to add automation here.

---

## 1. Three orchestrators, three scopes

They look alike. They are not the same job.

| Scope | Mechanism | Triggered by | Lives in |
|---|---|---|---|
| Editor lifecycle | `hooks.json` + `dead_pregnant_hooker` | session start, prompt submit, tool use, file change, stop | `.github/hooks/` |
| Workspace actions | `.vscode/tasks.json` + `task_master` | folder open, worktree created, manual command | `.vscode/`, `__sentinus__/00_Tasks/` |
| Agent identity | morning ritual modules + genes | one agent booting | `__sentinus__/01_Wake_Up/`, `genes/` |

Rule of thumb: if the trigger is **the editor**, it is a hook. If it is **a human or folder
state**, it is a task. If it is **"who am I this session"**, it is a gene.

---

## 2. Task master — `00_Tasks/__ssot_task_master.py`

One dispatcher. Many events. Each event is an ordered list of scripts, plus a folder that is
auto-discovered.

```python
TASK_REGISTRY = {
    "runOn_folderOpen": [...],
    "runOn_worktreeCreated": [...],
    "docsPublish": [
        "docsPublish/01_generate.py",
        "docsPublish/02_guard.py",
        "docsPublish/03_commit.py",
        "docsPublish/04_mirror.py",
        "docsPublish/05_archive.py",
    ],
}
```

**What you get for free by using it:**

- `run_script_safely()` — existence check, cooldown gate, dry-run, UTF-8 subprocess, timing,
  telemetry, and a JSONL log per event in `V:\.logs\Tasks\{event}\{date}.jsonl`.
- `dispatch_event()` — a dedicated `{Event}.py` handler first, then registry order, then every
  non-underscore `.py` in `00_Tasks/{event}/`, in sorted order.
- Fail-fast for pipelines: `docsPublish` and `dependsOn` stop at the first failing stage.
- `--release` is passed through to every stage.

**CLI**

```
python __sentinus__/00_Tasks/__ssot_task_master.py --event docsPublish
python ... --event docsPublish --dry-run
python ... --event docsPublish --release
python ... --force          # bypass cooldown
python ... --list           # show every event and whether its scripts exist
```

**To add a stage:** drop `06_something.py` into `00_Tasks/{event}/`. No orchestrator edit.
**To add an event:** one line in `TASK_REGISTRY`, or a `{Event}.py` handler with `handle(...)`.

---

## 3. Hooks — `.github/hooks/hooks.json` + `00_Hookers/`

Thirty lifecycle events (SessionStart, UserPromptSubmit, PreToolUse, FileChanged, Stop,
SubagentStart, TaskCreated, …). Each entry carries per-platform `command`, `cwd`, `timeout`,
`failOpen`, and `env`.

**The chain:**

```
hooks.json → {Event}.ps1 → __ssot_dead_pregnant_hooker.py --event {Event}
           → {Event}.py → scripts in 00_Hookers/{Event}/
           → _engine_adapters.py shapes output per engine (Copilot, Antigravity, Cline, Claude)
```

**Ironclad Stream Protection.** The hooker saves the real stdout for machine-readable JSON and
redirects `sys.stdout` to stderr before importing anything. That is why a chatty import can never
corrupt an engine's JSON parser. Copy that trick into any script whose stdout is a protocol.

**Use hooks for observation, not for publishing.** A hook that pushes to a live site is a hook
that can push at 3am with nobody watching.

---

## 4. Mirror primitives — `01_Wake_Up/morning_ritual_modules/__cubby_sync.py`

The safest copy/publish primitives in the substrate. They are written for cubby files but they
are generic:

```python
sync_file(path, content, check_only, backup_root) -> bool   # True if changed
atomic_write_text(path, content)                            # temp file + os.replace
backup_existing_file(path, backup_root)                     # copy before overwrite
```

`sync_file` **compares before writing**. If the content is identical, it writes nothing and
returns `False`. That property is what makes "publish" able to mean "no change, no commit, no
churn" — provided the generator upstream is also stable.

`atomic_write_text` writes to a temp file in the same directory and replaces, so a crash cannot
leave a half-written page. On Windows this is the correct replacement for delete-and-rename.

---

## 5. Archive pattern — `genes/agent_specific/b034_indestructible.py`

The reference implementation for "seal this, now, so it survives".

```python
_resolve_agent_paths(context)      # name -> (agent file, cubby)
_backup_agent(agent, file, cubby)  # -> (zip_path, error)
```

It resolves sources, skips cleanly if none exist, writes a deflated zip with **relative paths**
(`p.relative_to(src.parent)`), and timestamps the filename. Destination:
`B:/__general_backup/indestructible_trait/_{Agent}_{YYYY-MM-DD_HH-MM}.zip`.

Copy the shape for any release bundle. Two changes for a code release: put the commit SHA in the
name, and exclude `.git`, `__pycache__`, and any state directory.

---

## 6. Anti-wipe — `genes/agent_specific/handbook_deathgrip.gene.py`

Three rules that keep a bad generation from destroying good pages:

1. **Threshold alarm** — a critical file that is missing, or smaller than its expected size
   (its convention is 2 KB), is an emergency, not a housekeeping note.
2. **Safekeeping before work** — snapshot before the risky operation, not after the loss.
3. **Kintsugi** — never overwrite damage with a blank template. The wound stays visible until it
   is healed with real content.

The docs pipeline's `02_guard.py` is this gene wearing a different coat: a threshold table over
`index.html`, `api_sdk_lmnop.html`, the manifest, and the authored markdown.

---

## 7. Managed regions — `genes/GENE_SCHEMA_INJECTER.py`

When a file is **partly generated and partly authored**, do not regenerate the whole file.
This tool injects only between boundary markers and leaves everything outside untouched:

```
SCHEMA_VARIABLE_HEADER = "=-=-=-=-=-=-=-=-=VARIABLES/=-=-=-=-=-=-=-=-="
...managed block...
SCHEMA_VARIABLE_FOOTER = "=-=-=-=-=-=-=-=-=/VARIABLES=-=-=-=-=-=-=-=-="
```

`inject_schema_to_gene()` + `format_literal_assignment()` are idempotent: running twice produces
the same file. If shelf intros or page prose ever become hand-written, this is the pattern to
reach for instead of owning the entire page.

---

## 8. Module protocol — `01_Wake_Up/morning_ritual_modules/`

Every module is a file with:

```python
MODULE_ORDER = 1
MODULE_NAME  = "Inject_Critical_Agent_Files"

def run(context: MutableMapping[str, Any]) -> None: ...
```

`context` carries `root_dir`, `config`, `record_telemetry`, `agent_home_dir`, `started`,
`ok_count`, `total_count`. The runner counts successes and sets the exit code from
`ok_count == total_count`. `90_Telemetry` emits the boot record last.

The `check_only` pattern from `08_Cubby_Self_Check` is worth copying: pass a flag through the
whole module so the same code can report without writing.

Use this protocol for **identity boot only**. It is a fourth orchestrator if you use it for
anything else.

---

## 9. Self-replacement — `genes/_function/altered_carbon.py`

`resleeve(gene_path, new_content)` writes a temp copy, waits for the running file's lock to
release, deletes the original, and renames the temp into place, with backoff retries.

It exists because a Python module cannot safely rewrite the file it is currently executing from.
For normal file replacement use `atomic_write_text`. Reach for altered carbon only when the file
being replaced is the file that is running.

---

## 10. Worked example: `docsPublish`

```
publish.py  →  task_master --event docsPublish
                ├─ 01_generate  run the SSOT, produce manifest + markdown + HTML
                ├─ 02_guard     thresholds, secret scan, mirror divergence
                ├─ 03_commit    commit + push the authoring repo (01_Docs)
                ├─ 04_mirror    copy into the deploy target, update provenance/submodule
                └─ 05_archive   --release only: zip to B:\ and update RELEASED.json
```

Each stage is one file, returns an int, and gets cooldown, dry-run, logging, and telemetry from
the task master. Editing the pipeline means editing one small file or dropping in a new one.

---

## 11. What these do not do

Not defects — just the edges of the tools, so you do not expect them to do this:

- **No git-state awareness.** `sync_file` compares bytes, not history. Knowing *who was allowed*
  to change a mirror is a separate check (the docs pipeline keeps a `source_sha` + `tree_hash`
  in `.provenance.json`).
- **No scheduling.** Nothing here runs on a timer. Triggers are the editor, the folder, or you.
- **No content hashing at the generator level.** Compare-before-write exists per file in
  `sync_file`; a generator that stamps wall-clock time will still produce a diff every run.
- **Hooks are fire-and-forget.** `failOpen` means a broken hook is ignored rather than fatal.

---

## 12. Provenance

Read on 2026-10-21 against:

- `__sentinus__/00_Tasks/__ssot_task_master.py`
- `__sentinus__/00_Hookers/__ssot_dead_pregnant_hooker.py`, `.github/hooks/hooks.json`
- `__sentinus__/01_Wake_Up/morning_ritual_modules/{01,04,08,90}*.py`, `_cubby_helpers.py`, `__cubby_sync.py`
- `__sentinus__/01_Wake_Up/{_morning_ritual.py,_agentic_helix.py}`
- `__sentinus__/01_Wake_Up/genes/{template.gene.py,GENE_SCHEMA_INJECTER.py,_function/altered_carbon.py}`
- `__sentinus__/01_Wake_Up/genes/agent_specific/{b034_indestructible.py,handbook_deathgrip.gene.py}`
- `.vscode/tasks.json`
- `__sentinus__/00_Tasks/docsPublish/*.py`, `__marinus__/01_Docs/publish.py`

If a wheel changes shape, update this page in the same commit that changes it.
