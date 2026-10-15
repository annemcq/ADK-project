"""Regenerate the ADK free-energy landscape using the corrected CORE indexing.

Run from the repository root:
    python scripts/regenerate_landscape.py

Requires numpy, matplotlib and mdtraj; no new simulation is required.
The 2D PMF is estimated from a probability histogram as -ln(p/p_max)
(in dimensionless kBT units), rather than depending on a PyEMMA renderer.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TRAJECTORY = ROOT / "trajectories" / "traj_AKE4.xtc"
TOPOLOGY = ROOT / "data" / "structures" / "pdb_file_4AKE_Calpha.pdb"
OUTPUT = ROOT / "results" / "free_energy_landscape.png"


def residue_range(start, stop):
    """Inclusive 1-based residue numbers to zero-based indices."""
    return list(range(start - 1, stop))


def main():
    traj = md.load(str(TRAJECTORY), top=str(TOPOLOGY))
    nmp = residue_range(30, 59)
    lid = residue_range(122, 159)
    core = residue_range(1, 29) + residue_range(60, 121) + residue_range(160, 214)
    assert len(core) == 146
    assert len(set(core) & (set(nmp) | set(lid))) == 0
    assert len(traj.topology.atoms) == 214, "Expected one C-alpha bead per residue"
    def com(ids):
        return md.compute_center_of_mass(traj.atom_slice(ids))
    c = com(core)
    d_lid = np.linalg.norm(com(lid) - c, axis=1) * 10.0
    d_nmp = np.linalg.norm(com(nmp) - c, axis=1) * 10.0

    # Consistent with the notebook's PyEMMA free-energy axes.
    hist, xedges, yedges = np.histogram2d(d_lid, d_nmp, bins=100)
    with np.errstate(divide="ignore"):
        pmf = -np.log(hist / hist.max())
    pmf[~np.isfinite(pmf)] = np.nan

    fig, ax = plt.subplots(figsize=(7, 5))
    mesh = ax.pcolormesh(xedges, yedges, pmf.T, cmap="viridis", shading="auto")
    fig.colorbar(mesh, ax=ax, label="Relative free energy (kBT)")
    ax.set_xlabel("Distance between COM of CORE and LID domains (Å)")
    ax.set_ylabel("Distance between COM of CORE and NMP domains (Å)")
    ax.set_title("ADK conformational free-energy landscape (corrected CORE)")
    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Frames: {traj.n_frames}")
    print(f"NMP–CORE distance (Å): {d_nmp.min():.2f}–{d_nmp.max():.2f}")
    print(f"LID–CORE distance (Å): {d_lid.min():.2f}–{d_lid.max():.2f}")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
