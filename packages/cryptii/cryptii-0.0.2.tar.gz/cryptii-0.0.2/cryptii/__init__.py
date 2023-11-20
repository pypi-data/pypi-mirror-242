def frequency():
    s = '''
from functools import reduce
from itertools import groupby

input_data = ["Bus Car bus car train car bus car train bus TRAIN BUS buS caR CAR car BUS TRAIN"]

def mapper(sentence):
    words = sentence.split()
    return [(word.upper(), 1) for word in words]

def reducer(word, counts):
    return word, sum(counts)

mapped_data = map(mapper, input_data)
flattened_data = [item for sublist in mapped_data for item in sublist]
sorted_data = sorted(flattened_data, key=lambda x: x[0])
grouped_data = groupby(sorted_data, key=lambda x: x[0])
word_frequencies = [(word, sum(count for _, count in counts)) for word, counts in grouped_data]

for word, frequency in word_frequencies:
    print(f"({word}: {frequency})")
'''
    return s

def temperature():
    s = '''
from functools import reduce

# Dummy temperature data
temperature_data = [
    (2020, 25),
    (2020, 28),
    (2020, 22),
    (2021, 30),
    (2021, 32),
    (2021, 29),
    (2022, 20),
    (2022, 25),
    (2022, 18)
]

# Mapper function
def mapper(data):
    year, temperature = data
    return (year, temperature)

# Reducer function
def reducer(accumulated, current):
    year, temperature = current
    if year not in accumulated or temperature > accumulated[year]:
        accumulated[year] = temperature
    return accumulated

# Map step
mapped_data = map(mapper, temperature_data)

# Reduce step
max_temperatures = reduce(reducer, mapped_data, {})

# Output the result
for year, temperature in max_temperatures.items():
    print(f"Year: {year}, Max Temperature: {temperature}°C")'''
    return s

def grades():
    s = '''
def calculate_grade(score):
    if score >= 80:
        return 'A'
    elif 60 <= score < 80:
        return 'B'
    elif 40 <= score < 60:
        return 'C'
    else:
        return 'D'

def map_function(subject_marks):
    subject_marks = subject_marks.split("\n")
    marks = [int(mark.split(":")[1]) for mark in subject_marks if mark]
    total = sum(marks)
    avg = total / len(marks)
    return avg

def main():
    subject_marks = []
    for i in range(6):
        mark = input(f"Enter Marks of Subject{i+1}: ")
        subject_marks.append(f"Subject{i+1}:{mark}")

    # Map phase
    avg_scores = list(map(map_function, subject_marks))

    # Reduce phase
    total_avg = sum(avg_scores) / len(avg_scores)
    final_grade = calculate_grade(total_avg)
    
    print("The student Grade is:", final_grade)

if __name__ == "__main__":
    main()
'''
    return s

def matrix():
    s = '''
def mapper(key, value):
    matrix_name, i, j, val = value
    if matrix_name == 'A':
        for k in range(len(matrix_B[0])):
            yield (i, k), ('A', j, val)
    elif matrix_name == 'B':
        for k in range(len(matrix_A)):
            yield (k, j), ('B', i, val)

def reducer(key, values):
    row, col = key
    result = 0
    values_A = [v for v in values if v[0] == 'A']
    values_B = [v for v in values if v[0] == 'B']
    
    for val_A in values_A:
        for val_B in values_B:
            if val_A[1] == val_B[1]:
                result += val_A[2] * val_B[2]
    
    yield key, result

def input_matrix(matrix_name):
    print(f"Enter the dimensions of matrix {matrix_name}:")
    rows = int(input("Number of rows: "))
    cols = int(input("Number of columns: "))
    matrix = []
    
    print(f"Enter the values for matrix {matrix_name} (row-wise):")
    for i in range(rows):
        row = []
        for j in range(cols):
            value = int(input(f"Enter value at ({i+1}, {j+1}): "))
            row.append(value)
        matrix.append(row)
    
    return matrix

matrix_A = input_matrix('A')
matrix_B = input_matrix('B')

input_data = []

for i in range(len(matrix_A)):
    for j in range(len(matrix_B[0])):
        input_data.append(('A', i, j, matrix_A[i][j]))

for j in range(len(matrix_B[0])):
    for k in range(len(matrix_B)):
        input_data.append(('B', j, k, matrix_B[j][k]))

mapped_data = []

for data in input_data:
    key, value = data[1], data
    for key, value in mapper(key, value):
        mapped_data.append((key, value))

mapped_data.sort(key=lambda x: x[0])

grouped_data = {}

for key, value in mapped_data:
    if key not in grouped_data:
        grouped_data[key] = []
    grouped_data[key].append(value)

output = {}

for key, values in grouped_data.items():
    for output_key, output_value in reducer(key, values):
        output[output_key] = output_value

for key, value in sorted(output.items()):
    print(f"({key[0]}, {key[1]}): {value}")

# Enter the dimensions of matrix A:
# Number of rows: 2
# Number of columns: 2
# Enter the values for matrix A (row-wise):
# Enter value at (1, 1): 1
# Enter value at (1, 2): 2
# Enter value at (2, 1): 1
# Enter value at (2, 2): 2

# Enter the dimensions of matrix B:
# Number of rows: 2
# Number of columns: 2
# Enter the values for matrix B (row-wise):
# Enter value at (1, 1): 34
# Enter value at (1, 2): 1
# Enter value at (2, 1): 2
# Enter value at (2, 2): 4

# Resultant matrix C:
# (0, 0): 38
# (0, 1): 9
# (1, 0): 38
# (1, 1): 9
'''
    return s

