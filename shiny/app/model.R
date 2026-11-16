# Project: JupyterLite-R | Shiny model, shared with native tests.
# Author: project contributors with Codex | Created/updated: 2026-11-16.
# Inputs: integer seed, threshold | Outputs: original synthetic observations and summary.
# Dependencies: base R. No external data or geographies. Change log: initial example.
#' Generate a reproducible 10 by 10 grid with an artificial spatial signal.
#' Seed controls simulated measurement noise; coordinates are local kilometres.
make_field <- function(seed = 2026L) {
  stopifnot(length(seed) == 1, is.finite(seed), seed >= 1, seed <= 999999)
  set.seed(as.integer(seed))
  field <- expand.grid(x = 1:10, y = 1:10)
  field$id <- sprintf("P%03d", seq_len(nrow(field)))
  field$index <- with(field, 40 + 15 * exp(-((x-7)^2+(y-6)^2)/8) + rnorm(100, sd=2))
  field
}
#' Summarize sites meeting a chosen illustrative threshold; no inferential claim.
summarize_field <- function(field, threshold) {
  stopifnot(length(threshold) == 1, is.finite(threshold), !anyNA(field$index))
  selected <- field$index >= threshold
  data.frame(sites=nrow(field), selected=sum(selected),
             selected_percent=100*mean(selected), mean_index=mean(field$index))
}
