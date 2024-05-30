from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric,ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase
from utils.extract_cv_data import core_run
import json

expected_json = {
    "personal_info": {
        "firstname": "[Your First Name]",
        "lastname": "[Your Last Name]",
        "email": "[Your Email Address]",
        "phone": "[Your Phone Number]",
        "address": "[Your Address]",
        "willing_to_relocate": "[Is willing to relocate]",
        "linkedin": {
            "link": "[Your LinkedIn Profile Link]",
            "username": "[Your LinkedIn Username]",
        },
        "github": {
            "link": "[Your GitHub Profile Link]",
            "username": "[Your GitHub Username]",
        },
        "additional_websites": ["[Additional Website]", "[Additional Website]"],
    },
    "education": [
        {
            "degree": "[Degree Type]",
            "institution": "[University or College Name]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "graduation_date": "[Graduation Date]",
            "grade": "[Grade or GPA]",
        },
        {
            "degree": "[Degree Type]",
            "institution": "[University or College Name]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "graduation_date": "[Graduation Date]",
            "grade": "[Grade or GPA]",
        },
    ],
    "experience": [
        {
            "title": "[Job Title]",
            "company": "[Company Name]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "end_date": "[End Date or 'Ongoing']",
            "responsibilities": ["[Responsibility]", "[Responsibility]"],
            "keywords": ["[Extracted Keyword]", "[Extracted Keyword]"],
        },
        {
            "title": "[Job Title]",
            "company": "[Company Name]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "end_date": "[End Date or 'Ongoing']",
            "responsibilities": ["[Responsibility]", "[Responsibility]"],
            "keywords": ["[Extracted Keyword]", "[Extracted Keyword]"],
        },
    ],
    "skills": [
        {"name": "[Skill]", "level": "[Years]"},
        {"name": "[Skill]", "level": "[Years]"},
    ],
    "certifications": ["[Certification Name]", "[Certification Name]"],
    "projects": [
        {
            "title": "[Project Title]",
            "description": "[Project Description]",
            "technologies": [
                "[Technology Used]",
                "[Technology Used]",
                "[Technology Used]",
            ],
            "github_link": "[GitHub Repository Link]",
        },
        {
            "title": "[Project Title]",
            "description": "[Project Description]",
            "technologies": [
                "[Technology Used]",
                "[Technology Used]",
                "[Technology Used]",
            ],
            "github_link": "[GitHub Repository Link]",
        },
    ],
    "languages": [
        {
            "language": "[Language]",
            "level": "[Level of Proficiency (e.g., Native, Fluent, Intermediate, Basic)]",
        },
        {
            "language": "[Language]",
            "level": "[Level of Proficiency (e.g., Native, Fluent, Intermediate, Basic)]",
        },
        {
            "language": "[Language]",
            "level": "[Level of Proficiency (e.g., Native, Fluent, Intermediate, Basic)]",
        },
    ],
    "achievements": [
        {"achievement": "[Achievement Description]", "date": "[Date of Achievement]"},
        {"achievement": "[Achievement Description]", "date": "[Date of Achievement]"},
    ],
    "publications": [
        {
            "title": "[Publication Title]",
            "publish_date": "[Publication Date]",
            "published_venue": "[Published Venue if published]",
            "co_authors": "[ Co-Authors]",
            "description": "[Publication Description]",
            "publication": "[Where Published]",
            "link": "[Publication Link]",
        },
        {
            "title": "[Publication Title]",
            "publish_date": "[Publication Date]",
            "published_venue": "[Published Venue if published]",
            "co_authors": "[ Co-Authors]",
            "description": "[Publication Description]",
            "publication": "[Where Published]",
            "link": "[Publication Link]",
        },
    ],
    "volunteer_experience": [
        {
            "organization": "[Organization Name]",
            "role": "[Volunteer Role]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "end_date": "[End Date or 'Ongoing']",
            "description": "[Description of Volunteer Work]",
        },
        {
            "organization": "[Organization Name]",
            "role": "[Volunteer Role]",
            "location": "[City, Country]",
            "start_date": "[Start Date]",
            "end_date": "[End Date or 'Ongoing']",
            "description": "[Description of Volunteer Work]",
        },
    ],
    "hobbies": ["[Hobby]", "[Hobby]", "[Hobby]"],
    "summary": "[Summary of Yourself]",
}

