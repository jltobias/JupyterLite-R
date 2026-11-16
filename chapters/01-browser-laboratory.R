# %% [markdown]
# # 1. Your browser is an R laboratory
#
# **Question:** Can a small, reproducible spatial experiment run without a server-side R session?
# **Objectives:** run cells, generate a spatial field, audit values, and record the runtime.
# **Prerequisites:** basic vectors and data frames. **Time:** 20 minutes.
#
# Select **R (webR)**, then use **Run > Run All Cells**. First startup downloads webR;
# later package installations also need a network connection. Your working files live in browser
# storage. Download important notebooks with the file browser's Download command; clearing site
# data can erase your changes. Restarting the kernel clears R objects.
#
# This book uses fictional observations and generated geometry throughout. Nothing in a map
# describes a real population or place. Base R graphics keep the core small and work with the
# kernel's PNG display. Optional packages are extensions, clearly reported when unavailable.
#
# [Open this chapter in Lab](https://jltobias.github.io/JupyterLite-R/lite/lab/index.html?path=01-browser-laboratory.ipynb)
# %%
# Project: JupyterLite-R | Chapter: 01-browser-laboratory
# Purpose: reproducible browser-based spatial simulation.
# Author: project contributors with Codex; contact: repository Issues.
# Created/updated: 2026-11-16 | Inputs: none | Outputs: inline plots and tables.
# Dependencies: base R; webR in Lab. Change log: initial original lesson.
set.seed(20261116)
options(webr.fig.width = 9, webr.fig.height = 6)
stations <- expand.grid(easting_km = seq(0, 10, 2), northing_km = seq(0, 8, 2))
stations$id <- sprintf("S%02d", seq_len(nrow(stations)))
stations$signal <- with(stations, 15 + 2 * sin(easting_km / 3) + northing_km / 2) +
  rnorm(nrow(stations), sd = 0.35)
stopifnot(nrow(stations) == 30, !anyDuplicated(stations$id), all(is.finite(stations$signal)))
head(stations)
# %% [markdown]
# ## Make the spatial pattern visible
# Each point is a fictional instrument; coordinates are local kilometres with no Earth CRS.
# Color represents a simulated signal in arbitrary units. The coordinate grid is complete:
# there is no missingness, sampling weight, or real-world inference in this experiment.
# %%
colors <- hcl.colors(30, "Viridis")
bins <- cut(stations$signal, breaks = 30, include.lowest = TRUE, labels = FALSE)
plot(northing_km ~ easting_km, data = stations, asp = 1, pch = 21,
     bg = colors[bins], cex = 2, xlab = "Local easting (km)", ylab = "Local northing (km)",
     main = "A fictional sensor field")
text(stations$easting_km, stations$northing_km, stations$id, pos = 3, cex = 0.65)
legend("topleft", legend = sprintf("Signal %.1f to %.1f (arbitrary units)",
       min(stations$signal), max(stations$signal)), bty = "n", cex = 0.8)
# %% [markdown]
# **Read the figure:** the northward gradient was built into the generator. A visible pattern
# is evidence about this simulation, not a discovery about the Earth. The printed data frame
# is a text alternative to color. Change the noise standard deviation to see the pattern weaken.
#
# ## Package setup is a separate decision
# To install a package intentionally in Lab, run `webr::install("RColorBrewer")` in a new cell.
# Browser packages must be available as compatible WebAssembly binaries. Installing a desktop
# CRAN binary does not make it a browser package. Chapters check packages with `requireNamespace()`
# and print a skip message if an extension is unavailable; base R activities still run.
# %%
packages <- c("RColorBrewer", "sf", "terra", "spdep", "micromapST", "ggplot2")
availability <- data.frame(package = packages,
  installed = vapply(packages, requireNamespace, logical(1), quietly = TRUE))
print(availability, row.names = FALSE)
sessionInfo()
# %% [markdown]
# ## Practice and check
# 1. Double the grid resolution. How does the number of observations change?
# 2. Replace the seed, rerun, then restore it. Which quantities remain unchanged?
# 3. Download the notebook, restart the kernel, and rerun from the top.
# **Checkpoint:** the original grid has 30 unique stations; coordinates repeat in each direction,
# but station IDs do not. A seed reproduces draws within a compatible R RNG/runtime setup.
#
# ## Sources
# [webR package installation](https://docs.r-wasm.org/webr/latest/packages.html);
# [R kernel](https://github.com/r-wasm/jupyterlite-webr-kernel);
# [R graphics reference](https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/00Index.html).
# Prose, code, and simulated observations in this lesson are original.
