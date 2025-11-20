# 🧠 Caveman Article Agent

A powerful web application that generates professional articles with structured outlines, complete content, header images, and related resources using AI.

## ✨ Features

- **Article Outline Generation**: Create detailed, structured outlines using GPT-4 Turbo
- **Full Article Writing**: Generate complete, well-researched articles based on your title and word range
- **Smart Image Sourcing**: Automatically tries Freepik API first (cost-efficient), falls back to DALL-E if needed
- **Resource Suggestions**: Get 5 authoritative resources related to your article topic
- **Export Options**: Download articles as Markdown files

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Freepik API key (optional, but recommended for cost savings - [Get one here](https://www.freepik.com/api))

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `env.example` to `.env`
   - Fill in your API keys:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     FREEPIK_API_KEY=your_freepik_api_key_here
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 Usage

1. Enter an **Article Title** in the sidebar
2. Specify a **Word Range** (e.g., "800-1000")
3. Click **"Generate Article"**
4. Wait for the AI to generate:
   - Article outline
   - Complete article
   - Header image
   - Related resources
5. Download the article as Markdown if desired

## 💰 Cost Optimization

- **Primary cost**: GPT-4 Turbo API calls (~$0.01-0.03 per article)
- **Image costs**: 
  - Freepik API: Free (if you have API access)
  - DALL-E fallback: ~$0.04 per image
- **Estimated total**: <$0.10 per article

The app prioritizes Freepik for images to minimize costs, only using DALL-E when Freepik doesn't return results.

## ☁️ Deployment

### Option 1: Streamlit Cloud (Recommended - Free)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `FREEPIK_API_KEY` (optional)
5. Deploy!

### Option 2: Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment**: Python 3
4. Add environment variables in the Render dashboard
5. Deploy!

### Option 3: Railway

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect Python
4. Add environment variables in the Railway dashboard
5. Deploy!

### Option 4: Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select **Streamlit** as the SDK
3. Upload your files
4. Add secrets (environment variables) in Space settings
5. Deploy!

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (Required): Your OpenAI API key for GPT-4 Turbo and DALL-E
- `FREEPIK_API_KEY` (Optional): Your Freepik API key for cost-efficient image sourcing

### Model Settings

The app uses:
- **GPT-4 Turbo** (`gpt-4-turbo-preview`) for text generation
- **DALL-E 3** (`dall-e-3`) for image generation fallback

You can modify these in `app.py` if needed.

## 🎯 Future Enhancements

- [ ] PDF export functionality
- [ ] Adjustable tone/voice selection
- [ ] Batch article generation
- [ ] Article editing capabilities
- [ ] Custom image prompts
- [ ] Multiple language support

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## ⚠️ Disclaimer

This tool generates AI content. Always review and fact-check generated articles before publishing. The AI may occasionally produce inaccurate or biased content.

---

**Built with ❤️ by Caveman Productions**

