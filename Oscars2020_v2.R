#install.packages(c("tidyverse","rtweet","quanteda","stringr", "RColorBrewer"))

#nstall.packages("tidytext")

library(tidyverse)
library(rtweet)
library(quanteda)
library(stringr)
library(RColorBrewer)
library(tidytext)


## set twitter api credentials
app_name <- "***"
consumer_key <- "***"
consumer_secret <- "***"

## create token
token <- create_token(app_name, consumer_key, consumer_secret)

## search for a keyword and fetch
tweets <- search_tweets(q = "oscars", n=15000,lang = "en") 

##create custom stopword list
custom_stopwords <- c(stopwords('en'),'n','u','0001f97a', '0001f1f0', '0001f44f', 'fe0f',
                      '0001f1f7','0001f3c6','202f','0001f60d','0001f62d','0001f1f3', '0001f1ec',
                      '0001f49b', '0001f49b', '0001f49b', '0001f3fb')

#tokenize tweets
tokens <- tweets %>%
  filter(is_retweet=="FALSE") %>% #exclude retweets
  select(text) %>% 
  as.character() %>%
  str_replace_all("[\r\t\n]"," ") %>% #clean tweets and tokenize 
  tokens(remove_numbers = T, #
         remove_punct=T, 
         remove_symbols=T, 
         remove_twitter=T,
         remove_url=T,
         remove_separators=T) %>% 
  tokens_tolower(keep_acronyms = F) %>% 
  tokens_select(pattern = custom_stopwords, selection = 'remove') #remove stopwords
  
##top words
tokens %>%
  dfm(min_termfreq = 0.95, termfreq_type = "quantile") %>% 
  topfeatures(100)

##further cleaning 
tokens <- tokens %>% 
  tokens_replace(pattern = c('noscars','wonawards','joon','ntrump','njoaquin', 'njulia', 'historymaking',
                             'nthe', 'nbrad','parasitebestpicture',
                             'theacademy'),
                 replacement = c('oscars','won','joon-ho', 'trump', 'joaquin', 'julia', 'history', 
                    'the', 'brad','parasite','academyawards'))


##network plot
set.seed(2020)
tokens %>% 
  dfm() %>% 
  dfm_trim(min_termfreq = 15) %>% 
  textplot_network(edge_alpha = .2,
                   edge_size = 1,
                   edge_color='#7BBAD9')

##top n-grams
n = 2
tokens %>% 
  textstat_collocations(size = n) %>% 
  arrange(desc(count)) %>% 
  head(50)


