import random

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