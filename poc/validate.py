#!/usr/bin/env python3
"""Validate every atom + crossing on disk: schema, referential integrity, locators.

This is the CI guard (E2). Without it the schema constraints are advisory and a
bad atom merges silently. No-op pass when atoms/ is absent or empty (the state
before the migration), so it is safe to wire into CI today and it becomes a hard
gate the moment real atoms land.

Run: python validate.py [atoms_dir] [crossings_dir]   (defaults: atoms crossings)
"""
import sys
from pathlib import Path

from atomgraph import check_refs, load_atoms, load_crossings
from schema import valid_locator


def validate(atoms_dir="atoms", crossings_dir="crossings") -> list[str]:
    """Return a list of human-readable problems (empty = everything is valid)."""
    try:
        atoms = load_atoms(atoms_dir) if Path(atoms_dir).is_dir() else {}
    except Exception as e:  # schema validation failure on some atom file
        return [f"an atom failed schema validation: {e}"]
    try:
        crossings = load_crossings(crossings_dir) if Path(crossings_dir).is_dir() else []
    except Exception as e:
        return [f"a crossing failed schema validation: {e}"]

    errors = []
    try:
        check_refs(crossings, atoms)
    except Exception as e:
        errors.append(str(e))
    for name, atom in atoms.items():
        for claim in atom.musicological:
            if not valid_locator(claim.source.locator):
                errors.append(
                    f"{name}: claim {claim.claim!r} has an uncheckable locator "
                    f"{claim.source.locator!r} (need URL / DOI / ISBN+page / timecode)"
                )
    return errors


def main(argv) -> int:
    dirs = [a for a in argv if not a.startswith("--")]
    atoms_dir = dirs[0] if dirs else "atoms"
    crossings_dir = dirs[1] if len(dirs) > 1 else "crossings"
    n_atoms = len(load_atoms(atoms_dir)) if Path(atoms_dir).is_dir() else 0
    errors = validate(atoms_dir, crossings_dir)
    if errors:
        print(f"FAIL: {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"ok: {n_atoms} atom(s) valid (schema + refs + locators)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
