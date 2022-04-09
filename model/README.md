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

Our feature engineering process is based on the match dataframe consisted in two steps: 

* **Creating the target variable:** this feature has 3 categories: local, away or draw. For this, we computed the difference between the local and away team goals by match. If this difference is possitive we assign "local" to the target variable, if it is negative we assign "away" and if the difference is zero we assign "draw". This was done using the following function: 

* **Computing the accumulated goals by team:** we sorted matches by date for each season and calculated the accumulated number of goals until the previous match. These goals are separated by: scored, received and the difference between them. It is important to notice that we don't consider the goals of that game to compute the sum to prevent data leakage, since the difference of goals is used to calculate the target variable.

We created this pair of functions: 

```python
def sumaGoles(golesEquipo, totalPartidos):
    favor = 0
    contra = 0
    diferencia = 0
    for i in range(totalPartidos):
        #print("sumando el partido "+str(i))
        favor+=golesEquipo[i][0]
        contra+=golesEquipo[i][1]
        diferencia+=golesEquipo[i][2]
    return [favor, contra, diferencia]
```

```python
def FeatureEngineer(anio,partialRes):
    equipos = {} # para contar los partidos jugados por equipo
    totalGoals = {} # primero a favor, luego en contra, luego diferencia
    for res in partialRes:
        if(res[1]==anio and res[5] != None): # != None validdation required for non played matches
            #datos de equipos
            local = res[3]
            visita = res[4]

            #datos de goles
            goles_local = res[5]
            goles_visita = res[6]

            if(not (local in equipos)):
                equipos[local] = 0

            if(not (visita in equipos)):
                equipos[visita] = 0

            #logica para guardar los goles por equipo y el acumulado
            if(local in totalGoals):
                totalGoals[local].append([goles_local,goles_visita, goles_local-goles_visita])
            else:
                totalGoals[local] = [[goles_local,goles_visita, goles_local-goles_visita]]

            if(visita in totalGoals):
                totalGoals[visita].append([goles_visita, goles_local, goles_visita-goles_local])
            else:
                totalGoals[visita] = [[goles_visita, goles_local, goles_visita-goles_local]]


    featureEng = []

    for partido in partialRes:
        if (partido[1]==anio and partido[5] != None): # != None validdation required for non played matches
            #print(partido)
            local = partido[3]
            visita = partido[4]
            goles_acumulados_local = sumaGoles(totalGoals[local], equipos[local])
            goles_acumulados_visita = sumaGoles(totalGoals[visita], equipos[visita])
            
            #ahora se define si gana el local, el visita o empate
            resPredictor = 'empate'
            if(partido[5]>partido[6]):
                resPredictor = 'local'
            else:
                if(partido[5]<partido[6]):
                    resPredictor = 'visita'
            
            featureEng.append([partido[1],
                        local,
                        goles_acumulados_local[0],
                        goles_acumulados_local[1],
                        goles_acumulados_local[2],
                        equipos[local],#partidos jugados hasta el momento              
                        visita,
                        goles_acumulados_visita[0],
                        goles_acumulados_visita[1],
                        goles_acumulados_visita[2],
                        equipos[visita],#partidos jugados hasta el momento  
                        resPredictor]
                             )
            equipos[local] = equipos[local]+1
            equipos[visita] = equipos[visita]+1


    return featureEng
```

### Algorithm

### Experiments

### ML metrics

### Trade-offs
