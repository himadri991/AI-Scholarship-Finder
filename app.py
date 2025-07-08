import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

# Disable Streamlit file watcher to prevent torch.classes errors
os.environ["STREAMLIT_SERVER_WATCH_DIRS"] = "false"

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Check required environment variables - UPDATED FOR GEMINI
required_vars = ['GOOGLE_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    st.stop()

# Import our custom modules
from langchain_agent import ScholarshipChatAgent

# Page configuration - UPDATED FOR GEMINI
st.set_page_config(
    page_title="ScholarDeep AI Scholarship Finder - Powered by Scholardeep",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
@st.cache_resource
def initialize_chat_agent():
    """Initialize chat agent with proper error handling"""
    try:
        return ScholarshipChatAgent()
    except Exception as e:
        st.error(f"Failed to initialize AI agent: {e}")
        return None

if 'chat_agent' not in st.session_state:
    st.session_state.chat_agent = initialize_chat_agent()
if 'messages' not in st.session_state:
    st.session_state.messages = []

def main():
    # UPDATED TITLE AND INFO FOR GEMINI
    st.title("🎓 AI Scholarship Finder")
    st.markdown("**Powered by Scholardeep** - Advanced AI scholarship discovery!")
    
    # Display model info - UPDATED FOR GEMINI
    with st.expander("🤖 About this AI"):
        st.write("""
        This scholarship finder uses:
        - **Scholardeep** for advanced natural language understanding
        - **Real-time web access** for the latest scholarship opportunities
        - **Intelligent matching** based on your academic profile
        - **Personalized recommendations** using AI analysis
        - **No database dependency** - Pure AI-powered search
        """)
    
    # Display AI status with better error handling
    if st.session_state.chat_agent:
        st.success("🤖 **AI Status:** AI is ready and connected")
    else:
        st.error("❌ **AI Status:** Not connected. ")
        st.info("🔧 Make sure your .env.local file contains: GOOGLE_API_KEY=your_api_key_here")
    
    # Sidebar for student profile
    with st.sidebar:
        st.header("📝 Student Profile")
        
        name = st.text_input("Full Name", placeholder="Enter your full name")
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"]
        )
        field_of_study = st.selectbox(
            "Field of Study",
            ["Engineering", "Medicine", "Business", "Computer Science", "Arts", "Science", "Law", "Education", "Mathematics"]
        )
        degree_level = st.selectbox(
            "Degree Level",
            ["Undergraduate", "Postgraduate", "PhD"]
        )
        country = st.selectbox(
            "Country",
            ["India", "USA", "UK", "Canada", "Australia", "Germany", "Other"]
        )
        
        # Additional profile fields for better matching

        
        if st.button("💾 Save Profile", type="primary"):
            if name.strip():  # Validate that name is provided
                st.session_state.student_profile = {
                    'name': name,
                    'gender': gender,
                    'field_of_study': field_of_study,
                    'degree_level': degree_level,
                    'country': country
                }
                st.success("✅ Profile saved!")
                st.info("👉 Check the 'Eligible Scholarships' tab to see AI-powered recommendations!")
            else:
                st.error("❌ Please enter your full name to save the profile.")
    
    # Main content with tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat with AI", "🎯 Eligible Scholarships", "🔍 Search Scholarships"])
    
    with tab1:
        # UPDATED HEADER FOR GEMINI
        st.header("💬 Chat with Scholardeep Assistant")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me about scholarships..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response - UPDATED SPINNER TEXT FOR GEMINI
            with st.chat_message("assistant"):
                with st.spinner("🤖 Scholardeep is analyzing your request..."):
                    try:
                        if st.session_state.chat_agent:
                            # Get response from agent
                            response = st.session_state.chat_agent.chat(prompt)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        else:
                            error_msg = "❌ AI assistant is not available. Please check your Google API key configuration."
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        
                    except Exception as e:
                        # UPDATED ERROR MESSAGE FOR GEMINI
                        error_msg = f"⚠️ I encountered an error: {str(e)}\n\nPlease check your Google API key and try again."
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    with tab2:
        st.header("🎯 Eligible Scholarships For You")
        
        if 'student_profile' not in st.session_state:
            st.warning("⚠️ Please save your profile in the sidebar first!")
            st.info("👈 Fill out your information in the sidebar and click 'Save Profile'")
        else:
            # Add refresh button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🔄 Refresh Scholarships", key="refresh_scholarships"):
                    # Force refresh by clearing cache
                    st.rerun()
            
            # Create tabs for different scholarship sources
            source_tab1, source_tab2 = st.tabs(["📋 Database Scholarships", "🤖 AI Recommendations"])
            
            with source_tab1:
                st.subheader("📋 Eligible Scholarships from Database")
                try:
                    # Load scholarships from JSON file
                    with open("scholarships.json", "r") as f:
                        scholarships = json.load(f)
                    
                    profile = st.session_state.student_profile
                    
                    # Filter eligible scholarships
                    eligible_scholarships = []
                    for scholarship in scholarships:
                        is_eligible = True
                        
                        # Check degree level
                        if profile['degree_level'] not in scholarship['degree_level']:
                            is_eligible = False
                        
                        # Check field of study
                        if profile['field_of_study'] not in scholarship['field_of_study']:
                            is_eligible = False
                        
                        # Check gender eligibility if not "All"
                        if scholarship['gender_eligibility'] != "All" and profile['gender'] != scholarship['gender_eligibility']:
                            is_eligible = False
                        
                        if is_eligible:
                            eligible_scholarships.append(scholarship)
                    
                    # Display eligible scholarships count
                    if eligible_scholarships:
                        st.success(f"✅ Found {len(eligible_scholarships)} eligible scholarships for you!")
                    else:
                        st.warning("⚠️ No eligible scholarships found in our database for your profile.")
                        st.info("Try checking the AI Recommendations tab for more personalized options.")
                    
                    # Display eligible scholarships in a more structured way
                    for scholarship in eligible_scholarships:
                        with st.expander(f"🎓 {scholarship['scholarship_name']}"):
                            st.markdown(f"**Provider:** {scholarship['providing_body']}")
                            st.markdown(f"**Degree Level:** {', '.join(scholarship['degree_level'])}")
                            st.markdown(f"**Field of Study:** {', '.join(scholarship['field_of_study'])}")
                            st.markdown(f"**Gender Eligibility:** {scholarship['gender_eligibility']}")
                            st.markdown(f"**GPA Requirement:** {scholarship['gpa_requirement']}")
                            st.markdown(f"**Description:** {scholarship['brief_description']}")
                            st.markdown(f"**Link:** [{scholarship['link']}]({scholarship['link']})")
                            
                            # Add eligibility match indicators
                            st.success("✅ You are eligible for this scholarship!")
                            
                            # Show matching criteria
                            st.markdown("**Matching Criteria:**")
                            st.markdown(f"- ✓ Your degree level ({profile['degree_level']}) matches the required level")
                            st.markdown(f"- ✓ Your field of study ({profile['field_of_study']}) matches the required fields")
                            if scholarship['gender_eligibility'] == "All":
                                st.markdown(f"- ✓ This scholarship is available for all genders")
                            else:
                                st.markdown(f"- ✓ Your gender ({profile['gender']}) matches the eligibility requirement")
                            
                            # Add apply button
                            st.markdown(f"[🔗 Apply Now]({scholarship['link']})")
                    
                    # Add toggle to show all scholarships
                    if st.checkbox("Show all scholarships (including non-eligible)"):
                        st.subheader("All Available Scholarships")
                        for scholarship in scholarships:
                            # Skip already shown eligible scholarships
                            if scholarship in eligible_scholarships:
                                continue
                                
                            with st.expander(f"🎓 {scholarship['scholarship_name']}"):
                                st.markdown(f"**Provider:** {scholarship['providing_body']}")
                                st.markdown(f"**Degree Level:** {', '.join(scholarship['degree_level'])}")
                                st.markdown(f"**Field of Study:** {', '.join(scholarship['field_of_study'])}")
                                st.markdown(f"**Gender Eligibility:** {scholarship['gender_eligibility']}")
                                st.markdown(f"**GPA Requirement:** {scholarship['gpa_requirement']}")
                                st.markdown(f"**Description:** {scholarship['brief_description']}")
                                st.markdown(f"**Link:** [{scholarship['link']}]({scholarship['link']})")
                                
                                # Add eligibility check
                                reasons = []
                                
                                # Check degree level
                                if profile['degree_level'] not in scholarship['degree_level']:
                                    reasons.append(f"Your degree level ({profile['degree_level']}) doesn't match the required level ({', '.join(scholarship['degree_level'])})")
                                
                                # Check field of study
                                if profile['field_of_study'] not in scholarship['field_of_study']:
                                    reasons.append(f"Your field of study ({profile['field_of_study']}) doesn't match the required fields ({', '.join(scholarship['field_of_study'])})")
                                
                                # Check gender eligibility if not "All"
                                if scholarship['gender_eligibility'] != "All" and profile['gender'] != scholarship['gender_eligibility']:
                                    reasons.append(f"This scholarship is only available for {scholarship['gender_eligibility']} students")
                                
                                # Display eligibility status
                                st.warning("⚠️ You may not be eligible for this scholarship")
                                st.markdown("**Reasons:**")
                                for reason in reasons:
                                    st.markdown(f"- {reason}")
                    
                    # Add profile summary
                    st.divider()
                    st.subheader("📋 Your Profile Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Field", profile['field_of_study'])
                    with col2:
                        st.metric("Level", profile['degree_level'])
                    with col3:
                        st.metric("Gender", profile['gender'])
                    with col4:
                        st.metric("Country", profile['country'])
                    

                    
                except Exception as e:
                    st.error(f"❌ Error loading scholarships: {str(e)}")
                    st.info("🔄 Please try refreshing the page or check if the scholarships.json file exists.")
            
            with source_tab2:
                st.subheader("🤖 AI-Powered Scholarship Recommendations")
                with st.spinner("🤖 Scholardeep is finding scholarships for you..."):
                    try:
                        profile = st.session_state.student_profile
                        
                        # Get scholarships using the new method
                        if st.session_state.chat_agent:
                            # FIXED: Properly formatted f-string for Gemini prompt
                            gemini_prompt = f"""As an expert scholarship advisor with access to current scholarship information, provide a comprehensive analysis of scholarship opportunities for this student profile:

**Student Profile:**
- Name: {profile['name']}
- Gender: {profile['gender']}
- Field of Study: {profile['field_of_study']}
- Degree Level: {profile['degree_level']}
- Country: {profile['country']}

**Please provide:**

1. **🎯 TOP 5 ELIGIBLE SCHOLARSHIPS** - List specific scholarships this student is eligible for, including:
   - Scholarship name and provider
   - Award amount (if known)
   - Eligibility requirements
   - Application deadline (if known)
   - Application process overview

2. **📊 ELIGIBILITY ANALYSIS** - For each scholarship, provide:
   - ✅ Eligible / ⚠️ Potentially Eligible / ❌ Not Eligible
   - Match score (1-10) based on profile alignment
   - Specific requirements they meet/don't meet

3. **💡 PERSONALIZED RECOMMENDATIONS**:
   - Scholarship categories most suitable for this profile
   - Ways to strengthen their application
   - Timeline suggestions for applications
   - Additional opportunities to explore

4. **🚀 ACTION PLAN**:
   - Immediate next steps
   - Documents to prepare
   - Deadlines to watch
   - Tips for success

Please use current scholarship information and be specific about opportunities available in {profile['country']} and internationally for {profile['field_of_study']} students at the {profile['degree_level']} level. Format your response with clear headings, bullet points, and emoji indicators for easy reading."""
                            
                            # Get comprehensive response from Gemini
                            gemini_response = st.session_state.chat_agent.llm.invoke(gemini_prompt)
                            gemini_analysis = gemini_response.content if hasattr(gemini_response, 'content') else str(gemini_response)
                            
                            # Display the comprehensive analysis
                            st.markdown(gemini_analysis)
                            
                            # Success message
                            st.success("✅ AI recommendations loaded successfully!")
                            
                            # Add tips section
                            with st.expander("💡 Application Tips"):
                                st.write("""
                                **📝 Application Best Practices:**
                                - Start applications early (3-6 months before deadlines)
                                - Tailor each application to the specific scholarship
                                - Highlight achievements relevant to the scholarship's mission
                                - Get strong letters of recommendation
                                - Proofread all materials carefully
                                - Follow application instructions exactly
                                - Apply to multiple scholarships to increase chances
                                
                                **📚 Documents Usually Required:**
                                - Academic transcripts
                                - Personal statement/essay
                                - Letters of recommendation
                                - Resume/CV
                                - Financial information (for need-based scholarships)
                                - Portfolio (for creative fields)
                                """)
                        else:
                            st.error("❌ Scholardeep AI model not available. Please check your configuration.")
                            st.info("🔧 Ensure GOOGLE_API_KEY is set in your .env.local file")
                            
                    except Exception as e:
                        st.error(f"❌ Error analyzing scholarships: {str(e)}")
                        st.info("🔄 Please try refreshing the page or check your internet connection.")
                        
                        # Show fallback content on error
                        st.markdown("""
                        ## 📚 While we fix this, here are general scholarship tips:
                        
                        1. **University Financial Aid Office** - Your first stop for institutional aid
                        2. **Fastweb.com** - Comprehensive scholarship database  
                        3. **Professional Associations** - Field-specific opportunities
                        4. **Government Websites** - National and regional programs
                        5. **Local Community Foundations** - Often overlooked opportunities
                        6. **Company Scholarships** - Many corporations offer educational funding
                        """)
    
    with tab3:
        st.header("🔍 Search Scholarships")
        
        col1, col2 = st.columns(2)
        with col1:
            search_query = st.text_input(
                "Search Query", 
                placeholder="e.g., computer science scholarships undergraduate India"
            )
        with col2:
            search_field = st.selectbox(
                "Filter by Field", 
                ["All", "Engineering", "Medicine", "Business", "Computer Science", "Arts", "Science", "Law", "Education"]
            )
        
        if st.button("🔍 Search Now", type="primary"):
            if not search_query:
                st.warning("⚠️ Please enter a search query")
            else:
                with st.spinner("🤖 Scholardeep is searching for scholarships..."):
                    try:
                        # Create comprehensive search prompt for Gemini
                        field_filter = f" specifically for {search_field}" if search_field != "All" else ""
                        
                        search_prompt = f"""As an expert scholarship advisor with access to current scholarship information, please search for scholarships based on this query: "{search_query}"{field_filter}

**Please provide a comprehensive list of scholarships that match this search, including:**

1. **🎯 RELEVANT SCHOLARSHIPS** - List 5-10 scholarships that match the search criteria:
   - Scholarship name and provider organization
   - Award amount (if known)
   - Eligibility requirements
   - Application deadline (if known)
   - Target demographic/field
   - Application process overview
   - Website/contact information (if available)

2. **📊 SEARCH ANALYSIS**:
   - How well each scholarship matches the search query
   - Difficulty level of obtaining each scholarship
   - Best matches for the search criteria

3. **💡 ADDITIONAL OPPORTUNITIES**:
   - Related scholarship categories to explore
   - Alternative search terms that might yield more results
   - Seasonal opportunities (if applicable)

4. **🔍 SEARCH TIPS**:
   - How to refine the search for better results
   - Additional resources to check
   - Best practices for finding more scholarships

Please focus on current, active scholarships and provide specific, actionable information. Format your response with clear headings and bullet points for easy reading."""
                        
                        # Get search results from Gemini
                        if st.session_state.chat_agent:
                            gemini_response = st.session_state.chat_agent.llm.invoke(search_prompt)
                            search_results = gemini_response.content if hasattr(gemini_response, 'content') else str(gemini_response)
                            
                            # Display the search results
                            st.markdown(search_results)
                            
                            # Add search refinement suggestions
                            st.divider()
                            with st.expander("🔧 Refine Your Search"):
                                st.write("""
                                **💡 Search Tips for Better Results:**
                                - Be specific about your field of study
                                - Include your degree level (undergraduate, graduate, PhD)
                                - Mention your country or target country
                                - Add keywords like "merit-based", "need-based", "international"
                                - Try different combinations of terms
                                
                                **📝 Example Search Queries:**
                                - "Engineering scholarships for international students in USA"
                                - "Medical school scholarships for underrepresented minorities"
                                - "Computer science PhD funding opportunities"
                                - "Business school scholarships for women"
                                - "Arts scholarships for undergraduate students"
                                """)
                            
                            # Add related searches
                            st.subheader("🔗 Related Searches")
                            related_searches = [
                                f"{search_field} scholarships" if search_field != "All" else "Merit scholarships",
                                f"International {search_query}",
                                f"{search_query} deadlines",
                                f"Graduate {search_query}" if "graduate" not in search_query.lower() else f"Undergraduate {search_query}"
                            ]
                            
                            cols = st.columns(len(related_searches))
                            for i, related_search in enumerate(related_searches):
                                with cols[i]:
                                    if st.button(f"🔍 {related_search}", key=f"related_{i}"):
                                        st.rerun()
                        else:
                            st.error("❌ Scholardeep AI model not available. Please check your configuration.")
                        
                    except Exception as e:
                        st.error(f"❌ Search error: {str(e)}")
                        st.info("Please ensure your Google API key is properly configured and try again.")
        
        # Show search examples
        with st.expander("📝 Search Examples"):
            st.write("""
            **Good Search Examples:**
            - "Engineering scholarships for undergraduate students"
            - "Medical school funding opportunities"
            - "International student scholarships in Computer Science"
            - "Merit-based scholarships for Business students"
            - "PhD funding in Environmental Science"
            - "Scholarships for women in STEM fields"
            - "Need-based financial aid for graduate students"
            """)

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🎓 <strong>AI Scholarship Finder</strong> - Powered by Scholardeep</p>
        <p>Making scholarship discovery smarter and more accessible</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
