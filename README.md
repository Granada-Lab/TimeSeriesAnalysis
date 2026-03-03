# TimeSeriesAnalysis

A collection of Python scripts for quantitative analysis of single-cell time-series data,
developed for the study of circadian dynamics, proliferation, and drug response in live-cell imaging experiments.

These tools were used in the analysis underlying:

> Granada AE, Jimenez A, Stewart-Ornstein J, Blüthgen N, Reber S, Jambhekar A, Lahav G.
> *The effects of proliferation status and cell cycle phase on the responses of single cells to chemotherapy.*
> **Molecular Biology of the Cell** 2020;31(8):845–857. DOI: [10.1091/mbc.E19-10-0568](https://doi.org/10.1091/mbc.E19-10-0568)

## Contents

| Script | Description |
|---|---|
| `amplitude_vs_trend.py` | Amplitude extraction and trend comparison across conditions |
| `circadian_phases_at_division.py` | Circadian phase estimation at cell division events |
| `division_events.py` / `division_profiles.py` | Detection and profiling of single-cell division events |
| `cumul_distrib_division_events.py` | Cumulative distribution of division timing |
| `cv_period_ampl.py` | Coefficient of variation for period and amplitude |
| `period_density_boxplot.py` | Period distribution visualisation |
| `phase_locking_plots.py` / `ph_coh_linear_fit.py` | Phase coherence and locking analysis |
| `ridge_classification_proliferation.py` | Wavelet ridge classification linked to proliferation state |
| `growth_inhibition_curve.py` | Growth inhibition curve fitting |
| `filter_by_size.py` / `filter_similar_traces_pivot.py` | Trace filtering utilities |
| `ED_analysis.py` | Energy dissipation analysis |

## Requirements

- Python 3.8 or later
- `numpy`, `scipy`, `pandas`, `matplotlib`
- [pyBOAT](https://github.com/tensionhead/pyBOAT) for wavelet-based period analysis

## License

MIT — see [LICENSE](LICENSE).
This code was developed by members and collaborators of the Granada Lab research group.
For authorship and correspondence, please refer to the publication above.
