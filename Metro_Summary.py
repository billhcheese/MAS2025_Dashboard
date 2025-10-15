import pandas as pd
import altair as alt
import streamlit as st
import textwrap
import streamlit.components.v1 as components

st.set_page_config(page_icon="Assets/metro-atl-speaks.svg")
st.set_page_config(initial_sidebar_state="collapsed")

# Cache data loading for better performance
@st.cache_data
def load_data():
    """Load the MAS Dashboard data with caching."""
    return pd.read_parquet("Data/MAS_Dashboard_Records_2025_Updated.parquet")

# Load data
df = load_data()
#st.set_page_config(layout="wide")

custom_css = """
<style>
.stMainBlockContainer {
            max-width:65rem;
        }
.stSelectbox div[data-baseweb="select"] > div:first-child {
    border: 2px solid #808080; /* Example: 2px solid green border */
    border-radius: 5px; /* Optional: rounded corners */
}
/* This selector might need adjustment based on your Streamlit version and specific setup */
.stHeaderLogo img {
    width: auto; /* Adjust as needed */
    height: 100px; /* Maintain aspect ratio */
}
.stAppHeader { /* This class targets the top navigation container */
    background-color: #f9f9f9;
    min-height: 50px; /* Adjust height as needed */
    padding-top: 20px; /* Add padding for vertical spacing */
    padding-bottom: 20px;
}

/* Navigation menu items - comprehensive targeting */
.rc-overflow-item,
[data-testid="stHeader"] .rc-overflow-item,
.stAppHeader .rc-overflow-item,
header .rc-overflow-item,
.stApp > header .rc-overflow-item,
.stAppHeader *,
[data-testid="stHeader"] *,
header *,
.stApp > header * {
    font-size: 18px !important;
    font-weight: 600 !important;
    
}

.rc-overflow-item { /* This class targets the individual navigation items */
    font-size: 20px; /* Adjust font size as needed */
    padding: 15px; /* Adjust padding for button size */
}

/* Floating scroll down icon */
.scroll-indicator {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background-color: #2364a0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    opacity: 0.8;
}

.scroll-indicator::before {
    content: "↓";
    color: white;
    font-size: 24px;
    font-weight: bold;
}

/* Remove bouncing animation - keeping it static */
</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Add floating scroll indicator (visual only) and screen width detector


st.markdown("""
<div class="scroll-indicator"></div>
""", unsafe_allow_html=True)

# Log screen info to console for debugging
# components.html("""
# <!DOCTYPE html>
# <html>
# <head>
#     <script>
#         function logScreenInfo() {
#             const width = window.parent.innerWidth || window.innerWidth;
#             const height = window.parent.innerHeight || window.innerHeight;
#             const ratio = window.devicePixelRatio || 1;
            
#             console.log('╔════════════════════════════╗');
#             console.log('║    SCREEN INFORMATION      ║');
#             console.log('╠════════════════════════════╣');
#             console.log('║ Width:  ' + width + 'px');
#             console.log('║ Height: ' + height + 'px');
#             console.log('║ Ratio:  ' + ratio);
#             console.log('╚════════════════════════════╝');
#         }
        
#         // Log immediately
#         logScreenInfo();
        
#         // Log on resize
#         window.parent.addEventListener('resize', logScreenInfo);
#     </script>
# </head>
# <body></body>
# </html>
# """, height=0)

st.logo("Assets/arc-logo-black-trans.png",size="large")

# Initialize session state for mobile view if not exists
if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = False

# Sidebar - Mobile view toggle
st.sidebar.markdown("### 📱 Display Options")
st.session_state.is_mobile = st.sidebar.checkbox("Use Mobile View (Vertical Charts)", 
                                                   value=st.session_state.is_mobile,
                                                   help="Toggle this to switch between horizontal (desktop) and vertical (mobile) chart layouts")

if st.session_state.is_mobile:
    st.sidebar.info("📊 Charts displayed vertically")
else:
    st.sidebar.info("🖥️ Charts displayed horizontally")

