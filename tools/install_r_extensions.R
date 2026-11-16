# Project: JupyterLite-R | Install optional desktop validation packages deliberately.
# Author: project contributors with Codex | Created/updated: 2026-11-16.
# Input: CRAN packages | Output: project .cache/R-library | Does not change user/global libraries.
# Run from repository root. These desktop packages are NOT browser binaries.
lib <- file.path(getwd(), ".cache", "R-library")
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
packages <- c("RColorBrewer", "sf", "terra", "spdep", "micromapST", "ggplot2")
missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) install.packages(missing, lib = lib, repos = "https://cloud.r-project.org")
stopifnot(all(vapply(packages, requireNamespace, logical(1), quietly = TRUE)))
print(sapply(packages, packageVersion))
