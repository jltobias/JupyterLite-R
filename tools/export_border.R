# Generate our original border-group fixture for micromapST browser rendering.
# Created/updated: 2026-11-16 | Project: JupyterLite-R | Author: contributors with Codex.
# Inputs: chapter 08's square geometry and name table. Output: notebooks/data/FictionalBG.rda.
# Requires the native optional packages. No external boundary data is used.
.libPaths(c(file.path(getwd(),".cache","R-library"),.libPaths()))
stopifnot(requireNamespace("sf",quietly=TRUE),requireNamespace("micromapST",quietly=TRUE))
pdf(NULL)
source("chapters/08-linked-micromaps.R",local=TRUE)
invisible(dev.off())
dir.create("notebooks/data",showWarnings=FALSE)
stopifnot(file.copy(file.path(border_dir,"FictionalBG.rda"),"notebooks/data/FictionalBG.rda",overwrite=TRUE))
cat("Exported original FictionalBG border group.\n")
