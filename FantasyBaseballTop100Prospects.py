# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:10:38 2024

@author: homer
"""


import re
import pandas as pd
import os

# Your input data
data = """
1
Jackson Holliday
SS
BALTIMORE ORIOLES
Age:
20
Ht:
6-0
Wt:
185
Bats:
L
Throws:
R



BALTIMORE ORIOLES
SS
2
Jackson Chourio
OF
MILWAUKEE BREWERS
Age:
20
Ht:
5-11
Wt:
165
Bats:
R
Throws:
R



MILWAUKEE BREWERS
OF
3
Ethan Salas
C
SAN DIEGO PADRES
Age:
18
Ht:
6-2
Wt:
180
Bats:
L
Throws:
R



SAN DIEGO PADRES
C
4
Jordan Lawlar
SS
ARIZONA DIAMONDBACKS
Age:
21
Ht:
6-1
Wt:
190
Bats:
R
Throws:
R



ARIZONA DIAMONDBACKS
SS
5
Junior Caminero
3B,IF
TAMPA BAY RAYS
Age:
20
Ht:
6-1
Wt:
160
Bats:
R
Throws:
R



TAMPA BAY RAYS
3B
IF
6
Wyatt Langford
OF
TEXAS RANGERS
Age:
22
Ht:
6-1
Wt:
225
Bats:
R
Throws:
R



TEXAS RANGERS
OF
7
Dylan Crews
OF
WASHINGTON NATIONALS
Age:
22
Ht:
6-0
Wt:
205
Bats:
R
Throws:
R



WASHINGTON NATIONALS
OF
8
Marcelo Mayer
SS
BOSTON RED SOX
Age:
21
Ht:
6-2
Wt:
190
Bats:
L
Throws:
R



BOSTON RED SOX
SS
9
Evan Carter
OF
TEXAS RANGERS
Age:
21
Ht:
6-2
Wt:
190
Bats:
L
Throws:
R



TEXAS RANGERS
OF
10
Paul Skenes
RHP
PITTSBURGH PIRATES
Age:
22
Ht:
6-6
Wt:
235
Bats:
R
Throws:
R



PITTSBURGH PIRATES
RHP
11
Kyle Harrison
LHP
SAN FRANCISCO GIANTS
Age:
22
Ht:
6-2
Wt:
200
Bats:
R
Throws:
L



SAN FRANCISCO GIANTS
LHP
12
Jeferson Quero
C
MILWAUKEE BREWERS
Age:
21
Ht:
5-11
Wt:
215
Bats:
R
Throws:
R



MILWAUKEE BREWERS
C
13
Brayan Rocchio
SS
CLEVELAND GUARDIANS
Age:
23
Ht:
5-10
Wt:
170
Bats:
B
Throws:
R



CLEVELAND GUARDIANS
SS
14
Max Clark
OF
DETROIT TIGERS
Age:
19
Ht:
6-1
Wt:
205
Bats:
L
Throws:
L



DETROIT TIGERS
OF
15
Walker Jenkins
OF
MINNESOTA TWINS
Age:
19
Ht:
6-3
Wt:
210
Bats:
L
Throws:
R



MINNESOTA TWINS
OF
16
Masyn Winn
SS
ST. LOUIS CARDINALS
Age:
22
Ht:
5-11
Wt:
180
Bats:
R
Throws:
R



ST. LOUIS CARDINALS
SS
17
Noelvi Marte
3B,SS
CINCINNATI REDS
Age:
22
Ht:
6-0
Wt:
215
Bats:
R
Throws:
R



CINCINNATI REDS
3B
SS
18
Pete Crow-Armstrong
OF
CHICAGO CUBS
Age:
22
Ht:
5-11
Wt:
185
Bats:
L
Throws:
L



CHICAGO CUBS
OF
19
James Wood
OF
WASHINGTON NATIONALS
Age:
21
Ht:
6-6
Wt:
240
Bats:
L
Throws:
R



WASHINGTON NATIONALS
OF
20
Samuel Basallo
C
BALTIMORE ORIOLES
Age:
19
Ht:
6-3
Wt:
190
Bats:
L
Throws:
R



BALTIMORE ORIOLES
C
21
Jasson Domínguez
OF
NEW YORK YANKEES
Age:
21
Ht:
5-9
Wt:
190
Bats:
B
Throws:
R



