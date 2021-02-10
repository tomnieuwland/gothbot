FROM python
MAINTAINER Tom Nieuwland thomasnieuwland19@gmail.com

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/gothbot
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ARG DISCORD_TOKEN
ENV TOKEN=${DISCORD_TOKEN}
CMD python ./run.py -t $TOKEN

