---
title: Cómo hacer un efecto de relieve en R
author: Elio Campitelli
date: '2018-01-24'
slug: como-hacer-efecto-de-relieve-en-r
categories:
  - R
tags: []
---

Estaba tratando de hacer una guía de colores circular (que los extremos tengan el mismo color) para hacer gráficos de ángulos o direcciones del viento, cuando descubrí una forma interesante de crear un efecto de relieve en mapas de topografía. 

Digamos que tenemos datos de altura del suelo sobre el nivel del mar en una grilla regular. Como ejemplo vamos a usar la vieja y querida `volcano`.


```r
library(data.table)
library(ggplot2)
data(volcano)
volcano <- as.data.table(melt(volcano, varnames = c("x", "y"),
                              value.name = "h"))
```

La forma más básica de visualizarlos (en `ggplot2`) es con un `geom_raster()` (o `geom_tile()`):


```r
ggplot(volcano, aes(x, y)) + 
   geom_raster(aes(fill = h), interpolate = TRUE) +
   scale_fill_viridis_c(option = "A", guide = "none") +
   coord_fixed() +
   theme_void()
```

<img src="/post/2018-01-24-como-hacer-efecto-de-relieve-en-r_files/figure-html/unnamed-chunk-2-1.png" width="672" />

Y está bien. Grafica los datos correctamente y encima elegimos una escala de colores uniforme y no asquerosa. Pero si uno quiere que tenga un poco más de *punch*, y quizás está dispuesto a perder un poco de exactitud en la representación en favor de una impresión más instintiva de la forma de este volcán, podría preferir que tuviera algún sombreado que de una idea del relieve. Algo llamativo como esto: 

<p align = "center"><img scr = "/images/shading.jpg" /></p>

Lindo, ¿no? En R podemos hacer algo aproximado. Lo que vamos a hacer es calcular la pendiente en cada punto de grilla y luego pensar que la intensidad de las luces y sombras son proporcionales al producto escalar entre ésta y el ángulo con el que llega el Sol. 

