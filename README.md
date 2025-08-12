# Alplakes AI Summaries

Producing AI generated conditions summaries for the Alplakes website

Taking inspirations from: https://medium.com/@rob_cowling/%EF%B8%8Fhow-to-prompt-llms-to-craft-weather-summaries-for-flood-forecasting-cd9936828daf

## Docker

### Docker build

docker build -t eawag/ai-summaries:1.0.0 .

### Docker run

docker run -e OPENAI_API_KEY=XXXX -v /home/user/alplakes-ai-summaries:/repository --rm eawag/ai-summaries:1.0.0 -u -b XXXX -i XXXX -k XXXX