# Project: JupyterLite-R | Original reactive spatial explorer.
# Author: project contributors with Codex | Contact: repository Issues.
# Created/updated: 2026-11-16 | Inputs: controls, original simulation | Outputs: plots and CSV.
# Dependencies: shiny, base R. Run with shiny::runApp('shiny/app') from repo root,
# or export with shinylive. This is NOT executed inside the JupyterLite notebook kernel.
library(shiny)
source("model.R", local = TRUE)

ui <- fluidPage(
  # Fetch the generated file before downloading. This also works through Shinylive's
  # service-worker HTTP proxy, where direct navigation downloads can be cancelled.
  tags$head(tags$script(HTML("
    document.addEventListener('click', async function(event) {
      const link = event.target.closest && event.target.closest('#download');
      if (!link) return;
      event.preventDefault(); event.stopImmediatePropagation();
      const status = document.getElementById('download-status');
      status.textContent = 'Preparing CSV...';
      try {
        const response = await fetch(link.href);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const save = document.createElement('a');
        save.href = url; save.download = 'fictional-sites.csv';
        document.body.appendChild(save); save.click(); save.remove();
        setTimeout(function(){ URL.revokeObjectURL(url); }, 5000);
        status.textContent = 'CSV prepared with all observations.';
      } catch(error) { status.textContent = 'Download failed: ' + error.message; }
    }, true);
  "))),
  tags$head(tags$style(HTML("
    body{background:#f2f7f7;color:#183644;font-family:system-ui,sans-serif}
    .container-fluid{max-width:1320px;margin:auto;padding:25px}
    h1,h2,h3{font-family:Georgia,serif} h1{font-size:38px;margin-bottom:10px}
    .well{background:#e5eeee;border:1px solid #c6d9d8;box-shadow:none;border-radius:10px}
    .note{color:#526b76;font-size:14px;max-width:900px}.shiny-plot-output{background:white;border-radius:10px}
    .btn-default{background:#0d625e;color:white;border:0}a{color:#075e62}
    .metric{padding:15px 0;font-size:18px}.control-label{margin-top:12px}
  "))),
  titlePanel("A map that responds to your questions"),
  p(class="note", "An R Shiny laboratory: change the threshold, palette, or simulation seed. ",
    "Every point is fictional. The index has arbitrary units and is not a risk measure."),
  p(a("Read the textbook", href="https://jltobias.github.io/JupyterLite-R/book/"), " · ",
    a("Notebook and app source", href="https://github.com/jltobias/JupyterLite-R/tree/main/shiny")),
  sidebarLayout(
    sidebarPanel(width=3,
      sliderInput("threshold", "Highlight index at or above", min=35, max=60, value=48, step=1),
      selectInput("palette", "Sequential palette", choices=c("Viridis", "Blues 3", "Terrain"), selected="Viridis"),
      numericInput("seed", "Simulation seed", value=2026, min=1, max=999999, step=1),
      checkboxInput("labels", "Show selected site IDs", value=FALSE),
      downloadButton("download", "Download all observations"),
      tags$p(id="download-status",class="note",role="status",`aria-live`="polite"),
      hr(), p(class="note", "Thresholds are illustrative. Changing a threshold changes selection, ",
        "not the underlying observations. Only the seed regenerates the field."),
      p(class="note", "On the published Shinylive page, R and Shiny run in your browser. ",
        "Initial downloads require a network connection. No observations are uploaded.")
    ),
    mainPanel(width=9,
      div(class="metric", textOutput("summary")),
      plotOutput("map", height="470px"),
      plotOutput("distribution", height="240px"),
      h3("Selected observations"),
      p(class="note", "Sorted by index. The downloadable CSV includes all sites and a selection flag."),
      tableOutput("selected"),
      tags$details(tags$summary("How reactivity works"),
        p("input$seed invalidates field(). Threshold and palette changes reuse the same field. ",
          "Outputs read reactive values and redraw automatically; there is no polling loop."),
        verbatimTextOutput("runtime"))
    )
  ),
  hr(), p(class="note", "Original synthetic data and app: JupyterLite-R. ",
    a("Shiny",href="https://shiny.posit.co/"), " and ",
    a("Shinylive",href="https://posit-dev.github.io/r-shinylive/"),
    " by Posit and contributors (MIT); R/webR retain their upstream licenses.")
)

server <- function(input, output, session) {
  field <- reactive({
    req(input$seed)
    validate(need(input$seed >= 1 && input$seed <= 999999 && input$seed == floor(input$seed),
                  "Use a whole-number seed between 1 and 999999."))
    make_field(input$seed)
  })
  selected <- reactive({
    d <- field()
    d[d$index >= input$threshold, , drop=FALSE]
  })
  output$summary <- renderText({
    s <- summarize_field(field(), input$threshold)
    sprintf("%d of %d sites selected (%.0f%%) · Mean index %.2f", s$selected,s$sites,s$selected_percent,s$mean_index)
  })
  output$map <- renderPlot({
    d <- field(); chosen <- d$index >= input$threshold
    pal <- hcl.colors(40, input$palette)
    # Fixed index limits make color comparisons stable across seeds.
    bins <- pmax(1L,pmin(40L,as.integer(cut(d$index,breaks=seq(30,65,length.out=41),include.lowest=TRUE))))
    validate(need(!anyNA(bins), "Values fall outside the display range; choose another seed or extend the scale."))
    par(mar=c(4,4,3,1))
    plot(d$x,d$y,asp=1,xlim=c(.5,13.5),ylim=c(.5,11.5),pch=ifelse(chosen,24,21),bg=pal[bins],col="#183644",
      cex=2,xlab="Local x (km)",ylab="Local y (km)",main="Fictional spatial index | triangles meet threshold")
    if(input$labels && any(chosen))text(d$x[chosen],d$y[chosen],d$id[chosen],pos=3,cex=.7)
    legend("topleft",c("Below threshold","At/above threshold"),pch=c(21,24),pt.bg="grey80",bty="n",cex=.8)
    legend(11,10,legend=round(seq(30,65,length.out=5),1),
      fill=pal[round(seq(1,40,length.out=5))],title="Index",bty="n",cex=.8)
  },res=96,alt="Spatial scatter map of 100 fictional sites. Selected sites use triangles; the table provides values.")
  output$distribution <- renderPlot({
    par(mar=c(4,4,2,1))
    hist(field()$index,breaks=seq(25,70,by=2.5),col="#80c4b7",border="white",
      xlim=c(30,65),xlab="Index (arbitrary units)",main="One field; many possible thresholds")
    abline(v=input$threshold,col="#a34e06",lwd=3,lty=2)
  },res=96,alt="Histogram of the fictional index with the current threshold marked.")
  output$selected <- renderTable({
    d <- selected(); d <- d[order(d$index,decreasing=TRUE),]
    d$index <- round(d$index,2); d
  },striped=TRUE,rownames=FALSE)
  output$download <- downloadHandler(
    filename=function()sprintf("fictional-sites-seed-%s.csv",input$seed),
    content=function(file){d<-field();d$selected<-d$index>=input$threshold;write.csv(d,file,row.names=FALSE)}
  )
  output$runtime <- renderPrint({sessionInfo()})
}
shinyApp(ui, server)
