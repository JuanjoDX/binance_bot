library(TTR)
library(dplyr)
library(bigreadr)
library(ggplot2)
library(plotly)

df <- fread2("C:/Users/Usuario/Proyectos/Bot Trading/data/data_shibusdt_1m.csv",sep = ",")

df["precio_medio"] <- (df$Open+df$Close)/2

df["HMA10"] <- HMA(df$precio_medio,10)
df["SMA5"] <- SMA(df$precio_medio,5)
df["SMA10"] <- SMA(df$precio_medio,10)
df["SMA30"] <- SMA(df$precio_medio,30)
df["SMA60"] <- SMA(df$precio_medio,60)
df["SMA120"] <- SMA(df$precio_medio,120)
df["SMA240"] <- SMA(df$precio_medio,240)


# df <- df %>% mutate(SMA5 = lag(SMA5),
#                     SMA10 = lag(SMA10),
#                     SMA25 = lag(SMA25),
#                     SMA50 = lag(SMA50),
#                     SMA100 = lag(SMA100))


decidir_general <- function(data){
  df_prueba <- data.frame()
  aux <- ""
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
    h10 <- fila$HMA10
    m5 <- fila$SMA5
    m10 <- fila$SMA10
    m30 <- fila$SMA30 
    m60 <- fila$SMA60
    m120 <- fila$SMA120
    m240 <- fila$SMA240
    
    res <- c()
    
    for (j in c(h10,m5,m10,m30,m60,m120,m240)) {
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
    
    if (conteo_long >= 7) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= 7) {
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

decidir_corto <- function(data){
  df_prueba <- data.frame()
  aux <- ""
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
    h10 <- fila$HMA10
    m5 <- fila$SMA5
    m10 <- fila$SMA10
    m30 <- fila$SMA30 
    
    res <- c()
    
    for (j in c(h10,m5,m10,m30)) {
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
    
    if (conteo_long >= 4) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= 4) {
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

decidir_largo <- function(data){
  df_prueba <- data.frame()
  aux <- ""
  for (i in 1:nrow(data)) {
    fila <- data[i,]
    fecha <- fila$`Open Time`
    precio_medio <- fila$precio_medio
    
    m30 <- fila$SMA30 
    m60 <- fila$SMA60
    m120 <- fila$SMA120
    m240 <- fila$SMA240
    
    res <- c()
    res1 <- c()
    res2 <- c()
    
    for (j in c(m30,m60,m120,m240)) {
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
    
    if (conteo_long >= 4) {
      des <- "LONG"
      if (des != aux) {
        resultado <- data.frame("fila" = fecha,"precio" = precio_medio,"decision" = des)
        df_prueba <- df_prueba %>%
          bind_rows(resultado)
        aux <- des
      }
      
    }
    else if (conteo_short >= 4) {
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

rango <- c(105000:105500)
prueba <- tail(df,1000)

decision <- decidir_general(prueba)

p <- ggplot(prueba,aes(`Open Time`,precio_medio)) + geom_line() + 
  geom_point(data = decision, aes(x = fila, y = precio, color = decision), pch = 16) +
  scale_color_manual(values = c("LONG" = "green", "SHORT" = "red")) +
  labs(x = "Tiempo de Apertura", y = "Precio Medio", title = "Gráfico con Decisión")+
  scale_x_datetime(breaks = "1 day", date_labels = "%H:%M") +
  # geom_line(aes(`Open Time`, HMA10), color = "blue") +
  # geom_line(aes(`Open Time`, SMA5), color = "orange") +
  # geom_line(aes(`Open Time`, SMA10), color = "purple") +
  geom_line(aes(`Open Time`, SMA30), color = "cyan") +
  geom_line(aes(`Open Time`, SMA60), color = "gray")+
  geom_line(aes(`Open Time`, SMA120), color = "pink")+
  geom_line(aes(`Open Time`, SMA240), color = "salmon")


p_interactivo <- ggplotly(p)

# Mostrar el gráfico interactivo
p_interactivo

df_todo <- merge(df,decision,by.x = "Open Time", by.y = "fila",all.x = TRUE)
