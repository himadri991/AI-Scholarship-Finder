from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from typing import List, Dict
import streamlit as st

class ScholarshipChatAgent:
    def __init__(self):
        """Initialize the scholarship chat agent with Scholardeep"""
        try:
            # Validate API key first
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            # Initialize Gemini with correct model name
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model="gemini-2.5-flash",  # Fixed: Use valid model name
                temperature=0.3,  # Slightly higher for more creative responses
                max_output_tokens=96000,  # Reduced for better reliability
                convert_system_message_to_human=True
            )
            
            # Test the connection
            test_response = self.llm.invoke("Hello")
            print("✅ Scholardeep initialized and tested successfully")
            
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            st.error(f"Failed to initialize Gemini: {e}")
            raise e
        
        # Configure memory for conversations
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )
        
        # Initialize other components
        self.tools = self._create_tools()
        try:
            self.agent = self._initialize_agent()
        except Exception as e:
            print(f"Warning: Agent initialization failed: {e}")
            self.agent = None
    
    def get_scholarships_for_profile(self, profile):
        """Get scholarships specifically for a student profile with enhanced error handling"""
        try:
            # Create a more focused prompt
            prompt = f"""You are a scholarship expert. A student with the following profile needs scholarship recommendations:

**Student Profile:**
- Name: {profile.get('name', 'Student')}
- Gender: {profile.get('gender', 'Not specified')}
- Field of Study: {profile.get('field_of_study', 'Not specified')}
- Degree Level: {profile.get('degree_level', 'Not specified')}
- Country: {profile.get('country', 'Not specified')}

**Please provide EXACTLY 5 specific scholarships in this format:**

## 🎯 Scholarship Recommendations

### 1. [Scholarship Name]
- **Provider:** [Organization Name]
- **Amount:** $[Amount] or [Description]
- **Eligibility:** [Key requirements]
- **Deadline:** [Date or "Various"]
- **Match Score:** [X/10]
- **Why Perfect for You:** [Specific reason]

### 2. [Second Scholarship]
[Continue same format...]

**Important:** Provide real, existing scholarships that match this student's profile. Focus on current opportunities."""

            # Make the API call with better error handling
            response = self.llm.invoke(prompt)
            
            # Extract and validate response
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Check if response is meaningful
            if not content or len(content.strip()) < 50:
                return self._get_fallback_response(profile)
            
            return content
            
        except Exception as e:
            print(f"Error in get_scholarships_for_profile: {e}")
            return self._get_fallback_response(profile, error=str(e))
    
    def _get_fallback_response(self, profile, error=None):
        """Provide a fallback response when API fails"""
        field = profile.get('field_of_study', 'your field')
        level = profile.get('degree_level', 'your level')
        country = profile.get('country', 'your country')
        
        fallback = f"""## 🎯 Scholarship Opportunities for {field} Students

### Based on your profile, here are scholarship categories to explore:

#### 1. **Merit-Based Scholarships**
- **Target:** High-achieving {level} students
- **Focus:** Academic excellence in {field}
- **Typical Amount:** $1,000 - $25,000
- **Action:** Search university websites and scholarship databases

#### 2. **Field-Specific Scholarships**
- **Target:** {field} students at {level} level
- **Focus:** Supporting students in your specific field
- **Sources:** Professional associations, industry foundations
- **Action:** Contact {field} professional organizations

#### 3. **Regional Scholarships**
- **Target:** Students from {country}
- **Focus:** Supporting local talent
- **Sources:** Government programs, local foundations
- **Action:** Check education ministry websites

#### 4. **Diversity and Inclusion Scholarships**
- **Target:** Underrepresented groups in {field}
- **Focus:** Promoting diversity in education
- **Action:** Search diversity-focused scholarship programs

#### 5. **University-Specific Aid**
- **Target:** Students at specific institutions
- **Focus:** Institutional financial aid
- **Action:** Contact financial aid offices directly

### 🚀 Next Steps:
1. **Create accounts** on scholarship platforms like Fastweb, Scholarships.com
2. **Contact your university's** financial aid office
3. **Join {field} professional associations** for exclusive opportunities
4. **Set up Google alerts** for "{field} scholarships {level}"
5. **Prepare standard documents:** transcripts, essays, recommendation letters

### 💡 Pro Tips:
- Apply to multiple scholarships to increase chances
- Start applications 3-6 months before deadlines
- Tailor each application to the specific scholarship
- Keep detailed records of applications and deadlines"""

        if error:
            fallback += f"\n\n⚠️ **Note:** Experienced temporary API issues. Please try refreshing the page. Error: {error[:100]}..."
        
        return fallback
    
    # ... (rest of your existing methods remain the same)
    
    def _create_tools(self) -> List[Tool]:
        """Create tools optimized for Scholardeep"""
        tools = [
            Tool(
                name="search_scholarships",
                func=self.search_scholarships_tool,
                description="Search for scholarships by field, degree level, and criteria."
            ),
            Tool(
                name="check_eligibility",
                func=self.check_eligibility_tool,
                description="Check scholarship eligibility requirements."
            ),
            Tool(
                name="application_guidance",
                func=self.application_guidance_tool,
                description="Provide scholarship application guidance and tips."
            )
        ]
        return tools
    
    def _initialize_agent(self):
        """Initialize agent with better error handling"""
        try:
            return initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=False,
                max_iterations=2,
                early_stopping_method="generate",
                handle_parsing_errors=True
            )
        except Exception as e:
            print(f"Agent initialization failed: {e}")
            return None
    
    def search_scholarships_tool(self, query: str) -> str:
        """Search tool with fallback"""
        try:
            prompt = f"Provide 3-5 specific scholarships for: {query}. Include names, amounts, and eligibility."
            response = self.llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Search temporarily unavailable. Please try: 1) Check university websites 2) Visit Fastweb.com 3) Contact financial aid offices. Error: {e}"
    
    def check_eligibility_tool(self, query: str) -> str:
        """Eligibility checking with fallback"""
        return """📋 **To check scholarship eligibility, please provide:**

• **Academic field/major** (e.g., Engineering, Medicine, Business)
• **Degree level** (Undergraduate/Graduate/PhD)  
• **GPA** (on 4.0 or 10.0 scale)
• **Country/citizenship status**
• **Financial need level** (High/Medium/Low)
• **Special achievements** or circumstances

**Quick Eligibility Tips:**
- Most merit scholarships require 3.5+ GPA
- Field-specific scholarships match your major
- Check citizenship requirements carefully
- Apply even if you meet 80% of criteria"""
    
    def application_guidance_tool(self, scholarship_name: str) -> str:
        """Application guidance with practical tips"""
        return f"""## 📝 Application Guide for {scholarship_name}

### Essential Documents:
- ✅ **Transcripts** (official copies)
- ✅ **Personal Statement** (2-3 pages typical)
- ✅ **Letters of Recommendation** (2-3 letters)
- ✅ **Resume/CV** (academic focus)
- ✅ **Financial Information** (if need-based)

### Timeline:
- **3-6 months before:** Gather documents
- **2-3 months before:** Write essays
- **1 month before:** Submit application
- **After submission:** Follow up politely

### Writing Tips:
- Address the prompt directly
- Show impact and leadership
- Use specific examples
- Proofread multiple times
- Have others review your essays

### Common Mistakes to Avoid:
- Missing deadlines
- Generic essays
- Incomplete applications
- Poor proofreading
- Not following instructions exactly"""

    def chat(self, user_input: str) -> str:
        """Enhanced chat with better fallback"""
        try:
            if self.agent:
                response = self.agent.run(input=user_input)
                return response
            else:
                # Direct LLM call if agent failed
                response = self.llm.invoke(f"As a scholarship advisor, help with: {user_input}")
                return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"""I apologize for the technical difficulty. Here's what you can do:

**🔧 Immediate Solutions:**
1. **Refresh the page** and try again
2. **Check your internet connection**
3. **Verify your Google API key** is properly set

**📚 Alternative Resources:**
- Visit Fastweb.com for scholarship search
- Check your university's financial aid website
- Contact your school's financial aid office directly
- Search "[your field] scholarships [your level]" on Google

**Error Details:** {str(e)[:100]}..."""
