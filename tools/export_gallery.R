# Project: JupyterLite-R | Export numerical data for the browser gallery.
# Author: project contributors with Codex | Created/updated: 2026-11-16.
# Inputs: exact chapter sources 04, 05, 06, 09 | Outputs: original numeric CSV files.
# Dependencies: base R. Run from repo root. Change log: first export.
dir.create("gallery/data", recursive = TRUE, showWarnings = FALSE)
pdf(NULL)
source("chapters/04-terrain-and-rasters.R", local = TRUE)
terrain_grid <- expand.grid(x = x, y = y)
terrain_grid$z <- as.vector(z)
write.csv(terrain_grid, "gallery/data/terrain.csv", row.names = FALSE)
source("chapters/05-three-dimensional-scenes.R", local = TRUE)
write.csv(flight, "gallery/data/flight.csv", row.names = FALSE)
source("chapters/06-globes-and-great-circles.R", local = TRUE)
write.csv(setNames(as.data.frame(route), c("x","y","z")), "gallery/data/route.csv", row.names = FALSE)
source("chapters/09-capstone.R", local = TRUE)
write.csv(sites, "gallery/data/sites.csv", row.names = FALSE)
dev.off()
