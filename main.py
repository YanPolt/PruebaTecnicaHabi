import os
from dagster import job, op, schedule, AssetSelection, define_asset_job, ScheduleEvaluationContext, configurable_job, RunRequest

@op(config_schema={"scheduled_date": str})
def configurable_op(context):
    context.log.info(context.op_config["scheduled_date"])

@schedule(job=configurable_job, cron_schedule="0 0 * * *")
def configurable_job_schedule(context: ScheduleEvaluationContext):
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return RunRequest(
        run_key=None,
        run_config={
            "ops": {"configurable_op": {"config": {"scheduled_date": scheduled_date}}}
        },
        tags={"date": scheduled_date},
    )

@job
def configurable_job():
    configurable_op()