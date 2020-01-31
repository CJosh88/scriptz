#not sure if this would need to be run every time or just once?
install.packages("relaimpo") 

#loads package
library(relaimpo) 

#creating some random data with 5 variables for regression
data <- data.frame(replicate(5, sample(0:10,1000, rep=T))) 

#create ordinary regression first
regression <- lm(formula = X1 ~ X2+X3+X4+X5, data = data, na.action = na.omit) 

#create shapley reg
shap <- relaimpo::calc.relimp(regression, type="lmg", rela = T, rank = T)

#extract relevant info from shap object
shap@nobs #sample size
shap@R2 #R-square
shap@lmg #shap importance (standardized)