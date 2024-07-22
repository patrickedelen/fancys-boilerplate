# fancys-boilerplate
FastApi Nextjs CelerY Sqlalachemy THE BEST


# try it out
- make sure you have docker installed
- initialize the pipenv with `pipenv install --dev`
- build the containers with `docker compose -f docker-compose.development.yaml build`
- run everything with `docker compose -f docker-compose.development.yaml up`


# endpoints
- `localhost:8000/add/{number_1}/{number_2}` - returns a task ID
- `localhost:8000/result/{task_id}` - returns the completed result

