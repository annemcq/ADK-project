# Adenylate Kinase: Dual-Basin Coarse-Grained Model of a Conformational Transition

A two-person course project using instructor-provided SMOG-ready structures. I built a structure-based (Gō-like), Cα-resolution model of Adenylate Kinase (AKE) built to
study the conformational differences between the open (4AKE) and closed (1AKE)
end states and to provide a dual-basin model for exploring the associated
NMP/LID/CORE domain motion.

## Approach

- **Contact map construction** — native contacts extracted separately from the
  open (4AKE) and closed (1AKE) crystal structures.
- **Dual-basin ("microscopic mixing") potential** — native contacts from both
  end-states are combined into a single structure-based Hamiltonian, providing
  interactions associated with both reference conformations.
- **Coarse-grained simulation** — Cα-only Langevin dynamics run in OpenMM,
  parametrized from the mixed contact map. The stored trajectory is a 100 ns
  simulation initiated from the 4AKE (open) structure at the model temperature
  of 80 K. This is a coarse-grained simulation parameter, not a physiological temperature.
- **Analysis** — trajectory RMSD/Q analysis and domain-based collective
  coordinates (center-of-mass distances between the NMP, LID, and CORE domains);
  a PyEMMA free-energy representation is constructed along the selected
  collective coordinates.

## Repository structure

```text
notebooks/
  01_contact_map_creation.ipynb   – builds native-contact maps for 1AKE and 4AKE
  02_build_and_simulate.ipynb     – merges contact maps, builds the CG system, runs the simulation
  03_analysis.ipynb               – RMSD/Q analysis and free-energy landscape
data/
  structures/                     – input and processed PDB structures
  contact_maps/                   – native contact maps (per end-state and merged)
  system/                         – OpenMM system definition
trajectories/                     – simulation output (full system and per-domain)
results/
  free_energy_landscape.png   – PyEMMA free-energy landscape from the domain-distance coordinates
  distances/                      – inter-residue distance calculations
```

## Background

Adenylate Kinase is a well-studied benchmark for coarse-grained modeling of
large conformational changes: its LID and NMP domains close over the CORE
domain upon substrate binding, and the open (4AKE) and closed (1AKE) crystal
structures are commonly used as reference end-states for structure-based
models. In this repository, the dual-basin potential is constructed from both
end states, while the stored production trajectory is initiated from 4AKE;
the trajectory therefore demonstrates the behavior of that simulation rather
than by itself constituting a demonstration of repeated open ↔ closed
transitions.

## Tools

Python · OpenMM · MDTraj · PyEMMA · NumPy · Matplotlib
