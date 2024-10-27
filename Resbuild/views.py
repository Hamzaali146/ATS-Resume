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

def builderform(request):
    template = request.GET.get('template', 'default')
    request.session['template'] = template
    return render(request,'input.html')

def analyzer(request):
    return render(request,'analyzer.html')

def builder(request):
    return render(request,'res_select.html')

@csrf_exempt
def test(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    phone = request.POST['phone']
    country = request.POST['country']
    city = request.POST['city']
    role = request.POST['role']
    summary = request.POST['summary']
    educationCounter = int(request.POST["educationCounter"])
    skillsCounter=int(request.POST["skillsCounter"])
    coursesCounter=int(request.POST["coursesCounter"])
    languagesCounter=int(request.POST["languagesCounter"])
    internshipsCounter=int(request.POST["internshipsCounter"])
    projectsCounter=int(request.POST["projectsCounter"])
    template = request.session.get('template', 'default')
    
    print(f"education counter will be {educationCounter}")
    education_entries = []
    skill_entries = []
    courses_entries = []
    language_entries = []
    internship_entries = []
    project_entries = []
    profEntries = []
    for i in range(1, educationCounter+1):  
            degree = request.POST.get(f'degree_{i}', "no degree")
            institution = request.POST.get(f'institution_{i}', "no inst")
            date = request.POST.get(f'date_{i}', "no date")
            if degree and institution and date:
                education_entries.append({
                    'degree': degree,
                    'institution': institution,
                    'date': date,
                })
    for i in range(1, skillsCounter+1):  
            skill = request.POST.get(f'skills_{i}', "no skill")
            prof = request.POST.get(f'rating_{i}', "no rating")
            if skill:
                skill_entries.append({
                    'skill': skill,
                })
            if prof:
                profEntries.append({
                    'profeciency':prof
                })
    for i in range(1,coursesCounter+1):  
            course= request.POST.get(f'course_{i}', "no course")
            cinstitution = request.POST.get(f'cinstitution_{i}', "no inst")
            cdate = request.POST.get(f'completiondate_{i}', "no date")
            if course and cinstitution and cdate:
                courses_entries.append({
                    'course': course,
                    'cinstitution': cinstitution,
                    'cdate': cdate,
                })
    for i in range(1, languagesCounter+1):  
            language = request.POST.get(f'language_{i}', "no language")
            proficiency = request.POST.get(f'prof_{i}', "no prof")

            if language and proficiency:
                language_entries.append({
                    'language': language,
                    'proficiency': proficiency,
                })
    for i in range(1, internshipsCounter+1):  
            company = request.POST.get(f'company_{i}', "no company")
            intinstitution = request.POST.get(f'role_{i}', "no role")
            sintdate = request.POST.get(f'sintdate_{i}', "no date")
            lintdate = request.POST.get(f'lintdate_{i}', "no date")
            intdesc = request.POST.get(f'intdesc_{i}', "no description")
            if company and intinstitution and sintdate:
                internship_entries.append({
                    'company': company,
                    'intinstitution': intinstitution,
                    'sintdate': sintdate,
                    'lintdate': lintdate,
                    'intdesc':intdesc,
                })
    for i in range(1, projectsCounter+1):  
            project = request.POST.get(f'project_{i}', "no project")
            projdesc = request.POST.get(f'projdesc_{i}', "no descp")
            projectyr= request.POST.get(f'projectyr_{i}',"no date")
            if project and projdesc and projectyr:
                project_entries.append({
                    'project':project,
                    'projectdesc': projdesc,
                })

    if template =="classic":
        return render(request,'classic.html',{'fname':fname ,'lname':lname,'phone':phone, 'email':email,'country':country,'city':city,'summary':summary,'role':role,'education':education_entries,'skill':skill_entries,'courses':courses_entries,'languages':language_entries,'internships':internship_entries,'projects':project_entries,'template':template})
    elif template =="savvy":
        return render(request,'classic.html',{'fname':fname ,'lname':lname,'phone':phone, 'email':email,'country':country,'city':city,'summary':summary,'role':role,'education':education_entries,'skill':skill_entries,'courses':courses_entries,'languages':language_entries,'internships':internship_entries,'projects':project_entries,'template':template})
    return render(request,'classic.html',{'fname':fname ,'lname':lname,'phone':phone, 'email':email,'country':country,'city':city,'summary':summary,'role':role,'education':education_entries,'skill':skill_entries,'courses':courses_entries,'languages':language_entries,'internships':internship_entries,'projects':project_entries,'template':template})
    print(f"number of education entries {education_entries}" )

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
                    # job_requirements_researcher, resume_swot_analyser, graph_analyser = agentsGo(llm)
                    # research, resume_swot_analysis, graph_analysis = tasksGo(jobDesc, text)
                    # crew = Crew(
                    #     agents=[job_requirements_researcher, resume_swot_analyser, graph_analyser],
                    #     tasks=[research, resume_swot_analysis, graph_analysis],
                    #     verbose=1, 
                    #     process=Process.sequential
                    # )
                    # result = crew.kickoff()
                    result=llm.invoke(f"I am giving you a resume which is {text} give me a proper SWOT ANALYSIS. based on the job Description which is {jobDesc} try to gather more inofrmation and cover all areas!")
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