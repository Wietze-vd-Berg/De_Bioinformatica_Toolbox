import os

from Website.modules.salmon import salmon_handler

def start_salmon_verwerking(kwargs, task_id, tasks, results):
    try:
        tasks[task_id] = {"step": "index", "status": "processing"}

        print(f"[{task_id}] Start Salmon index")
        result = salmon_handler(kwargs, status_callback=lambda step, status: update_step(task_id, step, status, tasks))

        if result['success']:
            tasks[task_id] = {"step": "done", "status": "done"}
            results[task_id] = {
                "success": True,
                "result": result['result'],
                "kwargs": kwargs,
                "fasta_filename": os.path.basename(kwargs['fasta_file_path'])
            }
        else:
            tasks[task_id] = {"step": "error", "status": "error"}
            results[task_id] = {
                "success": False,
                "error": result.get("error", "Onbekende fout"),
                "status_code": 500
            }

    except Exception as e:
        error_trace = traceback.format_exc()
        tasks[task_id] = {"step": "error", "status": "error"}
        results[task_id] = {
            "success": False,
            "error": str(e),
            "trace": error_trace,
            "status_code": 500
        }

    finally:
        try:
            os.remove(kwargs['fasta_file_path'])
            os.remove(kwargs['fastq_file1_path'])
            os.remove(kwargs['fastq_file2_path'])
            os.rmdir(os.path.dirname(kwargs['fasta_file_path']))  # verwijder tijdelijke map
        except Exception as e:
            print(f"Fout bij opruimen: {e}")


def update_step(task_id, step, status, tasks):
    tasks[task_id] = {"step": step, "status": status}