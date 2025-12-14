
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
# df1 = pd.read_csv('CDQUE1.csv')
# df2 = pd.read_csv('CDQUE2.csv')
# df3 = pd.read_csv('CDQUE_modified33.csv')
# df4 = pd.read_csv('cdque4.csv')
def get_predictions(csv_path):
    df = pd.read_csv(csv_path)

# df = pd.concat([df1, df2, df3,df4], ignore_index=True)

# Convert to string (important!)
    df['Module'] = df['Module'].astype(str)
    df['Marks'] = df['Marks'].astype(str)
    df['Question'] = df['Question'].astype(str)

    # TF-IDF on questions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['Question'])

    # Cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    threshold = 0.70
    # adjust if needed
    groups = []
    visited = set()

    for i in range(len(df)):
        if i in visited:
            continue
        group = [i]
        visited.add(i)
        for j in range(i+1, len(df)):
            if similarity_matrix[i][j] >= threshold:
                group.append(j)
                visited.add(j)
        if len(group) > 1:  # only take similar ones
            groups.append(group)

    # ----------- FINAL OUTPUT FOR FRONTEND -----------------
    final_output = []  # JSON-friendly

    for group in groups:
        main_idx = group[0]  # take only ONE question
        question_text = df.iloc[main_idx]['Question']
        modules = list(df.iloc[group]['Module'].unique())
        marks = list(df.iloc[group]['Marks'].unique())
        repeat_count = len(group)

        final_output.append({
            "question_text": question_text,
            "repeat_count": repeat_count,
            "modules_found": modules,
            "marks_found": marks
        })

    # Sort by first module name (Unit-I, Unit-II, ...)
    final_output = sorted(final_output, key=lambda x: x['modules_found'][0])

    return final_output

    # Show Results
    print("\n REPEATED QUESTIONS")
    for item in final_output:
        
        print("Question:", item['question'])
        print("Repeated:", item['repeated_times'], "times")
        print("Modules:", item['modules_found'])
        print("Marks:", item['marks_found'],"\n")