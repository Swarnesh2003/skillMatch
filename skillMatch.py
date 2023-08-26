import json
import mysql.connector
from flask_cors import CORS
from flask import jsonify, request, redirect
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

from flask import Flask, render_template

app = Flask(__name__)
CORS(app)
def recommend_courses(candidate_skills):
    recommended_courses = []
    candidate_skills=[item.lower() for item in candidate_skills]
    skills_per_company = [skills.split(', ') for skills in recruiterData['Skills']]
    for i in skills_per_company:
        for j in range(len(i)):
            if(i[j].lower() not in candidate_skills):
                recommended_courses.append(i[j])
    unique_recommended_courses = list(set(recommended_courses))
    return (unique_recommended_courses)
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

@app.route('/api/recruitersList', methods=['POST'])
def post_data():
    candidate = request.json.get('name')
    my_skills = request.json.get('skills')
    rec_skills = recommend_courses(my_skills)
    # Process the data as needed
    candidateData['Candidate Name'].append(candidate)
    skl=''
    for i in my_skills:
        skl=skl+i+', '
    skl=skl[:-2]
    candidateData['Skills'].append(skl)
    df = pd.DataFrame(recruiterData)
    skill_data = df['Skills'].tolist() + [', '.join(my_skills)]
    vectorizer = CountVectorizer().fit(skill_data)
    skills_matrix = vectorizer.transform(skill_data)
    print(skill_data)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(skills_matrix)

    # The last row corresponds to the required skills
    match_scores = cosine_similarities[-1][:-1]

    # Create a DataFrame with match scores
    match_df = pd.DataFrame({'Company Name': df['Company Name'], 'Match Score': match_scores})

    # Sort candidates by match score
    sorted_df = match_df.sort_values(by='Match Score', ascending=False)
    sortedval=[]
    for i in range(len(sorted_df)):
            if sorted_df['Match Score'][i] > 0.6:
                row = sorted_df.iloc[i]
                sortedval.append(row['Company Name'])

    print(sortedval)
    response = {'message': f'{sortedval}', 'recom':f'{rec_skills}'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()