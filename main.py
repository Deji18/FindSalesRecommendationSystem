import streamlit as st
from io import BytesIO
from PIL import Image
import os
import requests
from dotenv import load_dotenv
load_dotenv()
GOOGLE_APIKEY = os.getenv('G_API')
SEARCHID=os.getenv('S_ID')
BASE_URL = os.getenv('BASE_URL')
OpenAI_API_KEY = os.getenv("OAK")

from openai import OpenAI
client = OpenAI(api_key=OpenAI_API_KEY)

# Define the initial messages array
messages=[
        {"role": "system", "content": "You are an expert at crafting search queries for brands to find their dream brand ambassador."}
    ]


@st.cache_data(persist="disk")
def get_report(search_query):
    # Define the base URL (this should be the server or API endpoint you're hitting)
    
    request_url =f"{BASE_URL}/getReportInstagram" 
    
    # Define the query parameter
    params = {
        'search_query': search_query
    }
    
    # Perform the GET request
    try:
        response = requests.get(request_url, params=params)
        try:
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                st.session_state.summaries = data
                for images in st.session_state.summaries:
                    if images.get("username")==None:
                        pass
                    else:
                        st.session_state.images.append(images.get("profilePic"))
                        st.session_state.userNames.append(images.get("username"))

            else:
                st.session_state.images=[]
                st.session_state.summaries=None
        except UnboundLocalError:
            pass
    except requests.exceptions.ConnectionError:
        
        st.error("Cant Connect to API") 
   




if "images" not in st.session_state:
    st.session_state.images=[]

if "summaries" not in st.session_state:
    st.session_state.summaries=None

if "userNames" not in st.session_state:
    st.session_state.userNames=[]

if "page" not in st.session_state:
    st.session_state.page = "landing"

def extract_image_links(json_data):
    items = json_data.get("items", [])
    image_links = [item.get("link") for item in items if "link" in item]
    return image_links


def search_func():
    st.session_state.images = []
    st.session_state.userNames=[]
    if st.session_state.search_query:
        with st.spinner(text="Loading Summary...",_cache=True):
            get_report(search_query=st.session_state.search_query)
            
            
        # Print results
        
        print("searching...")
    else:
        st.info("Nothing is in the search bar")
    print("Clicked!")

def go_to_app():
    st.session_state.page = "app"

def go_to_landing():
    st.session_state.page = "landing"

st.set_page_config(page_title="Find Sales- AI-powered Ambassador Finder",page_icon="👾", layout="wide")

#Css For the landing and main application page
st.markdown('''
<style>
    /* General styling */
    .stApp {
        background-color: #1a1a1a;
    }
    
    .main-header {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #9400D3 !important;
        margin-bottom: 0 !important;
        text-align: center;
    }
    
    .subheader {
        font-size: 1.5rem !important;
        color: #ffffff !important;
        margin-top: 0 !important;
        text-align: center;
    }
    
   
    
    .feature-section {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 3px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        color: #ffffff;
    }
    
    .feature-header {
        color: #9400D3;
        font-weight: 600;
    }
    
    .testimonial {
        background-color: #2d2d2d;
        border-left: 4px solid #9400D3;
        margin: 15px 0;
        border-radius: 0 8px 8px 0;
        color: #ffffff;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #333;
        color: #ffffff;
    }
    
    /* Back to top button style - keep this */
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #2d2d2d;
        color: #9400D3;
        border: none;
        border-radius: 100%;
        padding: 25px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        z-index: 100;
    }

    .back-to-top:hover {
        background-color: #9400D3;
        color: #1a1a1a;
    }
    

    .app-container {
        max-width: 10px;
        margin: 1 auto;
    }
    
   
    .stButton>button {
        background-color: #9400D3;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #6a0096;
        color: #1a1a1a;
    }
    
    /* Ensure text is readable */
    p, li, h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    
    /* Feature text styling */
    .feature-text {
        color: #ffffff !important;
    }
    
    /* Streamlit specific overrides */
    .stMarkdown {
        color: #ffffff;
    }
    
    .stText {
        color: #ffffff;
    }
    
    /* Center buttons */
    .center-button {
        display: flex;
        justify-content: center;
    }
    
    /* App screenshot container */
    .app-screenshot {
        text-align: center;
        margin: 30px 0;
    }
    
    .app-screenshot img {
        max-width: 80%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 2px solid #9400D3;
    }

</style>
''', unsafe_allow_html=True)

