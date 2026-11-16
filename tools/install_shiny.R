# Deliberate project-local build dependencies for the original Shiny example.
# Project: JupyterLite-R | Created/updated: 2026-11-16 | Author: contributors with Codex.
lib <- file.path(getwd(), ".cache", "R-library")
dir.create(lib, recursive=TRUE, showWarnings=FALSE)
.libPaths(c(lib,.libPaths()))
packages <- c("shiny","shinylive")
missing <- packages[!vapply(packages,requireNamespace,logical(1),quietly=TRUE)]
if(length(missing))install.packages(missing,lib=lib,repos="https://cloud.r-project.org")
stopifnot(all(vapply(packages,requireNamespace,logical(1),quietly=TRUE)))
print(sapply(packages,packageVersion))
