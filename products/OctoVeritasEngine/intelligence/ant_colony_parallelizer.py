import concurrent.futures
from typing import List, Any, Dict, Callable

class AntColonyParallelizer:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def execute_parallel(self, jobs: List[Dict[str, Any]], worker_func: Callable) -> List[Any]:
        """
        Executes injection jobs in parallel like an ant colony.
        """
        results = []
        # Sort by priority if available
        sorted_jobs = sorted(jobs, key=lambda x: x.get('priority', 1), reverse=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_job = {executor.submit(worker_func, job): job for job in sorted_jobs}
            for future in concurrent.futures.as_completed(future_to_job):
                job = future_to_job[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    print(f"Job {job.get('name')} generated an exception: {exc}")
                    results.append(None)

        return results
