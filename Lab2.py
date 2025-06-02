# %% [markdown]
# # Intelligent Systems
# 
# ## Academic year 2024-2025
# 
# ### Lab 2: Metaheuristic Search
# 
# #### Instructors
# 
# * Juan Carlos Alfaro Jimenez: JuanCarlos.Alfaro@uclm.es
# * Maria Julia Flores Gallego: Julia.Flores@uclm.es
# * Ismael Garcia Varea: Ismael.Garcia@uclm.es
# * Adrian Rodriguez Lopez: Adrian.Rodriguez18@alu.uclm.es

# %% [markdown]
# ## Power and Service Stations: Finding the Optimal Configuration

# %% [markdown]
# ## 1. Introduction
# 
# Exciting news! The **Ministry of Transport and Sustainable Mobility** was highly impressed with the solutions developed in our initial assignment, Lab 1. They are particularly interested in implementing these algorithms in autonomous vehicle route planning, with A* as THE most effective method for identifying the optimal path efficiently. To further advance this project, the Ministry aims to strategically establish service stations across urban areas to support their autonomous vehicle fleet. These stations will act as fleet hubs and provide essential vehicle services.
# 
# To achieve this, they have requested **our technical expertise to determine the optimal distribution of these stations** across city maps. However, not every intersection is eligible as a station location, the Ministry has pre-selected candidate intersections based on specific criteria established by their technical and administrative teams. Their primary focus is on sustainability and equitable access, aiming to ensure that all citizens are reasonably close to a service station. Among these selected points, only a specific number will ultimately be chosen. To aid in our task of determining which ones, they have provided data on the population coverage for each candidate intersection, allowing us to consider both accessibility and coverage in our distribution strategy.
# 
# The primary objective is then to ensure efficient access for the maximum possible population coverage while maintaining an even distribution across the city, a vital consideration for a fully autonomous transport system. As autonomous vehicles (AVs) become integral to urban transportation, ensuring reliable and readily accessible infrastructure support becomes essential. Service stations, which include power charging, maintenance, and other support services, must be strategically placed to maximize population coverage while avoiding over-servicing or neglecting certain areas. This reflects real-world urban planning and resource distribution challenges, especially relevant to AV systems where consistency and access to services are critical for safe and sustainable city-wide deployment.
# 

# %% [markdown]
# ### 1.1 Objectives of the Lab Assignment
# 
# In this lab, we will apply metaheuristic search techniques.
# 
# The first objective is to understand the task and formulate it from the perspective of metaheuristic searches (lessons 6, 7, and 8). This will involve the implementation of at least these two algorithms:
# 
# * **Random Search** as a simple baseline, which will generate multiple solutions, evaluate them, and return the best one.
# 
# * **Genetic Algorithm**, which should accept various parameter configurations, allowing easy tuning of arguments like population size, selection method, and operator types. (Lesson 8)
# 
# These two apply for students in the continuous evaluation modality. Those students submitting for **non-continuous evaluation**, in addition to the previous two algorithms, must also include:
# 
# * Required: **Hill Climbing**, the local search algorithm covered in Lesson 7.
# * Optional but included in the grading: **Iterated Local Search** (ILS), also discussed in Lesson 7.
# 
# Next, we will analyze and compare the performance of these algorithms by running them on problem instances of varying complexity.
# 
# We hope this hands-on practice deepens your understanding of metaheuristic techniques and encourages you to consider their applications in real-world combinatorial optimization problems.
# 
# **Good luck!**