def reddit():
    s = '''
-- Load Raw Data
raw_data = LOAD '/reddit_analysis/Reddit_Data.csv' USING PigStorage(',');

-- Project Specific Columns
get_details = FOREACH raw_data GENERATE $0 AS id, $1 AS text;

-- Tokenization
tokens = FOREACH get_details GENERATE id, text, FLATTEN(TOKENIZE(text)) AS words;

-- Load Sentiment Dictionary
dictionary = LOAD '/reddit_analysis/AFINN.txt' USING PigStorage('\t') AS (word:chararray, rating:int);

-- Left Outer Join
word_ratings = JOIN tokens BY words LEFT OUTER, dictionary BY word USING 'replicated';

-- Describe Relation (for debugging)
describe word_ratings;

-- Projection and Grouping
ratings = FOREACH word_ratings GENERATE tokens::id AS id, tokens::text AS text, dictionary::rating AS rating;
group_words = GROUP ratings BY (id, text);

-- Calculate Average Ratings
avg_ratings = FOREACH group_words GENERATE group, AVG(ratings.rating) AS text_rating;

-- Filter Positive and Negative Sentiments
positive = FILTER avg_ratings BY text_rating > 0;
negative = FILTER avg_ratings BY text_rating < 0;

-- Store Positive Sentiment Data
STORE positive INTO '/reddit_analysis/positive' USING PigStorage(',');
'''
    return s

def baseball():
    s = '''
-- Step 1: Load Data
raw_data = LOAD '/gamedata/*.EV{A,N}' USING PigStorage(',') AS (type: chararray, id: chararray, name: chararray);

-- Step 2: Filter Data
players_data = FILTER raw_data BY type MATCHES 'start' OR type MATCHES 'sub';

-- Step 3: Project Columns
id_name = FOREACH players_data GENERATE id, name;

-- Step 4: Remove Duplicates
distinct_data = DISTINCT id_name;

-- Step 5: Sort Data
sorted_data = ORDER distinct_data BY id;

-- Step 6: Store Results
STORE sorted_data INTO '/gamedata/id_player_mapping' USING PigStorage(',');

-- Hive Query: Create External Table
-- This Hive query creates an external table named "players" with two columns (id and name),
-- specifying comma and newline delimiters, and associates it with the HDFS location
-- '/gamedata/id_player_mapping/' where the data is stored.
-- Be sure to replace 'LOCATION' with 'LOCATION' for Hive version 2.0.0 and later.
-- 'FIELDS TERMINATED BY ','' and 'LINES TERMINATED BY '\n'' are optional, as they match the default PigStorage settings.
CREATE EXTERNAL TABLE players(id STRING, name STRING) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
LOCATION '/gamedata/id_player_mapping/';

-- Hive Query: Select Data
-- This query selects all data from the 'players' table and displays it.
SELECT * FROM players;
'''
    return s

