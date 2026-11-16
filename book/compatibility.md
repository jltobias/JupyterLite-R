# Browser and package compatibility

The build pairs JupyterLite 0.6.4 and JupyterLab 4.4.10 with `jupyterlite-webr` 0.6.0 and webR
0.5.1. These deliberate pins match the kernel's 0.6-generation APIs; upgrading Lite independently
can break a federated extension. Jupyter Book 2.1.7 builds the reading interface from `myst.yml`.

The package repository is a live service, not a frozen R package lockfile. Record package versions
and `sessionInfo()` for any reproduced analysis. A desktop package installation is not proof of
browser support. See [webR's installation guide](https://docs.r-wasm.org/webr/latest/packages.html).

| Lesson feature | Execution path | What can fail |
| --- | --- | --- |
| All ten core lessons | Base R in webR; no package installation | Runtime/CDN, browser memory, storage policy |
| ColorBrewer palettes | Optional `RColorBrewer` | Missing compatible binary or network |
| Simple features | Optional `sf` | WebAssembly GDAL/GEOS/PROJ build and package dependencies |
| Raster orientation | `terra` desktop extension | Failed loading/exports under the pinned webR; browser uses the base lesson |
| Moran comparison | Optional `spdep` | Browser-tested here; compiled dependency chain may change |
| Custom linked micromaps | `micromapST` + `sf`, original prebuilt border group | BuildBorderGroup fails in this browser runtime; the border is constructed in desktop R |
| Layered plot | Optional `ggplot2` | Package availability and installation size |
| Rotatable gallery | Plotly.js with saved R-generated data | CDN/network or WebGL availability |
| Reactive Shiny explorer | Separate Shinylive page, with its own webR runtime | Runtime and Shiny package downloads; browser memory |

Install only what you need, in a separate cell:

```r
webr::install("RColorBrewer")
# Later, if you choose the vector extension:
webr::install("sf")
```

Then rerun the extension cell. It prints a visible message if a package is absent. Do not confuse
that skipped cell with a passed package test. Unexpected errors in an installed package remain
errors and should be investigated. Desktop setup uses `Rscript tools/install_r_extensions.R` and
stores packages in a private project cache.

## Plots, HTML widgets, and files

The pinned kernel [publishes PNG plots and text results](https://github.com/r-wasm/jupyterlite-webr-kernel/blob/main/src/webr_kernel.ts).
It does not implement general HTML-widget display or widget comms. Consequently, a successful
`leaflet`, `plotly`, or `rgl` install is not enough to make its interactive output appear inline.
The separate gallery solves that display problem for this project's original numerical examples.
Changing a notebook does not automatically update the published gallery; regenerate its CSV exports.

## Serving and troubleshooting

Serve over HTTPS or localhost. This repository supplies an original isolation service worker for
the Lab page on GitHub Pages, and a local server that sends COOP/COEP headers. The bootstrap reloads
once after the worker controls the page. JupyterLite's separate worker manages notebook storage.
If initialization fails, check browser support, CDN access, service worker permissions, and the
browser console. A normal window is more reliable than a private window with restricted storage.

The pinned kernel has limited completion, inspection, and interrupt support. Avoid unbounded loops;
restart the kernel to recover from a stuck computation. Save/download work frequently. Initial
downloads mean this is not a fully offline distribution.

For exact execution evidence, see [the validation report](https://github.com/jltobias/JupyterLite-R/blob/main/validation/RESULTS.md).
