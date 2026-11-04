---
title: Data Analysis 12-10 — Linear regression model (1)
date: 2026-10-12
session: 10
wispr: https://notes.wisprflow.ai/shared/alhj5VyuHX4oLzAWRXD2PUfhr1o7rd6YtzsYtAFY198
---
Introduction to regression analysis: model structure, coefficient interpretation, key assumptions (exogeneity, homoskedasticity), reading regression tables and hypothesis testing.

### Regression Fundamentals
- Regression estimates the average of y conditional on x via an intercept and slope; individuals deviate by their error term
- A good project question fits in two lines and names the dependent and main independent variable
- Simple model assumes constant returns; non-linearities come next class
    - Theory, not the regression, should drive what goes into the model
- Intercept is average y when all x equal 0; slope is change in y from a unitary increase in x

### Key Assumptions and Bias
- **Zero conditional mean (exogeneity)**: x must be uncorrelated with the error term to make causal claims
    - Ability bias in wage on education is the classic violation
    - Omitted variables uncorrelated with x do not bias causal estimates
- Sample selection can make estimates differ from the population; observations should be independent
- Residual plot of food expenditure shows heteroskedasticity; **always run regressions with robust standard errors**

### Reading Output and Hypothesis Testing
- OLS minimizes the sum of squared residuals; tables report coefficient, standard error, t-statistic, p-value
- Food example: 100 dollar increase in weekly income linked to 10.21 dollars more food spending; intercept 83.42
    - **Check variable scale (hundreds of dollars), a typical exam trap**
- Default test is H0: beta = 0; alpha conventionally 0.05; say 'reject' or 'fail to reject', never 'accept'
    - p-value 0.062: significant at 10% not 5%; t-stat rule of thumb about 2 (2.06) at 5%
- Type I error controlled by alpha; Type II reduced only through more observations and power

### Multiple Regression
- Adding regressors removes confounders from the error term; coefficients read holding other variables fixed (ceteris paribus)