Tomando que el Sol brilla desde arriba a la izquierda, si una región tiene pendiente hacia arriba a la derecha, el producto escalar es negativo y tenemos una región de sombra. Lo mismo pasa al contrario... creo. En realidad no pensé esta parte demasiado bien, ¡pero el resultado en el gráfico es bueno y creo que que [coincide con métodos existentes](http://www.reliefshading.com/analytical/shading-methods/)! (Créanme :pray:).

Primero, tenemos que calcular el gradiente de la altura en cada punto. Acá estoy usando una función de mi paquete personal (que ustedes pueden adquirir en el puesto instalado en el hall del teatro... digo, [en github](https://github.com/eliocamp/metR)).


```r
volcano[, c("dx", "dy") := metR::Derivate(h ~ x + y)]
volcano[, angle := atan2(-dy, -dx)]
```

Ya con esto simplemente mapeamos el coseno del ángulo (por el producto vectorial) a una escala de grises que empiece y termine en el mismo color.  


```r
sun.angle <- pi/3
ggplot(volcano, aes(x, y)) +
   geom_raster(aes(fill = cos(angle + sun.angle)), alpha = 1, interpolate = TRUE) +
   scale_fill_gradient2(low = "white", high = "white", mid = "gray20", 
                        midpoint = sun.angle, guide = "none") +
   coord_fixed() +
   theme_void() 
```

<img src="/post/2018-01-24-como-hacer-efecto-de-relieve-en-r_files/figure-html/unnamed-chunk-4-1.png" width="672" />

¡Hermoso! :purple_heart: Si queremos cambiar la hora del día, sólo basta con cambiar el ángulo del sol. Esas áreas horribles en gris llano son regiones con errores, donde los datos son constantes, la derivada es nula y el ángulo entonces es cero. Por ahora dejémoslas ser porque todavía hay una última cosa que hacer. 

¿Qué tal si además de este sombreado genial queremos de alguna mantera mostrar la altura? ¿U otra variable como la temperatura o el uso del terreno o lo que sea? Como nuestra `scale_fill()` está siendo usada por el relieve, no podemos mapear otras variables a ese parámetro. Es decir, no podemos usar un `geom_tile()` con transparencia, por ejemplo. Que yo sepa hay dos formas de solucionar esto. Una fácil y una difícil. 

La primera implica hacer un poco de cirugía de plots. Primero, creamos un plot similar al anterior pero con transparencia y sin tanta fanfarria y más contraste. Después lo convertimos en un grob (GRaphical OBject) y luego le extraemos la parte que nos interesa. Esto acá está hecho manual pero podría automatizarse. Hay que buscar primero el grob que sea `gTree` (el 5, en este caso) y luego, entre sus `children`, encontrar el que sea un `rect` (el 3). 

Finalmente, con el grob del sombreado ya en nuestras manos, hacemos el gráfico que queremos, con las escalas que se nos ocurra, pero le agregamos el sombreado como una anotación con `annotation_custom()`. 


```r
shade <- ggplot(volcano, aes(x, y)) +
   geom_raster(aes(fill = cos(angle + sun.angle)), alpha = 0.5, interpolate = TRUE) +
   scale_fill_gradient2(low = "white", high = "white", mid = "black", 
                        midpoint = sun.angle, guide = "none")

grob.shade <- ggplotGrob(shade)
grob.shade <- grob.shade$grobs[[6]]$children[[3]]

ggplot(volcano, aes(x, y)) +
   geom_raster(aes(fill = h), alpha = 1, interpolate = TRUE) +
   annotation_custom(grob = grob.shade) +
   scale_fill_viridis_c(guide = "none", option = "A") +
   coord_fixed() +
   theme_void() 
```

<img src="/post/2018-01-24-como-hacer-efecto-de-relieve-en-r_files/figure-html/unnamed-chunk-5-1.png" width="672" />

La forma más difícil en realidad es difícil para quien escribe, pero mucho más fácil para quien lee: hacer un `geom` propio. Una vez que uno se mete en las entrañas de `ggplot2`, puede liberarse de las cadenas de las escalas y hacer `geoms` que dibujen las cosas como uno quiera. En este caso, creamos una versión de `geom_tile()` que, además de hacer los cálculos de derivadas internamente, genera el degradé (que puede ser modificado por el usuario mediante los parámetros `light` y `dark`) sin tocar ninguna escala. Además, se puede cambiar el ángulo del sol con `sun.angle`, decidir si se usa `raster` (rápido y permite interpolación, pero sólo en coordenadas cartesianas) o `rect` (más lento) y si interpola para un efecto más lindo. Les presento a `geom_relief()`: 


```r
geom_relief <- function(mapping = NULL, data = NULL,
                        stat = "identity", position = "identity",
                        ...,
                        raster = TRUE,
                        interpolate = TRUE,
                        na.rm = FALSE,
                        show.legend = NA,
                        inherit.aes = TRUE) {
   ggplot2::layer(
      data = data,
      mapping = mapping,
      stat = stat,
      geom = GeomRelief,
      position = position,
      show.legend = show.legend,
      inherit.aes = inherit.aes,
      params = list(
         raster = raster,
         interpolate = interpolate,
         na.rm = na.rm,
         ...
      )
   )
}

GeomRelief <- ggplot2::ggproto("GeomRelief", GeomTile,
  required_aes = c("x", "y", "z"),
  default_aes = ggplot2::aes(color = NA, fill = "grey35", size = 0.5, linetype = 1,
                             alpha = NA, light = "white", dark = "gray20", sun.angle = 60),
  draw_panel = function(data, panel_scales, coord, raster, interpolate) {
     if (!coord$is_linear()) {
        stop("non lineal coordinates are not implemented in GeomRelief", call. = FALSE)
     } else {
        coords <- as.data.table(coord$transform(data, panel_scales))
        
        # Esto es lo único que es nuevo. El resto es básicamente copy-paste
        # de geom_raster y geom_tile.
        coords[, sun.angle := (sun.angle + 90)*pi/180]
        coords[, dx := .derv(z, x), by = y]
        coords[, dy := .derv(z, y), by = x]
        coords[, shade := (cos(atan2(-dy, -dx) - sun.angle) + 1)/2]
        coords[is.na(shade), shade := 0]
        coords[, fill := .rgb2hex(colorRamp(c(dark, light), space = "Lab")(shade)),
               by = .(dark, light)]
        
        # Desde geom_raster y geom_tile
        if (raster == TRUE){
           if (!inherits(coord, "CoordCartesian")) {
              stop("geom_raster only works with Cartesian coordinates", call. = FALSE)
           }
           # Convert vector of data to raster
           x_pos <- as.integer((coords$x - min(coords$x)) / resolution(coords$x, FALSE))
           y_pos <- as.integer((coords$y - min(coords$y)) / resolution(coords$y, FALSE))
           
           nrow <- max(y_pos) + 1
           ncol <- max(x_pos) + 1
           
           raster <- matrix(NA_character_, nrow = nrow, ncol = ncol)
           raster[cbind(nrow - y_pos, x_pos + 1)] <- alpha(coords$fill, coords$alpha)
           
           # Figure out dimensions of raster on plot
           x_rng <- c(min(coords$xmin, na.rm = TRUE), max(coords$xmax, na.rm = TRUE))
           y_rng <- c(min(coords$ymin, na.rm = TRUE), max(coords$ymax, na.rm = TRUE))
           
           grid::rasterGrob(raster,
                            x = mean(x_rng), y = mean(y_rng),
                            width = diff(x_rng), height = diff(y_rng),
                            default.units = "native", interpolate = interpolate
           )
           
        } else {
           ggplot2:::ggname("geom_rect", grid::rectGrob(
              coords$xmin, coords$ymax,
              width = coords$xmax - coords$xmin,
              height = coords$ymax - coords$ymin,
              default.units = "native",
              just = c("left", "top"),
              gp = grid::gpar(
                 col = coords$fill,
                 fill = alpha(coords$fill, coords$alpha),
                 lwd = coords$size * .pt,
                 lty = coords$linetype,
                 lineend = "butt"
              )
           ))
           
        }
     }
  }
)

rect_to_poly <- function(xmin, xmax, ymin, ymax) {
   data.frame(
      y = c(ymax, ymax, ymin, ymin, ymax),
      x = c(xmin, xmax, xmax, xmin, xmin)
   )
}

.rgb2hex <- function(array) {
   rgb(array[, 1], array[, 2], array[, 3], maxColorValue = 255)
}


.derv <- function(x, y, order = 1, cyclical = FALSE, fill = FALSE) {
   N <- length(x)
   d <- y[2] - y[1]
   if (order >= 3) {
      dxdy <- .derv(.derv(x, y, order = 2, cyclical = cyclical, fill = fill),
                    y, order = order - 2, cyclical = cyclical, fill = fill)
   } else {
      if (order == 1) {
         dxdy <- (x[c(2:N, 1)] - x[c(N, 1:(N-1))])/(2*d)
      } else if (order == 2) {
         dxdy <- (x[c(2:N, 1)] + x[c(N, 1:(N-1))] - 2*x)/d^2
      }
      if (!cyclical) {
         if (!fill) {
            dxdy[c(1, N)] <- NA
         }
         if (fill) {
            dxdy[1] <- (-11/6*x[1] + 3*x[2] - 3/2*x[3] + 1/3*x[4])/d
            dxdy[N] <- (11/6*x[N] - 3*x[N-1] + 3/2*x[N-2] - 1/3*x[N-3])/d
         }
      }
      
   }
   return(dxdy)
}
```

De yapa, apliquemos esta técnica a datos topográficos reales de la Cordillera de los Andes cerca del Aconcagua, provistos por [ETOPO1 de la NOAA](https://www.ngdc.noaa.gov/mgg/global/).


```r
aconcagua <- metR::GetTopography(-70.0196223 - 3 + 360, -70.0196223 + 3 + 360,
                                 -32.6531782 + 2, -32.6531782 - 2, 
                                 resolution = 1/60)
aconcagua[, c("light", "dark") := .(ifelse(h > 0, "white", "slategray2"),
                                ifelse(h > 0, "gray20", "midnightblue"))] 
ggplot(aconcagua, aes(lon, lat)) +
   geom_relief(aes(z = h, light = light, dark = dark), 
               raster = TRUE, interpolate = TRUE, sun.angle = 60) +
   coord_fixed(expand = FALSE) +
   theme_void()
```

<img src="/post/2018-01-24-como-hacer-efecto-de-relieve-en-r_files/figure-html/unnamed-chunk-7-1.png" width="672" />

El resultado, para chuparse los dedos. :ok_hand: 
