# Export the original R Shiny app as static Shinylive files.
# Project: JupyterLite-R | Created/updated: 2026-11-16 | Author: contributors with Codex.
# Input: shiny/app | Output: _shiny | Requires deliberately installed shinylive.
lib <- file.path(getwd(), ".cache", "R-library")
if(dir.exists(lib)).libPaths(c(lib,.libPaths()))
if(!requireNamespace("shinylive",quietly=TRUE))stop("Run Rscript tools/install_shiny.R first.")
shinylive::export("shiny/app", "_shiny")
# Give the exported browser tab a project-specific title; preserve all upstream notices.
index <- readLines("_shiny/index.html", warn=FALSE)
index <- sub("<title>Shiny App</title>", "<title>Spatial explorer - JupyterLite-R</title>", index, fixed=TRUE)
writeLines(index,"_shiny/index.html",useBytes=TRUE)
shinylive::assets_info()
