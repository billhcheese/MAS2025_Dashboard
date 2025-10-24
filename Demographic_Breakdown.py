import pandas as pd
import altair as alt
import streamlit as st
import textwrap

st.set_page_config(page_icon="Assets/metro-atl-speaks.svg")

# Cache data loading for better performance
@st.cache_data
def load_data():
    """Load the MAS Dashboard data with caching."""
    return pd.read_parquet("Data/MAS_Dashboard_Records_2025_Updated.parquet")

# Load data
df = load_data()

custom_css = """
<style>
.stMainBlockContainer {
            max-width:68rem;
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
        <p>Demographic Breakdown Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='line-height: 1.5;'>
        <p>
            <span style='color: #59595b; font-size: 15px; font-weight:600 ;'>
            *Mobile view is available via a checkbox in the sidebar.
            </span>
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

chart_configs = {
    "bigprob": {
        # Year-specific configurations only
        "2025": {
            "exclude_responses": ["DK"],
            "custom_order": ["Housing Affordability", "Traffic", "Economy", "Crime", "Local Tax Increases", "Other", "Infrastructure", "Quality of Local Schools", "Public Health", "Environmental Pollution"],
            "custom_colors": {
                "Housing Affordability": "#FE6100",
                "Traffic": "#648FFF",
                "Economy": "#DC267F",
                "Crime": "#FFB000",
                "Local Tax Increases": "#BED77C",
                "Infrastructure": "#AE1EC7",
                "Quality of Local Schools": "#9DA786",
                "Public Health": "#425FA2",
                "Environmental Pollution": "#2D3A5A",
                "Other": "#AF1737",

                }
        },
        "2024": {
            "exclude_responses": ["DK"],
            "custom_order": ["Economy", "Crime", "Transportation", "Human Services", "Taxes", "Public Health", "Public Education", "Race Relations", "Other"],
            "custom_colors": {
                "Economy": "#DC267F",
                "Crime": "#FFB000",
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",
                "Other": "#AF1737"
                }
            },
        "2023": {
            "exclude_responses": ["DK"],
            "custom_order": ["Economy", "Crime", "Transportation", "Human Services", "Taxes", "Public Health", "Public Education", "Race Relations", "Other"],
            "custom_colors": {
                "Economy": "#DC267F",
                "Crime": "#FFB000",
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2021": {
            "exclude_responses": ["DK"],
            "custom_order": ["Crime", "Economy", "Transportation", "Public Health", "Race Relations", "Human Services", "Public Education", "Taxes", "Other"],
            "custom_colors": {
                "Economy": "#DC267F",
                "Crime": "#FFB000",
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2020": {
            "exclude_responses": ["DK"],
            "custom_order": ["Public Health", "Crime", "Economy", "Transportation", "Race Relations", "Human Services", "Public Education", "Taxes", "Other"],
            "custom_colors": {
                "Economy": "#DC267F",
                "Crime": "#FFB000",
                "Transportation": "#648FFF",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2019": {
            "exclude_responses": ["DK"],
            "custom_order": ["Transportation", "Crime", "Economy", "Human Services", "Public Education", "Public Health", "Taxes", "Race Relations", "Other"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2018": {
            "exclude_responses": ["DK"],
            "custom_order": ["Transportation", "Crime", "Public Education", "Economy", "Human Services", "Public Health", "Taxes", "Race Relations", "Other"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2017": {
            "exclude_responses": ["DK"],
            "custom_order": ["Transportation", "Crime", "Economy", "Human Services", "Public Education", "Public Health", "Taxes", "Race Relations", "Other"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
                "Other": "#AF1737"
                }
            },
        "2016": {
            "exclude_responses": ["DK"],
            "custom_order": ["Transportation", "Crime", "Economy", "Public Education", "Human Services", "Race Relations", "Public Health", "Taxes",  "Other"],
            "custom_colors": {
                "Transportation": "#648FFF",
                "Crime": "#FFB000",
                "Economy": "#DC267F",
                "Human Services": "#AE1EC7",
                "Taxes": "#BED77C",
                "Public Health": "#425FA2",
                "Public Education": "#9DA786",
                "Race Relations": "#FE6100",                
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

# Initialize widget key with saved value if coming from another page
if 'demo_question_selectbox' not in st.session_state:
    if 'shared_question_text' in st.session_state and st.session_state.shared_question_text in display_options:
        st.session_state.demo_question_selectbox = st.session_state.shared_question_text
    else:
        st.session_state.demo_question_selectbox = display_options[0]

# Callback to sync selection to shared state
def sync_question_selection():
    st.session_state.shared_question_text = st.session_state.demo_question_selectbox

selected_display = st.selectbox(
    "Choose a question from the MAS 2025 Survey", 
    display_options,
    key="demo_question_selectbox",
    on_change=sync_question_selection,
    help="Select a question to display, (No Trend) questions do not have year-over-year trend data whereas (Trend Available) questions do if you scroll down")

selected_question = question_map[display_to_question[selected_display]]

# Filter data for selected question
df_question = df[df["question"] == selected_question].copy()

# Year filter
if "survey year" in df_question.columns:
    col1, col2 = st.columns([3,1], gap="small")
    with col1:
         available_years = sorted(df_question["survey year"].dropna().unique(), reverse=True)
         year_options = [str(year) for year in available_years]
         
         # Initialize widget key with saved value if coming from another page
         if 'demo_year_radio' not in st.session_state:
             if 'shared_year_text' in st.session_state and st.session_state.shared_year_text in year_options:
                 st.session_state.demo_year_radio = st.session_state.shared_year_text
             else:
                 st.session_state.demo_year_radio = year_options[0]
         
         # Callback to sync selection to shared state
         def sync_year_selection():
             st.session_state.shared_year_text = st.session_state.demo_year_radio
         
         selected_year = st.radio(
             "Select Survey Year", 
             options=year_options,
             key="demo_year_radio",
             on_change=sync_year_selection,
             help="Select which MAS survey year to use for the graph",
             horizontal=True)
    with col2:
        brkdwn_mode = st.pills(
            "Select Summary Type", 
            options=["Topline", "Detailed"], 
            default="Detailed",
            help="Display summary responses for the whole Metro Atlanta Region (Topline) or responses broken down by demographic (Detailed)"
            )
        if brkdwn_mode == "Topline":
            st.switch_page("Metro_Summary.py")
    
    # Apply year filter for county breakdown
    df_year_filtered = df_question[df_question["survey year"] == int(selected_year)].copy()

else:
    df_year_filtered = df_question.copy()
    selected_year = "2025"

# Demographic selection for historical analysis
demographic_options = ["Jurisdiction", "Race", "Hispanic", "Gender", "Age", "Yrs in Metro", "Education", "Income", "Homeownership", "Employment", "Work Setting"]

# Initialize demographic selection state if not exists (use a separate variable for storage)
if 'saved_demographic' not in st.session_state:
    st.session_state.saved_demographic = "Jurisdiction"

# Initialize widget key with saved value on first load
if 'demo_segmented_control' not in st.session_state:
    st.session_state.demo_segmented_control = st.session_state.saved_demographic

# Callback to save selection
def save_demographic_selection():
    if st.session_state.demo_segmented_control is not None:
        st.session_state.saved_demographic = st.session_state.demo_segmented_control

selected_demographic = st.segmented_control(
    "Select Demographic", 
    options = demographic_options,
    selection_mode = "single",
    key="demo_segmented_control",
    on_change=save_demographic_selection,
    help="Select demographic type to breakdown results by")

# If user clicks on the same demographic again, it returns None, so use the saved value
if selected_demographic == None:
    selected_demographic = st.session_state.saved_demographic
placeholder_selected_demo_value = st.empty()

#selected_demographic = st.selectbox("Select demographic for historical analysis", demographic_options)

# Get the actual column name for the selected demographic
demo_col_map = {
    "Jurisdiction": "county",
    "Race": "black or white", 
    "Hispanic": "latino",
    "Gender": "gender",
    "Age": "age group more categories",
    "Yrs in Metro": "years in metro Atl categorized",
    "Education": "education",
    "Income": "income",
    "Homeownership": "homeownership",
    "Employment": "employment status",
    "Work Setting": "remote worker status"
}
demo_column = demo_col_map[selected_demographic]

excluded_demographics = {
    "Hispanic": ["DK"],
    "Gender":["Identified with gender in different way","DK"],
    "Education": ["DK"],
    "Income": ["DK"],
    "Homeownership": ["DK"],
    "Employment": ["Disabled","DK"],
    "Work Setting": ["DK"],
}

demo_grp_order = {
    "Race": ["black", "white", "other"], 
    "Hispanic": ["Yes", "No"],
    "Gender": ["Female", "Male"],
    "Yrs in Metro": ["5 years or less", "6-10 years", "11-20 years", "21-30 years", "over 30 years"],
    "Education": ["Less than high school", "High school or GED", "Some college or technical school", "BA or BS", "Graduate or Professional Degree"],
    "Income": ["Less than $25K", "$25K-60K", "$60k-$120K", "$120k-$250k", "Over $250k", "Refused"],
    "Employment": ["Working full-time", "Working part-time", "Unemployed but seeking work", "Unemployed and not looking for work", "Retired"],
}

demo_grp_rename = {
    "Jurisdiction": {
        "Atlanta": "City of Atlanta",
        "Cherokee": "Cherokee County",
        "Clayton": "Clayton County",
        "Cobb": "Cobb County",
        "DeKalb": "DeKalb County",
        "Douglas": "Douglas County",
        "Fayette": "Fayette County",
        "Forsyth": "Forsyth County",
        "Fulton": "Fulton County",
        "Gwinnett": "Gwinnett County",
        "Henry": "Henry County",
        "Rockdale": "Rockdale County",
    },
    "Race": {
        "black": "Black",
        "white": "White",
        "other": "Other"
    }, 
    "Age": {
        "18-24": "18-24 yrs",
        "25-34": "25-34 yrs",
        "35-44": "35-44 yrs",
        "45-54": "45-54 yrs",
        "55-64": "55-64 yrs",
        "65 and older": "65+ yrs",
    },
    "Yrs in Metro": {
        "5 years or less": "5 yrs or less",
        "6-10 years": "6-10 yrs",
        "11-20 years": "11-20 yrs",
        "21-30 years": "21-30 yrs",
        "over 30 years": "30+ yrs",
    },
    "Income": {
        "Less than $25K": "Less than $25k",
        "$25K-60K": "$25k-$60k",
        "$60K-$120K": "$60k-$120k",
        "$120k-$250k": "$120k-$250k",
        "Over $250k": "$250k+",
        "Refused": "Refused",
    },
    "Employment": {
        "Working full-time": "Full-time",
        "Working part-time": "Part-time",
        "Unemployed but seeking work": "Unemployed (seeking)",
        "Unemployed and not looking for work": "Unemployed (not seeking)",
        "Retired": "Retired",
    },
    "Work Setting": {
        "Work remotely all of the time": "Remote All of Time",
        "Work remotely some of the time and from a place of business": "Hybrid",
        "work at a place of business all the time": "Fully In-Person",
    }
}

# Demographic value selection for historical analysis
if demo_column in df_question.columns:
    demo_values = df_question[demo_column].dropna().unique().tolist()
    # Add Atlanta to county options if it's not already there
    if selected_demographic == "Jurisdiction" and "Atlanta" not in demo_values:
        demo_values.append("Atlanta")
else:
    demo_values = []
    selected_demo_value = None

if len(df_year_filtered) > 0:
    
    # --- Demographic Breakdown Chart ---
    
    if demo_column in df_year_filtered.columns:
        # Create demographic breakdown with Atlanta only for Jurisdiction demographic
        county_data = []
        
        # Process ALL demographic groups using countywt
        if len(df_year_filtered) > 0:
            regular_crosstab = (
                df_year_filtered.groupby([demo_column, "response"])["countywt"]
                .sum()
                .reset_index()
            )
            county_data.append(regular_crosstab)
        
        # Process Atlanta using atlwt ONLY if Jurisdiction is selected
        if (selected_demographic == "Jurisdiction" and 
            "atlanta resident" in df_year_filtered.columns and 
            "atlwt" in df_year_filtered.columns):
            atlanta_data = df_year_filtered[df_year_filtered["atlanta resident"] == "Yes"].copy()
            if len(atlanta_data) > 0:
                atlanta_crosstab = (
                    atlanta_data.groupby(["response"])["atlwt"]
                    .sum()
                    .reset_index()
                )
                # Add Atlanta as the county name
                atlanta_crosstab[demo_column] = "Atlanta"
                # Reorder columns to match regular counties
                atlanta_crosstab = atlanta_crosstab[[demo_column, "response", "atlwt"]]
                # Rename atlwt to countywt for consistency
                atlanta_crosstab = atlanta_crosstab.rename(columns={"atlwt": "countywt"})
                county_data.append(atlanta_crosstab)
        
        # Combine all demographic data
        if county_data:
            county_crosstab = pd.concat(county_data, ignore_index=True)
            
            # Calculate percentages within each demographic group
            county_crosstab["percent"] = (
                county_crosstab.groupby(demo_column)["countywt"]
                .transform(lambda x: x / x.sum())
            )
        else:
            county_crosstab = pd.DataFrame()
    else:
        st.warning(f"{selected_demographic} data not available for this question.")
        county_crosstab = pd.DataFrame()
    
    # Apply custom configurations if available for the selected year only
    # If no year-specific config exists, use Altair defaults
    if len(county_crosstab) > 0:
        question_config = chart_configs.get(selected_question, {})
        if str(selected_year) in question_config:
            config = question_config[str(selected_year)]
        else:
            config = {}  # Use Altair defaults
        
        # Filter out excluded responses
        if "exclude_responses" in config:
            county_crosstab = county_crosstab[~county_crosstab["response"].isin(config["exclude_responses"])]
        
        # Apply response aliases if available
        if "response_aliases" in config:
            county_crosstab["response_display"] = county_crosstab["response"].map(config["response_aliases"]).fillna(county_crosstab["response"])
            response_column = "response_display"
            # Create reverse mapping from alias to original
            alias_to_original = {v: k for k, v in config["response_aliases"].items()}
        else:
            response_column = "response"
            alias_to_original = {}
        
        # Apply custom ordering
        if "custom_order" in config:
            # Create a mapping for custom order
            # custom_order might contain either original or aliased values, so we need to handle both
            order_map = {}
            for i, resp in enumerate(config["custom_order"]):
                # Map both the value itself and its original (if it's an alias)
                order_map[resp] = i
                if resp in alias_to_original:
                    order_map[alias_to_original[resp]] = i
            
            # Apply order mapping to original response values
            county_crosstab["order"] = county_crosstab["response"].map(order_map)
            county_crosstab = county_crosstab.sort_values(["order", demo_column])
            # Sort order should use the custom_order as-is (it already contains the display values)
            sort_order = config["custom_order"]
        else:
            # Default to sorting by percentage (descending)
            county_crosstab = county_crosstab.sort_values("percent", ascending=False)
            sort_order = county_crosstab[response_column].unique().tolist()
        
        # Create color scale
        if "custom_colors" in config:
            # Map colors to aliased values if aliases exist
            if "response_aliases" in config:
                aliased_colors = {}
                for original_response, color in config["custom_colors"].items():
                    aliased_response = config["response_aliases"].get(original_response, original_response)
                    aliased_colors[aliased_response] = color
                color_scale = alt.Scale(domain=list(aliased_colors.keys()), 
                                       range=list(aliased_colors.values()))
                white_scale = alt.Scale(domain=list(aliased_colors.keys()), 
                                       range=list(["#FFFFFF"]*len(aliased_colors.keys())))
            else:
                color_scale = alt.Scale(domain=list(config["custom_colors"].keys()), 
                                       range=list(config["custom_colors"].values()))
                white_scale = alt.Scale(domain=list(config["custom_colors"].keys()), 
                                       range=list(["#FFFFFF"]*len(config["custom_colors"].keys())))
        else:
            color_scale = alt.Scale(scheme="category20")
        
        # Determine the correct column name for the chart
        if selected_demographic == "Atlanta":
            chart_column = "atlanta"
        else:
            chart_column = demo_column
        
        # Filter out excluded demographic groups (after chart_column is defined)
        exclude_demo_allyrs_switch = True
        if exclude_demo_allyrs_switch == True:
            if selected_demographic in excluded_demographics:
                excluded_groups = excluded_demographics[selected_demographic]
                county_crosstab = county_crosstab[~county_crosstab[chart_column].isin(excluded_groups)]
        else:
            if "exclude_demographics" in config:
                # Check if there are exclusions for the current demographic
                if selected_demographic in config["exclude_demographics"]:
                    excluded_groups = config["exclude_demographics"][selected_demographic]
                    county_crosstab = county_crosstab[~county_crosstab[chart_column].isin(excluded_groups)]
        
        # Apply demographic group renaming and ordering
        if selected_demographic in demo_grp_rename:
            # Create a display column with renamed values
            county_crosstab[f"{chart_column}_display"] = county_crosstab[chart_column].map(demo_grp_rename[selected_demographic]).fillna(county_crosstab[chart_column])
            chart_display_column = f"{chart_column}_display"
        else:
            # Use original column if no renaming defined
            chart_display_column = chart_column
        
        # Apply demographic group ordering
        if selected_demographic in demo_grp_order:
            # Create order mapping for demographic groups
            demo_order_map = {grp: i for i, grp in enumerate(demo_grp_order[selected_demographic])}
            county_crosstab["demo_order"] = county_crosstab[chart_column].map(demo_order_map)
            # Sort by demo_order (and existing order if present)
            if "order" in county_crosstab.columns:
                county_crosstab = county_crosstab.sort_values(["demo_order", "order"])
            else:
                county_crosstab = county_crosstab.sort_values("demo_order")
            demo_sort_order = [demo_grp_rename[selected_demographic].get(grp, grp) if selected_demographic in demo_grp_rename else grp 
                              for grp in demo_grp_order[selected_demographic]]
        else:
            demo_sort_order = None
            
        # Configure chart orientation based on mobile/desktop view
        if st.session_state.is_mobile:
            # Mobile view: Vertical stacked bars with legend below
            stacked_chart = alt.Chart(county_crosstab.round(2)).encode(
                x=alt.X(f"{chart_display_column}:N", title=selected_demographic,
                        axis=alt.Axis(labelLimit=0, labelAngle=-45), sort=demo_sort_order),
                y=alt.Y("percent:Q", title="Percentage", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=[0, 1])),
            )
            legend_config = alt.Legend(
                orient="bottom",
                direction="horizontal",
                titleOrient="top",
                columns=2,
                labelLimit=200
            )
        else:
            # Desktop view: Horizontal stacked bars with legend on right
            stacked_chart = alt.Chart(county_crosstab.round(2)).encode(
                x=alt.X("percent:Q", title="Percentage", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=[0, 1])),
                y=alt.Y(f"{chart_display_column}:N", title=selected_demographic,
                        axis=alt.Axis(labelLimit=0), sort=demo_sort_order),
            )
            legend_config = alt.Legend(
                orient="right",
                titleOrient="top"
            )
        
        #county_crosstab.to_csv("county_crosstab.csv")
        # Create selection for interactive chart
        selection = alt.selection_single(name="single", fields=[chart_column], empty="none")
        
        county_chart = (
            stacked_chart
            .mark_bar()
            .encode(
                #x=alt.X("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")),
                #y=alt.Y(f"{chart_column}:N", title=selected_demographic,
                #        axis=alt.Axis(labelLimit=0)),  # Remove label truncation
                color=alt.Color(f"{response_column}:N", title="Response", scale=color_scale, sort=sort_order, legend=legend_config),
                order=alt.Order("order:Q") if "custom_order" in config else alt.Order("percent:Q", sort="descending"),
                tooltip=[
                    alt.Tooltip(chart_display_column, title=selected_demographic),
                    alt.Tooltip(response_column, title="Response"), 
                    alt.Tooltip("percent", format=".0%")
                ],
                opacity=alt.condition(selection, alt.value(1.0), alt.value(0.7))
            )
            .add_selection(selection)
            .properties(
                title={
                    "text":textwrap.wrap(f"{df_year_filtered['q_verb'].iloc[0] if 'q_verb' in df_year_filtered.columns else selected_question}", width=140),
                    "subtitle":f"Response by {selected_demographic} Demographic ({selected_year})",
                    "subtitleFontSize": 12,
                    "subtitleColor": "#666666"
                },
                height=600 if st.session_state.is_mobile else 400  # Taller chart for mobile view
            )
            .configure_title(
                subtitlePadding=10
            )
        )
        
        # Add text labels for percentages (not supported by streamlit for now)
        # county_chart_labels = (
        #     stacked_chart
        #     .mark_text(
        #         align="center",
        #         baseline="middle",
        #         fontSize=12,
        #         fontWeight="normal",
        #         #color='white'
        #     )
        #     .encode(
        #         x=alt.X("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")).stack('zero'),
        #         y=alt.Y(f"{chart_column}:N", title=selected_demographic,
        #                 axis=alt.Axis(labelLimit=0)),
        #         color=alt.Color("response:N", title="Response", scale=white_scale),
        #         text=alt.Text("percent:Q", format=".0%")
        #     )
        # )

        
    else:
        st.warning("Data not available for this demographic group and question.")
    
    # --- Historical Demographic Analysis ---

    
    # Display the chart and get selection (only if data is available)
    if len(county_crosstab) > 0:
        chart_event = st.altair_chart(county_chart, use_container_width=True, on_select="rerun", selection_mode="single")
        
        # Add footer note below the chart
        st.caption("Note: Remaining percentages are either Don't Know or Not Available. Percentages may vary slightly from those reported in other MAS products, go to FAQ for more details.")
        # Get selected demographic from chart interaction
        if chart_event and chart_event['selection']['single']:
            try:
                # Debug: Show the structure of chart_event
                #st.write("Debug - Chart event structure:", chart_event)
                
                # Try to get the selection value
                selection_data = chart_event['selection']
                #st.write("Debug - Selection data:", selection_data)
                #st.write("Debug - Chart column:", chart_column)
                selected_demo_value = selection_data['single'][0][chart_column]
                #if chart_column in selection_data and selection_data[chart_column]:
                #    selected_demo_value = selection_data[chart_column][0]
                #    st.info(f"Showing historical trends for: **{selected_demo_value}**")
                #else:
                #    # Fallback to selectbox if selection data is not in expected format
                #    selected_demo_value = st.selectbox(f"Or select {selected_demographic} for historical analysis:", demo_values)
            except (KeyError, IndexError, TypeError) as e:
                # Fallback to selectbox if there's any error accessing selection data
                st.warning(f"Chart selection error: {e}. Please use the dropdown below.")
                selected_demo_value = st.selectbox(f"Select {selected_demographic} for historical analysis:", demo_values)
        else:
            # Fallback to selectbox if no selection
            #selected_demo_value = st.selectbox(f"{selected_demographic} Demographic Group",demo_values)
            selected_demo_value = None
    else:
        # Fallback to selectbox if no chart data
        selected_demo_value = st.selectbox(f"Select {selected_demographic} for historical analysis", demo_values)

    if demo_column in df_question.columns and selected_demo_value:
        # Handle Atlanta as special case for county analysis
        if selected_demographic == "Jurisdiction" and selected_demo_value == "Atlanta":
            # Filter for Atlanta residents using atlanta resident column
            if "atlanta resident" in df_question.columns and "atlwt" in df_question.columns:
                df_demo_filtered = df_question[df_question["atlanta resident"] == "Yes"].copy()
                weight_column = "atlwt"
            else:
                st.warning("Atlanta resident data or atlwt column not available.")
                df_demo_filtered = pd.DataFrame()
                weight_column = "countywt"
        else:
            # Regular demographic filtering
            df_demo_filtered = df_question[df_question[demo_column] == selected_demo_value].copy()
            weight_column = "countywt"
        
        if len(df_demo_filtered) > 0 and "survey year" in df_demo_filtered.columns:
            # Calculate historical trends for the selected demographic
            historical_trend = (
                df_demo_filtered.groupby(["survey year", "response"])[weight_column]
                .sum()
                .reset_index()
            )
            
            # Calculate percentages within each year
            historical_trend["percent"] = (
                historical_trend.groupby("survey year")[weight_column]
                .transform(lambda x: x / x.sum())
            )
        else:
            st.warning(f"No historical data available for {selected_demographic}.")
            historical_trend = pd.DataFrame()
    else:
        #st.warning(f"{selected_demographic} data not available for historical analysis because of demographic.")
        historical_trend = pd.DataFrame()
    
    # Create historical chart if data is available
    if question_hist[selected_question] == 1 and selected_demo_value is not None:
        # Apply the same custom configurations as the demographic breakdown chart
        # Use 2025 configuration for historical trends
        question_config = chart_configs.get(selected_question, {})
        if "2025" in question_config:
            hist_config = question_config["2025"]
        else:
            hist_config = {}  # Use Altair defaults
        
        # Filter out excluded responses
        if "exclude_responses" in hist_config:
            historical_trend = historical_trend[~historical_trend["response"].isin(hist_config["exclude_responses"])]
        
        # Apply response aliases if available
        if "response_aliases" in hist_config:
            historical_trend["response_display"] = historical_trend["response"].map(hist_config["response_aliases"]).fillna(historical_trend["response"])
        else:
            historical_trend["response_display"] = historical_trend["response"]
        
        # Create color scale
        if "custom_colors" in hist_config:
            if "response_aliases" in hist_config:
                # Map aliased values to colors
                aliased_colors = {}
                for original_response, color in hist_config["custom_colors"].items():
                    if original_response in hist_config["response_aliases"]:
                        aliased_colors[hist_config["response_aliases"][original_response]] = color
                    else:
                        aliased_colors[original_response] = color
                hist_color_scale = alt.Scale(domain=list(aliased_colors.keys()), 
                                           range=list(aliased_colors.values()))
            else:
                hist_color_scale = alt.Scale(domain=list(hist_config["custom_colors"].keys()), 
                                           range=list(hist_config["custom_colors"].values()))
        else:
            hist_color_scale = alt.Scale(scheme="category20")
        
        # Convert survey year to string for temporal encoding
        historical_trend["survey year"] = historical_trend["survey year"].astype(str)
        
        # Determine the start year from the data
        min_year = historical_trend["survey year"].min()
        start_date = f"{min_year}-01-01"
        end_date = "2025-12-31"
        
        # Configure legend position based on mobile/desktop view
        if st.session_state.is_mobile:
            # Mobile view: legend below the chart
            hist_legend_config = alt.Legend(
                orient="bottom",
                direction="horizontal",
                titleOrient="top",
                columns=2,
                labelLimit=200
            )
        else:
            # Desktop view: legend on the right (default)
            hist_legend_config = alt.Legend(
                orient="right",
                titleOrient="top"
            )
        
        historical_chart = (
            alt.Chart(historical_trend.round(2))
            .mark_line(point=True, strokeWidth=3)
            .encode(
                x=alt.X(
                    "survey year:T", 
                    title="Survey Year", 
                    axis=alt.Axis(tickCount="year"),
                    scale=alt.Scale(domain=[start_date, end_date]),
                ),
                y=alt.Y("percent:Q", title="Percentage", axis=alt.Axis(format=".0%")),
                color=alt.Color("response_display:N", title="Response", scale=hist_color_scale, legend=hist_legend_config),
                tooltip=[
                    alt.Tooltip("survey year:T", format="%Y", title="Survey Year", timeUnit='utcyear'),
                    alt.Tooltip("response_display", title="Response"),
                    alt.Tooltip("percent", format=".0%", title="Percentage")
                ]
            )
            .properties(
                title=f"Historic Response Trends: {selected_demo_value} ({selected_demographic.title()})",
                height=400
            )
        )
        
        st.altair_chart(historical_chart, use_container_width=True)
        st.info("📊 The Historic Response Trends chart shows trends across ALL survey years, regardless of the year filter above.")
        
    elif question_hist[selected_question] == 1 and selected_demo_value == None:
        with placeholder_selected_demo_value.container():
            st.markdown("💡 **Tip:** *Click on any bar in the stacked bar chart below and Scroll Down to see historical trends for that demographic group which will pop up in a lower chart*")
    else:
        st.info("Selected question does not have historical data or has no valid time series data.")
   
else:
    st.info("No data available for the selected filters.")

# Side-by-side logo display
st.markdown("---")  # Add a separator line
st.text("Survey Results Courtesy of the Kennesaw State University's A.L. Burruss Institute of Public Service & Research and ARC Research & Innovation")

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
