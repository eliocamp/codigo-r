build_site <- function(local = FALSE, method = c("html", "custom"), run_hugo = TRUE) {
   if (missing(method)) method = getOption("blogdown.method", method)
   method = match.arg(method)
   # on.exit(blogdown:::run_script("R/build.R", as.character(local)), add = TRUE)
   if (method == "custom") return()
   
   
   files = blogdown:::list_rmds("content", TRUE)
   if (length(files)) {
      files = files[mapply(blogdown:::require_rebuild, blogdown:::output_file(files), 
                           files)]
   }
   blogdown:::build_rmds(files)
   if (run_hugo) 
      on.exit(blogdown::hugo_build(local), add = TRUE)
   invisible()
}

build_site()