NEW YORK YANKEES
OF
22
Roman Anthony
OF
BOSTON RED SOX
Age:
20
Ht:
6-2
Wt:
190
Bats:
L
Throws:
R



BOSTON RED SOX
OF
23
Jackson Merrill
SS
SAN DIEGO PADRES
Age:
21
Ht:
6-3
Wt:
195
Bats:
L
Throws:
R



SAN DIEGO PADRES
SS
24
Termarr Johnson
2B
PITTSBURGH PIRATES
Age:
20
Ht:
5-8
Wt:
175
Bats:
L
Throws:
R



PITTSBURGH PIRATES
2B
25
Josue De Paula
OF
LOS ANGELES DODGERS
Age:
19
Ht:
6-2
Wt:
185
Bats:
L
Throws:
L



LOS ANGELES DODGERS
OF
26
Matt Shaw
IF
CHICAGO CUBS
Age:
22
Ht:
5-11
Wt:
185
Bats:
R
Throws:
R



CHICAGO CUBS
IF
27
Coby Mayo
3B,1B
BALTIMORE ORIOLES
Age:
22
Ht:
6-5
Wt:
230
Bats:
R
Throws:
R



BALTIMORE ORIOLES
3B
1B
28
Kevin Alcántara
OF
CHICAGO CUBS
Age:
21
Ht:
6-6
Wt:
190
Bats:
R
Throws:
R



CHICAGO CUBS
OF
29
Jackson Jobe
RHP
DETROIT TIGERS
Age:
21
Ht:
6-2
Wt:
190
Bats:
R
Throws:
R



DETROIT TIGERS
RHP
30
Jett Williams
SS
NEW YORK METS
Age:
20
Ht:
5-6
Wt:
175
Bats:
R
Throws:
R



NEW YORK METS
SS
31
Brooks Lee
SS,3B
MINNESOTA TWINS
Age:
23
Ht:
5-11
Wt:
205
Bats:
B
Throws:
R



MINNESOTA TWINS
SS
3B
32
Ceddanne Rafaela
OF,IF
BOSTON RED SOX
Age:
23
Ht:
5-9
Wt:
165
Bats:
R
Throws:
R



BOSTON RED SOX
OF
IF
33
River Ryan
RHP
LOS ANGELES DODGERS
Age:
25
Ht:
6-2
Wt:
195
Bats:
R
Throws:
R



LOS ANGELES DODGERS
RHP
34
Andrew Painter
RHP
PHILADELPHIA PHILLIES
Age:
21
Ht:
6-7
Wt:
215
Bats:
R
Throws:
R



PHILADELPHIA PHILLIES
RHP
35
Dylan Lesko
RHP
SAN DIEGO PADRES
Age:
20
Ht:
6-2
Wt:
195
Bats:
R
Throws:
R



SAN DIEGO PADRES
RHP
36
Colt Keith
3B
DETROIT TIGERS
Age:
22
Ht:
6-2
Wt:
200
Bats:
L
Throws:
R



DETROIT TIGERS
3B
37
Colt Emerson
SS,2B
SEATTLE MARINERS
Age:
18
Ht:
6-1
Wt:
195
Bats:
L
Throws:
R



SEATTLE MARINERS
SS
2B
38
Carson Williams
SS
TAMPA BAY RAYS
Age:
21
Ht:
6-1
Wt:
180
Bats:
R
Throws:
R



TAMPA BAY RAYS
SS
39
Jared Jones
RHP
PITTSBURGH PIRATES
Age:
22
Ht:
6-1
Wt:
190
Bats:
L
Throws:
R



PITTSBURGH PIRATES
RHP
40
Sebastian Walcott
3B
TEXAS RANGERS
Age:
18
Ht:
6-4
Wt:
190
Bats:
R
Throws:
R



TEXAS RANGERS
3B
41
Druw Jones
OF
ARIZONA DIAMONDBACKS
Age:
20
Ht:
6-4
Wt:
180
Bats:
R
Throws:
R



ARIZONA DIAMONDBACKS
OF
42
Colson Montgomery
SS
CHICAGO WHITE SOX
Age:
22
Ht:
6-3
Wt:
205
Bats:
L
Throws:
R



