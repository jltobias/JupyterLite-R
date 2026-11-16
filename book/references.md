# References and attribution

This book cites methods and software. It does not reproduce third-party publication text,
figures, geographic datasets, satellite imagery, or map tiles. See the README for the complete
project inventory and the distinction between original content and licensed software dependencies.

| Resource | Citation / purpose |
| --- | --- |
| R | R Core Team. *R: A Language and Environment for Statistical Computing*. [R Project](https://www.r-project.org/). Use `citation()` for the runtime citation. |
| JupyterLite | JupyterLite contributors. [Documentation](https://jupyterlite.readthedocs.io/). Browser application, BSD-3-Clause. |
| webR | George Stagg and webR contributors. [webR](https://docs.r-wasm.org/webr/latest/). Browser R runtime; see upstream licensing. |
| R kernel | George Stagg and contributors. [jupyterlite-webr-kernel](https://github.com/r-wasm/jupyterlite-webr-kernel). MIT. |
| Jupyter Book / MyST | Executable Books and MyST contributors. [Jupyter Book](https://jupyterbook.org/stable/) and [MyST](https://mystmd.org/). MIT. |
| RColorBrewer | Neuwirth, E. *RColorBrewer: ColorBrewer Palettes*. [CRAN DOI](https://doi.org/10.32614/CRAN.package.RColorBrewer). Apache-2.0. |
| ColorBrewer | Cynthia Brewer, Mark Harrower, and collaborators. [ColorBrewer](https://colorbrewer2.org/). Palette design; obtained through RColorBrewer. |
| sf | Pebesma, E. (2018). Simple Features for R: Standardized Support for Spatial Vector Data. *The R Journal*, 10(1), 439–446. [DOI](https://doi.org/10.32614/RJ-2018-009). |
| terra | Hijmans, R. J. and contributors. *terra: Spatial Data Analysis*. [CRAN DOI](https://doi.org/10.32614/CRAN.package.terra). |
| spdep | Bivand, R. S., and Wong, D. W. S. (2018). Comparing implementations of global and local indicators of spatial association. *TEST*, 27, 716–748. [DOI](https://doi.org/10.1007/s11749-018-0599-x). |
| micromapST | Pickle, L. W., Pearson, J. B., and Carr, D. B. (2015). micromapST: Exploring and Communicating Geospatial Patterns in US State Data. *Journal of Statistical Software*, 63(3), 1–25. [DOI](https://doi.org/10.18637/jss.v063.i03). |
| Wilson intervals | Wilson, E. B. (1927). Probable Inference, the Law of Succession, and Statistical Inference. *JASA*, 22(158), 209–212. [DOI](https://doi.org/10.1080/01621459.1927.10502953). |
| ggplot2 | Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis*. [Project](https://ggplot2.tidyverse.org/). |
| Plotly.js | Plotly contributors. [Plotly.js](https://github.com/plotly/plotly.js), MIT. Gallery renderer; third-party library loaded from CDN. |
| Shiny / Shinylive | Posit and contributors. [Shiny](https://shiny.posit.co/), [Shinylive for R](https://posit-dev.github.io/r-shinylive/). MIT; reactive application framework and browser exporter. |
| Package discovery | [R-spatial projects](https://r-spatial.org/projects/) and [CRAN Spatial Task View](https://cran.r-project.org/view=Spatial). These are directories, not webR compatibility lists. |

Run `citation("packageName")` for version-specific citations. Retain dependency licenses when
redistributing a built application. The repository's original-content notice does not relicense
R, webR, package binaries, fonts/icons bundled by upstream tools, or other dependencies.