# Create title with logo
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("Assets/metro-atl-speaks.svg", width=350)
with col_title:
    st.markdown("""
    <div style='color: #2364a0; font-size: 40px; font-weight:Semibold ; margin-top: 13px;'>
        <p>Metro Summary Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='line-height: 1.5;'>
        <p>
            <span style='color: #F15B29; font-size: 22px; font-weight:Bold ;'>Explore your Community's Opinions in 2025!</span>
            <span style='color: #29ABE2; font-size: 20px; font-weight:Semibold ;'>Housing Affordability is the top issue for Metro Atlanta
             Residents. Traffic concern came in second with the rest of the concerns trailing.</span> 
            <span style='color: #59595b; font-size: 15px; font-weight:400 ;'>
                The Metro Atlanta Speaks Survey is the largest survey
                of perceptions and attitudes in the Atlanta region that offer a statistically representative snapshot of residents
                across the Atlanta area on various topics. The Atlanta Regional Commission(ARC) conducts this in collaboration with
                community partners like Kennesaw State University's A.L. Burruss Institute of Public Service & Research. Find out more about
                the MAS survey in the <a href="https://mas2025dashboard.streamlit.app/FAQ" target="_self">FAQ</a>.
                This dashboard is best viewed on a desktop computer. Mobile view is available via a checkbox in the sidebar.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Get unique questions from the data
questions = df["q_short"].unique().tolist()
# Move BIGPROBLEM question to the front
bigprob_question = [q for q in questions if "BIGPROBLEM" in q]
other_questions = [q for q in questions if "BIGPROBLEM" not in q]
questions = bigprob_question + sorted(other_questions)

question_map = {
                "BIGPROBLEM| What is the biggest problem in metro Atlanta today?":"bigprob", #include note that covid 19 was offered as an answer in 2020 and 2021, but folded into public health
                "TRANSPORTATION| What is the best long-term solution to traffic problems in metro Atlanta?":"fixtraf",
                "WORKFORCE| Is now a good or bad time to find a well-paying job?":"findjob",
                "QUALITY OF LIFE| Would you move within, move out of, or stay in metro Atlanta?":"move",
                "TRANSPORTATION| I lack the transportation I need to get to places I need to go":"transport",
                "QUALITY OF LIFE| In 3 years, will living in metro Atlanta be better, worse, or same?":"lkahead",
                "WORKFORCE| What option would most likely attract and retain a skilled workforce for metro Atlanta?":"workfrce",
                "ECONOMY| How would you come up with $400 for an emergency?":"emerg",
                "AI| Impact of AI on job availability":"aijob",
                "AI| Impact of AI on business productivity":"aiproductiv",
                "AI| Impact of AI on making life easier or harder.":"aieasier",
                "AI| Impact of AI on energy consumption":"aienergy",
                "HOUSING| I could not afford to move to another residence in my current neighborhood right now":"nomovnhood",
                "TRANSPORTATION| Future growth in the metro area should be focused...":"growth",
                "ENVIRONMENT| How serious of a global threat will climate change be in the next 10 years?":"climtgblthrt",
                "ENVIRONMENT| How serious a threat to metro Atlanta will climate change be in the next 10 years?":"climtatlthrt",
                "HOUSING| Low-wage workers of local businesses have no problem finding affordable housing in my community.":"houswage",
                "HOUSING| What is the main reason for the affordable housing problems in metro Atlanta that people face?":"housreason",
                "ECONOMY| Comparing to a year ago, would you say that your financial situation is...":"finances"
            }

question_hist = {
    "bigprob": 0,
    "fixtraf": 1,
    "findjob": 1,
    "move": 1,
    "transport": 1,
    "lkahead": 1,
    "workfrce": 1,
    "emerg": 1,
    "aijob": 0,
    "aiproductiv": 0,
    "aieasier": 0,
    "aienergy": 0,
    "nomovnhood": 1,
    "growth": 1,
    "climtgblthrt": 1,
    "climtatlthrt": 1,
    "houswage": 1,
    "housreason": 0,
    "finances": 1
}

# Chart customization configurations for each question and year
# Only year-specific configurations - if no config exists for a year, Altair uses defaults
# 
# Available configuration options:
# - exclude_responses: List of response values to exclude from charts
# - custom_order: List defining the order of responses (left to right for bars, top to bottom for horizontal bars)
# - custom_colors: Dictionary mapping response values to hex color codes
# - response_aliases: Dictionary mapping response values to display names (shows aliases on charts while keeping original values for data processing)
chart_configs = {
    "bigprob": {
        # Year-specific configurations only
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Housing Affordability", "Traffic", "Economy", "Crime", "Local Tax Increases", "Other", "Infrastructure", "Quality of Local Schools", "Public Health"],
            "custom_colors": {
                "Traffic": "#648FFF",
                "Environmental Pollution": "#2D3A5A",
                "Infrastructure": "#AE1EC7",
                "Local Tax Increases": "#BED77C",
                "Crime": "#FFB000", 
                "Housing Affordability": "#FE6100",
                "Economy": "#DC267F",
                "Quality of Local Schools": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2021": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2020": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Race Relations": "#FE6100",
                "Taxes": "#BED77C",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Public Education": "#9DA786",
                "Public Health": "#785EF0",
                "Other": "#AF1737"
                }
            },
    },
    "aienergy": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Increase energy consumption", "About the same", "Decrease energy consumption"],
            "custom_colors": {
                "Increase energy consumption": "#FF9F58",
                "About the same": "#29ABE2",
                "Decrease energy consumption": "#3A80C1",
            }
        }
    },
    "aijob": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Increase the number of available jobs", "About the same", "Decrease the number of available jobs"],
            "custom_colors": {
                "Increase the number of available jobs": "#FF9F58",
                "About the same": "#29ABE2",
                "Decrease the number of available jobs": "#3A80C1",
            }
        }
    },
    "aieasier": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Make life easier", "About the same", "Make life harder"],
            "custom_colors": {
                "Make life easier": "#FF9F58",
                "About the same": "#29ABE2",
                "Make life harder": "#3A80C1",
            }
        }
    },
    "aiproductiv": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Increase business productivity", "About the same", "Decrease business productivity"],
            "custom_colors": {
                "Increase business productivity": "#FF9F58",
                "About the same": "#29ABE2",
                "Decrease business productivity": "#3A80C1",
            }
        }
    },
    "finances": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better off", "About the same", "Worse off"],
            "custom_colors": {
                "Better off": "#FF9F58",
                "About the same": "#29ABE2",
                "Worse off": "#3A80C1",
            }
        },
        "2024": {
                "exclude_responses": ["DK"],
                "custom_order": ["Better off", "About the same", "Worse off"],
                "custom_colors": {
                    "Better off": "#FF9F58",
                    "About the same": "#29ABE2",
                    "Worse off": "#3A80C1",
                }
            }
    },
    "emerg": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2021": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2020": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Cash, Check, or Debit", "Credit Card", "Borrow Someone's Money", "Sell or Pawn", "Not Able to Get Money"],
            "custom_colors": {
                "Pay it with cash, check, or debit card": "#F15B29", 
                "Put it on credit card": "#FF9F58", 
                "Borrow money from someone": "#B4E2EC", 
                "Sell or pawn something to get money": "#29ABE2", 
                "Not able to get money right now": "#3A80C1"
            },
            "response_aliases": {
                "Pay it with cash, check, or debit card": "Cash, Check, or Debit",
                "Put it on credit card": "Credit Card",
                "Borrow money from someone": "Borrow Someone's Money",
                "Sell or pawn something to get money": "Sell or Pawn",
                "Not able to get money right now": "Not Able to Get Money"
            }
        }
    },
    "climtatlthrt": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["major threat", "minor threat", "no threat"],
            "custom_colors": {
                "major threat": "#FF9F58",
                "minor threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["major threat", "minor threat", "no threat"],
            "custom_colors": {
                "major threat": "#FF9F58",
                "minor threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["major threat", "minor threat", "no threat"],
            "custom_colors": {
                "major threat": "#FF9F58",
                "minor threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        }
    },
    "climtgblthrt": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["major global threat", "minor global threat", "no threat"],
            "custom_colors": {
                "major global threat": "#FF9F58",
                "minor global threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["major global threat", "minor global threat", "no threat"],
            "custom_colors": {
                "major global threat": "#FF9F58",
                "minor global threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["major global threat", "minor global threat", "no threat"],
            "custom_colors": {
                "major global threat": "#FF9F58",
                "minor global threat": "#29ABE2",
                "no threat": "#3A80C1",
            }
        }
    },
    "nomovnhood": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            },
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        }
    },
    "houswage": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        }
    },
    "housreason": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Developers building too expensive units", "Investors buying properties to rent", "Local Zoning Laws", "Resident Opposition", "Other"],
            "custom_colors": {
                "Developers building too expensive units": "#FE6100",
                "Investors buying properties to rent": "#648FFF",
                "Local zoning laws don't allow for building enough housing": "#DC267F",
                "Existing residents opposed to building affordable housing in neighborhood": "#FFB000",
                "Other": "#AF1737",
            },
            "response_aliases": {
                "Developers building too expensive units": "Developers building too expensive units",
                "Investors buying properties to rent": "Investors buying properties to rent",
                "Local zoning laws don't allow for building enough housing":"Local Zoning Laws",
                "Existing residents opposed to building affordable housing in neighborhood": "Resident Opposition",
                "Other": "Other",
            }
        }
    },
    "lkahead": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2021": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2020": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Better", "Same", "Worse"],
            "custom_colors": {
                "Better": "#FF9F58",
                "Same": "#29ABE2",
                "Worse": "#3A80C1",
            }
        }
    },
    "move": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Stay where they are", "Move neighborhoods", "Move away from Atlanta"],
            "custom_colors": {
                "Stay where they are now": "#FF9F58",
                "Move away from Atlanta": "#29ABE2",
                "Move to a different neighborhood": "#3A80C1",
            },
            "response_aliases": {
                "Stay where they are now": "Stay where they are",
                "Move away from Atlanta": "Move away from Atlanta",
                "Move to a different neighborhood": "Move neighborhoods",
            }
        }
    },
    "growth": {
        "2025": {
            "exclude_responses": ["DK or NA"],
            "custom_order": ["Business centers", "Along corridors linking centers", "Undeveloped or rural places", "Other"],
            "custom_colors": {
                "in areas where businesses are already concentrated": "#FF9F58",
                "along transportation corridors that link existing business centers": "#29ABE2",
                "in currently undeveloped or more rural areas": "#3A80C1",
                "other": "#9DA786",
            },
            "response_aliases": {
                "in areas where businesses are already concentrated": "Business centers",
                "along transportation corridors that link existing business centers": "Along corridors linking centers",
                "in currently undeveloped or more rural areas": "Undeveloped or rural places",
                "other": "Other",
            }
        },
        "2024": {
            "exclude_responses": ["DK or NA"],
            "custom_order": ["Business centers", "Along corridors linking centers", "Undeveloped or rural places", "Other"],
            "custom_colors": {
                "in areas where businesses are already concentrated": "#FF9F58",
                "along transportation corridors that link existing business centers": "#29ABE2",
                "in currently undeveloped or more rural areas": "#3A80C1",
                "other": "#9DA786",
            },
            "response_aliases": {
                "in areas where businesses are already concentrated": "Business centers",
                "along transportation corridors that link existing business centers": "Along corridors linking centers",
                "in currently undeveloped or more rural areas": "Undeveloped or rural places",
                "other": "Other",
            }
        },
        "2023": {
            "exclude_responses": ["DK or NA"],
            "custom_order": ["Business centers", "Along corridors linking centers", "Undeveloped or rural places", "Other"],
            "custom_colors": {
                "in areas where businesses are already concentrated": "#FF9F58",
                "along transportation corridors that link existing business centers": "#29ABE2",
                "in currently undeveloped or more rural areas": "#3A80C1",
                "other": "#9DA786",
            },
            "response_aliases": {
                "in areas where businesses are already concentrated": "Business centers",
                "along transportation corridors that link existing business centers": "Along corridors linking centers",
                "in currently undeveloped or more rural areas": "Undeveloped or rural places",
                "other": "Other",
            }
        },

    },
    "transport": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"],
            "custom_colors": {
                "Strongly agree": "#F15B29",
                "Agree": "#FF9F58",
                "Disagree": "#29ABE2",
                "Strongly disagree": "#3A80C1",
            }
        }
    },
    "fixtraf": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Increase teleworking", "Do nothing", "Other"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Increase teleworking options": "#DC267F",
                "Do nothing": "#9DA786",
                "Other": "#2D3A5A",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Increase teleworking options": "Increase teleworking",
                "Do nothing": "Do nothing",
                "Other": "Other"
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Increase teleworking", "Do nothing"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Increase teleworking options": "#DC267F",
                "Do nothing": "#9DA786",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Increase teleworking options": "Increase teleworking",
                "Do nothing": "Do nothing",
            }
        },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Do nothing"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Do nothing": "#9DA786",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Do nothing": "Do nothing",
            }
        },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Do nothing"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Do nothing": "#9DA786",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Do nothing": "Do nothing",
            }
        },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Do nothing"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Do nothing": "#9DA786",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Do nothing": "Do nothing",
            }
        },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Expand public transit", "Improve roads and highways", "Live work developments", "Do nothing"],
            "custom_colors": {
                "Expand public transit": "#FE6100",
                "Improve roads and highways": "#648FFF",
                "Develop communities where people can live where they work": "#AE1EC7",
                "Do nothing": "#9DA786",
            },
            "response_aliases": {
                "Expand public transit": "Expand public transit",
                "Improve roads and highways": "Improve roads and highways",
                "Develop communities where people can live where they work": "Live work developments",
                "Do nothing": "Do nothing",
            }
        }
    },
    "findjob": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Good time", "Bad time"],
            "custom_colors": {
                "Good time": "#FF9F58",
                "Bad time": "#3A80C1",
            }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Good time", "Bad time"],
            "custom_colors": {
                "Good time": "#FF9F58",
                "Bad time": "#3A80C1",
            }
        }
    },
    "workfrce": {
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Affordable housing", "Training or retraining", "Transportation to work", "Better K-12 education", "Access to higher education"],
            "custom_colors": {
                "Providing more affordable housing options": "#FE6100",
                "Creating more training or retraining opportunities": "#648FFF",
                "Providing better transportation options to and from work": "#AE1EC7",
                "Improving K-12 education": "#FFB000",
                "Providing better access to higher education": "#AF1737",
            },
            "response_aliases": {
                "Providing more affordable housing options": "Affordable housing",
                "Creating more training or retraining opportunities": "Training or retraining",
                "Providing better transportation options to and from work": "Transportation to work",
                "Improving K-12 education": "Better K-12 education",
                "Providing better access to higher education": "Access to higher education",
            }
        },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Affordable housing", "Training or retraining", "Transportation to work", "Better K-12 education", "Access to higher education"],
            "custom_colors": {
                "Providing more affordable housing options": "#FE6100",
                "Creating more training or retraining opportunities": "#648FFF",
                "Providing better transportation options to and from work": "#AE1EC7",
                "Improving K-12 education": "#FFB000",
                "Providing better access to higher education": "#AF1737",
            },
            "response_aliases": {
                "Providing more affordable housing options": "Affordable housing",
                "Creating more training or retraining opportunities": "Training or retraining",
                "Providing better transportation options to and from work": "Transportation to work",
                "Improving K-12 education": "Better K-12 education",
                "Providing better access to higher education": "Access to higher education",
            }
        },
        "2021": {
            "exclude_responses": ["DK"],
            "custom_order": ["Affordable housing", "Training or retraining", "Transportation to work", "Better K-12 education", "Access to higher education"],
            "custom_colors": {
                "Providing more affordable housing options": "#FE6100",
                "Creating more training or retraining opportunities": "#648FFF",
                "Providing better transportation options to and from work": "#AE1EC7",
                "Improving K-12 education": "#FFB000",
                "Providing better access to higher education": "#AF1737",
            },
            "response_aliases": {
                "Providing more affordable housing options": "Affordable housing",
                "Creating more training or retraining opportunities": "Training or retraining",
                "Providing better transportation options to and from work": "Transportation to work",
                "Improving K-12 education": "Better K-12 education",
                "Providing better access to higher education": "Access to higher education",
            }
        },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Affordable housing", "Training or retraining", "Transportation to work", "Better K-12 education", "Access to higher education"],
            "custom_colors": {
                "Providing more affordable housing options": "#FE6100",
                "Creating more training or retraining opportunities": "#648FFF",
                "Providing better transportation options to and from work": "#AE1EC7",
                "Improving K-12 education": "#FFB000",
                "Providing better access to higher education": "#AF1737",
            },
            "response_aliases": {
                "Providing more affordable housing options": "Affordable housing",
                "Creating more training or retraining opportunities": "Training or retraining",
                "Providing better transportation options to and from work": "Transportation to work",
                "Improving K-12 education": "Better K-12 education",
                "Providing better access to higher education": "Access to higher education",
            }
        }
    }
}

# Create display options with time trend indicators
display_options = []
for question in questions:
    question_key = question_map[question]
    trend_status = question_hist.get(question_key, 0)
    
    if trend_status == 1:
        display_text = f"{question} (Trend Available)"
    else:
        display_text = f"{question} (No Trend)"
    
    display_options.append(display_text)

# Create mapping from display text back to original question
display_to_question = dict(zip(display_options, questions))

selected_display = st.selectbox(
    "Choose a question from the MAS 2025 Survey", 
    display_options, 
    help="Select a question to display, (No Trend) questions do not have year-over-year trend data whereas (Trend Available) questions do if you scroll down")
selected_question = question_map[display_to_question[selected_display]]

# Filter data for selected question
df_question = df[df["question"] == selected_question].copy()

# Year filter
if "survey year" in df_question.columns:
    available_years = sorted(df_question["survey year"].dropna().unique(), reverse=True)
    year_options = [str(year) for year in available_years]
    selected_year = st.radio(
        "Select Survey Year", 
        options=year_options, 
        index=0, #default to 2025
        help="Select which MAS survey year to use for the graph",
        horizontal=True)

    # Apply year filter for non-trend analysis
    df_filtered = df_question[df_question["survey year"] == int(selected_year)].copy()

else:
    df_filtered = df_question[df_question["survey year"] == "2025"].copy()
    selected_year = "2025"

# --- Response Distribution ---
response_summary = (
    df_filtered.groupby("response")["countywt"]
    .sum()
    .reset_index()
)
response_summary["percent"] = (response_summary["countywt"] / response_summary["countywt"].sum())

# Apply custom configurations if available for the selected year only
# If no year-specific config exists, use Altair defaults
question_config = chart_configs.get(selected_question, {})
if str(selected_year) in question_config:
    config = question_config[str(selected_year)]
else:
    config = {}  # Use Altair defaults

# Filter out excluded responses
if "exclude_responses" in config:
    response_summary = response_summary[~response_summary["response"].isin(config["exclude_responses"])]

# Apply response aliases if available
if "response_aliases" in config:
    response_summary["response_display"] = response_summary["response"].map(config["response_aliases"]).fillna(response_summary["response"])
else:
    response_summary["response_display"] = response_summary["response"]

# Apply custom ordering
if "custom_order" in config:
    # Create a mapping for custom order
    order_map = {resp: i for i, resp in enumerate(config["custom_order"])}
    response_summary["order"] = response_summary["response"].map(order_map)
    response_summary = response_summary.sort_values("order")
    sort_order = config["custom_order"]
else:
    # Default to sorting by percentage (descending)
    response_summary = response_summary.sort_values("percent", ascending=False)
    sort_order = response_summary["response"].tolist()

# Create color scale
if "custom_colors" in config:
    color_scale = alt.Scale(domain=list(config["custom_colors"].keys()), 
                           range=list(config["custom_colors"].values()))
else:
    color_scale = alt.Scale(scheme="category20")

# Create responsive bar chart based on detected screen size
if st.session_state.is_mobile:
    # Vertical bar chart for mobile devices with legend below
    legend_config = alt.Legend(
        orient="bottom",
        direction="horizontal",
        titleOrient="top",
        columns=2,
        labelLimit=200,
        title="Response"
    )
    
    response_chart = (
        alt.Chart(response_summary.round(2))
        .mark_bar()
        .encode(
            x=alt.X("response_display:N", title="Response", sort=sort_order,
                    axis=alt.Axis(labelAngle=-45, labelLimit=0)),
            y=alt.Y("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")),
            color=alt.Color("response_display:N", legend=legend_config, scale=color_scale, sort=sort_order),
            tooltip=[
                alt.Tooltip("response_display", title="Response"),
                alt.Tooltip("percent", format=".0%", title="Percentage")
            ]
        )
        .properties(
            title={
                "text": textwrap.wrap(f"{df_filtered['q_verb'].iloc[0] if 'q_verb' in df_filtered.columns else selected_question}", width=50),
                "fontSize": 16,
                "fontStyle": "italic",
                "fontWeight": 400,
                "color": "#59595b"
            },
            height=500
        )
    )
    
    # Create labels for vertical bars
    response_chart_label = (
        alt.Chart(response_summary.round(2))
        .mark_text(
            align="center",
            baseline="bottom",
            dy=-3  # Nudges text above the bar
        )
        .encode(
            x=alt.X("response_display:N", title="Response", sort=sort_order),
            y=alt.Y("percent:Q", title="Percentage"),
            color=alt.Color("response:N", legend=None, scale=color_scale),
            text=alt.Text("percent:Q", format=".0%")
        )
    )
else:
    # Horizontal bar chart for desktop
    response_chart = (
        alt.Chart(response_summary.round(2))
        .mark_bar()
        .encode(
            x=alt.X("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")),
            y=alt.Y("response_display:N", title="Response", sort=sort_order,
                    axis=alt.Axis(labelLimit=0)),  # Remove Y-axis label truncation
            color=alt.Color("response:N", legend=None, scale=color_scale),
            tooltip=[
                alt.Tooltip("response_display", title="Response"),
                alt.Tooltip("percent", format=".0%", title="Percentage")
            ]
        )
        .properties(
            title={
                "text": textwrap.wrap(f"{df_filtered['q_verb'].iloc[0] if 'q_verb' in df_filtered.columns else selected_question}", width=130),
                "fontSize": 18,
                "fontStyle": "italic",
                "fontWeight": 400,
                "color": "#59595b"
            }
        )
    )
    
    # Create labels for horizontal bars
    response_chart_label = (
        alt.Chart(response_summary.round(2))
        .mark_text(
            align="left",
            baseline="middle",
            dx=3  # Nudges text to the right
        )
        .encode(
            x=alt.X("percent:Q", title="Percentage"),
            y=alt.Y("response_display:N", title="Response", sort=sort_order),
            color=alt.Color("response:N", legend=None, scale=color_scale),
            text=alt.Text("percent:Q", format=".0%")
        )
    )

st.markdown(f"""
    <div style='color: #2364a0; font-size: 27px; font-weight: Bold;'>
        <p>{selected_year} Response Distribution</p>
    </div>
    """, unsafe_allow_html=True)
st.altair_chart(response_chart + response_chart_label, use_container_width=True)
st.caption("Note: Remaining percentages are either Don't Know or Not Available.")
if st.session_state.is_mobile is False:
    st.markdown("""
                <span style='color: #59595b; font-size: 15px; font-weight:600 ;'>
                *Chart displaying funky? Mobile view is available via a checkbox in the expandable sidebar.
                </span>
        """, unsafe_allow_html=True)


st.markdown("---")  # Add a separator line
# --- Year-over-Year Trends ---
if "survey year" in df_question.columns and question_hist[selected_question] == 1:
    # Use df_question (not df_filtered) to show all years regardless of year filter
    # But apply demographic filter if one is selected
    year_trend = (
        df_question.groupby(["survey year", "response"])["countywt"]
        .sum()
        .reset_index()
    )
    
    # Calculate percentages within each year
    year_trend["percent"] = (
        year_trend.groupby("survey year")["countywt"]
        .transform(lambda x: x / x.sum())
    )
    
    # Apply the same custom configurations as the main response chart
    # Use 2025 configuration for year-over-year trends
    question_config = chart_configs.get(selected_question, {})
    if "2025" in question_config:
        config = question_config["2025"]
    else:
        config = {}  # Use Altair defaults
    
    # Filter out excluded responses
    if "exclude_responses" in config:
        year_trend = year_trend[~year_trend["response"].isin(config["exclude_responses"])]
    
    # Apply response aliases if available
    if "response_aliases" in config:
        year_trend["response_display"] = year_trend["response"].map(config["response_aliases"]).fillna(year_trend["response"])
    else:
        year_trend["response_display"] = year_trend["response"]
    
    # Apply custom ordering
    if "custom_order" in config:
        sort_order = config["custom_order"]
    else:
        # Default to sorting by response name
        sort_order = sorted(year_trend["response"].unique().tolist())
    
    # Create color scale
    if "custom_colors" in config:
        if "response_aliases" in config:
            # Map aliased values to colors
            aliased_colors = {}
            for original_response, color in config["custom_colors"].items():
                if original_response in config["response_aliases"]:
                    aliased_colors[config["response_aliases"][original_response]] = color
                else:
                    aliased_colors[original_response] = color
            color_scale = alt.Scale(domain=list(aliased_colors.keys()), 
                                   range=list(aliased_colors.values()))
        else:
            color_scale = alt.Scale(domain=list(config["custom_colors"].keys()), 
                                   range=list(config["custom_colors"].values()))
    else:
        color_scale = alt.Scale(scheme="category20")
    
    year_trend["survey year"] = year_trend["survey year"].astype(str)
    
    # Determine the start year dynamically from the data
    min_year = year_trend["survey year"].min()
    start_date = f"{min_year}-01-01"
    end_date = "2025-12-31"
    
    # Configure legend position based on mobile/desktop view
    if st.session_state.is_mobile:
        # Mobile view: legend below the chart
        legend_config = alt.Legend(
            orient="bottom",
            direction="horizontal",
            titleOrient="top",
            columns=2,  # Show legend items in 2 columns for better mobile layout
            labelLimit=200
        )
    else:
        # Desktop view: legend on the right (default)
        legend_config = alt.Legend(
            orient="right",
            titleOrient="top"
        )
    
    trend_chart = (
        alt.Chart(year_trend.round(2))
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "survey year:T", 
                title="Survey Year", 
                axis=alt.Axis(tickCount="year"),
                scale=alt.Scale(domain=[start_date, end_date]),
            ),
            y=alt.Y("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")),
            color=alt.Color("response_display:N", title="Response", scale=color_scale, legend=legend_config),
            tooltip=[
                alt.Tooltip("survey year:T", format="%Y", title="Survey Year", timeUnit='utcyear'), 
                alt.Tooltip("response_display", title="Response"), 
                alt.Tooltip("percent", format=".0%", title="Percentage")
            ]
        )
        .properties(
            title="Response Trends Over Time (All Years)"
        )
    )
    
    st.markdown(f"""
    <div style='color: #2364a0; font-size: 27px; font-weight: Bold;'>
        <p>Year-over-Year Trends</p>
    </div>
    """, unsafe_allow_html=True)

    st.altair_chart(trend_chart, use_container_width=True)
    st.caption("Note: Remaining percentages are either Don't Know or Not Available.")
    st.info("📊 This chart shows trends across ALL survey years, regardless of the year filter above.")
else:
    st.markdown(f"""
    <div style='color: #2364a0; font-size: 27px; font-weight: Bold;'>
        <p>Year-over-Year Trends</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📊 There is no recent and viable year-over-year trend data for this question.")

# Logo display
st.markdown("---")  # Add a separator line

st.text("Survey Results Courtesy of the Kennesaw State University's A.L. Burruss Institute of Public Service & Research and the ARC Research & Innovation")

# Create centered columns with better alignment
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Assets/Fw_ltnUt_400x400.png", width=300, use_container_width=False)
    st.link_button("Visit KSU Burruss Institute", "https://www.kennesaw.edu/external-affairs/burruss-institute/index.php")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Assets/logo-with-text.svg", width=200, use_container_width=False)
    st.link_button("Visit Atlanta Regional Commission", "https://atlantaregional.org/")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p><span style='color: #2364a0; font-size: 15px; font-weight: Bold;'>More data from ARC Research & Innovation</span></p>", unsafe_allow_html=True)
    st.link_button("Visit ARC Research & Innovation", "https://atlantaregional.org/what-we-do/research-and-data/")
    st.link_button("Visit ARC Open Data", "https://opendata.atlantaregional.com/")
    st.link_button("Visit ARC 33°n Blog", "https://33n.atlantaregional.com/")
    st.markdown("</div>", unsafe_allow_html=True)
