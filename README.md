    # Latent Cluster Analysis on Opinion Survey Using Python
    #### Video Demo:  https://youtu.be/1ibFCEw_Iyo
    #### Description:

**Brief description**

This program works on a dataset containing the results of an opinion survey in a fixed format.  It aims at dividing respondents into an optimal number of clusters based on their opinion and produce summary tables and charts to facilitate further analysis.

**Introduction of Latent Cluster Anaylsis**

Latent Cluster Anaylsis (LCA) is a model-based clustering method, which is increasingly used in social, psychological and educational research.  The aim is to group targets of the study into homogeneous groups called clusters.

Compared with traditional clustering methods like K-means Clustering, which minimises the Euclidean distance (squared distance) among responses, LCA adopts a probabilistic approach and calculates conditional probabilities that indicate the chance that variables take on certain values.  K-means Clustering requires the dependent variables to be continuous, and LCA can be applied to categorical and binary dependent variables.

**Outline of methodology**

In this project, the survey has 5 opinion-type questions (named Q1 to Q5) and 3 demographic variables, namely, area, age and sex.  The dataset is arranged such that each question and demographic variable is a column and each row is a respondent’s record.  There is no limit on the number of respondents.

The respondents are grouped into a certain number of clusters (which will be optimised in the program) based on similarity of their opinion in Q1 to Q5.  Using LCA, the program will assign a cluster number to each record such that the demographic characteristics of each cluster can be analysed.  The ultimate purpose is to see if a certain type of respondents will tend to have similar opinion to the questions as a whole.

**Description of each function**

*main()*

The user is first asked to input the path (including file name) of the csv file containing the survey results (e.g. “Data.csv” in the root directory or other files with the same file structure).  Then the minimum and maximum number of clusters to be tested is asked.  Next, a few functions checking the path, extension and table structure are executed.

After the checking process, the dataset is loaded and transformed.  The optimal number of clusters to be used is generated based on a statistical indicator.  Then the data are fitted with LCA to form the clusters and some further analysis is conducted.  Finally, output csv files and visualisation are generated.

*check_file()*

This function checks whether the path and file specified by the user exists and whether it is a csv file.  If not, ValueError will be raised.

*check_table()*

This function checks the table structure of the input csv file.  Firstly, the columns "Serial", "Area", "Age", "Sex", "Q1", "Q2", "Q3", "Q4", "Q5" must exist.  Otherwise, KeyError will be raised.  Secondly, the response to "Area" and "Age" must be between 1 and 3, and that to "Sex" must be between 1 and 2.  Otherwise, ValueError will be raised.

*check_cluster()*

This function checks the range of the number of clusters entered by the user.  The numbers must be integers between 2 and 10, and the maximum must be greater than the minimum.  Otherwise, ValueError will be raised.

*load_transform()*
This function loads the csv file as a dataframe and creates two subsets, namely “demo” on the demographic variables and “Q” on the question variables such that LCA can be conducted on the question variables only.  Records with responses “NA” are dropped.

*decide_cluster_num()*
The number of clusters to be used is often determined based on the nature of the research, supplemented by indices like Bayesian Information Criterion (BIC), which is an index of how well a model fits and seeks to balance the complexity of the model against the sample size.  The smaller the BIC, the better the model fitness.

In this project, for simplicity, the optimal number of clusters is selected automatically by the program without regard to the nature of research.

This function fits the data to the LCA model using the number of clusters which is within the range specified by the user.  It then compares the BIC for each model.  For instance, if a minimum of 2 and a maximum of 5 are specified by the users, the program fits the model with 2, 3, 4 and 5 clusters and selects the one with the lowest BIC.  The number of clusters is then returned.

*cluster_analysis()*

Feeding on the number of clusters to be used, this function fits the model using model.fit( ) in the StepMix library.  A cluster number (i.e. 0,1,2 for a 3-cluster model) is assigned to each of the records by model.predict( ) as a new column in the question dataframe “Q”.  For further analysis, the demographic variables in dataframe “demo” are merged back to “Q” using “serial” as the key.  The combined file is exported as “combined.csv” to facilitate users in conducting further analysis.

*cluser_mean()*

This function calculates the average value of Q1 to Q5 within each cluster and prints out the cluster means.  If the scale in the original dataset is consistent, the cluster mean is useful for interpretation.  For example, respondents in a certain cluster may be more positive or negative towards the questions than those in other clusters.

*summarise()*

This function calculates the percentage distribution across clusters within each demographic variable (e.g. the percentage share of cluster 0, 1, 2 … among all males).  Summary tables by demographic variable are exported as separate csv files using a loop.  A dictionary has been created to map the coded values to textual labels to improve the readability of the outputs.

*visualise()*

This function serves to export 3 scatter plots as png files, one for “area” vs “age” and the other for “area” vs “sex”.  Since the demographic variables are categorical, respondents with the same characteristics (e.g. female aged 65+) will be totally overlapped and it is difficult to display the relative size of the clusters, which is unlike continuous variables.  To help visualise the relative size and distribution of the clusters in different demographic groups, random noise is generated so as to “separate the dots” for visualisation.

*test_project.py*

This unit test file serves to test the 3 checking functions in “project.py”, i.e. check_file(), check_table() and check_cluster().  The aspects to be checked as detailed in the function descriptions above are incorporated in the unit test.  For check_table(), some dummy files, viz.  “wrong.csv” (one column missing) and “wrong2.csv” (one value out of range) are saved in the same directory for testing purpose.




