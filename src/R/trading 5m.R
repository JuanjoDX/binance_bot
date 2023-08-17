library(readxl)
library(TTR)
library(dplyr)
library(bigreadr)
library(ggplot2)

df <- fread2("C:/Users/Usuario/Proyectos/Bot Trading/data/prueba_data_shibusdt_5m.csv",sep = ",")

df["precio_medio"] <- (df$Open+df$Close)/2

df["HMA6"] <- HMA(df$precio_medio,6)
df["SMA2"] <- SMA(df$precio_medio,2)
df["SMA3"] <- SMA(df$precio_medio,3)
df["SMA6"] <- SMA(df$precio_medio,6)
df["SMA12"] <- SMA(df$precio_medio,12)
df["SMA24"] <- SMA(df$precio_medio,24)
# 
# df <- df %>% mutate(HMA6 = lag(HMA6),
#                     SMA6 = lag(SMA2),
#                     SMA12 = lag(SMA3),
#                     SMA24 = lag(SMA6),
#                     SMA72 = lag(SMA12))

decidir <- function(data){
  df_prueba <- data.frame()
  aux <- ""
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
    hma6 <- fila$HMA6
    m2 <- fila$SMA2
    m3 <- fila$SMA3 
    m6 <- fila$SMA6
    m12 <- fila$SMA12
    m24 <- fila$SMA24
    
    res <- c()
    
    for (j in c(hma6,m2,m6,m12,m24)) {
      comp <- 2*(precio_medio-j)/(precio_medio+j)
      if (comp >= 0.0015) {
        res <- c(res,"LONG")
      }
      else if (comp <= -0.0015) {
        res <- c(res,"SHORT")
      }
    }
    
    conteo_long <- ifelse(is.na(table(res)["LONG"]),0,table(res)["LONG"])
    conteo_short <- ifelse(is.na(table(res)["SHORT"]),0,table(res)["SHORT"])
    
    if (conteo_long >= 5) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= 5){
      des <- "SHORT"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
    }
  }
  return(df_prueba)
}

rango <- c(1000:57600)
prueba <- tail(df,150)

decision <- decidir(prueba)

p <- ggplot(prueba,aes(`Open Time`,precio_medio)) + geom_line() + 
  geom_point(data = decision, aes(x = fila, y = precio, color = decision), pch = 16) +
  scale_color_manual(values = c("LONG" = "green", "SHORT" = "red")) +
  labs(x = "Tiempo de Apertura", y = "Precio Medio", title = "Gráfico con Decisión")# +
# geom_line(aes(`Open Time`, SMA2), color = "blue") +
# geom_line(aes(`Open Time`, SMA3), color = "orange") +
# geom_line(aes(`Open Time`, SMA6), color = "purple") +
# geom_line(aes(`Open Time`, SMA12), color = "cyan")+
# scale_x_datetime(breaks = "15 mins", date_labels = "%H:%M") # +  # Ajusta los breaks y etiquetas en el eje x
# scale_y_continuous(breaks = seq(0, max(prueba$precio_medio), by = 0.00005))  # Ajusta los breaks en el eje y


library(plotly)
p_interactivo <- ggplotly(p)

# Mostrar el gráfico interactivo
p_interactivo



df_todo <- merge(df,decision,by.x = "Open Time", by.y = "fila",all.x = TRUE)
