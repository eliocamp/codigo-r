library(ggperiodic)
library(ggplot2)
setwd("~/Pictures/periodic")

t <- seq(0, 360-20, by = 20)*pi/180
data <- data.frame(t = t*180/pi, x = cos(t))
data_p <- periodic(data, t = c(0, 360))

ranges_low <- c(  0,   180, -360*6, -360*4,   0)
ranges_hig <- c(360, 360*3,  360*6,      0, 360)
t          <- c(  1,     5,     10,     15,  20)
n <- 100
ranges_low_tween <- approx(t, ranges_low, n = n)$y
ranges_hig_tween <- approx(t, ranges_hig, n = n)$y

for (i in seq_len(n)[-1]) {
   range <- c(ranges_low_tween[i], ranges_hig_tween[i])
   g <- ggplot(data_p, aes(t, x), t = range) +
      geom_line() +
      geom_point(data = data) +
      scale_x_continuous(breaks = seq(min(ranges_low), max(ranges_hig), by = 60), 
                         expand = c(0, 0)) +
      coord_cartesian(xlim = range)
   ggsave(paste0("~/Pictures/periodic/plot_", formatC(i, width = 4, flag = "0"), ".png"), g,
          dpi = 72, width = 400/72, height = 200/72)
}

system("convert -delay 5 *.png periodic.gif")