# Page navigation logic
if st.session_state.page == "landing":
    # LANDING PAGE
    st.markdown("<h1 class='main-header'>Find Sales</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>AI-Powered Brand Ambassador Discovery Platform</h2>", unsafe_allow_html=True)
    
    # Centered "Get Started" button
    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    st.button("Get Started", key="get_started", on_click=go_to_app, use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # What is Brand Guy section
    st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='feature-header'>What is Find Sales?</h3>", unsafe_allow_html=True)
    st.write("""
    Find Sales is an innovative AI-powered platform designed to help businesses find the perfect brand ambassadors 
    for their products and services. Using advanced algorithms and social media data analysis, we connect you with 
    influencers whose audience demographics, engagement rates, and personal brand align perfectly with yours.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Features section
    st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='feature-header'>Key Features</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 AI-Powered Search", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Our platform uses OpenAI technology to craft perfect search queries based on your brand details.</p>", unsafe_allow_html=True)
        
        st.markdown("#### 📊 Comprehensive Insights", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Get detailed metrics and analytics about potential ambassadors, including follower counts, engagement rates, and demographic information.</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔄 Smart Matching", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Our algorithm matches your brand with influencers who share your values and have an audience that matches your target market.</p>", unsafe_allow_html=True)
        
        st.markdown("#### 💼 Time-Saving Solution", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Save hours of manual research and get a curated list of potential brand ambassadors with just a few clicks.</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # How it works section
    st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='feature-header'>How It Works</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='color: #0066cc;'>1️⃣ Input Your Details</h3>", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Tell us about your brand, location, industry, and the values that matter most to you.</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 style='color: #0066cc;'>2️⃣ AI Creates Search Query</h3>", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Our AI generates an optimized search query tailored to your specific requirements.</p>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h3 style='color: #0066cc;'>3️⃣ Review Matches</h3>", unsafe_allow_html=True)
        st.markdown("<p class='feature-text'>Browse through a list of potential brand ambassadors with detailed profiles and engagement metrics.</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='feature-header'>What Our Users Say</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='testimonial'>", unsafe_allow_html=True)
    st.write("""
    *"Find Sales helped us find the perfect ambassador for our eco-friendly packaging business. The AI-generated search queries were spot on, and we found someone who truly believes in our mission."*
    
    **— Sarah T., Marketing Director**
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='testimonial'>", unsafe_allow_html=True)
    st.write("""
    *"The detailed profiles and metrics saved us so much time. We were able to make an informed decision based on real data, not just gut feelings."*
    
    **— Miguel R., Brand Manager**
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Centered "Try Find Sales Now" button
    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    st.button("Try Find Sales Now", key="try_now", on_click=go_to_app, use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # App Screenshot at the bottom
    st.markdown("<div class='app-screenshot'>", unsafe_allow_html=True)
    st.markdown("<h3 class='feature-header'>See Our Platform in Action</h3>", unsafe_allow_html=True)
    # Replace the URL below with your actual app screenshot URL
    st.markdown("<img src='/api/placeholder/800/500' alt='Find Sales Application Screenshot' />", unsafe_allow_html=True)
    st.markdown("<p class='feature-text'>A glimpse of our powerful ambassador discovery interface</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.write("© 2025 Find Sales | AI-Powered Ambassador Discovery")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.write("# FIND SALES")
    # back button to the landing page
    if st.button("← Back to Home", key="back_to_home"):
        go_to_landing()
    
    st.selectbox(label="Where is your brand based in?",options=[
        "Nigeria", "London", "New York", "Tokyo", "Paris", "Sydney", "Beijing", "Toronto", "Mumbai", "Dubai",
        "Berlin", "Cape Town", "Buenos Aires", "Moscow", "Cairo", "Seoul", "Bangkok", "Mexico City", "Jakarta", "Istanbul",
        "Rio de Janeiro", "Lagos", "Singapore", "Los Angeles", "Kuala Lumpur", "Rome", "Shanghai", "Melbourne", "Hong Kong", "Madrid",
        "Dublin", "Nairobi", "Lima", "Vienna", "Athens", "Manila", "Karachi", "Dhaka", "Abu Dhabi", "Amsterdam",
        "Chicago", "Bogotá", "Riyadh", "Santiago", "Barcelona", "Colombo", "Ankara", "Brisbane", "Kiev", "Warsaw",
        "San Francisco", "Doha", "Edinburgh", "Helsinki", "Oslo", "Stockholm", "Copenhagen", "Lisbon", "Vancouver", "Montreal",
        "Zurich", "Geneva", "Prague", "Budapest", "Brussels", "Hanoi", "Phnom Penh", "Kathmandu", "Islamabad", "Jakarta",
        "Canberra", "Addis Ababa", "Accra", "Casablanca", "Tunis", "Rabat", "Algiers", "Amman", "Tehran", "Baghdad",
        "Ho Chi Minh City", "Taipei", "Macau", "Perth", "Adelaide", "Darwin", "Christchurch", "Auckland", "Wellington", "Hobart",
        "Bangalore", "Hyderabad", "Pune", "Chennai", "Ahmedabad", "Surat", "Lucknow", "Patna", "Kolkata", "Jaipur"
    ]
    ,key="brand_location")
    st.selectbox(label="What category or industry is your brand focused on?",options=[
        "Pet Care", "Security Services", "Luxury Shoes", "Bespoke Interior Designs", "Digital Marketing", "Fitness Coaching", 
        "Event Planning", "Handmade Jewelry", "Organic Farming", "Online Education", 
        "Photography Services", "Custom Furniture", "Tech Support", "Mobile App Development", "Virtual Assistant Services", 
        "Health and Wellness Products", "Eco-Friendly Packaging", "Financial Consulting", "Social Media Management", "Car Rental Services", 
        "Home Cleaning Services", "Landscaping", "Meal Prep Services", "Luxury Handbags", "Clothing Boutique", 
        "Graphic Design", "Tutoring Services", "Real Estate Development", "E-commerce Store", "Hair and Beauty Salon", 
        "Wedding Planning", "Drone Videography", "Food Truck", "Specialty Coffee", "Art Gallery", 
        "Catering Services", "Craft Supplies", "Mobile Car Wash", "Subscription Boxes", "Sustainable Fashion", 
        "IT Consulting", "Yoga Studio", "Auto Repair Shop", "Travel Agency", "Baking and Pastries", 
        "Bookstore", "Music Lessons", "Gift Wrapping Services", "Daycare Center", "Personal Training", 
        "Podcast Production", "Career Coaching", "Online Reselling", "Personal Styling", "Freelance Writing", 
        "Translation Services", "Gaming Lounge", "Interior Painting", "Renewable Energy Solutions", "Custom T-Shirts", 
        "Virtual Reality Experiences", "Public Relations Agency", "Coffee Roasting", "Candle Making", "Antique Restoration", 
        "Mobile Massage Therapy", "Life Coaching", "Childproofing Services", "Shoe Repair", "Toy Manufacturing", 
        "Pet Grooming", "Health Food Store", "Fishing Gear", "Gourmet Popcorn", "Customized Stationery", 
        "Self-Defense Classes", "Home Staging", "Party Supplies", "Computer Repair", "Sports Coaching", 
        "Mobile Notary Services", "Greenhouse Installation", "Car Detailing", "Solar Panel Installation", "Corporate Training", 
        "Video Editing Services", "Scented Soaps", "Woodworking", "Bed and Breakfast", "Sports Equipment Rental", 
        "Organic Skincare", "Wedding Photography", "Custom Cake Design", "Online Fitness Programs", "Property Management", 
        "SEO Services", "Virtual Event Hosting", "3D Printing Services", "Luxury Watches", "Tailoring and Alterations"
    ]
    ,key="brand_category")
    st.text_input(label="What values or traits are most important to your brand when choosing an ambassador?(optional)",key="extra")
    if st.button("Generate Search query"):
        new_user_input = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"I'm looking for someone to represent my brand help me write a search query for google to make it possible to find a brand ambassador my brand is of a {st.session_state.brand_category} category and the business is based in {st.session_state.brand_location} important values and traits to the brand--{st.session_state.extra}"
                }
            ]
        }

        # Append the new user input to the messages
        messages.append(new_user_input)

        # Make the API call
        response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:brand-ambassodor-project::BC34rmn6",
            messages=messages,
        )   

        # Extract and print the assistant's response
        assistant_response = response.choices[0].message.content
        st.session_state.search_query= assistant_response

    st.text_input("what are you looking for ?",key="search_query",disabled=True)
    st.button("Search",on_click=search_func)
    if st.session_state.images:
        print(st.session_state.userNames)
        tabs = st.tabs(st.session_state.userNames)
        for url,tab in enumerate(tabs):
             
        # Fetch image from the URL
            try:
                response = requests.get(st.session_state.images[url])
                image = Image.open(BytesIO(response.content))
                # Display image
                with tab:
                    st.code(st.session_state.summaries[url].get('username'))
                    st.image(image, caption=f"@{ st.session_state.summaries[url].get('username')}\'s Profile Picture ")
                    st.link_button(type='secondary',label=f"Click me to go to @{st.session_state.summaries[url].get('username')}'s instagram page ",url=f"{st.session_state.summaries[url].get('profileLink')}")
                    st.info(f"Bio: { st.session_state.summaries[url].get('biography')}",icon="🥇")
                    st.code(st.session_state.summaries[url].get('username'))
                    st.write(f"Full Name :red-background[{ st.session_state.summaries[url].get('fullName')}]")
                    st.write(f"Username @:blue-background[{ st.session_state.summaries[url].get('username')}]")
                    st.write(f"Number of People Following @{st.session_state.summaries[url].get('username')} :green-background[{ st.session_state.summaries[url].get('No_of_followers')}]")
                    st.write(f"Number of people @{st.session_state.summaries[url].get('username')} follows: :blue-background[{ st.session_state.summaries[url].get('No_of_following')}]")
                    st.write(f"### :rainbow-background[Related Profiles]")
                    st.divider()
                    st.write(st.session_state.summaries[url].get("relatedProfiles"))
                    st.divider()
                    
            except Exception as e:
                
                if str(e)=="bad argument type for built-in operation":
                    pass
                else:
                    st.warning(f"something went wrong {e}")
                    
    if st.session_state.userNames != None:
        st.markdown("[tap me to Go to the Top](#brand-ambassador-finder)")

        st.markdown('''
            <style>
                /* Style for the back-to-top button */
                .back-to-top {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background-color: #ffffff;
                    color: white;
                    border: none;
                    border-radius: 100%;
                    padding: 25px;
                    font-size: 20px;
                    cursor: pointer;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    z-index: 100;
                }

                .back-to-top:hover {
                    background-color: #499CD7;
                }

            </style>

            <!-- Button that will scroll the page back to the top -->
            <a href="#brand-ambassador-finder" class="back-to-top" id="back-to-top-button">
                👆🏿
            </a>

            <!-- Anchor at the top of the page to scroll to -->
            <a name="top"></a>
        ''', unsafe_allow_html=True)