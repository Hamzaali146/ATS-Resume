from django.shortcuts import render
from PyPDF2 import PdfReader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool, WebsiteSearchTool
from crewai import Crew, Process, Agent, Task
# Create your views here.

load_dotenv(find_dotenv())
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    temperature = 0.5,
    model_name = "llama-3.1-70b-versatile"
)

def index(request):
    return render(request,'index.html')

def signin(request):
    return render(request,'signin.html')

def analyzer(request):
    return render(request,'analyzer.html')

def builder(request):
    return render(request,'res_select.html')

@csrf_exempt
def getText(request):
    if request.method == 'POST':
        try:
            jobDesc = request.POST.get('desc')
            pdfFile = request.FILES.get('pdfFile')
            if pdfFile:
                reader = PdfReader(pdfFile)
                text = ''
                for page in reader.pages:
                    text+=page.extract_text()

                # combined_content = f"Job Description: {jobDesc}\n\nPDF Content: {text}"
                # print(llm.invoke("Hello"))
                try:
                    job_requirements_researcher, resume_swot_analyser, graph_analyser = agentsGo(llm)
                    research, resume_swot_analysis, graph_analysis = tasksGo(jobDesc, text)
                    # crew = Crew(
                    #     agents=[job_requirements_researcher, resume_swot_analyser, graph_analyser],
                    #     tasks=[research, resume_swot_analysis, graph_analysis],
                    #     verbose=1,
                    #     process=Process.sequential
                    # )
                    # result = crew.kickoff()
                    result=llm.invoke(f"Hi my name is hamza please analyze my resume {text}")
                    print(result.content)  # Log the result
                    return JsonResponse({'content': result.content.replace("*","")}, status=200)
                except Exception as e:
                    print(f"Error in agent/task processing: {str(e)}")  # Log error details
                    return JsonResponse({'content': str(e)}, status=500)

        except Exception as e:
            return JsonResponse({'content': str(e)}, status=500)
    
    return JsonResponse({'content':"Invalid Json Response"},status = 400)


def agentsGo(llm):
    """This Function is Basically making Agents the first agent name "job_requirements_researcher" is using tools like SerperDEV tool which is used to access the whole internet by their API and next agent is doing SWOT Analysis on that Resume given by the user. """
    search_tool = SerperDevTool()

    web_rag_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="llama-3.1-70b-versatile",
                temperature = 0.5
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2", 
                ),
            ),
        )
    )
    job_requirements_researcher = Agent(
                                            role='Market Research Analyst',
                                            goal='Provide up-to-date market analysis of industry job requirements of the domain specified',
                                            backstory='An expert analyst with a keen eye for market trends.',
                                            tools=[search_tool, web_rag_tool],
                                            verbose=True,
                                            llm=llm,
                                            max_iters=1
                                        )
    
    resume_swot_analyser = Agent(
                                    role='Resume SWOT Analyser',
                                    goal=f'Perform a SWOT Analysis on the Resume based on the industry Job Requirements report from job_requirements_researcher and provide a json report.',
                                    backstory='An expert in hiring so has a great idea on resumes',
                                    verbose=True,
                                    llm=llm,
                                    max_iters=1,
                                    allow_delegation=True
                            )

    graph_analyser = Agent(
                                    role='csv specialist',
                                    goal=f'just connvert report of Resume SWOT Analyser into csv',
                                    backstory='An expert in making dataframe',
                                    verbose=True,
                                    llm=llm,
                                    max_iters=1,
                                    allow_delegation=True
                            )



    return job_requirements_researcher,resume_swot_analyser,graph_analyser


def extractTextFromResume(res):
    reader=pdf.PdfReader(res)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def tasksGo(jd,resumeContent):
    job_requirements_researcher,resume_swot_analyser,graph_analyser = agentsGo(llm)
    research = Task(

        description=f'For Job Position of Desire: {jd} research to identify the current market requirements for a person at the job including the relevant skills, some unique research projects or common projects along with what experience would be required. For searching query use ACTION INPUT KEY as "search_query"',
        expected_output='A report on what are the skills required and some unique real time projects that can be there which enhances the chance of a person to get a job',
        agent=job_requirements_researcher
    )
    resume_swot_analysis = Task(

        description=f'Resume Content: {resumeContent} \n Analyse the resume provided and the report of job_requirements_researcher to provide a detailed SWOT analysis report on the resume along with the Resume Match Percentage and Suggestions to improve',
        expected_output="""A JSON formatted report as follows: "candidate": candidate, "strengths":[strengths], "weaknesses":[weaknesses], "opportunities":[opportunities], "threats":[threats], "resume_match_percentage": resume_match_percentage, "suggestions": "suggestions",technical_Skill_percentage,soft_skill_percentage
        ### NO PREAMBLE AND NO COMMENTS IN JSON FILE FILE SHOULD BE IN JSON OBJECT NO STRING means you dont need to add json object in string in JSON FILE###
        """,
        agent=resume_swot_analyser,
        output_file='resume-report/resume_review.json'
    )

    graph_analysis = Task(

        description=f'Your Job is to convert resume_swot_analysis report to convert into csv .',
        expected_output="""CSV file having field candidate,resume_match_percentage,technical_Skill_percentage,soft_skill_percentage
        ### NO PREAMBLE AND NO COMMENTS IN CSV FILE FILE SHOULD BE IN CSV STYLE NO STRING means you dont need to add CSV object in string in CSV FILE###
        """,
        agent=graph_analyser,
        output_file='visualization.csv'
    )
    return research,resume_swot_analysis,graph_analysis