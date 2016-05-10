# Twitter application <br />
Developed as a project for the course "Information Retrieval" part of for the Msc in Computer Science<br />
The application is implemented to crawl and analyze data(tweets) from the <br />
Greek Political scene, based on an account which follows members of the Greek Parliament.<br />
Analyzing includes standar Information Retrieval tasks and checks(word frequency etc.)<br />
Statistics based on mentions, hashtags, urls given.<br />
We also performed clustering based on tf*idf features of the texts.<br />
Finally we ran PageRank on the graph produced by our twitter network to note the <br />
"biggest" twitter players in the Greek political scene.<br />
All the data was loaded into an elasticsearch cluster to be used by a web application.<br />
<br />