CHICAGO WHITE SOX
SS
43
Justin Crawford
OF
PHILADELPHIA PHILLIES
Age:
20
Ht:
6-1
Wt:
175
Bats:
L
Throws:
R



PHILADELPHIA PHILLIES
OF
44
Tyler Black
3B
MILWAUKEE BREWERS
Age:
23
Ht:
5-10
Wt:
205
Bats:
L
Throws:
R



MILWAUKEE BREWERS
3B
45
Luisangel Acuña
SS
NEW YORK METS
Age:
22
Ht:
5-8
Wt:
180
Bats:
R
Throws:
R



NEW YORK METS
SS
46
Cole Young
SS
SEATTLE MARINERS
Age:
20
Ht:
6-0
Wt:
180
Bats:
L
Throws:
R



SEATTLE MARINERS
SS
47
Emmanuel Rodriguez
OF
MINNESOTA TWINS
Age:
21
Ht:
5-10
Wt:
210
Bats:
L
Throws:
L



MINNESOTA TWINS
OF
48
Bubba Chandler
RHP
PITTSBURGH PIRATES
Age:
21
Ht:
6-2
Wt:
200
Bats:
B
Throws:
R



PITTSBURGH PIRATES
RHP
49
Cade Horton
RHP
CHICAGO CUBS
Age:
22
Ht:
6-1
Wt:
210
Bats:
R
Throws:
R



CHICAGO CUBS
RHP
50
Cam Collier
3B
CINCINNATI REDS
Age:
19
Ht:
6-2
Wt:
210
Bats:
L
Throws:
R



CINCINNATI REDS
3B
51
Jansel Luis
SS
ARIZONA DIAMONDBACKS
Age:
19
Ht:
6-0
Wt:
170
Bats:
B
Throws:
R



ARIZONA DIAMONDBACKS
SS
52
Ricky Tiedemann
LHP
TORONTO BLUE JAYS
Age:
21
Ht:
6-4
Wt:
220
Bats:
L
Throws:
L



TORONTO BLUE JAYS
LHP
53
Brady House
3B
WASHINGTON NATIONALS
Age:
21
Ht:
6-4
Wt:
215
Bats:
R
Throws:
R



WASHINGTON NATIONALS
3B
54
Kyle Teel
C
BOSTON RED SOX
Age:
22
Ht:
6-1
Wt:
190
Bats:
L
Throws:
R



BOSTON RED SOX
C
55
Victor Scott II
OF
ST. LOUIS CARDINALS
Age:
23
Ht:
5-10
Wt:
190
Bats:
L
Throws:
L



ST. LOUIS CARDINALS
OF
56
Brayden Taylor
3B
TAMPA BAY RAYS
Age:
22
Ht:
6-1
Wt:
180
Bats:
L
Throws:
R



TAMPA BAY RAYS
3B
57
Orelvis Martinez
IF
TORONTO BLUE JAYS
Age:
22
Ht:
5-11
Wt:
200
Bats:
R
Throws:
R



TORONTO BLUE JAYS
IF
58
Joey Ortiz
SS
MILWAUKEE BREWERS
Age:
25
Ht:
5-9
Wt:
190
Bats:
R
Throws:
R



MILWAUKEE BREWERS
SS
59
Arjun Nimmala
SS
TORONTO BLUE JAYS
Age:
18
Ht:
6-1
Wt:
170
Bats:
R
Throws:
R



TORONTO BLUE JAYS
SS
60
Rhett Lowder
RHP
CINCINNATI REDS
Age:
22
Ht:
6-2
Wt:
200
Bats:
R
Throws:
R



CINCINNATI REDS
RHP
61
Harry Ford
C
SEATTLE MARINERS
Age:
21
Ht:
6-0
Wt:
200
Bats:
R
Throws:
R



SEATTLE MARINERS
C
62
Heston Kjerstad
OF
BALTIMORE ORIOLES
Age:
25
Ht:
6-3
Wt:
205
Bats:
L
Throws:
R



BALTIMORE ORIOLES
OF
63
Everson Pereira
OF
NEW YORK YANKEES
Age:
23
Ht:
5-11
Wt:
190
Bats:
R
Throws:
R



NEW YORK YANKEES
OF
64
Enrique Bradfield, Jr.
OF
BALTIMORE ORIOLES
Age:
22
Ht:
6-1
Wt:
170
Bats:
L
Throws:
L



