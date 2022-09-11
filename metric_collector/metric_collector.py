from kubernetes import client, config
import os
from prometheus_client.core import GaugeMetricFamily as Gauge


class MetricCollector:
    def __init__(self):
        if os.environ.get('USE_K8S_CONFIG_FILE'):
            config.load_kube_config()
        else:
            config.load_incluster_config()
        self.batch_v1_client = client.BatchV1Api()
        self.core_v1_client = client.CoreV1Api()
        self.namespace = "handbrake-jobs"
        self.job_label_selector = "app=handbrake-job"
        self.job_list = None
        self.pod_list = None

    def get_total_jobs(self):
        job_list = self.get_all_jobs()
        return len(job_list.items)

    def get_all_jobs(self):
        if not self.job_list:
            self.job_list = self.batch_v1_client.list_namespaced_job(namespace=self.namespace,
                                                                     label_selector=self.job_label_selector)
        return self.job_list

    def get_all_job_pods(self):
        if not self.pod_list:
            self.pod_list = self.core_v1_client.list_namespaced_pod(namespace=self.namespace,
                                                                    label_selector=self.job_label_selector)
        return self.pod_list

    def get_completed_jobs(self):
        job_list = self.get_all_jobs()
        count = 0
        for job in job_list.items:
            status = job.status
            if status.completion_time:
                count += 1
        return count

    def get_failed_jobs(self):
        job_list = self.get_all_jobs()
        count = 0
        for job in job_list.items:
            status = job.status
            conditions = status.conditions
            if conditions:
                for condition in conditions:
                    if condition.type == "Failed":
                        count += 1
        return count

    def get_running_jobs(self):
        pod_list = self.get_all_job_pods()
        count = 0
        for pod in pod_list.items:
            status = pod.status
            phase = status.phase
            if phase == "Running":
                count += 1
        return count

    def get_pending_jobs(self):
        pod_list = self.get_all_job_pods()
        count = 0
        for pod in pod_list.items:
            status = pod.status
            phase = status.phase
            if phase == "Pending":
                count += 1
        return count

    def collect(self):
        total = Gauge('handbrake_job_total_count', 'The total count of Handbrake Encoding jobs')
        running = Gauge('handbrake_job_running_count', 'The count of running Handbrake Encoding jobs')
        pending = Gauge('handbrake_job_pending_count', 'The count of pending Handbrake Encoding jobs')
        failed = Gauge('handbrake_job_failed_count', 'The count of failed Handbrake Encoding jobs')

        total.add_metric(value=self.get_total_jobs(), labels=[])
        running.add_metric(value=self.get_running_jobs(), labels=[])
        pending.add_metric(value=self.get_pending_jobs(), labels=[])
        failed.add_metric(value=self.get_failed_jobs(), labels=[])

        yield total
        yield running
        yield pending
        yield failed
