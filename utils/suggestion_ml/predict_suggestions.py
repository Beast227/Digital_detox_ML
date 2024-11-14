import random
import sqlite3

# Initial suggestions pool for each cluster
suggestions_pool = {
    0: [
        "Take a 15-minute walk outdoors.",
        "Practice a short guided meditation.",
        "Schedule a coffee chat with a friend.",
        "Spend some time doing yoga or stretching.",
        "Try cooking a new healthy recipe.",
        "Visit a local park or green space.",
        "Spend some quality time playing with a pet.",
        "Write in a gratitude journal for 10 minutes."
    ],
    1: [
        "Read a chapter of a book you've been meaning to start.",
        "Work on a creative hobby, like painting or knitting.",
        "Declutter and organize a small part of your room.",
        "Explore a new podcast episode on a topic you love.",
        "Plan your week and set personal goals.",
        "Take a tech-free nap to refresh your mind.",
        "Volunteer at a local organization or charity.",
        "Watch the sunset or do some stargazing."
    ],
    2: [
        "Start with 5-10 minutes of mindfulness meditation daily to reduce stress.",
        "Encourage setting a 'tech-free day' to focus on offline activities.",
        "Try low-stress physical activities (e.g., biking, hiking) that can be rewarding and offer a break from gaming.",
        "Suggest non-digital hobbies like drawing, playing an instrument, or writing.",
        "Encourage connecting with a friend to set goals for reduced screen time.",
        "Set aside a specific time each week (e.g., Sunday afternoons) for a tech-free window to recharge mentally.",
        "Try picking up a physically engaging hobby such as hiking, swimming, or learning a sport to get a break from screen activities.",
        "Encourage meeting with friends for board games or other non-digital social activities to maintain social engagement without screens.",
        "Incorporate short, guided body relaxation exercises to ease any tension from long gaming sessions.",
        "Suggest using part of their screen time for creative digital pursuits like digital art or music mixing, which can be enjoyable but mentally enriching.",
    ],
    3: [
        "Practice deep breathing or short meditations daily.",
        "Suggest setting app notifications to a single time each day to reduce distraction.",
        "Encourage activities like hiking, picnicking, or joining outdoor group events to reduce stress.",
        "Promote daily journaling to process emotions and reflect on stressors.",
        "Suggest trying new creative outlets like painting, cooking, or a fitness class.",
        "Try setting daily limits or taking one full day off from social media each week to help unwind.",
        "Use physical supplies or a non-digital planner to create a visual board for relaxation ideas or personal inspiration.",
        "Go for a walk in a green space, beach, or park for at least 20 minutes a few times a week to help manage stress levels.",
        "Encourage writing down positive reflections or thoughts for 5 minutes each day to promote relaxation.",
        "Explore a relaxing craft like watercolor painting, clay sculpting, or gardening as an enjoyable way to de-stress."
    ],
    4: [
        "Implement 25-minute work intervals with 5-minute tech-free breaks to enhance focus.",
        "Suggest starting mornings with offline activities to set a productive tone.",
        "Use written or app reminders to maintain productivity goals.",
        "Declutter the workspace to reduce digital distractions.",
        "Engage in short, productive reading breaks to stimulate the mind.",
        "Encourage a mindful break every hour (e.g., quick deep breathing or a light stretch) to stay focused.",
        "Use a physical or digital planner to prioritize tasks with a 1-3-5 rule (1 major task, 3 medium, and 5 small tasks per day).",
        "Incorporate learning sessions on new skills or industry trends to keep their screen time productive.",
        "At the end of each day, write down thoughts or unfinished tasks to clear the mind for the evening.",
        "Schedule a daily or weekly “thinking time” where they can reflect on goals and planning without using any screens."
    ],
    # More clusters can be added here...
    "default": [
        "Go for a short walk to clear your mind.",
        "Read an inspiring article or blog post.",
        "Practice deep breathing exercises for 5 minutes.",
        "Call or message a loved one to catch up.",
        "Enjoy a healthy snack mindfully, without distractions."
    ]
}

# Function to get suggestions based on the cluster
def generate_suggestions(cluster=None):
    """Generates a list of suggestions based on the provided cluster.

    Args:
        cluster (int, optional): The cluster number. If not provided,
            default suggestions will be used.

    Returns:
        list: A list of suggestions.
    """

    if cluster is None:
        suggestions_list = suggestions_pool["default"]
    else:
        suggestions_list = suggestions_pool.get(cluster, [])

    num_suggestions = min(5, len(suggestions_list))
    return random.sample(suggestions_list, k=num_suggestions)

def view_feedback():
    conn = sqlite3.connect('suggestions_feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedback_records = cursor.fetchall()
    conn.close()
    
    print("Feedback Records:")
    for record in feedback_records:
        print(f"Cluster: {record[1]}, Feedback: {record[2]}")


# Separate function to collect and log feedback
def collect_feedback(cluster, feedback):
    """Collects and logs user feedback on suggestions.

    Args:
        cluster (int): The cluster number associated with the suggestions.
    """
    if feedback:
        # Log feedback in the database
        conn = sqlite3.connect('suggestions_feedback.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            cluster INTEGER,
                            feedback TEXT
                         )''')
        cursor.execute("INSERT INTO feedback (cluster, feedback) VALUES (?, ?)", (cluster, feedback))
        conn.commit()
        conn.close()
        print("Thank you! Your feedback has been recorded.")
    else:
        print("No feedback provided.")
