from utils.pdf_util import extract_3


def test_pdf_reader():
    text = extract_3("data_set/Curriculum_Vitae_Jan24.pdf")
    
    keyword_must_contain = [
        "Sefi Erlich",
        "github.com/erlichsefi",
        "erlichsefi@gmail.com",
        "+972 524 307 093",
        "M.Sc Computer Science",
        "Thesis: Development of a Polynomial Time Algorithm for an deterministic automated negotiation AI in avarious of scenarios",
        "B.Sc Mathematics and Computer Science",
        "Ariel University, 92.7, Twice Dean Honor, Magna Cum Laude.",
        "Negotiation Strategies for Agents with Ordinal Preferences: Theoretical Analysis and Human Study",
        #"STWSN: A Novel Secure Distributed Transport Protocol for Wireless Sensor Network",
        "Negotiation Strategies for Agents with Ordinal Preference",
        "Heterogeneous SDN controller placement problem—The Wi-Fi and 4G LTE-U case"
        ]
    for keyword in keyword_must_contain:
        if keyword not in text.replace("\n",""):
            assert False,f"Keyword '{keyword}' not in text"


"""
Sefi ErlichTLV, Israel - willing to relocate(cid:72) +972 524 307 093(cid:66) erlichsefi@gmail.comCurriculum Vitae (cid:205)github.com/erlichsefiLeadAppliedDataScientistwithexperienceofoverfiveyearsinthetechindustryinTimeSeries,NLP,andGenerative.Four years of experience in academic research: Two years of experience in ML and two years in algorithmic gametheory research. Additionally, one year as DS Guild manager. Entrepreneur mindset.Skills Programming Languages: Java (3 years), Python (5 years) Cload Platforms: AWS (2 years) Languages: Hebrew - Native. English - high level.Previous EmploymentJan 2020 - Lead Data Scientist, Salesforce - Several positions , Tel-Aviv/Remote.Present Workforce Management: E2E Data Scientist (customers until back-end) Multivariate Time Series forecast-ing Service. Development for an E2E dockerized pipeline for Model Deployment and Serving. Technolo- gies:Mongo,Docker,python,Sklearn,Pandas,Numpy,Git,etc.Einstein Language Intelligence: Applied Data Scientist, Deploying language models in production. Devel-oping the first generative GA Salesforce application. Technologies: Tensorflow, Keras, Torch, Huggingface,LLM, Embedding, Autonomous agents. Data Cloud: Applied Data Scientist, Generative Database applica-tions.Feb 2019 - Data Scientist, ClickSoftware (Acquired by Salesforce.), Petah Tikva. Jan 2020 "Full Stack" Data Scientist, working on Multivariate Time Series forecasting in a Multi-tenant environment.Development of an e2e dockerized pipeline (periodic training, data processing, and serving)Technologies: AWS,Docker,python,Keras,Tensorflow,Dask,Git.Nov 2016 - AI Researcher, Ariel University, Ariel.Oct 2018 -"Machine learning for football match violence prediction"-"Classification and enrichment of encrypted traffic Using Machine Learning algorithms"Oct 2014 - Research Assistant, Ariel University, Ariel. Jul 2016 Researching Malware network behavior using Wireshark and Python, Design and development of a centeredintrusion detection system in Java and Python, which uses Multiparty Computation in C++ and testing inDETER (Cybersecurity cloud). Dr. Eran Omri and Dr. Amit Dvir.Education2016 - 2018 M.Sc Computer Science, Ariel University, 93, Full scholarship.Thesis: Development of a Polynomial Time Algorithm for an deterministic automated negotiation AI in avarious of scenarios.2013 - 2016 B.Sc Mathematics and Computer Science, Ariel University, 92.7, Twice Dean Honor, Magna Cum Laude.Outstanding Final Project "Malware detection system" with Dr. Eran Omri and Dr. Amit Dvir.publications "Negotiation Strategies for Agents with Ordinal Preferences: Theoretical Analysis and Human Study". ArtificialIntelligence, Elsevier 2024 "STWSN:ANovelSecureDistributedTransportProtocolforWirelessSensorNetworks". Dr. AmitDvir(publishedin IJCS18’) "Negotiation Strategies for Agents with Ordinal Preferences",Thesis. supervision of Prof. Sarit Krus and Dr.Noam Hazon. (published in COMSOC18’ and IJCAI18’) "Heterogeneous SDN controller placement problem—The Wi-Fi and 4G LTE-U case" A. Zilberman at el.

"""