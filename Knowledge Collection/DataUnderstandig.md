# Data Understanding

## 1) Data Set Types
	
### 1.1 Record Data
Each row = data example
column = attribute
--> most common type of data set
  
### 1.2 Non-Record Data: 

#### Text data
text documents ( e.g. MS word) --> text analytics (e.g. word counts: word xy repeat 7 times, just a website = it has equal quality/ value but no structure)

#### Image data:
- image is stored as a sequence of pixels
- image = 28*28px = 784, each pixel has a single pixel value [0, 255] 
- indicating the lightness/ darkness of that pixel
	
#### Sequence Data:
- DNA data, looking for sequences 
	
#### Transaction Data:
- can be converted to record data --> storing 1 for 0 for each attribute/product that was bought
- but not efficient, bcs maybe lots of 0: sparse matrix to reduce the number of columns

#### Network Data:
- need to avoid traffic and increase reliability: build more hubs, build algorithms that chooses the least busy route to the destination --> increases speed and reliability
	
 ## 2) Preparing Data for Analysis
	
### 2.1 Understand Variables:
- Nominal Data (used for labeling variables, without any quantitative value)
- Ordinal Data (Order with meaning)
- Numeric Data (numbers that describe a measurable quantity)
#### 4. Interval (numeric scales in which we know both the order and difference bw. The values, base is fixed)
#### 5. Ratio (percentage, use data on same scale to better compare, base is not fixed)

--> Paying attention to the data types and convert data types if necessary
	
### 2.2 Data Quality Issues
Noise (modification of original values)
Outliers (data objects with characteristics that are considerably different than most of the other data objects --> analyze and decide whether outliers can be excluded)
Missing Values (information not collected/ not applicable --> eliminate record, ignore value or make estimation)
Duplicate Data (often when merging data --> clean data)

### 2.3 Numeric Variables
Mean (Average)
Median (Value that separates the higher half from the lower half of the data sample)Mode (Value that appears most often)
Standard Deviation (Measure to quantify the amount of variation of a data set)
Variance (Measure to quantify how far a set of numbers are spread out from their average value)


### 2.4 Transformation
- Aggregation
- Discreatization
- Log Transformation
- Z- Score transformation (Adjust for different sizes of populations to better compare numbers - Z(x) = (x-u)/sd)
- Min-max transformation

### 2.5 Sampling
- Sampling when obtaining or analyzing the entire set of data of interest is too expensive or time consuming
- The sample is representative, meaning it has approx. the same property as the orginial data set

--> Therefore, the analysis results on the sample data may be reliably generalized to the entire data set

1. Convenience sampling: 
- sample students to represent all students from a university
2. Random Sampling:
- Randomly sample students around campus
3. Stratified sampling:
- Sample equal number of students from each school 
4. Systematic sampling
- E.g. sort students’ SUID numbers in increasing order, pick the 1st, 11th, 21st, 31st, …, students until 300 students are sampled.


