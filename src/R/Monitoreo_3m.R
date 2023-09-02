# Función para calcular el tiempo de espera hasta el segundo 1
calcular_tiempo_espera <- function() {
  tiempo_actual <- as.POSIXlt(Sys.time())
  tiempo_espera <- 60 - tiempo_actual$sec + 1
  return(tiempo_espera)
}

library(TTR)
library(dplyr)
library(bigreadr)
library(ggplot2)
library(plotly)

decidir <- function(data,ind){
  df_prueba <- data.frame()
  aux <- ""
  
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$Close
    
    res <- c()
    
    for (j in ind) {
      aux1 <- fila[j]
      comp <- 2*(precio_medio-aux1)/(precio_medio+aux1)
      if (comp >= 0.00015) {
        res <- c(res,"LONG")
      }
      else if (comp <= -0.00015) {
        res <- c(res,"SHORT")
      }
    }
    
    conteo_long <- ifelse(is.na(table(res)["LONG"]),0,table(res)["LONG"])
    conteo_short <- ifelse(is.na(table(res)["SHORT"]),0,table(res)["SHORT"])
    
    if (conteo_long >= length(ind)) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,
                                "decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= length(ind)) {
      des <- "SHORT"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,
                                "decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
    }
    else {
      des <- "SALIR"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,
                                "decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
    }
  }
  return(df_prueba)
}

# Bucle para ejecutar la función en el segundo 1 de cada minuto
while (TRUE) {
  tiempo_espera <- calcular_tiempo_espera()
  Sys.sleep(tiempo_espera)
  # R script
  tiempo_inicio <- Sys.time()
  print(tiempo_inicio)
  # Ruta al archivo .bat que deseas ejecutar
  ruta_archivo_bat <- "C:/Users/Usuario/Proyectos/Bot Trading/Traer_historicos_3m.bat"
  shell(shQuote(ruta_archivo_bat), wait = TRUE)
  
  # Obtén el tiempo de finalización
  tiempo_fin <- Sys.time()
  
  # Calcula la diferencia de tiempo
  tiempo_total <- tiempo_fin - tiempo_inicio
  
  # Imprime el tiempo total
  print(tiempo_total)
  
  df <- fread2("C:/Users/Usuario/Proyectos/Bot Trading/data/data_shibusdt_3m.csv",sep = ",")
  
  df["precio_medio"] <- (df$Close)
  
  df["HMA10"] <- HMA(df$precio_medio,10)
  df["SMA3"] <- SMA(df$precio_medio,3)
  df["SMA5"] <- SMA(df$precio_medio,5)
  df["SMA10"] <- SMA(df$precio_medio,10)
  df["SMA20"] <- SMA(df$precio_medio,20)
  df["SMA50"] <- SMA(df$precio_medio,50)

  
  prueba <- tail(df,100)
  decision <- decidir(prueba,c("SMA3","SMA5","SMA10"))
  print(decision)
  
  p <- ggplot(prueba,aes(`Open Time`,precio_medio)) + geom_line(size = 2) +
    labs(x = "Tiempo de Apertura", y = "Precio Medio", title = "Gráfico con Decisión") +
    scale_x_datetime(breaks = "30 mins", date_labels = "%H:%M") +
    geom_line(aes(`Open Time`, HMA10), color = "pink",size = 1.2) +
    geom_line(aes(`Open Time`, SMA3), color = "orange",size = 1.2) +
    geom_line(aes(`Open Time`, SMA5), color = "purple",size = 1.2) +
    geom_line(aes(`Open Time`, SMA10), color = "cyan",size = 1.2) +
    geom_point(data = decision, aes(x = fila, y = precio, color = decision), pch = 16,size = 3) +
    scale_color_manual(values = c("LONG" = "green", "SHORT" = "red","SALIR" = "#FF7F24"))
  # geom_line(aes(`Open Time`, SMA60), color = "gray",size = 1.2)+
  # geom_line(aes(`Open Time`, SMA120), color = "yellow",size = 1.2)+
  # geom_line(aes(`Open Time`, SMA240), color = "salmon",size = 1.2)
  p_interactivo <- ggplotly(p)
  print(p)
}

