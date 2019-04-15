
```{r}
Labs <- ChargeOff.Data %>% group_by(series_id) %>% summarise(SeriesTitle = first(title)) %>% ungroup()
Labs2 <- Labs %>% str_split(SeriesTitle, n=2) 
ChargeOff.Data %>% ggplot(data = ., mapping = aes(x = date, y = value)) +
  geom_line() +
  labs(x = "Date", y = "Rate", title=Labs[[1]], subtitle = Labs[[2]] ) + facet_wrap(series_id)
```

