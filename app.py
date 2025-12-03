import os
import openai
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Caveman Article Agent",
    page_icon="🧠",
    layout="wide"
)

# --- 🔧 Railway Hosting Compatibility Fix ---
# Forces Streamlit to use the correct network interface and port
port = int(os.environ.get("PORT", 8501))
st.set_option('server.port', port)
st.set_option('server.address', '0.0.0.0')

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None


def get_freepik_image(title):
    """Attempt to get an image from Freepik API."""
    try:
        api_key = os.getenv("FREEPIK_API_KEY")
        if not api_key:
            return None
        
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {
            "term": title,
            "limit": 1,
            "filters[content_type]": "photo"
        }
        
        response = requests.get(
            "https://api.freepik.com/v1/resources",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                item = data["data"][0]
                if "attributes" in item and "preview" in item["attributes"]:
                    return item["attributes"]["preview"].get("url")
                elif "images" in item and "preview" in item["images"]:
                    return item["images"]["preview"].get("url")
        return None
    except Exception as e:
        st.warning(f"Freepik API error: {str(e)}")
        return None


def generate_dalle_image(title):
    """Generate an image using DALL-E as fallback."""
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=f"Create a modern, professional header image for an article titled '{title}'. The image should be visually appealing and relevant to the topic.",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"DALL-E generation error: {str(e)}")
        return None


def generate_outline(title, word_range):
    """Generate article outline using GPT-4 Turbo."""
    try:
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_VERSION"),
            messages=[{
                "role": "user",
                "content": f"Create a detailed, structured outline for an article titled '{title}' that should be approximately {word_range} words. Format it as a clear, hierarchical outline with main sections and subsections."
            }],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Outline generation error: {str(e)}")
        return None


def write_article(title, outline, word_range):
    """Write full article using the outline and word range."""
    try:
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_VERSION"),
            messages=[{
                "role": "user",
                "content": f"Write a complete, well-researched article titled '{title}' using this outline:\n\n{outline}\n\nThe article should be approximately {word_range} words. Make it engaging, informative, and professional. Include an introduction, well-structured body paragraphs, and a conclusion."
            }],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Article writing error: {str(e)}")
        return None


def suggest_resources(title):
    """Suggest authoritative resources related to the article topic."""
    try:
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_VERSION"),
            messages=[{
                "role": "user",
                "content": f"Provide 5 authoritative online resources (websites, articles, studies, or references) related to '{title}'. Format each as a clear title and description. Include why each resource is valuable."
            }],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Resource suggestion error: {str(e)}")
        return None


def generate_header_image(title):
    """Generate header image with Freepik first, DALL-E fallback."""
    freepik_image = get_freepik_image(title)
    if freepik_image:
        return freepik_image, "Freepik"
    
    dalle_image = generate_dalle_image(title)
    if dalle_image:
        return dalle_image, "DALL-E"
    
    return None, None


# Main UI
st.title("🧠 Caveman Article Agent")
st.markdown("Generate professional articles with outlines, images, and resources")

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Article Settings")
    title = st.text_input(
        "Article Title:",
        placeholder="e.g., The Future of Artificial Intelligence",
        help="Enter the title of the article you want to generate"
    )
    word_range = st.text_input(
        "Word Range:",
        placeholder="e.g., 800-1000",
        help="Specify the target word count range for your article"
    )
    
    generate_button = st.button(
        "🚀 Generate Article",
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be specific with your title for better results  
    - Word range helps control article length  
    - Images are sourced from Freepik first (free), then DALL-E  
    - All content is AI-generated using GPT-4 Turbo
    """)

# Main content area
if generate_button:
    if not title or not word_range:
        st.error("⚠️ Please fill in both the title and word range fields.")
    elif not openai.api_key:
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        generated_content = {}
        
        status_text.info("📋 Generating article outline...")
        progress_bar.progress(20)
        outline = generate_outline(title, word_range)
        
        if outline:
            generated_content['outline'] = outline
            progress_bar.progress(40)
            
            status_text.info("✍️ Writing full article...")
            article = write_article(title, outline, word_range)
            
            if article:
                generated_content['article'] = article
                progress_bar.progress(60)
                
                status_text.info("🖼️ Searching for header image...")
                image_url, image_source = generate_header_image(title)
                
                if image_url:
                    generated_content['image_url'] = image_url
                    generated_content['image_source'] = image_source
                    progress_bar.progress(80)
                else:
                    st.warning("⚠️ Could not generate header image.")
                    generated_content['image_url'] = None
                    generated_content['image_source'] = None
                
                status_text.info("📚 Gathering related resources...")
                resources = suggest_resources(title)
                
                if resources:
                    generated_content['resources'] = resources
                    progress_bar.progress(100)
                
                st.session_state.generated_content = generated_content
                status_text.success("✅ Article generation complete!")
            else:
                st.error("❌ Failed to generate article. Please try again.")
        else:
            st.error("❌ Failed to generate outline. Please try again.")
        
        progress_bar.empty()
        status_text.empty()

# Display generated content
if st.session_state.generated_content:
    content = st.session_state.generated_content
    
    with st.expander("📋 Article Outline", expanded=True):
        st.markdown(content.get('outline', 'No outline generated.'))
    
    st.markdown("---")
    st.markdown("### 📝 Complete Article")
    st.markdown(content.get('article', 'No article generated.'))
    st.markdown("---")
    
    if content.get('image_url'):
        st.markdown("### 🖼️ Header Image")
        st.image(
            content['image_url'],
            caption=f"Header Image (Source: {content.get('image_source', 'Unknown')})",
            width=700
        )
    else:
        st.markdown("### 🖼️ Header Image")
        st.info("No header image available.")
    
    st.markdown("---")
    st.markdown("### 📚 Additional Resources")
    st.markdown(content.get('resources', 'No resources generated.'))
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download as Markdown"):
            markdown_content = f"""# {title}

## Outline
{content.get('outline', '')}

## Article
{content.get('article', '')}

## Resources
{content.get('resources', '')}
"""
            st.download_button(
                label="Download Markdown File",
                data=markdown_content,
                file_name=f"{title.replace(' ', '_')}.md",
                mime="text/markdown"
            )
    with col2:
        st.info("💡 PDF export coming soon!")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ by Caveman Productions | Powered by OpenAI GPT-4 Turbo"
    "</div>",
    unsafe_allow_html=True
)