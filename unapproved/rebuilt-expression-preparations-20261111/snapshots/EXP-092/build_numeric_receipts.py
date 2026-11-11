"""Explicit one-shot numeric authoring, separate from read-only verification."""
from numeric_model import W,build_receipts,canonical

def main():
    paths=[W/'NUMERIC_TRAJECTORY.json',W/'NUMERIC_LIFECYCLE.json']
    if any(p.exists() for p in paths): raise SystemExit('Preserving existing receipts; refusing overwrite.')
    data=build_receipts()
    for p,value in zip(paths,data):
        with p.open('x') as f: f.write(canonical(value))
    print('Wrote fresh deterministic numerical receipts, not native/render evidence.')

if __name__=='__main__': main()
