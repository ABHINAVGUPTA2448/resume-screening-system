def read_job_description(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        job_description = file.read()

    return job_description


jd_path = "data/job_descriptions/ml_engineer.txt"

jd_text = read_job_description(jd_path)

print("----- JOB DESCRIPTION -----")
print(jd_text)