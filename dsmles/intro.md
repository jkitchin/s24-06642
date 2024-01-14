# Data science and machine learning in engineering and science

These notes are from a short (1/2 semester) course I have taught for a few years at CMU. It is a brief introduction to data science and machine learning in engineering and science. I assume you have some basic scientific programming skill in Python. If not, you should familiarize yourself with [pycse](https://kitchingroup.cheme.cmu.edu/pycse). Everything here builds on that content.

In some ways data science and machine learning is just next level scientific programming. You don't technically need much that isn't part of the pycse notes. However, it quickly gets tedious to reimplement these ideas over and over, and people who do this work a lot developed new libraries like Pandas and scikit-learn to abstract out and reduce repetitive code.

![img](dsmles-hydra.png)

The path we take is to first build on {{ pycse }} and show how to leverage numpy arrays for data science tasks. This leads us to use Pandas to mitigate some complications we have with just arrays. We show how to use numpy for linear regression, and then transition to scikit-learn to get an easier interface for all kinds of regression models and data analysis tasks.

It is not possible to cover all aspects of this fast-moving and growing field. Instead, our aim here is to see how this field builds on foundational aspects of {{ pycse }}, and introduce some main ideas in data science and machine learning in engineering and science.