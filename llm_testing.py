
import utils


if __name__ == "__main__":

    sample_uuid = "first_test"
    termianl = utils.LLMTesting(cv_file="Curriculum_Vitae_Jan24.pdf",
                                profile_file="expected_cv.json",
                                poistion_text="""
                                Do you want to be a Data Scientist on an elite Data Science team? Do you want to build Data Analytics for a global Security Product? Do you want your work to be impactful on millions of users?
                                Join us and become part of a winning Data Science team that builds the “brain” of one of Microsoft’s most exciting security products, Microsoft Defender for Endpoint (MDE). As cyber-attacks have become more sophisticated, MDE helps enterprises detect, investigate, and automatically disrupt advanced attacks and data breaches on their networks. Our team is responsible for developing and deploying Machine Learning (ML) models that protect organizations worldwide and owning Data Analytics systems that facilitate data-driven decisions and operational excellence.

                                If you are a talented Data Scientist with excellent analytical, statistical, and data-visualization skills, who is passionate about applying Data Science to drive a revolutionary cyber-security product, we would like to talk to you!

                                Microsoft’s mission is to empower every person and every organization on the planet to achieve more. As employees we come together with a growth mindset, innovate to empower others, and collaborate to realize our shared goals. Each day we build on our values of respect, integrity, and accountability to create a culture of inclusion where everyone can thrive at work and beyond.

                                Responsibilities

                                Collaborate with Security experts and other stakeholders to define Business metrics. 
                                Work with data engineers to implement these metrics over Big Data sources. 
                                Create and maintain dashboards and visualizations. 
                                Conduct data analysis and present insights to the leadership team and stakeholders. 
                                Develop Anomaly Detection and monitoring solutions to ensure operation excellence of AI and other systems in MDE. 

                                Qualifications

                                2+ Years of experience as a Data Scientist/Data Analyst 
                                Good coding skills in Python 
                                Excellent logical reasoning and problem-solving skills
                                A university degree in technical discipline
                                Interest in Data Science and Cyber Security 
                                A team player with great communication skills and drive for results 

                                Preferred Qualifications

                                Experience in Cyber Security (big plus!) 
                                Experience with Big Data systems
                                Azure Data Explorer, KQL
                                C# 
                                
                                """,how_to_act=[
                                    "Be truthful, don't invent any information."
                                ])

    utils.pdf_to_user_data(termianl)

    # ask the user about the data
    utils.verify_user_data(termianl)

    # ask the user to upload position snippet
    utils.position_snippet_to_position_data(termianl)

    # overcome gaps
    utils.overcome_gaps(termianl)

    # to pdfs
    utils.to_pdfs(termianl)

    termianl.wrap_up(uuid=sample_uuid)













