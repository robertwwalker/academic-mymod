---
title: Some Basic Text on the Mueller Report
author: RWW
date: '2019-05-22'
slug: some-basic-text-on-the-mueller-report
categories:
  - tidyverse
  - tidytext
tags:
  - tidytext
  - R
header:
  caption: ''
  image: ''
  preview: yes
---


# So this Robert Mueller guy wrote a report

I may as well analyse it a bit.

First, let me see if I can get a hold of the data.  I grabbed the report directly from the Department of Justice website.  You can follow this [link](https://www.justice.gov/storage/report.pdf).


```r
library(tidyverse)
library(pdftools)
# Download report from link above
mueller_report_txt <- pdf_text("../data/report.pdf")
# Create a tibble of the text with line numbers and pages
mueller_report <- tibble(
  page = 1:length(mueller_report_txt),
  text = mueller_report_txt) %>% 
  separate_rows(text, sep = "\n") %>% 
  group_by(page) %>% 
  mutate(line = row_number()) %>% 
  ungroup() %>% 
  select(page, line, text)
write_csv(mueller_report, "data/mueller_report.csv")
```

Now I can use a .csv of the data; reading the .pdf and hacking it up takes time.


```r
library(tidyverse)
library(pdftools)
mueller_report <- read_csv("../../data/mueller_report.csv")
head(mueller_report)
```

```
## # A tibble: 6 x 3
##    page  line text                                                         
##   <dbl> <dbl> <chr>                                                        
## 1     1     1 U.S. Department of Justice                                   
## 2     1     2 "AttarAe:,c \\\\'erlc Predtiet // Mtt; CeA1:ttiA Ma1:ertal P…
## 3     1     3 Report On The Investigation Into                             
## 4     1     4 Russian Interference In The                                  
## 5     1     5 2016 Presidential Election                                   
## 6     1     6 Volume I of II
```

The text is generally pretty good though there is some garbage.  The second line contains redactions and those are the underlying cause.  In fact, every page contains this same line though they convert to text in a non-uniform fashion.


```r
mueller_report %>% filter(line!=2) -> mueller_ml2
```

I want to make use of [cleanNLP](https://github.com/statsmaths/cleanNLP) to turn this into something that I can analyze.  The first step is to get rid of the tidyness, of sorts.


```r
library(tidyverse)
library(RCurl)
library(tokenizers)
library(cleanNLP)
MRep <- paste(as.character(mueller_ml2$text), " ")
cnlp_init_spacy()
starttime <- Sys.time()
spacy_annotate <- MRep %>% as.character() %>% cnlp_annotate(as_strings = TRUE, backend = "spaCy") 
endtime <- Sys.time()
```

I wanted to find the bigrams while removing stop words.  Apparently, the easiest way to do this is `quanteda`.  I got this from [stack overflow](https://stackoverflow.com/questions/34282370/form-bigrams-without-stopwords-in-r)


```r
library(quanteda)
```

```
## Package version: 1.4.3
```

```
## Parallel computing: 2 of 16 threads used.
```

```
## See https://quanteda.io for tutorials and examples.
```

```
## 
## Attaching package: 'quanteda'
```

```
## The following object is masked from 'package:utils':
## 
##     View
```

```r
library(wordcloud2)
myDfm <- tokens(MRep) %>%
    tokens_remove("\\p{P}", valuetype = "regex", padding = TRUE) %>%
    tokens_remove(stopwords("english"), padding  = TRUE) %>%
    tokens_ngrams(n = 2) %>%
    dfm()
wc2 <- topfeatures(myDfm, n=150, scheme="count")
wc2.df <- data.frame(word = names(wc2), freq=as.numeric(wc2))
wc2.df$word <- as.character(wc2.df$word)
wc2.df <- wc2.df %>% filter(freq < 300)
wordcloud2(wc2.df, size=0.4)
```

<!--html_preserve--><div id="htmlwidget-792ff5bd10c06f0831b5" style="width:672px;height:480px;" class="wordcloud2 html-widget"></div>
<script type="application/json" data-for="htmlwidget-792ff5bd10c06f0831b5">{"x":{"word":["trump_campaign","16_email","special_counsel","white_house","ongoing_matter","states_v","trump_jr","russian_government","new_york","attorney_general","june_9","trump_tower","personal_counsel","trump_organization","et_al","candidate_trump","moscow_project","17_notes","foreign_policy","york_times","russia_investigation","donald_trump","text_message","tower_moscow","cohen_9","paul_manafort","presidential_election","mcgahn_12","michael_cohen","president_trump","9_meeting","grand_jury","campaign_officials","washington_post","fbi_director","national_security","social_media","mcgahn_3","false_statements","president_said","19_302","flynn_11","president_told","transition_team","election_interference","hillary_clinton","sessions_1","section_1512","russian_election","16_text","oval_office","clinton_campaign","see_also","investigative_technique","simes_3","president_asked","june_8","text_messages","mcfarland_12","17_memorandum","17_text","donald_j","russian_ambassador","acting_attorney","trump_moscow","hicks_3","senate_select","pleaded_guilty","select_intelligence","james_b","next_day","2016_presidential","intelligence_committee","cohen_11","jared_kushner","2016_meeting","corney_11","hicks_12","michael_flynn","volume_ii","president_also","8_302","june_2016","policy_advisor","former_director","gru_officers","cohen_recalled","page_3","hunt_5","george_papadopoulos","incoming_administration","115th_cong","counsel_removed","security_advisor","15th_cong","see_volume","porter_4","judiciary_committee","president_called","kushner_4","july_2016","senate_judiciary","christie_2","netyksho_indictment","15_email","call_records","papadopoulos_8","lewandowski_4","manafort_9","october_7","government_officials","priebus_1","see_united","official_proceeding","article_ii","clinton_emails","bannon_2","obstructive_act","plea_agreement","obstruction_statutes","russian_officials","press_conference","17_email","anyone_else","russian_interference","carter_page","flynn_statement","vice_president","16_facebook","president_tweeted","fox_news","vladimir_putin","email_accounts","flynn_1","deputy_attorney","house_counsel","nader_1","quotation_marks","jeff_sessions","december_2016","april_2016","june_14","cohen_said","president_knew","emin_agalarov","written_responses","papadopoulos_statement"],"freq":[229,220,215,204,197,175,150,145,141,134,131,128,117,100,100,90,83,82,81,81,79,76,74,72,72,70,69,69,68,68,67,64,63,63,61,60,59,59,58,58,56,55,55,54,54,53,53,53,52,52,51,50,50,50,49,47,47,47,46,46,45,44,42,42,42,41,41,40,39,39,38,36,36,36,35,35,34,34,33,33,33,32,32,32,32,32,32,31,31,30,30,30,30,29,29,29,29,28,28,28,27,27,27,27,27,27,27,27,27,26,26,26,26,26,26,25,25,25,25,25,24,24,24,24,23,23,23,23,23,23,22,22,22,22,22,22,22,22,21,21,21,21,21,21,21,21,21],"fontFamily":"Segoe UI","fontWeight":"bold","color":"random-dark","minSize":0,"weightFactor":0.314410480349345,"backgroundColor":"white","gridSize":0,"minRotation":-0.785398163397448,"maxRotation":0.785398163397448,"shuffle":true,"rotateRatio":0.4,"shape":"circle","ellipticity":0.65,"figBase64":null,"hover":null},"evals":[],"jsHooks":{"render":[{"code":"function(el,x){\n                        console.log(123);\n                        if(!iii){\n                          window.location.reload();\n                          iii = False;\n\n                        }\n  }","data":null}]}}</script><!--/html_preserve-->



## pdfpages: A little plot

I found some instructions on constructing the entire document on a grid and pulled the report apart to visualise it in that way.



![A Graphic]("../../all_pages.png")
