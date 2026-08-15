# AWS Deployment Baseline

The portable image maps to ECS/Fargate services with RDS MariaDB, ElastiCache Redis/Valkey, private subnets, an Application Load Balancer, Secrets Manager and CloudWatch Logs. The supplied task definition is the web-role baseline; create separate task definitions by replacing the command with `websocket`, `scheduler`, `worker-short`, `worker-long` or `migrate`.

The ECS task definition must retain explicit container health checks because ECS evaluates task-definition health checks. Store `DB_PASSWORD` and `SITE_ENCRYPTION_KEY` in Secrets Manager, not task-definition environment values.

This template is not applied automatically and creates no AWS resources.
