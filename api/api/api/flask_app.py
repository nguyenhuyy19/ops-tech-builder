from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
import logging
import json
from typing import Dict, Any, Optional
import time

# openai-api
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("install python-dotenv")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    print(f"OPENAI_API_KEY:{OPENAI_API_KEY[:10]}...")
else:
    print(" OPENAI_API_KEY not found")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()

        if 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        text = data.get('text', '').strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400

        # Extract parameters (optional)
        max_length = data.get('max_length', 100)
        api_key = data.get('api_key') or os.getenv('OPENAI_API_KEY') or os.getenv('LLM_API_KEY')
        summary_style = data.get('summary_style', 'concise')
        output_format = data.get('output_format', 'paragraph')
        provider = data.get('provider', 'openai')

        summary_text = integrate_with_llm_api(
            text=text,
            api_key=api_key,
            max_length=max_length,
            summary_style=summary_style,
            output_format=output_format,
            provider=provider
        )

        return jsonify({"summary": summary_text}), 200

    except Exception as e:
        logger.error(f"Error POST endpoint: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
    
def simple_summarize(text, max_sentences=3):
    if not text or not text.strip():
        return ""
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    summary_sentences = sentences[:max_sentences]
    return '. '.join(summary_sentences) + ('.' if summary_sentences else '')

def openai_summarize(text: str, api_key: str, max_length: int = 100,
                     summary_style: str = "concise", output_format: str = "paragraph") -> str:
    if not OPENAI_AVAILABLE:
        raise Exception("OpenAI library not installed")

    client = OpenAI(api_key=api_key)

    style_prompts = {
        'concise': f"Concise in {max_length} words.",
        'detailed': f"Detailed in {max_length} words.",
        'bullet_points': f"Bullet-point summary with {max_length//10} main points.",
        'executive': f"Executive summary in {max_length} key insights and conclusions."
    }

    format_prompts = {
        'paragraph': "Format as a paragraph.",
        'bullets': "Format as bullet points.",
        'json': "JSON object with 'summary', 'key_points','conclusion'.",
        'structured': " Clear sections: Summary, Key Points, and Conclusion."
    }

    system_prompt = f"""You are an expert text summarizer. {style_prompts.get(summary_style)} 
{format_prompts.get(output_format)}"""

    user_prompt = f"Please input the text:\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=min(max_length * 2, 1000),
            temperature=0.3,
            top_p=0.9
        )

        content = response.choices[0].message.content if response.choices else ""
        summary_text = content.strip() if isinstance(content, str) else ""

        # For JSON format, try to parse and extract summary
        if output_format == 'json':
            try:
                summary_json = json.loads(summary_text)
                summary_text = summary_json.get('summary', summary_text)
            except json.JSONDecodeError:
                pass

        return summary_text

    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    
# optional future-proofing
def claude_summarize(text: str, max_length: int = 100) -> str:
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    summary_sentences = sentences[:max_length//20 or 3]
    mock_summary = '. '.join(summary_sentences) + ('.' if summary_sentences else '')
    return f"[Claude Summary] {mock_summary}"

def integrate_with_llm_api(text: str, api_key: Optional[str] = None,
                          max_length: int = 100, summary_style: str = "concise",
                          output_format: str = "paragraph", provider: str = "openai") -> str:

    if provider == "openai" and api_key and OPENAI_AVAILABLE:
        try:
            return openai_summarize(text, api_key, max_length, summary_style, output_format)
        except Exception as e:
            logger.warning(f"OpenAI failed, falling back to simple summarization: {str(e)}")
            return simple_summarize(text, max_sentences=max_length//20 or 3)
    elif provider == "claude":
        try:
            return claude_summarize(text, max_length)
        except Exception as e:
            logger.warning(f"Claude failed, falling back to simple summarization: {str(e)}")
            return simple_summarize(text, max_sentences=max_length//20 or 3)

    return simple_summarize(text, max_sentences=max_length//20 or 3)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'

    print(f"Flask LLM API server on port {port}")
    print("Endpoints: POST /summarize")
    print("Providers: openai (enabled), claude (mocked)")
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
