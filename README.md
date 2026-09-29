# Adenylate Kinase: Dual-Basin Coarse-Grained Model of a Conformational Transition

A structure-based (Gō-like), Cα-resolution model of Adenylate Kinase (AKE) built to
study its large-scale open ↔ closed conformational transition — the classic
NMP/LID/CORE domain motion that couples substrate binding to catalysis.

## Approach

- **Contact map construction** — native contacts extracted separately from the
  open (4AKE) and closed (1AKE) crystal structures.
- **Dual-basin ("microscopic mixing") potential** — native contacts from both
  end-states are combined into a single structure-based Hamiltonian, so the
  model can access both conformations rather than being biased toward one.
- **Coarse-grained simulation** — Cα-only Langevin dynamics run in OpenMM,
  parametrized from the merged contact map.
- **Analysis** — RMSD and fraction-of-native-contacts (Q) relative to each
  end-state; domain-based collective coordinates (center-of-mass distances
  between the NMP, LID, and CORE domains); free-energy landscape along these
  coordinates via PyEMMA.

## Repository structure

```
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
  distances/                      – inter-residue distance calculations
```

## Background

Adenylate Kinase is a well-studied benchmark for coarse-grained modeling of
large conformational changes: its LID and NMP domains close over the CORE
domain upon substrate binding, and the open (4AKE) and closed (1AKE) crystal
structures are commonly used as reference end-states for structure-based
models of this transition.

## Tools

Python · OpenMM · MDTraj · PyEMMA · NumPy · Matplotlib