def movie():
    s = '''
-- Set Default Parallel
SET default_parallel 4;

-- Data Loading
UI = LOAD '/RecSys/d_1.rmse' USING PigStorage('\t') AS (uid:int, itemid:int, rating:double);
t1 = LOAD '/RcomSys/d_2.rmse' USING PigStorage('\t') AS (uid:int, itemid:int, rating:double);

-- Data Splitting
SPLIT UI INTO NonZero IF rating != 0, Zero IF rating == 0;

-- Average Calculation
G = GROUP NonZero BY itemid;
Avg = FOREACH G GENERATE group AS itemid, AVG(NonZero.rating) AS avg;

-- Rating Normalization
J = JOIN NonZero BY itemid, Avg BY itemid;
S = FOREACH J GENERATE NonZero::uid AS uid, NonZero::itemid AS itemid,
    (DOUBLE)(NonZero::rating - Avg::avg) AS rating;
CA = UNION S, Zero;

-- User-Item Matrix
A = FOREACH CA GENERATE uid, itemid, rating;
B = FOREACH CA GENERATE uid, itemid, rating;
C = JOIN A BY uid, B BY uid;
P = FOREACH C GENERATE A::itemid, B::itemid, A::uid, (DOUBLE)(A::rating * B::rating) AS rp;

-- Item Similarity Calculation
Gr = GROUP P BY (A::itemid, B::itemid);
G_Sum = FOREACH Gr GENERATE group AS pid, SUM(P.rp) AS sum;
G_Sum1 = FOREACH G_Sum GENERATE pid, FLATTEN(pid), sum;
Numerator = FOREACH G_Sum1 GENERATE pid::A::itemid AS it1, pid::B::itemid AS it2, sum;

P_1 = FOREACH CA GENERATE uid, itemid, rating;
P_2 = FOREACH P_1 GENERATE uid, itemid, (DOUBLE)(rating * rating) AS sq;
P_3 = GROUP P_2 BY itemid;
P_4 = FOREACH P_3 GENERATE group AS itemid, (DOUBLE)(SUM(P_2.sq)) AS ss;
Sqrt = FOREACH P_4 GENERATE itemid, (DOUBLE)(SQRT(ss)) AS rms;
P_5 = FOREACH Sqrt GENERATE itemid, rms;
P_6 = FOREACH Sqrt GENERATE itemid, rms;
P_7 = CROSS P_5, P_6;
Denominator = FOREACH P_7 GENERATE P_5::itemid AS it1, P_6::itemid AS it2,
    (DOUBLE)(P_5::rms * P_6::rms) AS prms;
P_8 = JOIN Numerator BY (it1, it2), Denominator BY (it1, it2);
II = FOREACH P_8 GENERATE Numerator::it1 AS it1, Numerator::it2 AS it2,
    (DOUBLE)(Numerator::sum / Denominator::prms) AS sim;

-- Recommendation Generation
JNZ = JOIN NonZero BY itemid, II BY it1;
BJ = JOIN JNZ BY (NonZero::uid, II::it2), Zero BY (uid, itemid);
Test = FOREACH BJ GENERATE Zero::uid AS uid, Zero::itemid AS pitem,
    JNZ::II::it1 AS sitem, JNZ::NonZero::rating AS rating, JNZ::II::sim AS sim;

-- Top-N Recommendations
P_13 = GROUP Test BY (uid, pitem);
P_14 = FOREACH P_13 {
    sim_ord = ORDER Test BY sim DESC;
    lim = LIMIT sim_ord 10;
    GENERATE group AS uid_itemnotrated, lim;
};

-- Prediction Calculation
P_15 = FOREACH P_14 GENERATE FLATTEN(uid_itemnotrated), FLATTEN(lim);
P_16 = FOREACH P_15 GENERATE FLATTEN(uid_itemnotrated),
    (DOUBLE)(lim::rating * lim::sim) AS pro, lim::sim AS sim;
P_17 = GROUP P_16 BY (uid_itemnotrated::uid, uid_itemnotrated::pitem);
P_18 = FOREACH P_17 GENERATE group AS uid_item, (DOUBLE)SUM(P_16.pro) AS sum_pro,
    (DOUBLE)SUM(P_16.sim) AS sum_sim;
P_19 = FOREACH P_18 GENERATE uid_item, (DOUBLE)(sum_pro / sum_sim) AS PredictedRating;
Prediction = FOREACH P_19 GENERATE FLATTEN(uid_item), PredictedRating;
A_23 = FOREACH Prediction GENERATE uid_item::uid_itemnotrated::uid AS uid
'''
    return s