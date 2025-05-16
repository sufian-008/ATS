import numpy as np
from sklearn.cluster import KMeans


JOB_DATA = [
    {
        "title": "Python Developer",
        "skills": ["Python", "Django", "SQL"],
        "location": "remote",
        "salary": 35000
    },
    {
        "title": "Frontend Developer",
        "skills": ["JavaScript", "React", "CSS"],
        "location": "onsite",
        "salary": 30000
    },
    {
        "title": "ML Engineer",
        "skills": ["Python", "Machine Learning", "TensorFlow"],
        "location": "remote",
        "salary": 50000
    },
    {
        "title": "Data Analyst",
        "skills": ["Python", "SQL", "Excel"],
        "location": "hybrid",
        "salary": 40000
    },
    {
        "title": "Backend Developer",
        "skills": ["Python", "Flask", "Docker"],
        "location": "remote",
        "salary": 42000
    },
    {
        "title": "DevOps Engineer",
        "skills": ["AWS", "Docker", "CI/CD"],
        "location": "onsite",
        "salary": 48000
    },
    {
        "title": "Full Stack Developer",
        "skills": ["JavaScript", "Python", "React", "Django"],
        "location": "remote",
        "salary": 53000
    }
]



def skill_match_score(job_skills, user_skills):
    return len(set(job_skills) & set(user_skills))



def prepare_job_features(JOB_DATA):
    locations = ['remote', 'onsite', 'hybrid']
    job_features = []

    for job in JOB_DATA:
        skill_count = len(set(job['skills']))
        location = locations.index(job['location'])
        salary = job['salary']

        job_features.append([skill_count, location, salary])

    return np.array(job_features)



def apply_kmeans(job_features, num_clusters=3):
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(job_features)
    return kmeans.labels_



def recommend_job(user_input, num_clusters=3):
    user_skills = user_input.get("skills", [])

    if not user_skills:
        return ["No skills provided."]

    # job feature of preapred korteteci
    job_features = prepare_job_features(JOB_DATA)
    job_clusters = apply_kmeans(job_features, num_clusters)

    # cluster label korchi
    for i, job in enumerate(JOB_DATA):
        job['cluster'] = job_clusters[i]

    # Job skill match kore scoring korteci
    scored_jobs = []
    for job in JOB_DATA:
        score = skill_match_score(job["skills"], user_skills)
        if score > 0:
            scored_jobs.append((score, job))

    if not scored_jobs:
        return ["No matching jobs found."]


    scored_jobs.sort(reverse=True, key=lambda x: x[0])
    top_jobs = [job['title'] for _, job in scored_jobs[:3]]


    top_cluster = scored_jobs[0][1]['cluster']
    cluster_jobs = [job['title'] for job in JOB_DATA if job['cluster'] == top_cluster]

    return cluster_jobs[:3]