# %% [markdown]
# ## 2. Problem Description
# 
# ### 2.1 Input Problems
# 
# Each scenario will be provided in a `json` format file containing the following information, formatted as a dictionary with these keys:
# 
# * `address`: The address used.
# * `distance`: Maximum radius used to define intersections and segments around the address.
# * `intersections`: A list of dictionaries with information on intersections.
# * `segments`: A list of dictionaries with information on segments, which represent streets between two intersections.
# * `candidates`: A list of pairs (identifier, population), which contains the candidate intersections. Note that the identifiers in this list must be included in the list of intersections.
# * `number_stations`: The number of vehicle stations to locate, which must not exceed the number of candidates.
# 
# Each dictionary in `intersections` includes three keys:
# 
# * `identifier`: Intersection identifier
# * `longitude`: Longitude of the intersection
# * `latitude`: Latitude of the intersection
# 
# Each dictionary in `segments` includes four keys:
# 
# * `origin`: Origin intersection
# * `destination`: Destination intersection
# * `distance`: Distance between the two intersections
# * `speed`: Maximum speed allowed between the two intersections
# 
# **IMPORTANT**: `initial` and `final` are no longer included in the JSON file as they are not needed. During the evaluation of a possible configuration, these initial and final points will change multiple times. This may require some adjustments to your Lab 1 code for executing A*. These changes should be clearly indicated (your code should match Lab 1 except for these changes) and discussed in the lab report.
# 

# %% [markdown]
# ### 2.2. Illustrative example
# 
# A possible example of this problem could be the one shown in the following image, which shows a part of the city of Albacete:
# ![title](sample-problems-lab2/toy/example.png)
# In this case, the number of vehicle services to be located is 4, among the 15 candidate intersections represented with blue dots (labeled with the population covered). A possible solution is represented with green dots.
# 
# ---
# 
# ##### Notes:
# 
# * The file containing the image must be saved in the path indicated in the code for this cell.
# 
# ---

# %% [markdown]
# 
# ### 2.2 Formal problem definition
# We need to choose $s$ stations from a number of $c$ candidate or eligible intersections, with $s<=c$. Therefore, our **objective** is to decide at which of these $c$ candidate intersections we should locate the $s$ vehicle stations, so as to minimize the average travel time that each inhabitant takes from his home to the nearest station. If we denote by $S$ the vector of size $s$ containing the intersections in which the vehicle stations are located and by $C$ the vector of candidate intersections containing the pair (id, pop) for each candidate intersections, then formally, we want to solve the following optimization problem:
# 
# $$
# S^* = \arg\min_{S} \frac{1}{\sum_{i=0}^{c-1} C[i].pop} \cdot \left\{\sum_{i=0}^{c-1} \; C[i].pop \cdot \min_{j=0,\dots,s-1} time(C[i].id,S[j])\right\}
# $$
# 
# where:
# - $C[i].pop$ accounts for the population (number of inhabitants) covered by the candidate intersection $i$.
# - $C[i].int$ is the identifier of candidate intersection $i$.
# - $time(A,B)$ accounts for the lowest real time to travel from intersection $A$ to intersection $B$. 
# - $S$ contains exactly $s$ distinct intersections, which must all belong to the set of candidates solutions, and being $s<=c$
# 
# The following considerations must be done regarding the previous expression:
# - We are dealing with a **minimization problem**
# - The cardinality of the search space is:
# $$
# \binom{c}{s} = \frac{c!}{(c-s)!s!}
# $$
# for example if we have 20 eligible intersections and 4 vehicle stations the number of possible solutions is 210, not so many; but if we have 100 candidates and 10 sations, then the number of possible solutions is $1.7\times10^{13}$ ($5.3\times 10^{20}$ with 20 stations). 
# 
# 

# %% [markdown]
# ## 3. Development of the lab assignment
# 
# Before implementing the algorithms, you should first consider to define the basic elements in this type of problems, namely:
# 
# - A convenient representation for the solutions (configurations, chromosomes, individuals, ...) of the problem to be used in the combinatorial optimization algorithms. Think carefully about the distinct options and you'll have to discuss it in the assignment report. 
# 
# - Implement an evaluation mechanism in order to manage the evaluations carried out by the combinatorial optimization algorithms. How the evaluation should be done is going to be detailed below. 
#         
# - Important notes: 
#     - In the case A* returns no solution (cost=inf) replace this value by a very high number in comparison with the maximum time in our problem. Think about the need for this and discuss it in the report.
#     - You can take advantage of the Evaluation object to save some computations, collect statistics and printout the results.
#     - Notice that this assignment needs that you had already solved Lab 1, and you need to re-use the code you have there to solve this.
# 
# You will have to solve many problems similar to the ones in Lab1. The maps will be the same, but the problems need to incorporate new information, which is the list of candidate intersection, and per every of them, the population that is covered. The number of stations to be located is also indicated in the problem as `number_stations`.
# 

