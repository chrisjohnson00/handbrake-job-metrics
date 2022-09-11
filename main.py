import pygogo as gogo
from metric_collector.metric_collector import MetricCollector

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Starting")
    mc = MetricCollector()
    total_jobs = mc.get_total_jobs()
    logger.info(f"Job Count {total_jobs}")
    completed_jobs = mc.get_completed_jobs()
    logger.info(f"Completed Jobs {completed_jobs}")
    failed_jobs = mc.get_failed_jobs()
    logger.info(f"Failed Jobs {failed_jobs}")
    running_jobs = mc.get_running_jobs()
    logger.info(f"Running Jobs {running_jobs}")
    pending_jobs = mc.get_pending_jobs()
    logger.info(f"Pending Jobs {pending_jobs}")


if __name__ == '__main__':
    main()
