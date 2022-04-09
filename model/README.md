### Data

Data is provided by [Api sports](https://api-sports.io/). The idea is to get relevant information about matches from the Premier League in order to predict the possible results of the competition. The requests to the API are done using an API Key and responses are return in a JSON format. As an example, hitting the fixtures endpoint we get back the following: 

```json
{
  "get":"fixtures"
    "parameters":{
    "league":"39"
    "season":"2020"
  }
  "errors":[]
    "results":380
    "paging":{
    "current":1
    "total":1
  }
  "response":
   [
     0:{
      "fixture":{...}
      "league":{...}
      "teams":{...}
      "goals":{...}
      "score":{...}
    }
     1:{
      "fixture":{...}
      "league":{...}
      "teams":{...}
      "goals":{...}
      "score":{...}
    }
    ...
   ]
}
```

### Dataframes

* **Seasons** 

This dataframe contains the results of the previous matches and are divided by season. From the API we can get information at least of the last 5 seasons. The shape of this dataframe looks like:

| id | season | match_date | local_team | away_team | local_goals | away_goals |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2019 | datetime.date(2019, 8, 9) | 'Liverpool' | 'Norwich' | 4 | 1 |
| 2 | 2019 | datetime.date(2019, 8, 10) | 'West Ham' | 'Manchester City' | 0 | 5 |
| 3 | 2019 | datetime.date(2019, 8, 10) | 'Bournemouth' | 'Sheffield Utd' | 1 | 1 |
| 4 | 2019 | datetime.date(2019, 8, 10) | 'Burnley' | 'Southampton' | 3 | 0 |
| 5 | 2019 | datetime.date(2019, 8, 10) | 'Crystal Palace' | 'Everton' | 0 | 0 |
| 6 | 2019 | datetime.date(2019, 8, 11) | 'Leicester' | 'Wolves' | 0 | 0 |
| 7 | 2019 | datetime.date(2019, 8, 10) | 'Watford' | 'Brighton' | 0 | 3 |
| 8 | 2019 | datetime.date(2019, 8, 10) | 'Tottenham' | 'Aston Villa' | 3 | 1 |
| 9 | 2019 | datetime.date(2019, 8, 11) | 'Newcastle' | 'Arsenal' | 0 | 1 |
| 10 | 2019 | datetime.date(2019, 8, 11) | 'Manchester United' | 'Chelsea' | 4 | 0 |
| ... | ... | ... | ... | ... | ... | ... |


* **Statistics**

This dataframe contains information about team players and their performance. On this dataframe, the information we have about players is: injuries, appareances, played minutes, assist and rating per player. These kind of statistics are relevant to infere the result of a soccer match. 

| id | season | player_id | player_name | age | injured | weight | appearences | minutes | position | rating | shots | goals | assist | total_duels | won_duels |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2019 | 160 | 'M. Vorm' | 38 | False | 47 | 0 | 0 | 'Goalkeeper' | None | 0 | None | None | None | None |
| 2 | 2019 | 642 | 'S. Agüero' | 33 | False | 50 | 24 | 1456 | 'Attacker' | 7.160869 | 16 | 3 | 79.0 | 114 | 43 |
| 3 | 2019 | 2795 | 'G. Sigurosson' | 33 | False | 45 | 35 | 2562 | 'Midfieder' | 6.854285 | 2 | 3 | 82.0 | 250 | 103 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |


Some other characteristics important about our data:
* It has a total of 20 teams per season. 
* Each season, the team with worst performance is replaced by a new one. 
* Some matches can be rescheduled.
* There are a total of 380 matches in each season.
* The number of players by season can be vary.


### Feature engineering

que hicimos 

tomamos solo la tabla de match, construimos la variable objetivo (local, visita, empata) lo que queremos predecir con el modelo.

transformar las variables iniciales, para cada equipo por partido añadimos el total de goles que anotó ese equipo hasta un partido anterior, también el total de goles que recibio hasta un partido anterior, y la diferencia entre estos dos valores. Es importante señalar que no incorporamos el numero de goles de ese partido en la prediccion para evitar data leakage. el numero de partidos previos jugados. 

como lo hicimos

para la variable resultado los valores posibles local, visita o empate se obtienen al restar los goles del local menos los de visitante, si esta diferencia es positiva se asigna "local", si es cero se asigna "empate" y si es negativa se asigna el valor "visitante". 

for accumulated data: ordenamos los partidos por fecha, para cada partido se añadieron los goles 

### Algorithm

### Experiments

### ML metrics

### Trade-offs
