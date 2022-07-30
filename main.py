# SOURCES:
# https://www.kaggle.com/datasets/yashgpt/us-college-data
# https://blog.prepscholar.com/whats-the-average-high-school-gpa
# https://blog.collegevine.com/wp-content/uploads/2020/01/Screen_Shot_2019-04-30_at_11.57.14_AM.png
# https://nces.ed.gov/programs/digest/d17/tables/dt17_226.40.asp

import pandas as pd
import matplotlib.pyplot as plt
import math

# read csv -> pandas dataframe
college_data = pd.read_csv("collegedata.csv")
MEAN_GPA = 85
SD_GPA = 4
MEAN_EC = 4
SD_EC = 2
MEAN_SAT = 1060
SD_SAT = 195

# normal_dist stuff
def seq(min, max, k):
    vec = []
    c = min
    while c < max:
        c += k
        vec.append(c)
    return vec
def get_dens(x, mean=0, sd=1):
    density = (1 / (sd * math.sqrt(2 * math.pi))) * (math.e ** (-0.5 * ((x - mean) / sd) ** 2)) # density calculation function i don't understand because integrated calculus is hard
    return density
def normal_dist(vec, mean=0, sd=1, integer=False):
    dens_vec = []
    for i in range(len(vec)):
        if not integer:
            dens_vec += [get_dens(vec[i], mean=mean, sd=sd)]
        else:
            dens_vec += [round(get_dens(vec[i], mean=mean, sd=sd))]
    return dens_vec
def percentile(vec_x, vec_pdf, x): # technically its the probability but whatever
    less = 0
    for i in range(len(vec_x)):
        if vec_x[i] <= x:
            less += vec_pdf[i]
        else:
            break
    return less

# User Edit These (Should really get them from console input lol)
USERNAME = "Randy"
SAT_SCORE = 1500
GPA = 94.21
ECS = 4

def calc_percentile(gpa=85, sat_score=1060, ecs=4):
    gpa_x = seq(1, 100, 1)
    gpa_pdf = normal_dist(gpa_x, mean=MEAN_GPA, sd=SD_GPA)
    gpa_perc = percentile(gpa_x, gpa_pdf, gpa)

    sat_x = seq(1, 1600, 1)
    sat_pdf = normal_dist(sat_x, mean=MEAN_SAT, sd=SD_SAT)
    sat_perc = percentile(sat_x, sat_pdf, sat_score)

    ecs_x = seq(1, 10, 1)
    ecs_pdf = normal_dist(ecs_x, mean=MEAN_EC, sd=SD_EC)
    ecs_perc = percentile(ecs_x, ecs_pdf, ecs)
    # take weighted mean
    return (gpa_perc * (0.15 / 0.65)) + (sat_perc * (0.2 / 0.65)) + (ecs_perc * (0.3 / 0.65))
def college_acceptance(name, gpa, sat_score, ecs):
    cdata = college_data.loc[college_data["Name"] == name]
    req_perc = 1 - (cdata["Accept"].values[0]/cdata["Apps"].values[0])
    u_perc = calc_percentile(gpa=gpa, sat_score=sat_score, ecs=ecs)

    if (u_perc >= req_perc):
        return True
    return False

user_perc = calc_percentile(gpa=GPA, sat_score=SAT_SCORE, ecs=ECS) # compare to colleges, what percentile is the cutoff
accepted_colleges = college_data.loc[1 - (college_data["Accept"] / college_data["Apps"]) < user_perc]
is_harvard = college_acceptance("Harvard University", GPA, SAT_SCORE, ECS) # I won't get into harvard lol
if is_harvard:
    print(USERNAME + " is likely to get accepted into Harvard")
else:
    print(USERNAME + " is unlikely to get accepted into Harvard")

# PLOT
gpa_x = seq(1, 100, 1)
gpa_pdf = normal_dist(gpa_x, mean=MEAN_GPA, sd=SD_GPA)
rounded_gpa = math.floor(GPA)
plt.plot(gpa_x, gpa_pdf, color="red")
plt.plot(rounded_gpa, gpa_pdf[rounded_gpa - 1], marker="o", markersize=10, color="green")
plt.xlabel("GPA")
plt.ylabel("GPA Density")
plt.title("GPA Distribution")
plt.show()