# Gemini API Integration Guide

## Overview
This guide explains how to set up and use the Google Gemini API for chatbot features in the Agricultural Yield Prediction System.

## Features Added
✅ **Gemini AI Chatbot** - Advanced agricultural assistant powered by Google Gemini Pro
✅ **Conversation History** - All chats are stored in the database  
✅ **Context-Aware Responses** - The bot remembers previous messages in a conversation
✅ **Tamil Nadu Specialized** - Tailored responses for Tamil Nadu farming practices
✅ **Chat History API** - Retrieve past conversations via API endpoint

## Setup Instructions

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" button
3. Create a new API key in your project
4. Copy the API key

### 2. Configure the API Key

Edit the `.env` file in your project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual API key from step 1.

**⚠️ Important Security Notes:**
- Never commit the `.env` file to version control
- Add `.env` to your `.gitignore` file
- Keep your API key private and secure
- Regenerate the key if it's accidentally exposed

### 3. Verify Installation

Run the Flask app:

```bash
python app.py
```

You should see in the console:
```
✅ Gemini API configured successfully!
🤖 AI Chat Assistant: ENABLED (Google Gemini)
```

## Database Setup

The system automatically creates a `chat_history` table on first run with the following structure:

```sql
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT NOT NULL,
    bot_response LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    conversation_id VARCHAR(50)
)
```

All chat messages are automatically stored for:
- Conversation context
- Historical reference
- Analytics and improvements

## API Endpoints

### Chat Endpoint
**POST** `/chat`

Send a message to the AI chatbot:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What crops are best for Coimbatore district?",
    "conversation_id": "conv_123"
  }'
```

**Response:**
```json
{
  "response": "For Coimbatore district in Tamil Nadu...",
  "conversation_id": "conv_123",
  "model": "Gemini Pro"
}
```

### Chat History Endpoint
**GET** `/chat-history`

Retrieve past conversations:

```bash
curl "http://localhost:5000/chat-history?conversation_id=conv_123&limit=10"
```

**Response:**
```json
{
  "history": [
    {
      "user_message": "What crops are best for Coimbatore?",
      "bot_response": "For Coimbatore district...",
      "created_at": "2024-03-05 10:30:45"
    }
  ],
  "conversation_id": "conv_123",
  "count": 1
}
```

## Chatbot Capabilities

The Gemini-powered chatbot can assist with:

🌾 **Crop Management**
- Crop selection for different Tamil Nadu districts
- Fertilizer recommendations
- Pest and disease management
- Irrigation scheduling

🌱 **Soil & Nutrients**
- Soil testing interpretation
- Nutrient management
- NPK fertilizer planning
- Soil pH optimization

💧 **Water Management**
- Irrigation scheduling
- Rainwater harvesting
- Drainage management
- Water conservation techniques

🏆 **Yield Optimization**
- Best practices for each crop
- Fertilizer application timing
- Pest prevention strategies
- Weather-based recommendations

🎯 **Government Schemes**
- Agricultural subsidies
- Government programs
- Official regulations
- Support services

## Code Changes Made

### Files Modified:
1. **requirements.txt** - Added google-generativeai and python-dotenv
2. **app.py** - Complete Gemini integration

### New Functions in app.py:
- `get_gemini_response()` - Main Gemini API integration
- `store_chat_history()` - Database storage
- `get_chat_history()` - History retrieval
- `create_chat_history_table()` - Database setup

### Updated Endpoints:
- `POST /chat` - Now uses Gemini API
- `GET /chat-history` - New endpoint for history
- `/` - Startup includes chat table creation

## Troubleshooting

### "Gemini API key not found in .env file"
**Solution:** Make sure you've added the GEMINI_API_KEY to the `.env` file

### Chat responses are slow
**Solution:** 
- This is normal for the first request (model warming up)
- Subsequent requests should be faster
- Check your internet connection
- Verify API key is valid

### "chat_history table not found"
**Solution:** 
- The table is created automatically on first run
- Check your database connection
- Run the app once to initialize

### API limit reached
**Solution:**
- Gemini API has usage limits
- Check your usage at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Consider upgrading your plan if needed

## Performance Tips

1. **Conversation Context** - The system uses the last 5 messages for context
2. **Response Speed** - First request takes ~2-3 seconds, subsequent requests are faster
3. **Database Storage** - Chat history is automatically pruned (optional feature)
4. **Concurrent Requests** - Handle multiple users simultaneously with conversation_id

## Security Considerations

✅ **What the system does:**
- Stores chat messages in a local database
- Uses encrypted API calls to Google
- Validates input (max 2000 characters)
- Sanitizes responses

⚠️ **What you should do:**
- Keep your API key in `.env` file
- Don't share your API key
- Regularly check your API usage
- Consider rate limiting in production

## Advanced Configuration

### Change Model (from app.py)
```python
model = genai.GenerativeModel('gemini-2.5-flash')  # Current model (latest, fast & capable)
# Other available models: 'gemini-2.5-pro' (most powerful), 'gemini-3.1-pro-preview'
```

### System Prompt Customization
Edit the `get_gemini_response()` function's `system_prompt` variable to change the chatbot's behavior.

### Temperature & Creative Responses
In `get_gemini_response()`:
```python
response = chat.send_message(message)  # Default behavior
# For more creative responses: modify model settings
```

## Testing the Integration

### Test via cURL
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Best crops for Madurai?"}'
```

### Test via Python
```python
import requests

response = requests.post('http://localhost:5000/chat', json={
    'message': 'Best crops for Madurai?',
    'conversation_id': 'test_conv'
})
print(response.json())
```

## Next Steps

1. Replace the API key in `.env` with your actual key
2. Start the Flask app: `python app.py`
3. Test the chatbot at `http://localhost:5000`
4. Integrate the chat UI into your frontend (if needed)
5. Monitor usage and chat history in the database

## Support & Resources

- [Google Generative AI Documentation](https://ai.google.dev/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini Models Reference](https://ai.google.dev/models)
- [Rate Limits & Pricing](https://ai.google.dev/pricing)

## Version Information

- **Integration Date:** March 5, 2024
- **Gemini API Version:** 0.3.0
- **Python Version:** 3.8+
- **Flask Version:** 2.3.3

---

**Happy Farming! 🌾**

For questions or issues, please check the troubleshooting section above.
