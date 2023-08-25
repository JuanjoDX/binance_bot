library(TTR)
library(dplyr)
library(bigreadr)
library(ggplot2)
library(plotly)

df <- fread2("C:/Users/Usuario/Proyectos/Bot Trading/data/historico_data_shibusdt_1m.csv",sep = ",")

df["precio_medio"] <- (df$Open+df$Close)/2

df["HMA10"] <- HMA(df$Close,10)
df["SMA5"] <- SMA(df$Close,5)
df["SMA10"] <- SMA(df$Close,10)
df["SMA30"] <- SMA(df$Close,30)
df["SMA60"] <- SMA(df$Close,60)
df["SMA120"] <- SMA(df$Close,120)
df["SMA240"] <- SMA(df$Close,240)


# df <- df %>% mutate(SMA5 = lag(SMA5),
#                     SMA10 = lag(SMA10),
#                     SMA25 = lag(SMA25),
#                     SMA50 = lag(SMA50),
#                     SMA100 = lag(SMA100))



decidir <- function(data,ind){
  df_prueba <- data.frame()
  aux <- ""
  
  for (i in 1:nrow(data)) {
    print(i)
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
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

rango <- c(105000:105500)
prueba <- tail(df,7000)

decision <- decidir(prueba,c("SMA5","SMA10","SMA30","SMA60","SMA120"))

p <- ggplot(prueba,aes(`Open Time`,precio_medio)) + geom_line() + 
  geom_point(data = decision, aes(x = fila, y = precio, color = decision), pch = 16) +
  scale_color_manual(values = c("LONG" = "green", "SHORT" = "red")) +
  labs(x = "Tiempo de Apertura", y = "Precio Medio", title = "Gráfico con Decisión")+
  scale_x_datetime(breaks = "1 day", date_labels = "%H:%M") +
  geom_line(aes(`Open Time`, HMA10), color = "blue") +
  geom_line(aes(`Open Time`, SMA5), color = "orange") +
  geom_line(aes(`Open Time`, SMA10), color = "purple") +
  geom_line(aes(`Open Time`, SMA30), color = "cyan")
  # geom_line(aes(`Open Time`, SMA60), color = "gray")+
  # geom_line(aes(`Open Time`, SMA120), color = "pink")+
  # geom_line(aes(`Open Time`, SMA240), color = "salmon")


p_interactivo <- ggplotly(p)

# Mostrar el gráfico interactivo
p_interactivo

df_todo <- merge(df,decision,by.x = "Open Time", by.y = "fila",all.x = TRUE)