extracted_text = """Sefi Erlich
TLV, Israel - willing to relocate H +972 524 307 093 B erlichsefi@gmail.com Curriculum Vitae Í github.com/erlichsefi
Lead Applied Data Scientist with experience of over five years in the tech industry in Time Series, NLP, and Generative. Four years of experience in academic research: Two years of experience in ML and two years in algorithmic game theory research. Additionally, one year as DS Guild manager. Entrepreneur mindset.
Skills
{ Programming Languages: Java (3 years), Python (5 years)
{ Cload Platforms: AWS (2 years)
{ Languages: Hebrew - Native. English - high level.
{
{
{
{
{
{
Feb 2019 - Data Scientist, ClickSoftware (Acquired by Salesforce.), Petah Tikva.
Jan 2020 "Full Stack" Data Scientist, working on Multivariate Time Series forecasting in a Multi-tenant environment.
Development of an e2e dockerized pipeline (periodic training, data processing, and serving) Technologies: AWS,Docker,python,Keras,Tensorflow,Dask,Git.
Nov 2016 - AI Researcher, Ariel University, Ariel.
Oct 2018 -"Machine learning for football match violence prediction"
-"Classification and enrichment of encrypted traffic Using Machine Learning algorithms" Oct 2014 - Research Assistant, Ariel University, Ariel.
Jul 2016 Researching Malware network behavior using Wireshark and Python, Design and development of a centered intrusion detection system in Java and Python, which uses Multiparty Computation in C++ and testing in DETER (Cybersecurity cloud). Dr. Eran Omri and Dr. Amit Dvir.
Education
2016 - 2018 M.Sc Computer Science, Ariel University, 93, Full scholarship.
Thesis: Development of a Polynomial Time Algorithm for an deterministic automated negotiation AI in a various of scenarios.
B.Sc Mathematics and Computer Science, Ariel University, 92.7, Twice Dean Honor, Magna Cum Laude.
Outstanding Final Project "Malware detection system" with Dr. Eran Omri and Dr. Amit Dvir.
publications
Previous Employment
Jan 2020 - Lead Data Scientist, Salesforce - Several positions , Tel-Aviv/Remote.
Present
Workforce Management: E2E Data Scientist (customers until back-end) Multivariate Time Series forecast- ing Service. Development for an E2E dockerized pipeline for Model Deployment and Serving. Technolo- gies:Mongo,Docker,python,Sklearn,Pandas,Numpy,Git,etc.
Einstein Language Intelligence: Applied Data Scientist, Deploying language models in production. Devel- oping the first generative GA Salesforce application. Technologies: Tensorflow, Keras, Torch, Huggingface, LLM, Embedding, Autonomous agents. Data Cloud: Applied Data Scientist, Generative Database applica- tions.
2013 - 2016
{ "Negotiation Strategies for Agents with Ordinal Preferences: Theoretical Analysis and Human Study". Artificial Intelligence, Elsevier 2024
{ "STWSN: A Novel Secure Distributed Transport Protocol for Wireless Sensor Networks". Dr. Amit Dvir (published in IJCS18’)
{ "Negotiation Strategies for Agents with Ordinal Preferences",Thesis. supervision of Prof. Sarit Krus and Dr. Noam Hazon. (published in COMSOC18’ and IJCAI18’)
{ "Heterogeneous SDN controller placement problem—The Wi-Fi and 4G LTE-U case" A. Zilberman at el."""


def test_examples():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

    extracted_json = core_run(expected_json, extracted_text)

    test_cases = [
        LLMTestCase(
            input=json.dumps(expected_json[key], indent=4),
            # Replace this with the actual output from your LLM application
            actual_output=json.dumps(extracted_json[key], indent=4),
            retrieval_context=[extracted_text],
        )
        for key in extracted_json
    ]

    evaluate(test_cases, [answer_relevancy_metric])
