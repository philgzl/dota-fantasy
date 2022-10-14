# dota-fantasy
Fantasy predictions using Monte Carlo simulations for The International 2022, factoring in ELO ratings and card bonuses. 

## Method

### Data
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

### Model
For each player, each fantasy statistic (`fantasy_points`, `kills`, `deaths`, `last_hits`, `gold_per_min`, `towers_killed`, `roshans_killed`, `teamfight_participation`, `observers_placed`, `camps_stacked`, `rune_pickups`, `firstblood_claimed`, `stuns`) was modeled as a Gaussian conditioned on the outcome of the game. The win and loss statistics (mean and standard deviation) were estimated using the data collected from the leagues listed above.

A stationary model was preferred over a dynamic model like a time series process as the data is quite noisy and no particular trend can be observed. Attempts at fitting ARMA models to the individual series resulted in poor results.

### Simulations
For each series, win and lose probabilities are calculated using ELO ratings as provided by [Opendota](https://www.opendota.com/teams). A biased coin flip is then used to determine the outcome of each game within a series.

The fantasy scores are then obtained by simply sampling from the Gaussians based on the outcome of the game. The outcome for each fantasy statistic is scaled according to the card bonus specified in `teams.json`.

For Bo3 and Bo5 series, only the top 2 and 3 games are counted respectively. If a team plays more than one series on the same day, only the highest scoring series is counted.

## Results

Below are some results obtained from 10000 simulations. No card bonuses were applied. Only the top picks for each day are displayed. The complete results for all players are available in the `results` directory.

### October 15

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
bzm           OG                     Mid      38.61   3.76    32.54   44.99   23.31   54.67  
Yopaj-        BOOM Esports           Mid      38.28   3.92    32.23   45.06   25.31   56.96  
Somnus        Royal Never Give Up    Mid      38.16   3.58    32.49   44.28   25.78   51.82  
Nisha         Team Secret            Mid      37.63   4.94    29.79   45.91   20.09   56.25  
Stormstormer  Entity                 Mid      37.38   4.24    30.71   44.59   20.93   56.61  
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Ame           PSG.LGD                Core     37.00   3.68    31.04   43.12   24.23   53.00  
Yuragi        OG                     Core     36.99   4.35    29.96   44.22   22.02   53.24  
Lumière       Hokori                 Core     36.44   5.72    27.14   45.83   19.35   57.61  
Monet         Team Aster             Core     35.60   4.46    28.39   42.97   18.17   53.02  
MATUMBAMAN    Team Liquid            Core     35.37   3.52    29.82   41.35   24.23   49.20  
Daxak         BetBoom Team           Core     35.04   3.85    28.86   41.63   21.74   48.97  
Pure          Entity                 Core     34.68   6.15    24.36   44.55   15.77   54.47  
dyrachyo      Gaimin Gladiators      Core     34.56   4.88    27.07   43.31   21.51   54.64  
JACKBOYS      BOOM Esports           Core     34.46   4.39    27.44   41.88   20.50   50.82  
YATOROGOD     Team Spirit            Core     34.26   4.70    26.71   42.12   18.44   51.66  
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Fata          Soniqs                 Support  36.61   3.97    30.71   43.67   24.02   51.94  
W_Zayac       Team Secret            Support  35.32   4.08    28.77   42.25   20.71   53.06  
skem          BOOM Esports           Support  34.26   3.41    28.99   40.17   22.99   49.90  
iNsania       Team Liquid            Support  33.87   3.15    28.89   39.25   24.31   47.27  
Taiga         OG                     Support  33.65   4.01    27.51   40.65   18.42   52.58  
SoNNeikO      BetBoom Team           Support  32.76   3.51    27.23   38.84   22.51   47.76  
Hyde-         Talon                  Support  32.30   4.86    24.51   40.54   17.80   50.67  
y`            PSG.LGD                Support  31.92   2.95    27.23   37.05   20.84   44.31  
Fishman       Entity                 Support  31.90   4.24    25.21   39.22   19.23   49.24  
Jaunuel       Fnatic                 Support  31.70   4.23    25.11   39.05   18.37   51.75  
...
```

### October 16

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Nisha         Team Secret            Mid      39.94   4.44    32.91   47.39   25.24   57.35  
Stormstormer  Entity                 Mid      39.73   3.79    33.82   46.29   27.26   55.61  
Somnus        Royal Never Give Up    Mid      38.14   3.79    31.99   44.43   23.13   53.09  
Yopaj-        BOOM Esports           Mid      37.84   4.13    31.33   44.91   24.41   54.31  
bzm           OG                     Mid      35.87   4.35    29.03   43.26   21.66   54.62  
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Pure          Entity                 Core     38.72   4.72    30.44   46.03   19.98   55.62  
YATOROGOD     Team Spirit            Core     36.76   4.04    30.05   43.35   21.77   52.93  
Monet         Team Aster             Core     36.12   4.21    29.37   43.33   22.68   51.02  
Crystallis    Team Secret            Core     35.17   4.46    28.02   42.52   19.65   54.76  
23savage      Talon                  Core     34.82   5.69    25.67   44.46   18.40   55.05  
Ghost         Royal Never Give Up    Core     34.28   4.73    26.47   42.01   18.69   52.44  
JACKBOYS      BOOM Esports           Core     34.17   4.68    26.55   41.96   20.10   51.61  
Daxak         BetBoom Team           Core     33.87   4.18    27.04   40.93   18.62   51.86  
Pakazs        Thunder Awaken         Core     33.87   4.54    26.81   41.73   20.28   52.04  
Ame           PSG.LGD                Core     33.70   4.68    26.03   41.33   16.83   50.33  
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
W_Zayac       Team Secret            Support  37.04   3.60    31.44   43.32   24.91   52.48  
Fata          Soniqs                 Support  34.82   4.09    28.70   42.21   22.07   52.54  
Hyde-         Talon                  Support  34.38   4.47    27.20   41.98   19.83   51.82  
Fishman       Entity                 Support  34.26   3.83    28.22   40.75   22.42   50.45  
skem          BOOM Esports           Support  33.34   3.79    27.38   39.77   21.53   51.09  
Jaunuel       Fnatic                 Support  33.05   3.87    27.02   39.78   21.70   51.72  
iNsania       Team Liquid            Support  32.45   3.53    26.83   38.40   20.12   47.46  
Miposhka      Team Spirit            Support  32.41   3.58    26.81   38.54   20.47   50.18  
SoNNeikO      BetBoom Team           Support  31.72   3.82    25.60   38.16   18.34   46.69  
DJ            Fnatic                 Support  31.58   3.22    26.61   37.30   20.99   46.62  
...
```

### October 17

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Somnus        Royal Never Give Up    Mid      38.41   3.61    32.64   44.55   26.89   54.31  
Stormstormer  Entity                 Mid      38.36   4.23    31.52   45.52   22.89   54.81  
Yopaj-        BOOM Esports           Mid      38.17   3.85    32.18   44.67   24.41   57.61  
bzm           OG                     Mid      38.13   3.84    32.04   44.71   25.65   52.43  
Quinn         Soniqs                 Mid      36.86   4.86    29.23   45.25   23.19   56.56  
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Ame           PSG.LGD                Core     36.74   3.82    30.48   43.10   22.95   52.29  
Pure          Entity                 Core     36.70   5.67    27.18   45.59   14.06   55.47  
Yuragi        OG                     Core     36.23   4.56    28.90   43.95   21.20   55.40  
Monet         Team Aster             Core     35.62   4.48    28.36   43.11   21.35   54.16  
MATUMBAMAN    Team Liquid            Core     35.58   3.52    30.00   41.63   23.40   50.07  
Arteezy       Evil Geniuses          Core     34.94   4.08    28.53   41.84   21.79   51.08  
YATOROGOD     Team Spirit            Core     34.93   4.61    27.39   42.42   18.60   55.60  
Lumière       Hokori                 Core     34.80   5.68    25.79   44.74   18.27   57.63  
Daxak         BetBoom Team           Core     34.65   3.90    28.45   41.36   21.51   52.83  
Ghost         Royal Never Give Up    Core     34.35   4.49    27.07   41.81   18.31   51.23  
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Fata          Soniqs                 Support  37.45   4.01    31.33   44.48   26.34   54.79  
skem          BOOM Esports           Support  34.21   3.40    28.95   40.17   23.92   48.20  
iNsania       Team Liquid            Support  34.01   3.20    28.95   39.45   23.66   50.22  
W_Zayac       Team Secret            Support  34.00   3.97    27.82   40.71   20.01   54.76  
Taiga         OG                     Support  33.28   4.08    26.90   40.28   20.74   51.53  
Hyde-         Talon                  Support  33.06   4.87    25.26   41.27   17.95   52.33  
Fishman       Entity                 Support  32.74   4.22    26.05   39.97   19.27   54.34  
SoNNeikO      BetBoom Team           Support  32.46   3.52    26.90   38.59   20.71   49.20  
Jaunuel       Fnatic                 Support  31.95   4.17    25.37   39.03   18.25   49.26  
y`            PSG.LGD                Support  31.76   2.98    27.01   36.73   20.37   43.99  
...
```

### October 18

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Stormstormer  Entity                 Mid      38.72   4.08    32.16   45.62   23.69   56.13  
Nisha         Team Secret            Mid      37.06   4.96    29.10   45.30   19.84   56.94  
Yopaj-        BOOM Esports           Mid      34.79   4.96    26.74   43.04   18.21   52.04  
Quinn         Soniqs                 Mid      34.21   6.02    24.40   44.24   18.37   60.07  
DarkMago♥     Thunder Awaken         Mid      33.52   3.92    27.33   40.22   20.71   48.00  
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Pure          Entity                 Core     37.50   5.28    28.41   45.62   17.44   56.13  
YATOROGOD     Team Spirit            Core     33.87   4.81    26.00   41.82   17.30   50.79  
Raven         Fnatic                 Core     33.85   5.43    25.02   42.97   17.74   53.91  
Monet         Team Aster             Core     33.67   4.74    26.25   41.65   19.73   55.33  
Pakazs        Thunder Awaken         Core     33.47   4.91    25.63   41.92   18.62   51.94  
MATUMBAMAN    Team Liquid            Core     32.45   4.54    24.98   39.99   15.16   49.17  
Crystallis    Team Secret            Core     32.07   5.18    23.68   40.75   16.47   51.28  
Ame           PSG.LGD                Core     31.15   5.62    21.78   40.15   11.06   49.53  
dyrachyo      Gaimin Gladiators      Core     30.81   5.97    21.75   41.28   15.48   56.01  
JACKBOYS      BOOM Esports           Core     30.69   5.59    21.67   40.06   13.22   49.76  
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
W_Zayac       Team Secret            Support  35.06   4.02    28.76   41.91   22.84   52.69  
Fata          Soniqs                 Support  34.58   5.02    26.75   43.18   17.29   57.36  
Fishman       Entity                 Support  33.16   4.17    26.53   40.28   18.10   49.51  
Jaunuel       Fnatic                 Support  32.72   4.19    26.06   39.78   19.11   47.27  
Hyde-         Talon                  Support  31.76   4.88    23.96   40.05   16.10   51.56  
DJ            Fnatic                 Support  31.31   3.54    25.71   37.33   20.25   46.88  
skem          BOOM Esports           Support  30.85   4.47    23.69   38.39   15.87   48.01  
iNsania       Team Liquid            Support  30.84   4.21    23.99   37.80   13.72   46.88  
Miposhka      Team Spirit            Support  30.55   3.91    24.31   37.20   16.83   48.10  
Matthew       Thunder Awaken         Support  30.27   3.39    24.89   35.97   18.78   44.47  
...
```
