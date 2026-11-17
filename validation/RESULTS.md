# Validation record

Checked on 2026-11-16. This report distinguishes native R execution, browser execution, UI rendering,
and publishing. All numerical inputs are original synthetic fixtures.

## Native R

All ten core chapters passed in clean **R 4.6.0**, Windows x64 sessions. Their final code hashes,
executed-cell counts, and optional-cell skips are recorded in `native-core.json`.
Saved notebook plots come from this run, with provenance in notebook metadata.

All optional package extensions also completed in separate native R sessions: RColorBrewer 1.1-3,
sf 1.1-3, terra 1.9-50, spdep 1.4-2, micromapST 3.1.1, and ggplot2 4.0.4. The micromapST
figure uses original square polygons and an original name table. Two upstream warnings remain:
`WorkTemp` was not found during cleanup and `detailsVariables` was not found during data loading.
The border group and linked figure were generated and inspected; those warnings were not suppressed.

The Shiny model and reactive server passed with **Shiny 1.14.0**: fixed-seed reproducibility,
different-seed variation, monotone selection counts, empty selection, unchanged data when only the
threshold changes, and regenerated data when the seed changes. The installed Shiny binary reports
that it was built under R 4.6.2; the tested session ran R 4.6.0 successfully.

## Numerical checks

| Example | Checked result |
| --- | --- |
| Browser laboratory | 30 unique synthetic station IDs; finite generated readings |
| Vector geometry | Three strictly interior points; 12,000,000 m² rectangle; CRS round trip within 1 cm |
| Raster | 3,721 elevations, 100 m spacing, exact XYZ extraction round trip with terra |
| 3D scene | 140 m sampled clearance; 3D path length exceeds horizontal path length |
| Globe | Unit-length interpolated vectors; preserved endpoints; spherical distance about 10,255.88 km |
| Moran experiment | Two-node reference I = -1; simulated I about 0.8589934; spdep agrees within 1e-10 |
| Micromaps | Wilson intervals within 0–100%; valid custom border group and linked plot |
| Capstone | Thresholds 45, 48, 51 select 33, 16, 8 sites in the native fixture |
| Shiny | Palette/threshold controls do not regenerate the field; seed changes do |

## Browser checks

All ten core chapters passed in **webR 0.5.1 / R 4.5.1 (wasm32-unknown-emscripten)** inside
Chrome 157 using the exact notebook cell sources and captured browser graphics. Browser package
checks passed for RColorBrewer 1.1-3, sf 1.1-0, spdep 1.4-2, ggplot2 4.0.3, and micromapST 3.1.1.
See `webr-final.json` for the final result and runtime details.

The initial compatibility experiment is preserved in `webr-discovery.json`. It found two failures:
terra 1.9-11 did not load correctly in this runtime, and micromapST's V8-backed border construction
failed. The final lessons explicitly restrict terra to desktop R, and use a 1,780-byte original
prebuilt border group for micromapST browser rendering. That rendering subsequently passed. The
base raster lesson runs in webR. A package namespace loading successfully alone is not sufficient
evidence that all of its functions work.

The JupyterLite UI opened Chapter 1 with R (webR), ran its cells, and displayed fresh numeric
results and a plot without JavaScript errors. A separate webR evaluator tested the full core
cell sources; this does not claim that every notebook was manually exercised through Lab menus.
Cross-origin isolation succeeded through the original Lab service worker on a localhost server
without COOP/COEP headers, simulating that GitHub Pages hosting condition.

All five gallery views loaded in Chrome without JavaScript errors. Screenshots were inspected for
the contour map, surface, layered scene, globe, and ranked data view. The gallery renders R CSV
exports with Plotly.js; it is not an inline Jupyter HTML widget.

The landing page, Book home, and Chapters 1 and 10 returned successfully with all images loaded and
no JavaScript errors. The gallery also passed a 390-pixel viewport overflow check. Shiny's exported
interface was visually inspected and its seed, restored-seed, threshold, and palette controls were
exercised in the browser. The exporter is shinylive 0.5.0 with web assets 0.10.12; it manages a
separate browser runtime from the notebook kernel.

The final Shinylive download test passed: 100 observations plus a header, with the selection flag
included. The original navigation-style download was cancelled by the browser; an original small
client handler now fetches the generated CSV through Shinylive's proxy and downloads a Blob.
The final seed/threshold/palette/download check reported no JavaScript errors; see `shiny-browser.json`.

## Build and deployment boundary

The Jupyter Book / JupyterLite static build completed locally. Local BibTeX entries avoid dependence
on DOI metadata services during the Book build. A stale MyST search-route build was resolved by
cleaning generated Book output; the build tool now does this explicitly. One upstream Book theme
schema warning (`multiple`, ignored) remains; it does not prevent rendering.

The checks above were completed locally before publication; the hosted follow-up is recorded below.
Safari, Firefox, private-window storage behavior, full offline use, and large real-world datasets
are unverified.

Reproduce with the commands in the README. Detailed local logs, individual cell sources, screenshots,
and runtime session details are under `validation/runs/` (ignored by Git; core logs are also uploaded
as CI artifacts). Native and browser results should not be interpreted as universal package support.

## Hosted follow-up: 2026-11-17

The first deployment failed because the Linux build lacked `libuv1-dev`, preventing the R package
`fs` and its downstream Shiny dependencies from installing. Commit `d1ef765` adds those headers.
The [replacement workflow](https://github.com/jltobias/JupyterLite-R/actions/runs/44159085025)
passed Shiny tests, all ten core notebook checks, the combined build, and GitHub Pages deployment.

The public [Shiny app](https://jltobias.github.io/JupyterLite-R/shiny/) passed the existing Chrome
browser checks against its deployed URL: initial rendering, changed and restored seed, threshold,
palette, and a CSV download containing 100 observations plus the header. No JavaScript errors were
recorded. Public landing and Book routes, chapter images, and the gallery at 390 pixels also passed.
The Lab entry URL returned HTTP 200; this follow-up did not rerun the hosted notebook kernel.
See `published-browser.json` for the deployed commit, workflow, and browser results. Screenshots
and the downloaded CSV are retained locally in `validation/runs/published/` (ignored by Git).
