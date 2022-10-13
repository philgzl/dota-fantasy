# dota-fantasy
Fantasy predictions using Monte Carlo simulations for The International 2022, factoring in ELO ratings and card bonuses. 

# Method

## Data
Fantasy data from the following leagues was collected from [Opendota](https://www.opendota.com/):
```
PGL Arlington Major 2022
Riyadh Masters by Gamers8
DPC CN Division I Summer Tour - 2021/2022 presented by Perfect World Esports
ESL One Malaysia 2022 powered by Intel
ESL One Malaysia 2022 Qualifiers powered by Intel
DPC WEU Division I Summer Tour - 2021/2022 - DreamLeague Season 18 presented by Intel
DPC SA Division I  Summer Tour \u2013 2021/2022 by 4D Esports
DPC NA Division I Summer Tour - 2021/2022 - ESL One Summer presented by Intel
DPC SEA Division I Tour 3 - 2021/2022 by Beyond The Summit
NA TI 11 Regional Qualifiers
EEU TI 11 Regional Qualifiers
SA TI 11 Regional Qualifiers
CN TI 11 Regional Qualifiers
SEA TI 11 Regional Qualifiers
WEU TI 11 Regional Qualifiers
The International 2022 Last Chance Qualifiers
```
All leagues were equally weighted. An argument could be made in favor of using the fewer most recent leagues. However I believe the model requires a sufficient amount of data to perform well.

## Model
For each player, each fantasy statistic (`fantasy_points`, `kills`, `deaths`, `last_hits`, `gold_per_min`, `towers_killed`, `roshans_killed`, `teamfight_participation`, `observers_placed`, `camps_stacked`, `rune_pickups`, `firstblood_claimed`, `stuns`) was modelled as a Gaussian conditioned on the outcome of the game. The win and loss statistics (mean and standard deviation) were estimed using the data collected from the leagues listed above.

A stationary model was preferred over a dynamic model like a time series process as the data is quite noisy and no particular trend can be observed. Attempts at fitting ARMA models to the individual series resulted in poor results.

## Simulations
For each series, win and lose probabilities are calculated using ELO ratings as provided by [Opendota](https://www.opendota.com/teams). A biased coin flip is then used to determine the outcome of each game within a series.

The fantasy scores are then obtained by simply sampling from the Gaussians based on the outcome of the game. The outcome for each fantasy statistic is scaled according to the card bonus specified in `teams.json`.

For Bo3 and Bo5 series, only the top 2 and 3 games are counted respectively.

# Results

The following results were obtained from 10000 simulations. No card bonuses were applied.

(coming soon)
