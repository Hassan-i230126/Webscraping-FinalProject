import streamlit as st
import json

# Load the categorized reviews JSON file
def load_reviews(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load and parse the ratings file
def read_ratings(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    reviews = data.split("\n\n")  # Split reviews by blank line
    parsed_reviews = []

    for review in reviews:
        lines = review.split("\n")
        review_data = {}
        for line in lines:
            if line.startswith("Review"):
                review_data["Review"] = line.strip()
            elif "Overall" in line:
                review_data["Overall"] = line.split(" ")[-1].strip()
            elif "Food" in line:
                review_data["Food"] = line.split(" ")[-1].strip()
            elif "Service" in line:
                review_data["Service"] = line.split(" ")[-1].strip()
            elif "Ambience" in line:
                review_data["Ambience"] = line.split(" ")[-1].strip()
        if review_data:
            parsed_reviews.append(review_data)

    return parsed_reviews

# Convert rating to stars
def rating_with_stars(rating):
    try:
        stars = "⭐" * int(float(rating))
        return f"{stars} ({rating})"
    except:
        return "N/A"

# Streamlit app configuration
st.set_page_config(page_title="Vetro Dashboard", page_icon="🍷", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home", "Reviews", "Ratings", "Statistics"])

# Load reviews and ratings
reviews_file = "categorized_reviews.json"
categorized_reviews = load_reviews(reviews_file)

file_path = "ratings.txt"
ratings_data = read_ratings(file_path)

# Home Page
if page == "Home":
    st.markdown(
        """
        <style>
        body {
            background-color: #ffffff;
        }
        .hero-section {
            background: url('https://source.unsplash.com/1600x600/?dining,restaurant') no-repeat center center;
            background-size: cover;
            color: white;
            padding: 100px 20px;
            text-align: center;
        }
        .hero-title {
            font-size: 3em;
            font-weight: bold;
            color: #e74c3c;
        }
        .hero-subtitle {
            font-size: 1.5em;
            margin-top: 10px;
            font-weight: 300;
            color: #f8f9fa;
        }
        .welcome-section {
            text-align: center;
            padding: 50px;
        }
        .welcome-title {
            font-size: 2em;
            font-weight: bold;
            color: #e74c3c;
        }
        .welcome-text {
            font-size: 1.2em;
            color: #333;
            line-height: 1.6;
            max-width: 800px;
            margin: 20px auto;
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>

        <!-- Hero Section -->
        <div class="hero-section">
            <div class="hero-title">🍽️ Vetro Restaurant & Lounge 🍽️</div>
            <div class="hero-subtitle">✨ Fine Dining, Perfect Ambience, and Unforgettable Experiences ✨</div>
        </div>

        <!-- Welcome Section -->
        <div class="welcome-section">
            <div class="welcome-title">🍴 Welcome 🍴</div>
            <div class="welcome-text">
                Welcome to Vetro Restaurant & Lounge – where a unique dining experience awaits you. 
                Vetro offers a modern, elegant setting for all your event occasions. Enjoy the best 
                fine dining experience with exquisite cuisine, top-notch service, and an unmatched atmosphere. 
                Whether you're celebrating a special moment or enjoying a casual evening out, 
                we promise to make it unforgettable.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("image.jpg", use_container_width=True, caption="A Taste of Luxury")

    st.audio("Tunes.mp3")

# Reviews Page
elif page == "Reviews":
    st.header("Customer Reviews")
    category = st.selectbox("Select a Review Category", ["positive", "neutral", "negative"])

    if category in categorized_reviews:
        st.subheader(f"{category.capitalize()} Reviews")
        for i, review in enumerate(categorized_reviews[category], 1):
            overall_rating = ratings_data[i - 1]["Overall"] if i - 1 < len(ratings_data) else "N/A"
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                    <strong>{review}</strong>
                    <br>Overall Rating: {rating_with_stars(overall_rating)}
                </div>
                """,
                unsafe_allow_html=True,
            )

# Ratings Page
elif page == "Ratings":
    st.header("Ratings Overview")
    st.table(
        {
            "Overall": [rating_with_stars(r["Overall"]) for r in ratings_data],
            "Food": [rating_with_stars(r["Food"]) for r in ratings_data],
            "Service": [rating_with_stars(r["Service"]) for r in ratings_data],
            "Ambience": [rating_with_stars(r["Ambience"]) for r in ratings_data],
        }
    )

# Visualizations Page
elif page == "Statistics":
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    # Prepare data for visualization
    categories = ["Overall", "Food", "Service", "Ambience"]
    ratings = [float(r["Overall"]) if "Overall" in r else 0 for r in ratings_data[:4]]
    food_ratings = [float(r["Food"]) if "Food" in r else 0 for r in ratings_data[:4]]
    service_ratings = [float(r["Service"]) if "Service" in r else 0 for r in ratings_data[:4]]
    ambience_ratings = [float(r["Ambience"]) if "Ambience" in r else 0 for r in ratings_data[:4]]

    ratings_summary = {
        "Categories": categories,
        "Ratings": [sum(ratings)/len(ratings), sum(food_ratings)/len(food_ratings),
                    sum(service_ratings)/len(service_ratings), sum(ambience_ratings)/len(ambience_ratings)]
    }

    # Page header
    st.markdown(
        """
        <style>
        .page-header {
            font-size: 2.5em;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px;
            font-weight: bold;
            color: #e74c3c;
        }
        .chart-container {
            margin-top: 30px;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="page-header">📊 Ratings Visualizations</div>
        """,
        unsafe_allow_html=True,
    )

    # Visualization 1: Horizontal Bar Chart
    with st.container():
        st.markdown("<div class='chart-container'><h3>🔹 Horizontal Bar Chart</h3></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=ratings_summary["Ratings"], y=ratings_summary["Categories"], palette="coolwarm", ax=ax)
        ax.set_title("Average Ratings by Category", fontsize=16, weight="bold")
        ax.set_xlabel("Average Rating", fontsize=12)
        ax.set_ylabel("Categories", fontsize=12)
        st.pyplot(fig)

    # Visualization 2: Pie Chart
    with st.container():
        st.markdown("<div class='chart-container'><h3>🔹 Pie Chart</h3></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = sns.color_palette("pastel")
        ax.pie(
            ratings_summary["Ratings"],
            labels=ratings_summary["Categories"],
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
        )
        ax.set_title("Ratings Distribution", fontsize=16, weight="bold")
        st.pyplot(fig)

    # Visualization 3: Line Chart
    with st.container():
        st.markdown("<div class='chart-container'><h3>🔹 Line Chart</h3></div>", unsafe_allow_html=True)
        df = pd.DataFrame(
            {
                "Categories": categories,
                "Ratings": [sum(ratings)/len(ratings), sum(food_ratings)/len(food_ratings),
                            sum(service_ratings)/len(service_ratings), sum(ambience_ratings)/len(ambience_ratings)],
            }
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(data=df, x="Categories", y="Ratings", marker="o", ax=ax)
        ax.set_title("Trends in Average Ratings", fontsize=16, weight="bold")
        ax.set_xlabel("Categories", fontsize=12)
        ax.set_ylabel("Average Rating", fontsize=12)
        st.pyplot(fig)
