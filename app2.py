import streamlit as st
import re
import random
from collections import Counter

# A simple list of common English stopwords
STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
    "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at",
    "by", "for", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

def extract_keywords(text, num_keywords=15):
    """Extracts the most common words from the text, excluding stopwords."""
    # Clean the text: lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    
    # Filter out stopwords and short words
    words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    
    # Count word frequencies and get the most common ones
    most_common_words = [word for word, count in Counter(words).most_common(num_keywords)]
    
    return most_common_words

def generate_assignments(keywords):
    """Generates two essay-style assignment questions based on keywords."""
    if len(keywords) < 2:
        return ["Not enough unique content to generate assignment questions."]
    
    # Select two random keywords for the prompts
    q1_keyword = random.choice(keywords)
    q2_keyword = random.choice([k for k in keywords if k != q1_keyword])
    
    assignments = [
        f"Write a detailed essay on the role and significance of '{q1_keyword}' based on the provided document.",
        f"Discuss the implications and applications of '{q2_keyword}' as presented in the text."
    ]
    return assignments

def generate_quizzes(text, keywords):
    """Generates three multiple-choice questions."""
    if len(keywords) < 4:
        return [{"question": "Not enough unique keywords to generate a quiz.", "options": [], "answer": ""}]

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    quizzes = []
    used_answers = []

    for _ in range(3):
        possible_answers = [k for k in keywords if k not in used_answers]
        if not possible_answers:
            break

        answer = random.choice(possible_answers)
        used_answers.append(answer)

        # Find a sentence containing the answer to form the question
        question_sentence = next((s for s in sentences if answer in s.lower()), None)
        
        if not question_sentence:
            # If no sentence found, create a simple definition question
            question = f"What is the definition or context of '{answer}' in the document?"
        else:
            # Create a fill-in-the-blank question
            question = question_sentence.replace(answer, "________")

        # Select three incorrect options (distractors)
        distractors = random.sample([k for k in keywords if k != answer], 3)
        options = distractors + [answer]
        random.shuffle(options)
        
        quizzes.append({
            "question": question,
            "options": options,
            "answer": answer
        })
        
    return quizzes

def main():
    """Defines the Streamlit user interface."""
    st.set_page_config(page_title="EduGen", layout="wide")
    st.title("📚 Assignment and Quiz Generator")
    st.write("Paste any text document below and click 'Generate' to create study materials.")

    # Text input from user
    input_text = st.text_area("Enter your document text here:", height=250, placeholder="Paste your text...")

    if st.button("Generate Materials"):
        if input_text and len(input_text.split()) > 20:
            with st.spinner("Analyzing text and generating questions..."):
                keywords = extract_keywords(input_text)
                
                if not keywords:
                    st.error("Could not extract any meaningful keywords from the text. Please provide a longer document.")
                    return

                assignments = generate_assignments(keywords)
                quizzes = generate_quizzes(input_text, keywords)
                
                st.success("Successfully generated materials!")

                # Display Assignments
                st.header("✍️ Assignment Questions")
                for i, question in enumerate(assignments, 1):
                    st.write(f"**{i}.** {question}")
                
                # Display Quizzes
                st.header("❓ Multiple-Choice Quiz")
                for i, quiz in enumerate(quizzes, 1):
                    st.write(f"**{i}. {quiz['question']}**")
                    for j, option in enumerate(quiz['options']):
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;**{chr(65+j)}.** {option}")
                    
                    with st.expander("Show Answer"):
                        st.write(f"**Correct Answer:** {quiz['answer']}")
                
        else:
            st.warning("Please enter a document with at least 20 words to generate questions.")

if __name__ == "__main__":
    main()