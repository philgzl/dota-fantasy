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

For Bo3 and Bo5 series, only the top 2 and 3 games are counted respectively.

## Results

Below are some results obtained from 10000 simulations. No card bonuses were applied. Only the top picks for each day are displayed. The complete results for all players are available in the `results` directory.

### October 15

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
bzm           OG                     Mid      102.95  8.61    88.80   116.92  71.05   134.01 
Somnus        Royal Never Give Up    Mid      102.30  8.28    88.69   116.14  71.19   132.26 
Yopaj-        BOOM Esports           Mid      102.02  8.39    88.42   116.07  73.04   132.34 
Larl          BetBoom Team           Mid      92.94   9.83    76.92   109.21  55.44   132.10 
m1CKe         Team Liquid            Mid      92.46   7.51    80.19   104.79  66.51   127.72 
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Ame           PSG.LGD                Core     97.74   9.08    82.69   112.47  61.23   130.11 
Yuragi        OG                     Core     95.66   10.32   78.90   112.64  58.09   130.11 
MATUMBAMAN    Team Liquid            Core     94.36   7.90    81.56   107.43  66.83   122.48 
Daxak         BetBoom Team           Core     91.56   8.63    77.62   106.05  62.81   125.28 
Lumière       Hokori                 Core     89.50   11.39   71.28   108.73  54.98   134.83 
JACKBOYS      BOOM Esports           Core     88.79   9.30    73.76   104.58  55.84   124.43 
dyrachyo      Gaimin Gladiators      Core     88.32   9.41    73.59   104.50  60.90   130.13 
Arteezy       Evil Geniuses          Core     87.43   8.25    74.29   101.38  60.39   118.67 
Ghost         Royal Never Give Up    Core     86.40   10.12   70.23   103.49  53.42   133.39 
Faith_bian    PSG.LGD                Core     81.42   7.11    69.61   93.06   57.02   108.08 
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Fata          Soniqs                 Support  97.72   8.05    84.94   111.18  69.27   130.26 
skem          BOOM Esports           Support  91.75   7.60    79.47   104.30  65.57   119.35 
iNsania       Team Liquid            Support  90.96   7.27    79.16   103.02  60.13   117.17 
Taiga         OG                     Support  87.56   8.96    73.11   102.25  51.76   119.38 
SoNNeikO      BetBoom Team           Support  86.12   7.87    73.20   99.23   57.63   115.71 
y`            PSG.LGD                Support  85.49   7.03    73.88   96.95   58.12   111.36 
TIMS          BOOM Esports           Support  82.84   7.37    70.87   94.97   56.40   112.72 
Gard1ck       Hokori                 Support  81.30   7.44    69.30   93.64   56.02   108.89 
Boxi          Team Liquid            Support  79.45   6.74    68.38   90.53   55.30   106.15 
RodjER        BetBoom Team           Support  77.90   7.88    65.25   91.00   52.80   107.64 
...
```