BALTIMORE ORIOLES
OF
65
Tommy Troy
IF
ARIZONA DIAMONDBACKS
Age:
22
Ht:
5-10
Wt:
195
Bats:
R
Throws:
R



ARIZONA DIAMONDBACKS
IF
66
Kyle Manzardo
1B
CLEVELAND GUARDIANS
Age:
23
Ht:
6-0
Wt:
205
Bats:
L
Throws:
L



CLEVELAND GUARDIANS
1B
67
Edgar Quero
C
CHICAGO WHITE SOX
Age:
21
Ht:
5-11
Wt:
175
Bats:
B
Throws:
R



CHICAGO WHITE SOX
C
68
Michael Busch
IF
CHICAGO CUBS
Age:
26
Ht:
6-1
Wt:
210
Bats:
L
Throws:
R



CHICAGO CUBS
IF
69
Bryan Ramos
3B
CHICAGO WHITE SOX
Age:
22
Ht:
6-2
Wt:
190
Bats:
R
Throws:
R



CHICAGO WHITE SOX
3B
70
Sterlin Thompson
OF,IF
COLORADO ROCKIES
Age:
23
Ht:
6-4
Wt:
200
Bats:
L
Throws:
R



COLORADO ROCKIES
OF
IF
71
Brock Wilken
3B
MILWAUKEE BREWERS
Age:
22
Ht:
6-4
Wt:
220
Bats:
R
Throws:
R



MILWAUKEE BREWERS
3B
72
Robby Snelling
LHP
SAN DIEGO PADRES
Age:
20
Ht:
6-3
Wt:
210
Bats:
R
Throws:
L



SAN DIEGO PADRES
LHP
73
Tink Hence
RHP
ST. LOUIS CARDINALS
Age:
21
Ht:
6-1
Wt:
185
Bats:
R
Throws:
R



ST. LOUIS CARDINALS
RHP
74
Cade Cavalli
RHP
WASHINGTON NATIONALS
Age:
25
Ht:
6-4
Wt:
230
Bats:
R
Throws:
R



WASHINGTON NATIONALS
RHP
75
Chase Dollander
RHP
COLORADO ROCKIES
Age:
22
Ht:
6-2
Wt:
200
Bats:
R
Throws:
R



COLORADO ROCKIES
RHP
76
Nick Nastrini
RHP
CHICAGO WHITE SOX
Age:
24
Ht:
6-3
Wt:
215
Bats:
R
Throws:
R



CHICAGO WHITE SOX
RHP
77
Curtis Mead
IF
TAMPA BAY RAYS
Age:
23
Ht:
6-0
Wt:
170
Bats:
R
Throws:
R



TAMPA BAY RAYS
IF
78
Edwin Arroyo
SS
CINCINNATI REDS
Age:
20
Ht:
6-0
Wt:
175
Bats:
B
Throws:
R



CINCINNATI REDS
SS
79
Noah Schultz
LHP
CHICAGO WHITE SOX
Age:
20
Ht:
6-9
Wt:
220
Bats:
L
Throws:
L



CHICAGO WHITE SOX
LHP
80
Hurston Waldrep
RHP
ATLANTA BRAVES
Age:
22
Ht:
6-2
Wt:
210
Bats:
R
Throws:
R



ATLANTA BRAVES
RHP
81
Chase Delauter
OF
CLEVELAND GUARDIANS
Age:
22
Ht:
6-4
Wt:
235
Bats:
L
Throws:
L



CLEVELAND GUARDIANS
OF
82
Yanquiel Fernandez
OF
COLORADO ROCKIES
Age:
21
Ht:
6-2
Wt:
200
Bats:
L
Throws:
L



COLORADO ROCKIES
OF
83
Yu-Min Lin
LHP
ARIZONA DIAMONDBACKS
Age:
20
Ht:
5-11
Wt:
160
Bats:
L
Throws:
L



ARIZONA DIAMONDBACKS
LHP
84
Marco Luciano
SS
SAN FRANCISCO GIANTS
Age:
22
Ht:
6-1
Wt:
180
Bats:
R
Throws:
R



SAN FRANCISCO GIANTS
SS
85
Bryce Eldridge
1B,OF
SAN FRANCISCO GIANTS
Age:
19
Ht:
6-7
Wt:
225
Bats:
L
Throws:
R



