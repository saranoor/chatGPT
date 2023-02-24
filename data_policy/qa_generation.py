import openai
API_KEY = '' # Add your API key here
openai.api_key = API_KEY
model = 'davinci'
def get_questions(context):
    try:
        response = openai.Completion.create(
            prompt=f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            #prompt="Write questions based on text below: Principal Test Engineer to Associate Test Architect – Promotion Criteria • Scoring Matrix Confidential and Prepared by Human Resources Department 13 Support Departments Promotion Policy Policy Name Support Departments Promotion Policy Policy Group Human Resources Issuing Authority Human Resources Department Version v.11.6.1 Syeda Sana Hussain Approved By Approval Date 11/30/2021 Senior Director Human Resources Revision Date - Original Date 11/30/2021 Revision Frequency Annually V. OBJECTIVE / PURPOSE As the company scales and grows to take on new operational challenges, it is imperative to have a more robust mechanism in place for different aspects of the organization. The objective of this document is to provide guidelines to further strengthen the selection/nomination and promotion criteria of support departments at 10Pearls. VI. SCOPE This policy is applicable on all employees working in the support departments. VII. PROCESS II.I Eligibility Criteria Promotion shall be based on overall experience, attitude towards work, and abilities to fit in a higher-level position. • An employee must be full-time confirmed and have completed a minimum of two years in a particular designation before being nominated for promotion to the next designative level. • Only employees falling in Grade 3 of a particular designation can be nominated. For exceptional resources, Grade 2 can also be considered but must be accompanied by a very strong recommendation note. II.III Evaluation • Managers and above shall nominate employees based on their performances upon initiation of nomination process in every appraisal cycle. II.IV Decision Making & Feedback • These nominations are subject to Management discretion/approval based on Employee’s consistent performance in accordance with expectations in their specific roles. Confidential and Prepared by Human Resources Department 14",
            model='text-davinci-003',
            temperature=0.1,
            max_tokens=3500,
        )
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return "Could not generate anything"
import csv
file = open('Promotion_Policy.txt')
doc=file.read()
doc=doc.strip()
doc=doc.replace(r"\s*","")
doc=" ".join(doc.split())
print(len(doc)/3)
print(get_questions(doc[0:round(len(doc)/8)]))
print(get_questions(doc[2222:4444]))
print(get_questions(doc[4444:6666]))
print(get_questions(doc[6666:8888]))
print(get_questions(doc[8888:11000]))
print(get_questions(doc[11000:13000]))
print(get_questions(doc[13000:15000]))
print(get_questions(doc[15000:17000]))
print(get_questions(doc[17000:19000]))
print(get_questions(doc[19000:20000]))
print(get_questions(doc[20000:22000]))

#print(get_questions("Principal Test Engineer to Associate Test Architect – Promotion Criteria • Scoring Matrix Confidential and Prepared by Human Resources Department 13 Support Departments Promotion Policy Policy Name Support Departments Promotion Policy Policy Group Human Resources Issuing Authority Human Resources Department Version v.11.6.1 Syeda Sana Hussain Approved By Approval Date 11/30/2021 Senior Director Human Resources Revision Date - Original Date 11/30/2021 Revision Frequency Annually V. OBJECTIVE / PURPOSE As the company scales and grows to take on new operational challenges, it is imperative to have a more robust mechanism in place for different aspects of the organization. The objective of this document is to provide guidelines to further strengthen the selection/nomination and promotion criteria of support departments at 10Pearls. VI. SCOPE This policy is applicable on all employees working in the support departments. VII. PROCESS II.I Eligibility Criteria Promotion shall be based on overall experience, attitude towards work, and abilities to fit in a higher-level position. • An employee must be full-time confirmed and have completed a minimum of two years in a particular designation before being nominated for promotion to the next designative level. • Only employees falling in Grade 3 of a particular designation can be nominated. For exceptional resources, Grade 2 can also be considered but must be accompanied by a very strong recommendation note. II.III Evaluation • Managers and above shall nominate employees based on their performances upon initiation of nomination process in every appraisal cycle. II.IV Decision Making & Feedback • These nominations are subject to Management discretion/approval based on Employee’s consistent performance in accordance with expectations in their specific roles. Confidential and Prepared by Human Resources Department 14"))
#print("Policies are meant to keep people organized and organization managed")