# %% [markdown]
# ### 3.1 Evaluation of a single solution
# 
# Given a specific instance of the problem to solve, and assuming that $C$ denotes its list of candidate intersections, the value of every possible solution $S$ should be computed as:
# 
# $$value(S) = \frac{1}{\sum_{i=0}^{c-1} C[i].pop} \cdot  \left\{\sum_{i=0}^{c-1} \; C[i].pop \cdot \min_{j=0,\dots,s-1} time(C[i].id,S[j])\right\}$$
# 
# according to the formula presented in section 2.2. 

# %% [markdown]
# ## 4. Work plan

# %% [markdown]
# ### 4.1. Tasks
# 
# * Transfer and change your code for Lab1 to solve A* searches as yo will need here:
#     * Reuse the most of the code needed from your Lab 1.
#     * Describe what has been modified, why and how.
# 
# * Process the new json files and save the problem accordingly:
#     * Apart from the search classes (Problem_2, State, Action, ...), you need to work with the candidate intersections
#     * Construct a mechanism able to store and retrieve the candidate interesections and their associated population
# 
# * Representation of a possible configuration:
#     * Among those seen in Lesson 6, find the most appropriate representation for this problem and adapt it to it, considering that every problem has distinct values for the number of total intersections, eligible intersections and the requested number of stations.
#     * Connect it to an appropriate way to evaluate each one considering the indications above at 3.2.
# 
# * Algorithms implementation:
#     * Implement, at least, the two required algorithms (Random search and a Genetic Algorithm -- GA). Notice that for the non-continuous evaluation, you should also add Hill Climbing and, optionally, ILS.
#     * In the GA, you have to check that you have implemented the generation of a population together with the main elements within the main loop: selection, crossover, mutation and combination of generations. 
# 
# * Experimentation and analysis:
#     * Those parameters which can be tuned must be adequately explored, also in relation with the given problems (dimensionality, complexity, etc.).
#     * The resulted output in terms of performance, convergence, number of generations, etc... should also be studied.
#     * Random search and GA should be compared assuring you get consistent results.
# 
# * Report:
#     * Write a report detailing the process followed, the strategies implemented and the results obtained, together with plots and visual comparisons.
# 

# %% [markdown]
# ### 4.2. Evaluation of the assignment
# 
# In the **continuos evaluation** modality, the evaluation of the practice will be carried out through an individual exam in which the following will be taken into account:
# 
# * Correct definition and implementation of the configuration representation and the evaluation function: 25%
# * Correct implementation of the genetic algorithm: 50%, which covers
#     * The general loop for generations is correct: 10%
#     * The distinct operators are correctly designed and coded: 40%
# * Efficiency and optimization: 15%   
# * Experimentation carried out and analysis of results: 10%
# 
# It is required that Lab1 is correctly integrated and that the Random Search works in a consistent way so that every student can use it as a proper baseline.
# 
# All of this is weighted by the level of knowledge that the student offers of the practice in case the exam is a personal interview.
# 
# For the **non-continuos evaluation** modality, the evaluation will be  modified as indicated below:
# 
# * Correct definition and implementation of the configuration representation and the evaluation function: 15%
# * Correct implementation of the genetic algorithm: 40%, which covers
#     * The general loop for generations is correct: 7%
#     * The distinct operators are correctly designed and coded: 33%
# * Correct implementation of hill climbing algorithm (compulsory): 15%    
# * Correct implementation of ILS algorithm (optional): 5%   
# * Efficiency and optimization: 15%   
# * Experimentation carried out and analysis of results: 10%

# %% [markdown]
# ### 4.3. Important dates
# 
# * Deadline to submit code: **December 13, 2024**.
# * Deadline for submission of the report: **End of the semester**.

# %%