SAN FRANCISCO GIANTS
1B
OF
86
Dalton Rushing
C
LOS ANGELES DODGERS
Age:
23
Ht:
6-1
Wt:
220
Bats:
L
Throws:
R



LOS ANGELES DODGERS
C
87
Jace Jung
IF
DETROIT TIGERS
Age:
23
Ht:
6-0
Wt:
205
Bats:
L
Throws:
R



DETROIT TIGERS
IF
88
Miguel Bleis
OF
BOSTON RED SOX
Age:
20
Ht:
6-0
Wt:
170
Bats:
R
Throws:
R



BOSTON RED SOX
OF
89
Aidan Miller
IF
PHILADELPHIA PHILLIES
Age:
20
Ht:
6-2
Wt:
205
Bats:
R
Throws:
R



PHILADELPHIA PHILLIES
IF
90
Jacob Misiorowski
RHP
MILWAUKEE BREWERS
Age:
22
Ht:
6-7
Wt:
190
Bats:
R
Throws:
R



MILWAUKEE BREWERS
RHP
91
Nolan Schanuel
1B
LOS ANGELES ANGELS
Age:
22
Ht:
6-4
Wt:
220
Bats:
L
Throws:
L



LOS ANGELES ANGELS
1B
92
Noble Meyer
RHP
MIAMI MARLINS
Age:
19
Ht:
6-5
Wt:
185
Bats:
R
Throws:
R



MIAMI MARLINS
RHP
93
Sal Stewart
3B
CINCINNATI REDS
Age:
20
Ht:
6-3
Wt:
215
Bats:
R
Throws:
R



CINCINNATI REDS
3B
94
Ronny Mauricio
SS
NEW YORK METS
Age:
23
Ht:
6-3
Wt:
170
Bats:
B
Throws:
R



NEW YORK METS
SS
95
Gavin Stone
RHP
LOS ANGELES DODGERS
Age:
25
Ht:
6-1
Wt:
175
Bats:
R
Throws:
R



LOS ANGELES DODGERS
RHP
96
Gabriel Gonzalez
OF
MINNESOTA TWINS
Age:
20
Ht:
5-10
Wt:
165
Bats:
R
Throws:
R



MINNESOTA TWINS
OF
97
Parker Meadows
OF
DETROIT TIGERS
Age:
24
Ht:
6-5
Wt:
205
Bats:
L
Throws:
R



DETROIT TIGERS
OF
98
Roderick Arias
SS
NEW YORK YANKEES
Age:
19
Ht:
6-0
Wt:
180
Bats:
B
Throws:
R



NEW YORK YANKEES
SS
99
Thayron Liranzo
C
LOS ANGELES DODGERS
Age:
20
Ht:
6-3
Wt:
195
Bats:
B
Throws:
R



LOS ANGELES DODGERS
C
100
Drew Gilbert
OF
NEW YORK METS
Age:
23
Ht:
5-9
Wt:
195
Bats:
L
Throws:
L



NEW YORK METS
OF
"""


def extract_info(text):
    matches = re.findall(r'(\d+)\s+(.+)\s+([\s\S]+?)\s+([A-Z\s]+)\s+Age:\s+(\d+)\s+Ht:\s+([\d-]+)\s+Wt:\s+(\d+)\s+Bats:\s+([LRB])\s+Throws:\s+([LR])', text)
    print("Matches:", matches)
    return matches

# Extract information from the data
entries = extract_info(data)

# Create a Pandas DataFrame
columns = ['Rank', 'Name', 'Position', 'Team', 'Age', 'Height', 'Weight', 'Bats', 'Throws']
df = pd.DataFrame(entries, columns=columns)

# Quality check for missing ranks
expected_ranks = set(range(1, len(entries) + 1))
actual_ranks = set(df['Rank'].astype(int))

missing_ranks = expected_ranks - actual_ranks

if missing_ranks:
    print(f"Missing ranks: {sorted(list(missing_ranks))}")
else:
    print("All expected ranks are present.")

# Display the DataFrame
print(df)

folder_path = r'C:\Users\homer\Downloads'
output_file_path = os.path.join(folder_path, "100prospects.csv")
df.to_csv(output_file_path, index=False, sep='\t')