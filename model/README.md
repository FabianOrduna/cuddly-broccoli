### Data

Data is provading for [Api sports](https://api-sports.io/). The idea is to get relevant information about matches from the Premier League in order to predict the possible results of the competition. The data is divided in two data sets with the following characteristics:

* **Seasons data frame:** 
This data frame contain the information about the results of the games in te previos matches and divided for season. Into the API we can get information at least of the last 5 season. The shape of this data frame is as follow:

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

* **Statistics data frame:**
This data frame is about a relevent information repect each team playes and his performance. On this data frame we have a relevant information like a player's injures, appareances, played minutes, assist and rating per player. This kind of statistics are relevant at the moment to decide the result in a one soccer march. 


| id | season | player_id | player_name | age | injured | weight | appearences | team_id | minutes | position | rating | shots | goals | assist | total_duels | won_duels |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2019 | 160 | 'M. Vorm' | 38 | False | 47 | 0 | 0 | 'Goalkeeper' | None | None | 0 | None | None | None | None |
| 2 | 2019 | 642 | 'S. Agüero' | 33 | False | 50 | 24 | 1456 | 'Attacker' | 7.160869 | 76 | 16 | 3 | 79.0 | 114 | 43 |
| 3 | 2019 | 2795 | 'G. Sigurosson' | 33 | False | 45 | 35 | 2562 | 'Midfieder' | 6.854285 | 46 | 2 | 3 | 82.0 | 250 | 103 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |


### Feature engineering

### Algorithm

### Experiments

### ML metrics

### Trade-offs
