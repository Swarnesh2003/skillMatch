from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Example dataset
data = {
    'Candidate Name': ['John Smith', 'Emily Johnson', 'Michael Williams', 'Sarah Miller', 'Alex Davis'],
    'Skills': ['Java, Python, Software Development',
               'Machine Learning, Python, Data Analysis',
               'Leadership, Finance, Communication',
               'C++, Web Development, Database Management',
               'JavaScript, UI/UX Design, Frontend Development']
}

# Create a DataFrame
df = pd.DataFrame(data)
'''
# Placeholder for course recommendations
courses_data = {
    'Python': ['Python for Beginners', 'Intermediate Python'],
    'Machine Learning': ['Introduction to Machine Learning', 'Advanced ML Concepts'],
    'Data Analysis': ['Data Analysis Fundamentals', 'Advanced Data Analytics']
    # ... and so on
}
'''
def recommend_courses(candidate_skills):
    recommended_courses = []
    skills_per_company = [skills.split(', ') for skills in recruiterData['Skills']]
    for i in skills_per_company:
        for j in range(len(i)):
            if(i[j].lower() not in candidate_skills):
                recommended_courses.append(i[j])
    unique_recommended_courses = list(set(recommended_courses))
    print("\nRecommended")
    print(unique_recommended_courses)


    
recruiterData = {'Company Name':['KLA','JPM'],
                'Skills':['Java, Python, c++', 'JavaScript, Java, c']}

candidateData = {
    'Candidate Name': ['John Smith', 'Emily Johnson', 'Michael Williams', 'Sarah Miller', 'Alex Davis'],
    'Skills': ['Java, Python, Software Development',
            'Machine Learning, Python, Data Analysis',
            'Leadership, Finance, Communication',
            'C++, Web Development, Database Management',
            'JavaScript, UI/UX Design, Frontend Development']
    }
yes = 1

while yes:
    choice = int(input("1. Recruiter\n2. Candidate\nEnter your choice: "))
    
    if choice == 1:
        required_skills = []
        recruiter=input("Enter your company name: ")
        recruiterData['Company Name'].append(recruiter)
        print("Enter the skills that you expect (press 0 if last skill):")
        skill=input("Enter skill: ")
        skl=''
        while(skill!='0'):
            skl=skl+skill+', '
            required_skills.append(skill)
            skill=input("Enter skill: ")
        skl=skl[:-2]
        recruiterData['Skills'].append(skl)
        df = pd.DataFrame(candidateData)
        skill_data = df['Skills'].tolist() + [', '.join(required_skills)]
        vectorizer = CountVectorizer().fit(skill_data)
        skills_matrix = vectorizer.transform(skill_data)
        #print(skill_data)

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(skills_matrix)

        # The last row corresponds to the required skills
        match_scores = cosine_similarities[-1][:-1]

        # Create a DataFrame with match scores
        match_df = pd.DataFrame({'Candidate Name': df['Candidate Name'], 'Match Score': match_scores})

        # Sort candidates by match score
        sorted_df = match_df.sort_values(by='Match Score', ascending=False)
        # Access the match scores
        for i in range(len(sorted_df)):
            if(sorted_df['Match Score'][i]>0):
                print(sorted_df.iloc[i])
        
    elif choice == 2:
        my_skills = []
        candidate = input("Enter your name: ")
        data['Candidate Name'].append(candidate)
        print("Enter the skills that you have (press 0 if last skill):")
        skill = input("Enter skill: ")
        skl = ''
        while skill != '0':
            skl = skl + skill + ', '
            my_skills.append(skill)
            skill = input("Enter skill: ")
        skl = skl[:-2]
        data['Skills'].append(skl)
        
        # Use CountVectorizer to create a document-term matrix
        skill_data = df['Skills'].tolist() + [', '.join(my_skills)]
        vectorizer = CountVectorizer().fit(skill_data)
        skills_matrix = vectorizer.transform(skill_data)

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(skills_matrix)

        # The last row corresponds to the candidate's skills
        match_scores = cosine_similarities[-1][:-1]

        # Create a DataFrame with match scores
        match_df = pd.DataFrame({'Candidate Name': df['Candidate Name'], 'Match Score': match_scores})

        # Sort candidates by match score
        sorted_df = match_df.sort_values(by='Match Score', ascending=False)

        # Recommend courses
        print(my_skills)
        recommend_courses(my_skills)

        # Print match scores and recommended courses
        print("Match scores and recommended courses:")
        for i in range(len(sorted_df)):
            if sorted_df['Match Score'][i] > 0:
                print(sorted_df.iloc[i])
        
            
            
    
    yes = int(input("Want to continue? (1/0): "))

print("Final dataset:")
print(data)