### October 16

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Stormstormer  Entity                 Mid      106.59  8.49    92.80   120.54  72.13   139.90 
Nisha         Team Secret            Mid      105.04  10.00   88.65   121.63  66.73   143.74 
TORONTOTOKYO  Team Spirit            Mid      94.53   7.68    81.77   107.14  64.77   122.70 
Ori           Team Aster             Mid      91.42   8.85    77.17   106.25  57.96   125.56 
C. smile  <   beastcoast             Mid      90.77   8.58    76.88   105.11  59.79   124.63 
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Pure          Entity                 Core     97.90   12.04   78.08   117.79  50.76   136.74 
YATOROGOD     Team Spirit            Core     95.98   9.60    80.29   111.78  64.49   130.64 
Monet         Team Aster             Core     93.92   9.51    78.64   109.90  62.53   128.88 
Crystallis    Team Secret            Core     90.22   10.18   73.62   107.26  57.64   134.58 
Pakazs        Thunder Awaken         Core     87.00   9.26    72.12   102.67  57.66   125.03 
23savage      Talon                  Core     84.82   11.80   66.31   104.82  47.16   128.63 
Raven         Fnatic                 Core     84.54   10.35   68.26   102.52  54.52   135.61 
K1            beastcoast             Core     82.94   9.56    67.20   98.63   52.33   117.66 
Resolut1on    Team Secret            Core     82.64   9.22    67.65   98.30   48.74   120.35 
CoLLapse      Team Spirit            Core     81.14   7.45    69.09   93.57   49.84   111.02 
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
W_Zayac       Team Secret            Support  98.99   8.24    85.48   112.71  71.76   130.60 
Fishman       Entity                 Support  89.80   8.53    75.97   104.07  53.09   125.77 
Hyde-         Talon                  Support  87.69   9.89    71.54   104.13  47.21   133.16 
Jaunuel       Fnatic                 Support  86.52   8.52    72.64   100.88  52.07   125.96 
Miposhka      Team Spirit            Support  85.19   8.13    71.90   98.60   56.02   115.69 
DJ            Fnatic                 Support  84.19   6.89    73.15   95.72   61.78   112.20 
Siamese.C     Team Aster             Support  83.39   6.72    72.60   94.62   57.99   107.62 
Matthew       Thunder Awaken         Support  82.55   6.93    71.41   93.90   57.10   109.32 
Saksa         Tundra Esports         Support  80.63   6.05    70.83   90.70   58.95   106.27 
DuBu          TSM FTX                Support  80.17   6.60    69.51   91.35   57.95   104.52 
...
```

### October 17

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Somnus        Royal Never Give Up    Mid      102.45  8.07    89.28   115.75  72.29   131.94 
Yopaj-        BOOM Esports           Mid      101.61  8.34    88.09   115.48  74.19   137.71 
bzm           OG                     Mid      101.08  8.81    86.86   115.40  68.30   134.54 
Quinn         Soniqs                 Mid      94.92   10.18   78.73   112.35  64.44   139.32 
m1CKe         Team Liquid            Mid      93.13   7.41    81.20   105.37  63.90   120.63 
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Ame           PSG.LGD                Core     96.21   9.30    80.77   111.31  62.59   129.67 
MATUMBAMAN    Team Liquid            Core     94.73   7.84    81.98   107.80  64.56   129.47 
Yuragi        OG                     Core     92.89   10.58   75.44   110.61  55.29   130.50 
Arteezy       Evil Geniuses          Core     91.25   8.63    77.25   105.50  58.95   126.43 
Daxak         BetBoom Team           Core     90.46   8.63    76.28   104.63  60.83   126.48 
JACKBOYS      BOOM Esports           Core     87.80   9.33    73.04   103.57  60.04   126.42 
dyrachyo      Gaimin Gladiators      Core     86.97   9.25    72.52   102.90  57.43   125.64 
Ghost         Royal Never Give Up    Core     86.70   9.77    71.03   102.87  52.78   128.64 
Lumière       Hokori                 Core     85.99   11.24   68.34   105.20  54.06   134.75 
Yawar         Soniqs                 Core     80.99   10.64   64.21   99.12   50.04   122.50 
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Fata          Soniqs                 Support  99.87   8.31    86.56   113.83  69.38   134.69 
iNsania       Team Liquid            Support  91.33   7.31    79.28   103.34  62.57   117.39 
skem          BOOM Esports           Support  91.32   7.59    79.07   104.06  63.26   123.37 
Taiga         OG                     Support  86.17   8.90    71.94   101.18  56.55   121.56 
SoNNeikO      BetBoom Team           Support  85.11   7.87    72.33   98.05   57.72   116.24 
y`            PSG.LGD                Support  84.89   7.23    72.65   96.60   56.81   113.21 
TIMS          BOOM Esports           Support  82.42   7.41    70.67   94.72   55.06   117.13 
Gard1ck       Hokori                 Support  79.83   7.43    67.85   92.41   53.25   107.15 
Boxi          Team Liquid            Support  79.61   6.73    68.66   90.79   53.70   105.06 
kaka          Royal Never Give Up    Support  77.96   6.72    67.16   89.19   54.67   106.17 
...
```

### October 18

#### Mid
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Stormstormer  Entity                 Mid      72.07   6.89    60.79   83.44   46.74   100.79 
Nisha         Team Secret            Mid      67.37   8.05    54.29   80.70   39.80   95.61  
DarkMago♥     Thunder Awaken         Mid      61.90   6.35    51.86   72.72   39.26   86.70  
TORONTOTOKYO  Team Spirit            Mid      60.71   6.58    49.80   71.53   36.67   86.50  
Ori           Team Aster             Mid      59.30   7.22    47.67   71.45   34.87   87.70  
...
```

#### Core
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
Pure          Entity                 Core     67.46   9.53    51.22   82.44   32.55   104.73 
Monet         Team Aster             Core     61.17   7.75    48.83   74.25   36.93   91.64  
YATOROGOD     Team Spirit            Core     61.06   8.17    47.75   74.52   33.45   91.66  
Raven         Fnatic                 Core     60.60   8.91    46.37   75.72   33.23   93.65  
Pakazs        Thunder Awaken         Core     60.56   8.11    47.64   74.42   33.90   90.03  
Crystallis    Team Secret            Core     57.02   8.34    43.76   71.28   32.55   86.43  
Timado        TSM FTX                Core     55.28   7.06    44.21   67.13   36.02   80.64  
23savage      Talon                  Core     53.73   9.44    39.46   70.19   26.16   91.79  
33            Tundra Esports         Core     53.22   7.46    41.62   66.03   30.38   83.61  
K1            beastcoast             Core     52.69   7.84    40.31   66.12   28.66   81.93  
...
```

#### Support
```
NAME          TEAM                   ROLE     MEAN    STD     5% CI   95% CI  MIN     MAX    
------------  ---------------------  -------  ------  ------  ------  ------  ------  ------ 
W_Zayac       Team Secret            Support  64.61   6.67    53.83   75.81   39.09   89.54  
Fishman       Entity                 Support  60.65   6.96    49.42   72.22   35.46   86.31  
Jaunuel       Fnatic                 Support  59.81   6.99    48.58   71.47   34.71   87.12  
DJ            Fnatic                 Support  57.98   5.76    48.66   67.59   38.20   82.91  
Hyde-         Talon                  Support  56.94   8.17    43.82   70.62   31.55   86.68  
Matthew       Thunder Awaken         Support  56.03   5.63    46.97   65.46   34.56   80.15  
Miposhka      Team Spirit            Support  55.86   6.61    45.12   66.89   33.10   83.28  
Siamese.C     Team Aster             Support  55.10   5.52    45.99   64.23   34.22   75.00  
DuBu          TSM FTX                Support  54.70   5.58    45.63   63.88   33.71   77.49  
Kataomi`      Entity                 Support  53.84   5.98    44.06   63.63   31.82   77.18  
...
```
