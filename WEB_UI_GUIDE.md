# 🌐 JanSahayak Web UI Guide

## Quick Start

### 1. Install Flask

Flask is already included in `requirements.txt`. If you need to install it separately:

```bash
pip install flask
```

### 2. Start the Web Server

```bash
python app.py
```

You should see:

```
🙏 JANSAHAYAK - Starting Web Server
======================================================================

📱 Access the application at: http://localhost:5000
🛑 Press CTRL+C to stop the server
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## Features

### 🏠 Home Page

- **Hero Section**: Overview of JanSahayak system
- **Input Form**: Enter your details for analysis
- **Quick Fill**: Pre-filled example profiles (Student, Farmer, Job Seeker)
- **Character Counter**: Tracks input length
- **Real-time Validation**: Ensures quality input

### 📊 Results Page

- **Profile Summary**: Extracted structured profile
- **Government Schemes**: Personalized scheme recommendations
- **Competitive Exams**: Suitable exam suggestions
- **Benefit Analysis**: Missed benefits calculator
- **Download**: Export results as JSON
- **Actions**: Start new analysis or view history

### 📚 About Page

- System architecture
- Agent descriptions
- Technology stack
- Privacy information

### 📜 History Page

- View past analyses
- Download previous reports
- Quick access to results
- Timestamp tracking

## UI Features

### Modern Design

- **Gradient Backgrounds**: Beautiful purple/blue gradients
- **Card-Based Layout**: Clean, organized content
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Fade-in effects and transitions
- **Icon Integration**: Font Awesome icons throughout

### User Experience

- **Progress Indicators**: Shows which agents are working
- **Loading States**: Animated spinner with status updates
- **Error Handling**: User-friendly error messages
- **Success Notifications**: Confirmation messages
- **Empty States**: Helpful messages when no data

### Interactivity

- **Quick Fill Buttons**: One-click example profiles
- **Real-time Validation**: Form validation before submission
- **Modal Views**: Popup windows for detailed data
- **Download Options**: Export results as JSON
- **Navigation**: Easy movement between pages

## API Endpoints

### Public Routes

- `GET /` - Home page with input form
- `GET /about` - About page
- `GET /history` - Analysis history
- `GET /result/<session_id>` - View specific result

### API Routes

- `POST /analyze` - Submit user input for analysis
  - Request: `{ "user_input": "your details here..." }`
  - Response: `{ "success": true, "session_id": "...", "result": {...} }`

- `GET /api/status/<session_id>` - Check analysis status
  - Response: `{ "status": "processing|completed", ... }`

- `GET /api/file/<filename>` - Download result file
  - Response: JSON result data

## Customization

### Modify Colors

Edit `static/css/style.css` and change CSS variables:

```css
:root {
    --primary: #6366f1;        /* Primary color */
    --secondary: #8b5cf6;      /* Secondary color */
    --success: #10b981;        /* Success color */
    --danger: #ef4444;         /* Error color */
    /* ... more colors ... */
}
```

### Add New Pages

1. Create template in `templates/newpage.html`
2. Add route in `app.py`:

```python
@app.route('/newpage')
def newpage():
    return render_template('newpage.html')
```

3. Add navigation link in `templates/layout.html`

### Modify Agent Progress

Edit the agent steps in `templates/index.html`:

```html
<div class="agent-step">
    <div class="step-icon"><i class="fas fa-icon-name"></i></div>
    <div class="step-info">
        <h4>Agent Name</h4>
        <p>Description...</p>
    </div>
</div>
```

## Deployment

### Local Network Access

To allow other devices on your network to access:

```python
# In app.py, change:
app.run(debug=True, host='0.0.0.0', port=5000)
```

Then access via: `http://YOUR_IP:5000`

### Production Deployment

For production use, use a production server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or use waitress:

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t jansahayak .
docker run -p 5000:5000 jansahayak
```

## Troubleshooting

### Port Already in Use

If port 5000 is busy, change the port:

```python
# In app.py:
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Templates Not Found

Ensure the `templates/` directory exists with all HTML files.

### Static Files Not Loading

Ensure the `static/` directory structure:

```
static/
├── css/
│   └── style.css
└── js/
    └── main.js
```

### Session Errors

If you see session-related errors, ensure Flask secret key is set:

```python
# In app.py:
app.secret_key = os.urandom(24)
```

### Analysis Takes Too Long

- Check API keys are valid
- Ensure vectorstores are built
- Check internet connection
- Reduce timeout values if needed

## Performance Tips

1. **Build Vectorstores First**: Run `python setup.py --build-vectorstores` before starting the web server

2. **Cache Results**: Results are automatically cached in `outputs/` directory

3. **Limit History**: The history page shows only last 10 results by default

4. **Optimize Images**: Compress static images if added

5. **Enable Production Mode**: Set `debug=False` in production

## Security Notes

- Never commit `.env` file with real API keys
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Sanitize user inputs
- Use session timeouts
- Add CORS headers if needed

## Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## Mobile Responsive

The UI is fully responsive and works on:
- 📱 Mobile phones (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop (1024px+)
- 🖥️ Large screens (1920px+)

## Keyboard Shortcuts

- `Tab` - Navigate between form fields
- `Enter` - Submit form (when focused)
- `Esc` - Close modals
- `Ctrl+Enter` - Submit textarea

## Accessibility

- Semantic HTML5 elements
- ARIA labels where needed
- Keyboard navigation support
- Screen reader friendly
- High contrast mode compatible

## Next Steps

1. Start the server: `python app.py`
2. Open browser: http://localhost:5000
3. Try the example profiles
4. Analyze your own profile
5. View and download results

Enjoy using JanSahayak! 🎉
