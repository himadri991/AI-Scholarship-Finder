from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from typing import List, Dict

class ScholarshipChatAgent:
    def __init__(self):
        """Initialize the scholarship chat agent with Google Gemini"""
        try:
            # Initialize Google Gemini 2.5 Flash
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=os.getenv('GOOGLE_API_KEY'),
                model="gemini-2.5-flash-preview-05-20",
                temperature=0.7,
                max_output_tokens=96000,
                convert_system_message_to_human=True
            )
            print("✅ Gemini API initialized successfully")
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            print("🔧 Please enable the Generative Language API in your Google Cloud project")
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
        self.agent = self._initialize_agent()
        
    def _create_tools(self) -> List[Tool]:
        """Create tools optimized for Gemini"""
        tools = [
            Tool(
                name="search_scholarships",
                func=self.search_scholarships_tool,
                description="Search for scholarships by field, degree level, and criteria. Use when user asks about finding scholarships."
            ),
            Tool(
                name="check_eligibility",
                func=self.check_eligibility_tool,
                description="Check scholarship eligibility requirements. Use when user asks about eligibility."
            ),
            Tool(
                name="application_guidance",
                func=self.application_guidance_tool,
                description="Provide scholarship application guidance and tips. Use when user asks about application process."
            ),
            Tool(
                name="scholarship_recommendations",
                func=self.scholarship_recommendations_tool,
                description="Get personalized scholarship recommendations based on student profile."
            )
        ]
        return tools
    
    def _initialize_agent(self):
        """Initialize agent with Gemini optimizations"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            handle_parsing_errors=True,
            agent_kwargs={
                "system_message": "You are a helpful scholarship advisor AI assistant powered by Google Gemini. Use the available tools to help students find scholarships, check eligibility, and get application guidance. Be encouraging and provide actionable advice."
            }
        )
    
    def search_scholarships_tool(self, query: str) -> str:
        """Enhanced scholarship search tool using pure Gemini knowledge"""
        try:
            search_prompt = f"""As an expert scholarship advisor with access to current scholarship information, please search for scholarships based on this query: "{query}"

Provide a comprehensive list of relevant scholarships including:
1. **Scholarship name and provider**
2. **Award amount** (if known)
3. **Eligibility requirements**
4. **Application deadline** (if known)
5. **Target demographic/field**
6. **Application process overview**
7. **Website/contact information** (if available)

Focus on current, active scholarships and provide specific, actionable information. Format with clear headings and bullet points."""
            
            response = self.llm.invoke(search_prompt)
            return response.content if hasattr(response, 'content') else str(response)
                
        except Exception as e:
            return f"Error searching scholarships: {str(e)}"
    
    def check_eligibility_tool(self, query: str) -> str:
        """Eligibility checking tool"""
        return """📋 **To check scholarship eligibility, I need information about:**
        
• **Academic field/major** (e.g., Engineering, Medicine, Business)
• **Degree level** (Undergraduate/Graduate/PhD)
• **GPA or academic standing** (on 4.0 or 10.0 scale)
• **Country/citizenship status**
• **Financial need level** (High/Medium/Low)
• **Any special achievements** or circumstances

Please provide these details so I can help assess your eligibility for specific scholarships and provide personalized recommendations."""
    
    def scholarship_recommendations_tool(self, profile_info: str) -> str:
        """Get personalized scholarship recommendations using pure Gemini knowledge"""
        try:
            recommendation_prompt = f"""As an expert scholarship advisor with comprehensive knowledge of current scholarships worldwide, analyze this student profile and provide personalized recommendations:

Student Profile: {profile_info}

Please provide:
1. **Top 5-7 Most Suitable Scholarships** with:
   - Scholarship name and provider
   - Award amount and coverage
   - Specific eligibility requirements
   - Application deadline (if known)
   - Why this scholarship matches the student's profile

2. **Match Analysis** explaining:
   - Student's strongest qualification areas
   - Potential challenges or gaps
   - Competitive advantages

3. **Application Strategy**:
   - Priority order for applications
   - Timeline recommendations
   - Key preparation steps

4. **Additional Opportunities**:
   - Alternative funding sources
   - Professional development scholarships
   - Research or internship opportunities

Focus on current, active opportunities and provide specific, actionable advice. Format with clear headings and bullet points."""
            
            response = self.llm.invoke(recommendation_prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    def application_guidance_tool(self, scholarship_name: str) -> str:
        """Application guidance using Gemini"""
        try:
            guidance_prompt = f"""
            Provide comprehensive scholarship application guidance for: {scholarship_name}
            
            Include practical, actionable advice covering:
            1. **Essential documents and requirements**
            2. **Timeline and deadline management**
            3. **Writing tips for personal statements**
            4. **Common application mistakes to avoid**
            5. **Follow-up and next steps**
            
            Keep the response organized with clear headings and helpful for students.
            Format with bullet points and actionable steps.
            """
            
            response = self.llm.invoke(guidance_prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            return f"Error providing guidance: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """Main chat interface optimized for Gemini"""
        try:
            
            # Enhanced context for Gemini
            enhanced_input = f"""
            User Query: {user_input}
            
            Context: You are helping a student find scholarships and application guidance. 
            Use available tools when appropriate to provide specific, helpful information.
            Always be encouraging and provide actionable advice.
            """
            
            response = self.agent.run(input=enhanced_input)
            return response
            
        except Exception as e:
            # Gemini-specific fallback with direct LLM call
            try:
                fallback_prompt = f"""
                You are a scholarship advisor AI assistant powered by Google Gemini. 
                A student asked: "{user_input}"
                
                Provide helpful information about:
                - Scholarship opportunities and types
                - Eligibility requirements and criteria  
                - Application process and tips
                - Deadlines and important dates
                
                Be encouraging and provide actionable advice. If you need more specific information 
                from the student, ask relevant questions to better help them.
                
                Use emojis and clear formatting to make your response engaging and easy to read.
                """
                
                response = self.llm.invoke(fallback_prompt)
                return response.content if hasattr(response, 'content') else str(response)
                
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please ensure your Google API key is properly configured and the Generative Language API is enabled in your Google Cloud project. Error: {str(e)}"
    
    def analyze_student_profile(self, profile: Dict) -> str:
        """Analyze student profile and provide scholarship suggestions"""
        try:
            analysis_prompt = f"""
            Analyze this student profile and provide personalized scholarship guidance:
            
            Student Profile:
            - Name: {profile.get('name', 'Student')}
            - Field of Study: {profile.get('field_of_study', 'Not specified')}
            - Degree Level: {profile.get('degree_level', 'Not specified')}
            - GPA: {profile.get('gpa', 'Not specified')}
            - Country: {profile.get('country', 'Not specified')}
            
            Provide:
            1. **Scholarship Match Assessment** (Rate compatibility 1-10)
            2. **Top 3 Scholarship Categories** for this profile
            3. **Eligibility Strengths** (what makes them competitive)
            4. **Areas for Improvement** (how to strengthen their profile)
            5. **Action Plan** (next steps to take)
            
            Be specific, encouraging, and actionable in your analysis.
            """
            
            response = self.llm.invoke(analysis_prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            return f"Error analyzing profile: {str(e)}"