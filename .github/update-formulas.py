#!/usr/bin/env python3
"""Update formulas listed in upstreams.json from stable X.Y.Z tags (optional v).

Each release supplies <formula>.rb and the configured archive with GitHub SHA-256 digests.
Archive patterns support {tag} and {version}.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def version(value):
    match = re.fullmatch(r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value)
    if not match:
        raise SystemExit(f"Invalid stable version: {value}")
    return tuple(map(int, match.groups()))


def field(formula, name):
    values = re.findall(rf'''^[ \t]*{name}[ \t]+(["'])([^\r\n]*?)\1[ \t]*(?:#.*)?$''',
                        formula, re.MULTILINE)
    if len(values) != 1:
        raise SystemExit(f"Formula must contain one {name}")
    return values[0][1]


def prepare_update(name, upstream):
    if not re.fullmatch(r"[a-z0-9][a-z0-9+@._-]*", name):
        raise SystemExit(f"Invalid formula name: {name}")
    repository = upstream["repository"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise SystemExit(f"Invalid repository: {repository}")
    target = ROOT / "Formula" / f"{name}.rb"
    if target.is_symlink() or target.parent.is_symlink():
        raise SystemExit("Formula paths must not be symlinks")
    release = json.loads(subprocess.check_output(["gh", "api", f"repos/{repository}/releases/latest"]))
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"]:
        raise SystemExit("Expected a published stable release")
    release_version = tag.removeprefix("v")
    latest = version(tag)
    if target.exists() and latest <= version(field(target.read_text(), "version")):
        return

    archive = upstream["archive"].replace("{tag}", tag).replace("{version}", release_version)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", archive):
        raise SystemExit(f"Invalid archive name: {archive}")
    formula_name = f"{name}.rb"
    names = [formula_name, archive]
    assets = {asset["name"]: asset for asset in release["assets"]}
    if any(name not in assets or assets[name]["state"] != "uploaded" for name in names):
        raise SystemExit("Release assets are incomplete")

    with tempfile.TemporaryDirectory() as directory:
        command = ["gh", "release", "download", tag, "--repo", repository, "--dir", directory]
        for filename in names:
            command += ["--pattern", filename]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        files = {filename: (Path(directory) / filename).read_bytes() for filename in names}
        hashes = {filename: hashlib.sha256(data).hexdigest() for filename, data in files.items()}
        for filename in names:
            if assets[filename].get("digest") != "sha256:" + hashes[filename]:
                raise SystemExit(f"GitHub checksum mismatch: {filename}")
        formula = files[formula_name].decode()
        url = f"https://github.com/{repository}/releases/download/{tag}/{archive}"
        if (field(formula, "url") != url or field(formula, "sha256") != hashes[archive]
                or field(formula, "version") != release_version):
            raise SystemExit("Formula does not match release asset")
        subprocess.run(["ruby", "-c", str(Path(directory) / formula_name)],
                       check=True, stdout=subprocess.DEVNULL)
        return name, target, files[formula_name], tag


def main():
    upstreams = json.loads((ROOT / ".github/upstreams.json").read_text())
    updates = []
    for name, upstream in upstreams.items():
        try:
            update = prepare_update(name, upstream)
        except (SystemExit, subprocess.CalledProcessError) as error:
            raise SystemExit(f"{name}: {error}")
        if update:
            updates.append(update)
    if updates:
        (ROOT / "Formula").mkdir(exist_ok=True)
    for name, target, formula, tag in updates:
        target.write_bytes(formula)
        print(f"{name} {tag}")


if __name__ == "__main__":
    main()
