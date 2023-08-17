library(TTR)
library(dplyr)
library(bigreadr)
library(ggplot2)

df <- fread2("C:/Users/Usuario/Proyectos/Bot Trading/data/data_shibusdt_3m.csv",sep = ",")

df["precio_medio"] <- (df$Open+df$Close)/2

df["HMA10"] <- HMA(df$precio_medio,10)
df["SMA3"] <- SMA(df$precio_medio,3)
df["SMA5"] <- SMA(df$precio_medio,5)
df["SMA10"] <- SMA(df$precio_medio,10)
df["SMA20"] <- SMA(df$precio_medio,20)
df["SMA50"] <- SMA(df$precio_medio,50)

# df <- df %>% mutate(HMA10 = lag(HMA10),
#                     SMA3 = lag(SMA3),
#                     SMA5 = lag(SMA5),
#                     SMA10 = lag(SMA10),
#                     SMA20 = lag(SMA20))

decidir <- function(data){
  df_prueba <- data.frame()
  aux <- ""
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
    hma10 <- fila$HMA10
    m3 <- fila$SMA3
    m5 <- fila$SMA5 
    m10 <- fila$SMA10
    m20 <- fila$SMA20
    m50 <- fila$SMA50
    
    res <- c()
    
    for (j in c(hma10,m3,m5,m10,m20,m50)) {
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
    
    if (conteo_long >= 6) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= 6) {
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

rango <- c(95000:96000)
prueba <- df[rango,]

decision <- decidir(prueba)

p <- ggplot(prueba,aes(`Open Time`,precio_medio)) + geom_line() + 
  geom_point(data = decision, aes(x = fila, y = precio, color = decision), pch = 16) +
  scale_color_manual(values = c("LONG" = "green", "SHORT" = "red")) +
  labs(x = "Tiempo de Apertura", y = "Precio Medio", title = "Gráfico con Decisión")+
  scale_x_datetime(breaks = "1 day", date_labels = "%H:%M") # 
# # geom_line(aes(`Open Time`, SMA10), color = "blue") +
# geom_line(aes(`Open Time`, SMA5), color = "orange") +
# geom_line(aes(`Open Time`, SMA10), color = "purple") +
# geom_line(aes(`Open Time`, SMA20), color = "cyan")

library(plotly)
p_interactivo <- ggplotly(p)

# Mostrar el gráfico interactivo
p_interactivo

df_todo <- merge(df,decision,by.x = "Open Time", by.y = "fila",all.x = TRUE)
