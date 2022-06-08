#!/usr/bin/env Rscript


files = blogdown:::list_rmds("content", TRUE)
if (length(files)) {
  files = files[mapply(blogdown:::require_rebuild, blogdown:::output_file(files), 
                       files)]
}
blogdown:::build_rmds(files)
blogdown::hugo_build(local = FALSE)
