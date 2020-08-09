FROM python:3
ADD classify.py /
RUN pip install numpy
RUN pip install torch
RUN pip install torchvision
env DATASET=mnist
env TYPE=ff
CMD [ "python", "./classify.py" ]