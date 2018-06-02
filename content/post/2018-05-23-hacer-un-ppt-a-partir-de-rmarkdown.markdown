---
title: Hacer una presentación de PowerPoint a partir de rmarkdown
author: Elio Campitelli
date: '2018-05-23'
slug: presentacion-powerpoint-rmarkdown
categories:
  - R
tags: []
---

La interfaz entre usuarios de knitr/markdown y word/powerpoint no deja de ser áspera ya que es difícil cambiar el workflow propio para acomodar el de otras personas. En particular, es muy común tener que colaborar con personas que se sienten mucho más cómodas trabajando con presentaciones en PowerPoint que en las creadas con beamer o ioslides. Una forma de reducir la fricción sería la de generar un ppt automáticamente a partir de una archivo de markdown. 

La clave está en "secuestrar" la función que knitr ejecuta cuando se encuentra con un plot y agregar la imagen a un ppt con el paquete [`officer`](https://davidgohel.github.io/officer/index.html). Lo primero necesario es un archivo con un template. De este archivo va a salir el patrón para agregar distintas diapositivas según lo que queramos insertar. Esto se puede editar cambiando el [Patrón de Diapositivas](https://support.office.com/es-es/article/%C2%BFqu%C3%A9-es-un-patr%C3%B3n-de-diapositivas-b9abb2a0-7aef-4257-a14e-4329c904da54). Como yo soy muy básico, creé uno que tiene una imagen con un texto abajo y nada más y lo llamé "figure".

Una vez hecho esto, hay que poner esto en el primer chunk de setup:


```r
library(officer)
library(magrittr)

## Opciones que hay que cambiar. 
ppt <- TRUE                        # ¿quiero que salga un ppt?
pptfile <- "figuras.pptx"          # nombre de archivo del ppt saliente
ppttemplate <- "ppttemplate.pptx"  # nombre del template

# Crea el archivo inicial
if (ppt == TRUE){
   my_pres <- read_pptx(ppttemplate)
   print(my_pres, pptfile)   
}

# Hay que apagar la cache en los chunks con figuras
knitr::opts_hooks$set(fig.cap = function(options) {
   if (ppt == TRUE) options$cache <- FALSE
   options
})

# Agrega un slide con el gráfico y el caption
# para cada chunk con figuras
knit_plot <- knitr::knit_hooks$get("plot")

knitr::knit_hooks$set(plot = function(x, options) {
   if (ppt == TRUE) {
      if (inherits(last_plot(), "gg")) {
         read_pptx(pptfile)  %>%
            add_slide(layout = "figure", master = "Office Theme") %>%
            ph_with_gg(last_plot(), type = "pic") %>%
            ph_with_text(options$fig.cap, type = "body") %>%
            print(pptfile)
         set_last_plot(NULL)   # remove last_plot()
      } else {
         read_pptx(pptfile)  %>%
            add_slide(layout = "figure", master = "Office Theme") %>%
            rvg::ph_with_vg(code = eval(parse(text = options$code)), 
                            type = "pic") %>%
            ph_with_text(options$fig.cap, type = "body") %>% 
            print(pptfile)
      }
   }
   knit_plot(x, options)
})
```

Hay dos cosas importantes. Primero es setear un `opts_hook` que se ejecute siempre que la opción `fig.cap` no sea `NULL` que desactive la cache. Esto es porque sino knitr no ejecuta nada de lo que sigue y entonces no agrega la figura al ppt. 

Luego está la parte más jugosa. Cambiamos el `knit_hook` para el `plot` para que antes de hacer lo que hace siempre (que primero guardamos con `knitr::knit_hooks$get("plot")`) le decimos que guarde el plot en una nueva diapositiva. El código es ligeramente distinto si se trata de un gráfico de `ggplot2` o uno de `base`. En el caso de `ggplot2`, usamos la función `last_plot()` para guardar el último plot generado en la nueva diapositiva y luego seteamos que el `last_plot` sea `NULL` (por si el siguiente gráfico que hay que guardar es uno en base). Si es base, hay que pasarle el código del chunk evaluado a la función `ph_with_vg()`, que crea un gráfico de vectores a partir de un gráfico base.  

Y listo. Al *knitear* el documento se va a generar el pdf o html y, además, el ppt. 


![](/images/ppt.jpg#center)

Así como está es una versión mínima que cubre mis necesidades. Sólo tiene en cuenta los gráficos con epígrafe, no funciona sin un chunk genera varias figuras, el proceso de renderizar todo es lento (porque desactiva la cache) y peor aún si los chunks que generan figuras también tienen código que manipula datos. Además, no guarda tablas ni texto plano. 
