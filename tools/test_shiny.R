# Meaningful model and reactive-server checks, executed without opening a public server.
# Project: JupyterLite-R | Created/updated: 2026-11-16 | Author: contributors with Codex.
.libPaths(c(file.path(getwd(),".cache","R-library"),.libPaths()))
source("shiny/app/model.R")
a <- make_field(2026)
stopifnot(identical(a,make_field(2026)),!identical(a$index,make_field(2027)$index),
          nrow(a)==100,!anyDuplicated(a$id))
counts <- vapply(c(35,48,60),function(t)summarize_field(a,t)$selected,integer(1))
stopifnot(all(diff(counts)<=0),summarize_field(a,100)$selected==0)
setwd("shiny/app")
app <- source("app.R",local=TRUE)$value
stopifnot(inherits(app,"shiny.appobj"))
shiny::testServer(server, {
  session$setInputs(seed=2026,threshold=48,palette="Viridis",labels=FALSE)
  original <- field()
  before <- nrow(selected())
  session$setInputs(threshold=55)
  stopifnot(identical(field(),original),nrow(selected())<=before)
  session$setInputs(seed=2027)
  stopifnot(!identical(field()$index,original$index))
})
cat("PASS: deterministic seed; threshold monotonicity; zero selection; reactive invalidation.\n")
sessionInfo()
