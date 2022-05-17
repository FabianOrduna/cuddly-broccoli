# Easy money betting soccer

## Team members

| Name  | Email | Clave única | Github handler | Website
| :-------------: | :-------------: | :-------------: | :-------------: | :-------------:
| Fabián Orduña Ferreira  | fabian.orduna@itam.mx  | 159001  | FabianOrduna |
| Nelson Gil Vargas  | ngilvarg@itam.mx  | 203058  | nelsonalejandrov | [Nelson Portfolio](https://nelsonalejandrov.github.io/Nelson_Portfolio/)
| Jorge Garcia  | jgarc401@itam.mx  | 202945  | jgarciad |
| Miguel Lerdo de Tejada  | miguel.lerdodetejada@itam.mx  | 168450  | MikeLdT |


### Hi there 👋

Why are we awesome?

-	🔭 Because Nelson is a geophysicist (no, earthquakes can’t be predicted), leftie and gamer.
-	📫 Because Miguel is an economist/actuarial scientist and will judge you based on your p-values. 
-	⚡ Because Jorge enjoys writting code and thinks that the cloud rocks. 
- 🖥️ Because Fabian is a software engineer with experience in web development, distributed systems and can hack your phone if he wants.

Together we can learn about each other, and we can solve many kinds of problems merging our skills as one brain to conquer Data Product Architecture.

# Project Proposal 

### 1. Objectives

1. What is the problem that your Data Product will solve? 

According to [topendsports](https://www.topendsports.com/world/lists/popular-sport/fans.htm) football is the most popular sport globally approximately 3.5 billion fans followed by cricket with 2.5 billion fans. Many of these fans like to be aware of the odds for future games of their teams, specially with upcoming fooball classics like FC Barcelona vs Real Madrid, Manchester United vs Liverpool or America vs Chivas in the mexican league. Another proportion of these followers are looking for betting tips. This data product intends to predict football match results (win, loss or tie), this prediction could be used for informative means or as betting tips. 

2. If a company was to use this application, what would be their ML objectives and business objectives? 

The ML objectives is to reduce the false positive rate over the output predictions. By false positive we mean the model predicts a team will win a match when in reality the opposite happens.

The company's business objective would be to provide an additional set of tools to help gamblers in decision making process. But also, this can be used by different betting houses to improve their business income.

### 2. Users

1. Who will be the users of your application?

Football fans looking for predictions about football game results and betting houses.

2. How are users going to interact with your application? 

Match results will be displayed, in a website, with tables containing the opponents in the game and the probability of a win, loss or tie. We will display some comboboxes with basic parameters like league, team, date, etc and then it will provide the user with win, draw or lose probabilities for the next match. Also, it will display recent statistics of both the home and away teams (since football is usually about streaks). The idea is to provide to the client with the best tools to bet. 


### 3. Data Product Architecture Diagram

<img width="520" alt="Picture1" src="https://user-images.githubusercontent.com/48302106/168720848-22cc1c9a-ad69-493d-906c-b4797dbc4b07.png">



### 4. Data

1. Where would you get your data from? How much data would you need? Is there anything publicily available or do you need to build your own dataset? 

The data for our project will be extracted from the [API-FOOTBALL](https://www.api-football.com/documentation-v3), a free API containing Timezones, Countries, Leagues, Teams, Venues, Standings, Fixtures, Injuries, Predictions, Coachs, Players, Transfers, Trophies, Sidelined and Odds.

The football API will be complemented with player scores that will be obtained from the [FIFA API](https://futdb.app/api/doc). The FIFA team database will give us information about the ranking of team players. This will allow us to make comparisons between goalkeeprs, center, strickers of the local and visitor teams. One model will be trained considering these rankings and another won't to see if this information is relevant for the final model. 
 
### 5. Modeling


**Model**:. 

The objective of the model is simple, we want to determine the probability of three possible results. How can you determine this result? We only need to predict the goals of each team.

We will also consider:

1. Home or away condition
2. Attack and defence scores
3. Budget

We will use the FIFA API as proxy of a team's overall skills. 

We will follow [this repo](https://dashee87.github.io/football/python/predicting-football-results-with-statistical-modelling-dixon-coles-and-time-weighting/) of Mark j. Dixon and Stuart G. Coles  but with a variant on the parameter because we want to use a FIFA API instead of  maximum likelihood estimator.

We want to explore different algorithms like neural networks, logistic regression and so on to get the best prediction based on several available variables  (recent matches, venue, expected goals, etc).


**Software**: 

Python to train the models and PHP to display the front-end application. Postgres as data base management system. The idea is use Postgres to conserve results of the prediction model to compare and implement improvements over the last production model. On the other hand, with Postgres we store the data to train a model and the statistic of the requested matches. 

**User interface**: 

Our interface will be user-friendly. we will display some comboboxes with basic parameters like league, team, date, etc and then it will provide the user with win, draw or lose probabilities for the next match. Also, it will also display recent statistics of both the home and away teams (since football is usually about streaks). The idea is to provide to the client with the best tools to bet. 

**Scope**: Premier League matches. 


### 6. Evaluation

1. How would you evaluate your model performance, both during training and
inference?

We will evaluate if the percentage of false positives is strictly smaller than a threshold defined by the client. In this case, we understand a false positive as a situation where the model predicts a team will win a match when in reality the opposite happens. We believe false positives are what the client is ultimately interested in minimizing, whereas alternative measures like accuracy might be misleading.


2. How would you evaluate whether your application satisfies its objectives?

We would compare our performance against that of profesional betting houses. From the Football API we can retrieve betting odds from several webpages. If we can manage to get data of the results of professional gamblers, we might compare against them as well.


### 7. Inference

1. Will you be doing online prediction or batch prediction or a combination of both?

We intend to do batch prediction. Our beta product will need weekly data, so we don't need to orchestratre a very sophisticated online prediction.
However we might do online prediction if we can manage to, as to provide pre-match and through-match prediction.


2. Will the inference run on-device or through a server?

On-device 

3. Can you run inference on CPUs or an edge device or do you need GPUs?

We will only need CPUs.

### 8. Compute

1. How much compute do you need to develop this application as a market-ready
product?

In order to develop this application we require to use different tools. On this case we are using a Compute Engine for AI so we could have a space with pre installed libraries and ready to use for this purpose. We also need Cloud Storage service for the data retrieved from the API so we could be able to store the information. The use of databases is required so we could retrieve information and query information from there in the future. For the machine learning model we could use the Auto ML Google Service but also a script to perform this. We need to use an orchestrator and a hosting space to place a dashboard to be used by the customer.

2. To train your model (if you train your own model): do you need GPUs/TPUs or just CPUs? How many machines? For how long?

Since the amount of data for this project is not that much we could perform all the operations with only CPUs in a single machine and for training the models we estimate the time needed is gonna be at most 24 hours but that depends, at the end, in the amount of algorithms we compare and the different configurations. 

   a. To serve your model: can your models make predictions on CPUs?

   At the end, when models are ready and based on the amount of data the predictions can be done with CPUs.

   b. How much compute do you need to develop this application for this project?

   As mentioned above we need different tools from GCP and apart from that clarify that use of single CPU with an Intel processor is enough.

### 9. MVP

As an MVP we want to have all the pipeline since the API data retrieval, data transformation, data storage, the model training, etc. and a dashboard to the end user to make predictions in an easy and quick way

### 10. Pre-mortems

1. What are the risky aspects of the project? i. e.g. not enough data, limited compute resources, not knowing how to implement an interface, network latency, inference latency, etc.

 We consider there are many different risky aspects for this project:

  Model related:
  - Amount of data.
  - Data quality.
  - Importance of variables to build a functional model.
  - Availability of data like match coverage.
  - Model quality and performance. Overfiting vs underfiting vs dummy classifier.
  - Non-infomative model. Select a bad threshold.

   Infraestructure related:
   - Availability of GCP tools.
   - Data availability of APIs

In this case, if we have a low-performance model we will be in serious problems. Our potential clients might prefer to trust their guts rather than buy our data product. 
It is important to mention that we have the best available data, but if we want to scale up our product we will need to invest more in the API (or do tedious webscrapping).

2. If your team fails to build the application you want, what do you think might have caused the failure?

    Based on the knowledge we have about the context of the project we consider the only way we could fail to build the application is related to things we cannot control as data availabilit, infraestrucute problems, data availability/quality. But also a failure can be related with the way we build/train/evaluate the model so we won't be innovating and we would have a low predictive power/model.

3. What are the limitations of your application?

   It's going to work only with the Premier League, it won't consider unexpected events like important players transfered to other teams, team players injuries, etc. It does not use the current competition information to predict, but could be incoporated as an enhancement for a real-time model.

3. What are the potential biases of your application?

   During a campaign there are several teams that are consider as potential winners like Manchester City, Chelsea, Manchester United so we could never think about a team like Leicester City could be a winner so the model won't be able to predict accurately results involving new teams in the league. If we use the team income as a variable it could include potential biases to the model. The model does not consider the lineup for every match so if a really important player does not play would have the same score as if he plays.
   
### ML Model

Magic is not in our dictionary but machine learning is. This technique is used to infer some event in this case a soccer game results. You can find the requiere steps to achive this goal in this section. We explain how to use the data, how to process it, the way to train the models to find the best. It will allow us to dicover improvement areas to do better predictions. 

### References: 

* [Base gitignore file.](https://github.com/github/gitignore/blob/main/Python.gitignore)
