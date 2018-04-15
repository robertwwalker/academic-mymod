data.creator <- function(data) { 
  data %>% html_nodes("table") %>% html_table(header=TRUE, fill=TRUE) -> ret.tab
  nrowsm <- dim(ret.tab[[1]])[[1]]
  split.me <- ret.tab[[1]][,4]
#  splme <- apply(split.me, 1, function(x) { str_split(x, "\\n")})
#  do.call("rbind",splme)
  tempdf <- data.frame(matrix(data=gsub("\t|-","",unlist(strsplit(split.me, "\\n"))), nrow=nrowsm, byrow=TRUE))
  names(tempdf) <- c("value","years","value.pds")
  data %>% html_nodes(".player") %>% html_nodes("a") %>% html_text() -> Player.Names
  Player.Names <- Player.Names[c(1:nrowsm)]
  data %>% html_nodes(".player") %>% html_nodes("a") %>% html_attr("href") -> Player.Links
  Player.links <- Player.Links[c(1:nrowsm)]
  data %>% html_nodes(".player") %>% html_nodes("span") %>% html_text() -> Last.Name
  Last.Name <- Last.Name[c(1:nrowsm)]
#  data.frame(ret.tab[,c(5,6,7)]) 
  return(data.frame(ret.tab[1][[1]],tempdf,Player.Names,Player.links,Last.Name))
    }
PN1 <- Base.Contracts[[1]] 

tempdat1 <- lapply(Base.Contracts, data.creator)